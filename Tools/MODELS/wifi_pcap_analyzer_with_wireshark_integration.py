"""
Real-Time WiFi Traffic Capture & AI Analysis System
Directly captures packets using tshark/tcpdump and processes them in real-time
Optimized for Kali Linux

Requirements:
pip install scapy numpy pandas scikit-learn xgboost lightgbm pyshark psutil

System Requirements (Kali Linux):
- tshark (wireshark-cli) - usually pre-installed
- Root/sudo privileges for packet capture
"""

import subprocess
import threading
import queue
import time
import signal
import sys
import os
from collections import defaultdict, deque
from datetime import datetime

import numpy as np
import pandas as pd
from scapy.all import sniff, IP, TCP, UDP, ICMP, wrpcap, Ether, RadioTap
from sklearn.ensemble import IsolationForest, RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import lightgbm as lgb
import warnings
warnings.filterwarnings('ignore')


class LivePacketCapture:
    """Live packet capture using Scapy and system tools"""
    
    def __init__(self, interface='wlan0', buffer_size=100):
        self.interface = interface
        self.buffer_size = buffer_size
        self.packet_buffer = deque(maxlen=buffer_size)
        self.capture_active = False
        self.packet_count = 0
        self.capture_thread = None
        
    def list_interfaces(self):
        """List available network interfaces"""
        try:
            result = subprocess.run(['ip', 'link', 'show'], 
                                  capture_output=True, text=True)
            print("\n=== Available Network Interfaces ===")
            print(result.stdout)
            
            # Also try iwconfig for wireless interfaces
            result = subprocess.run(['iwconfig'], 
                                  capture_output=True, text=True, stderr=subprocess.DEVNULL)
            if result.stdout:
                print("\n=== Wireless Interfaces ===")
                print(result.stdout)
        except Exception as e:
            print(f"Error listing interfaces: {e}")
    
    def enable_monitor_mode(self):
        """Enable monitor mode on wireless interface (Kali Linux)"""
        print(f"\n[*] Attempting to enable monitor mode on {self.interface}...")
        try:
            # Stop network manager
            subprocess.run(['sudo', 'airmon-ng', 'check', 'kill'], 
                         capture_output=True)
            
            # Enable monitor mode
            result = subprocess.run(['sudo', 'airmon-ng', 'start', self.interface], 
                                  capture_output=True, text=True)
            print(result.stdout)
            
            # Check if monitor interface was created (usually wlan0mon)
            if 'mon' in result.stdout:
                self.interface = self.interface + 'mon'
                print(f"[+] Monitor mode enabled on {self.interface}")
                return True
            else:
                print("[!] Monitor mode may already be enabled")
                return True
                
        except Exception as e:
            print(f"[!] Error enabling monitor mode: {e}")
            print("[*] Continuing with managed mode...")
            return False
    
    def disable_monitor_mode(self):
        """Disable monitor mode"""
        try:
            original_interface = self.interface.replace('mon', '')
            subprocess.run(['sudo', 'airmon-ng', 'stop', self.interface], 
                         capture_output=True)
            print(f"[+] Monitor mode disabled on {original_interface}")
        except Exception as e:
            print(f"[!] Error disabling monitor mode: {e}")
    
    def packet_callback(self, packet):
        """Callback for each captured packet"""
        self.packet_count += 1
        self.packet_buffer.append(packet)
        
        # Print progress every 100 packets
        if self.packet_count % 100 == 0:
            print(f"[*] Captured {self.packet_count} packets...")
    
    def start_capture(self, duration=None, packet_count=None, prn=None):
        """Start live packet capture"""
        self.capture_active = True
        self.packet_count = 0
        
        print(f"\n[*] Starting packet capture on interface: {self.interface}")
        print(f"[*] Press Ctrl+C to stop capture")
        
        try:
            if prn is None:
                prn = self.packet_callback
            
            # Start sniffing
            sniff(
                iface=self.interface,
                prn=prn,
                store=False,
                timeout=duration,
                count=packet_count,
                stop_filter=lambda x: not self.capture_active
            )
            
        except PermissionError:
            print("\n[!] ERROR: Permission denied. Please run with sudo:")
            print(f"    sudo python3 {sys.argv[0]}")
            sys.exit(1)
        except Exception as e:
            print(f"\n[!] Capture error: {e}")
        finally:
            self.capture_active = False
    
    def stop_capture(self):
        """Stop packet capture"""
        self.capture_active = False
        print(f"\n[+] Capture stopped. Total packets: {self.packet_count}")
    
    def get_packets(self):
        """Get captured packets from buffer"""
        return list(self.packet_buffer)


class RealTimeFeatureExtractor:
    """Extract features from packets in real-time"""
    
    def __init__(self, window_size=50):
        self.window_size = window_size
        self.flow_windows = defaultdict(lambda: deque(maxlen=window_size))
        self.flow_stats = defaultdict(lambda: {
            'packet_count': 0,
            'byte_count': 0,
            'start_time': None,
            'last_time': None,
            'src_ip': None,
            'dst_ip': None,
            'src_port': None,
            'dst_port': None,
            'protocol': None
        })
    
    def extract_packet_features(self, packet):
        """Extract features from single packet"""
        features = {
            'timestamp': time.time(),
            'packet_length': len(packet),
            'has_ip': 0,
            'has_tcp': 0,
            'has_udp': 0,
            'has_icmp': 0
        }
        
        if packet.haslayer(IP):
            features['has_ip'] = 1
            ip = packet[IP]
            features['ip_len'] = ip.len
            features['ip_ttl'] = ip.ttl
            features['ip_proto'] = ip.proto
            features['src_ip'] = ip.src
            features['dst_ip'] = ip.dst
            
            if packet.haslayer(TCP):
                features['has_tcp'] = 1
                tcp = packet[TCP]
                features['src_port'] = tcp.sport
                features['dst_port'] = tcp.dport
                features['tcp_window'] = tcp.window
                features['flag_syn'] = 1 if tcp.flags.S else 0
                features['flag_ack'] = 1 if tcp.flags.A else 0
                features['flag_fin'] = 1 if tcp.flags.F else 0
                features['flag_rst'] = 1 if tcp.flags.R else 0
                features['flag_psh'] = 1 if tcp.flags.P else 0
                
            elif packet.haslayer(UDP):
                features['has_udp'] = 1
                udp = packet[UDP]
                features['src_port'] = udp.sport
                features['dst_port'] = udp.dport
                features['udp_len'] = udp.len
            
            elif packet.haslayer(ICMP):
                features['has_icmp'] = 1
        
        return features
    
    def update_flow_stats(self, packet):
        """Update flow statistics with new packet"""
        if not packet.haslayer(IP):
            return None
        
        flow_key = self._get_flow_key(packet)
        if not flow_key:
            return None
        
        stats = self.flow_stats[flow_key]
        current_time = time.time()
        
        # Update basic stats
        stats['packet_count'] += 1
        stats['byte_count'] += len(packet)
        
        if stats['start_time'] is None:
            stats['start_time'] = current_time
        stats['last_time'] = current_time
        
        # Store packet info
        ip = packet[IP]
        stats['src_ip'] = ip.src
        stats['dst_ip'] = ip.dst
        
        if packet.haslayer(TCP):
            stats['protocol'] = 'TCP'
            stats['src_port'] = packet[TCP].sport
            stats['dst_port'] = packet[TCP].dport
        elif packet.haslayer(UDP):
            stats['protocol'] = 'UDP'
            stats['src_port'] = packet[UDP].sport
            stats['dst_port'] = packet[UDP].dport
        
        # Add to flow window
        self.flow_windows[flow_key].append({
            'length': len(packet),
            'time': current_time
        })
        
        return flow_key
    
    def get_flow_features(self, flow_key):
        """Get comprehensive features for a flow"""
        stats = self.flow_stats[flow_key]
        window = list(self.flow_windows[flow_key])
        
        if len(window) < 2:
            return None
        
        # Calculate statistics
        lengths = [p['length'] for p in window]
        times = [p['time'] for p in window]
        intervals = [times[i] - times[i-1] for i in range(1, len(times))]
        
        features = {
            'flow_duration': stats['last_time'] - stats['start_time'] if stats['start_time'] else 0,
            'flow_packet_count': stats['packet_count'],
            'flow_byte_count': stats['byte_count'],
            'flow_bytes_per_packet_mean': np.mean(lengths),
            'flow_bytes_per_packet_std': np.std(lengths),
            'flow_bytes_per_packet_min': np.min(lengths),
            'flow_bytes_per_packet_max': np.max(lengths),
            'src_ip': stats['src_ip'],
            'dst_ip': stats['dst_ip'],
            'src_port': stats.get('src_port', 0),
            'dst_port': stats.get('dst_port', 0),
            'protocol': stats.get('protocol', 'OTHER')
        }
        
        if intervals:
            features['flow_inter_arrival_mean'] = np.mean(intervals)
            features['flow_inter_arrival_std'] = np.std(intervals)
            features['flow_inter_arrival_min'] = np.min(intervals)
            features['flow_inter_arrival_max'] = np.max(intervals)
        else:
            features['flow_inter_arrival_mean'] = 0
            features['flow_inter_arrival_std'] = 0
            features['flow_inter_arrival_min'] = 0
            features['flow_inter_arrival_max'] = 0
        
        return features
    
    def _get_flow_key(self, packet):
        """Generate flow identifier"""
        if not packet.haslayer(IP):
            return None
        
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        
        if packet.haslayer(TCP):
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
            proto = 'TCP'
        elif packet.haslayer(UDP):
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport
            proto = 'UDP'
        else:
            src_port = 0
            dst_port = 0
            proto = 'OTHER'
        
        return tuple(sorted([(src_ip, src_port), (dst_ip, dst_port)]) + [proto])


class RealTimeAnalyzer:
    """Real-time AI analysis of network traffic"""
    
    def __init__(self, update_interval=10):
        self.extractor = RealTimeFeatureExtractor()
        self.models_trained = False
        self.anomaly_detector = None
        self.scaler = StandardScaler()
        self.feature_columns = None
        self.update_interval = update_interval
        self.last_update = time.time()
        self.total_packets = 0
        self.total_flows = 0
        self.anomaly_count = 0
        
    def process_packet(self, packet):
        """Process single packet in real-time"""
        self.total_packets += 1
        
        # Extract features and update flow stats
        flow_key = self.extractor.update_flow_stats(packet)
        
        if flow_key:
            self.total_flows = len(self.extractor.flow_stats)
        
        # Periodically update display and analyze
        current_time = time.time()
        if current_time - self.last_update >= self.update_interval:
            self.display_status()
            self.analyze_flows()
            self.last_update = current_time
    
    def train_models(self, initial_packets):
        """Train models on initial packet capture"""
        print("\n[*] Training models on initial traffic sample...")
        
        # Extract flow features
        flow_features = []
        for flow_key in self.extractor.flow_stats.keys():
            feat = self.extractor.get_flow_features(flow_key)
            if feat:
                flow_features.append(feat)
        
        if len(flow_features) < 10:
            print("[!] Not enough flows for training. Need at least 10 flows.")
            return False
        
        # Prepare features
        X = self._prepare_features(flow_features)
        
        if X is None or len(X) < 10:
            print("[!] Failed to prepare features")
            return False
        
        # Train anomaly detector
        print(f"[*] Training Isolation Forest on {len(X)} flows...")
        self.anomaly_detector = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100
        )
        
        X_scaled = self.scaler.fit_transform(X)
        self.anomaly_detector.fit(X_scaled)
        
        self.models_trained = True
        print("[+] Models trained successfully!")
        return True
    
    def analyze_flows(self):
        """Analyze current flows"""
        if not self.models_trained:
            return
        
        # Get flow features
        flow_features = []
        flow_keys = []
        
        for flow_key in list(self.extractor.flow_stats.keys()):
            feat = self.extractor.get_flow_features(flow_key)
            if feat:
                flow_features.append(feat)
                flow_keys.append(flow_key)
        
        if not flow_features:
            return
        
        # Prepare features
        X = self._prepare_features(flow_features)
        if X is None:
            return
        
        # Detect anomalies
        X_scaled = self.scaler.transform(X)
        predictions = self.anomaly_detector.predict(X_scaled)
        scores = self.anomaly_detector.score_samples(X_scaled)
        
        # Find anomalies
        anomaly_indices = np.where(predictions == -1)[0]
        
        if len(anomaly_indices) > 0:
            print(f"\n{'='*70}")
            print(f"[!] ANOMALIES DETECTED: {len(anomaly_indices)} suspicious flows")
            print(f"{'='*70}")
            
            for idx in anomaly_indices[:5]:  # Show top 5
                if idx < len(flow_features):
                    flow = flow_features[idx]
                    print(f"\n  Flow: {flow.get('src_ip', 'N/A')}:{flow.get('src_port', 'N/A')} -> "
                          f"{flow.get('dst_ip', 'N/A')}:{flow.get('dst_port', 'N/A')}")
                    print(f"  Protocol: {flow.get('protocol', 'N/A')}")
                    print(f"  Packets: {flow.get('flow_packet_count', 0)}, "
                          f"Bytes: {flow.get('flow_byte_count', 0)}")
                    print(f"  Anomaly Score: {scores[idx]:.4f}")
            
            self.anomaly_count += len(anomaly_indices)
    
    def display_status(self):
        """Display current analysis status"""
        print(f"\n{'='*70}")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Real-Time Traffic Analysis Status")
        print(f"{'='*70}")
        print(f"  Total Packets Captured: {self.total_packets}")
        print(f"  Active Flows: {self.total_flows}")
        print(f"  Total Anomalies Detected: {self.anomaly_count}")
        print(f"  Models Trained: {'Yes' if self.models_trained else 'No'}")
        print(f"{'='*70}")
    
    def _prepare_features(self, flow_features):
        """Convert flow features to numerical array"""
        if not flow_features:
            return None
        
        df = pd.DataFrame(flow_features)
        
        # Select numerical features
        numerical_cols = [col for col in df.columns 
                         if col not in ['src_ip', 'dst_ip', 'protocol']]
        
        X = df[numerical_cols].fillna(0)
        
        if self.feature_columns is None:
            self.feature_columns = X.columns.tolist()
        
        # Ensure consistent columns
        for col in self.feature_columns:
            if col not in X.columns:
                X[col] = 0
        
        X = X[self.feature_columns]
        return X.values


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\n[*] Shutting down gracefully...")
    sys.exit(0)


def main():
    """Main execution"""
    
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║         Real-Time WiFi Traffic AI Analysis System              ║
    ║              Optimized for Kali Linux                          ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    # Check if running as root
    if os.geteuid() != 0:
        print("[!] This script requires root privileges.")
        print("[*] Please run with: sudo python3 script.py")
        sys.exit(1)
    
    # Setup signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Initialize capture
    capture = LivePacketCapture()
    
    # List available interfaces
    capture.list_interfaces()
    
    # Get interface from user
    interface = input("\n[?] Enter interface name (default: wlan0): ").strip()
    if interface:
        capture.interface = interface
    
    # Ask about monitor mode
    monitor = input("[?] Enable monitor mode? (y/n, default: n): ").strip().lower()
    if monitor == 'y':
        capture.enable_monitor_mode()
    
    # Initialize analyzer
    analyzer = RealTimeAnalyzer(update_interval=10)
    
    print("\n[*] Phase 1: Capturing initial traffic for model training...")
    print("[*] Capturing 500 packets for baseline...")
    
    # Capture initial packets for training
    initial_packets = []
    def training_callback(packet):
        initial_packets.append(packet)
        analyzer.extractor.update_flow_stats(packet)
        if len(initial_packets) % 100 == 0:
            print(f"[*] Training packets: {len(initial_packets)}/500")
    
    try:
        capture.start_capture(packet_count=500, prn=training_callback)
        
        # Train models
        if len(initial_packets) >= 100:
            analyzer.train_models(initial_packets)
        else:
            print("[!] Not enough packets captured for training")
            return
        
        print("\n[*] Phase 2: Starting real-time analysis...")
        print("[*] Press Ctrl+C to stop\n")
        
        # Start real-time capture and analysis
        capture.packet_count = 0
        capture.start_capture(prn=analyzer.process_packet)
        
    except KeyboardInterrupt:
        print("\n[*] Stopping capture...")
    finally:
        capture.stop_capture()
        
        if monitor == 'y':
            capture.disable_monitor_mode()
        
        # Final summary
        analyzer.display_status()
        print("\n[+] Analysis complete!")
        print(f"[+] Total packets analyzed: {analyzer.total_packets}")
        print(f"[+] Total flows tracked: {analyzer.total_flows}")
        print(f"[+] Total anomalies detected: {analyzer.anomaly_count}")


if __name__ == "__main__":
    main()
