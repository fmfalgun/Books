"""
WiFi Traffic Multi-Task AI Analysis System
Analyzes Wireshark .pcap files for:
- Anomaly/Intrusion Detection
- Traffic Classification
- Network Performance Prediction
- Device Fingerprinting

Requirements:
pip install scapy numpy pandas scikit-learn xgboost lightgbm tensorflow pyshark
"""

import numpy as np
import pandas as pd
from scapy.all import rdpcap, IP, TCP, UDP, ICMP
from sklearn.ensemble import IsolationForest, RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import xgboost as xgb
import lightgbm as lgb
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# For deep learning models
try:
    from tensorflow.keras.models import Model, Sequential
    from tensorflow.keras.layers import Input, Dense, LSTM, Dropout, Conv1D, MaxPooling1D, Flatten
    from tensorflow.keras.optimizers import Adam
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("TensorFlow not available. Deep learning models disabled.")


class PCAPFeatureExtractor:
    """Extract features from PCAP files for ML analysis"""
    
    def __init__(self):
        self.features = []
        self.flow_dict = defaultdict(list)
        
    def extract_packet_features(self, packet):
        """Extract features from a single packet"""
        features = {}
        
        # Basic packet info
        features['packet_length'] = len(packet)
        features['timestamp'] = float(packet.time)
        
        # Protocol flags
        features['has_ip'] = 1 if packet.haslayer(IP) else 0
        features['has_tcp'] = 1 if packet.haslayer(TCP) else 0
        features['has_udp'] = 1 if packet.haslayer(UDP) else 0
        features['has_icmp'] = 1 if packet.haslayer(ICMP) else 0
        
        if packet.haslayer(IP):
            ip_layer = packet[IP]
            features['ip_len'] = ip_layer.len
            features['ip_ttl'] = ip_layer.ttl
            features['ip_proto'] = ip_layer.proto
            features['src_ip'] = ip_layer.src
            features['dst_ip'] = ip_layer.dst
            
            # TCP features
            if packet.haslayer(TCP):
                tcp_layer = packet[TCP]
                features['src_port'] = tcp_layer.sport
                features['dst_port'] = tcp_layer.dport
                features['tcp_flags'] = int(tcp_layer.flags)
                features['tcp_window'] = tcp_layer.window
                features['tcp_seq'] = tcp_layer.seq
                features['tcp_ack'] = tcp_layer.ack
                
                # Flag breakdown
                features['flag_syn'] = 1 if 'S' in str(tcp_layer.flags) else 0
                features['flag_ack'] = 1 if 'A' in str(tcp_layer.flags) else 0
                features['flag_fin'] = 1 if 'F' in str(tcp_layer.flags) else 0
                features['flag_rst'] = 1 if 'R' in str(tcp_layer.flags) else 0
                features['flag_psh'] = 1 if 'P' in str(tcp_layer.flags) else 0
                
            # UDP features
            elif packet.haslayer(UDP):
                udp_layer = packet[UDP]
                features['src_port'] = udp_layer.sport
                features['dst_port'] = udp_layer.dport
                features['udp_len'] = udp_layer.len
            else:
                features['src_port'] = 0
                features['dst_port'] = 0
        
        return features
    
    def extract_flow_features(self, packets, window_size=10):
        """Extract flow-level features from packet sequences"""
        flows = defaultdict(lambda: {
            'packets': [],
            'bytes': [],
            'intervals': [],
            'src_ip': None,
            'dst_ip': None
        })
        
        # Group packets into flows
        for pkt in packets:
            if pkt.haslayer(IP):
                flow_key = self._get_flow_key(pkt)
                flows[flow_key]['packets'].append(pkt)
                flows[flow_key]['bytes'].append(len(pkt))
                flows[flow_key]['src_ip'] = pkt[IP].src
                flows[flow_key]['dst_ip'] = pkt[IP].dst
                
                if len(flows[flow_key]['packets']) > 1:
                    time_diff = float(pkt.time) - float(flows[flow_key]['packets'][-2].time)
                    flows[flow_key]['intervals'].append(time_diff)
        
        # Compute flow statistics
        flow_features = []
        for flow_key, flow_data in flows.items():
            if len(flow_data['packets']) < 2:
                continue
                
            feat = {}
            feat['flow_duration'] = float(flow_data['packets'][-1].time) - float(flow_data['packets'][0].time)
            feat['flow_packet_count'] = len(flow_data['packets'])
            feat['flow_byte_count'] = sum(flow_data['bytes'])
            feat['flow_bytes_per_packet_mean'] = np.mean(flow_data['bytes'])
            feat['flow_bytes_per_packet_std'] = np.std(flow_data['bytes'])
            feat['flow_bytes_per_packet_min'] = np.min(flow_data['bytes'])
            feat['flow_bytes_per_packet_max'] = np.max(flow_data['bytes'])
            
            if flow_data['intervals']:
                feat['flow_inter_arrival_mean'] = np.mean(flow_data['intervals'])
                feat['flow_inter_arrival_std'] = np.std(flow_data['intervals'])
                feat['flow_inter_arrival_min'] = np.min(flow_data['intervals'])
                feat['flow_inter_arrival_max'] = np.max(flow_data['intervals'])
            else:
                feat['flow_inter_arrival_mean'] = 0
                feat['flow_inter_arrival_std'] = 0
                feat['flow_inter_arrival_min'] = 0
                feat['flow_inter_arrival_max'] = 0
            
            feat['src_ip'] = flow_data['src_ip']
            feat['dst_ip'] = flow_data['dst_ip']
            
            flow_features.append(feat)
        
        return flow_features
    
    def _get_flow_key(self, packet):
        """Generate flow identifier"""
        if packet.haslayer(IP):
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
            
            # Bidirectional flow
            return tuple(sorted([(src_ip, src_port), (dst_ip, dst_port)]) + [proto])
        return None
    
    def process_pcap(self, pcap_file, max_packets=None):
        """Process PCAP file and extract all features"""
        print(f"Reading PCAP file: {pcap_file}")
        packets = rdpcap(pcap_file)
        
        if max_packets:
            packets = packets[:max_packets]
        
        print(f"Processing {len(packets)} packets...")
        
        # Extract packet-level features
        packet_features = []
        for pkt in packets:
            try:
                feat = self.extract_packet_features(pkt)
                packet_features.append(feat)
            except Exception as e:
                continue
        
        # Extract flow-level features
        flow_features = self.extract_flow_features(packets)
        
        return packet_features, flow_features


class MultiTaskWiFiAnalyzer:
    """Multi-task AI system for WiFi traffic analysis"""
    
    def __init__(self):
        self.anomaly_detector = None
        self.traffic_classifier = None
        self.performance_predictor = None
        self.device_fingerprinter = None
        self.scaler = StandardScaler()
        self.feature_columns = None
        
    def prepare_features(self, flow_features_list):
        """Convert flow features to numerical array"""
        df = pd.DataFrame(flow_features_list)
        
        # Store IP addresses separately for device fingerprinting
        ip_data = df[['src_ip', 'dst_ip']].copy() if 'src_ip' in df.columns else None
        
        # Select numerical features
        numerical_cols = [col for col in df.columns if col not in ['src_ip', 'dst_ip']]
        X = df[numerical_cols].fillna(0)
        
        if self.feature_columns is None:
            self.feature_columns = X.columns.tolist()
        
        # Ensure consistent feature columns
        for col in self.feature_columns:
            if col not in X.columns:
                X[col] = 0
        
        X = X[self.feature_columns]
        
        return X.values, ip_data
    
    def train_anomaly_detector(self, X, contamination=0.1):
        """Train Isolation Forest for anomaly detection"""
        print("\n=== Training Anomaly Detector (Isolation Forest) ===")
        self.anomaly_detector = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100,
            max_samples='auto'
        )
        
        X_scaled = self.scaler.fit_transform(X)
        self.anomaly_detector.fit(X_scaled)
        
        # Get anomaly scores
        scores = self.anomaly_detector.score_samples(X_scaled)
        predictions = self.anomaly_detector.predict(X_scaled)
        
        anomaly_count = np.sum(predictions == -1)
        print(f"Training complete. Detected {anomaly_count}/{len(predictions)} anomalies ({anomaly_count/len(predictions)*100:.2f}%)")
        
        return predictions
    
    def train_traffic_classifier(self, X, y=None):
        """Train traffic classifier (unsupervised clustering if no labels)"""
        print("\n=== Training Traffic Classifier (XGBoost) ===")
        
        if y is None:
            # Unsupervised: use clustering to create pseudo-labels
            from sklearn.cluster import KMeans
            print("No labels provided. Using KMeans clustering for pseudo-labeling...")
            kmeans = KMeans(n_clusters=5, random_state=42)
            y = kmeans.fit_predict(self.scaler.fit_transform(X))
            print(f"Created {len(np.unique(y))} traffic classes")
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.traffic_classifier = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42
        )
        
        self.traffic_classifier.fit(X_train, y_train)
        
        train_acc = self.traffic_classifier.score(X_train, y_train)
        test_acc = self.traffic_classifier.score(X_test, y_test)
        
        print(f"Training accuracy: {train_acc:.4f}")
        print(f"Testing accuracy: {test_acc:.4f}")
        
        return self.traffic_classifier
    
    def train_performance_predictor(self, X, throughput=None):
        """Train network performance predictor"""
        print("\n=== Training Performance Predictor (Random Forest Regressor) ===")
        
        if throughput is None:
            # Simulate throughput based on flow characteristics
            throughput = X[:, 2] / (X[:, 0] + 1)  # bytes / duration
        
        X_train, X_test, y_train, y_test = train_test_split(X, throughput, test_size=0.2, random_state=42)
        
        self.performance_predictor = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        self.performance_predictor.fit(X_train, y_train)
        
        train_score = self.performance_predictor.score(X_train, y_train)
        test_score = self.performance_predictor.score(X_test, y_test)
        
        print(f"Training R² score: {train_score:.4f}")
        print(f"Testing R² score: {test_score:.4f}")
        
        return self.performance_predictor
    
    def train_device_fingerprinter(self, X, device_labels=None):
        """Train device fingerprinting model"""
        print("\n=== Training Device Fingerprinter (LightGBM) ===")
        
        if device_labels is None:
            # Unsupervised: cluster devices
            from sklearn.cluster import DBSCAN
            print("No device labels provided. Using DBSCAN clustering...")
            dbscan = DBSCAN(eps=0.5, min_samples=5)
            device_labels = dbscan.fit_predict(self.scaler.fit_transform(X))
            n_devices = len(set(device_labels)) - (1 if -1 in device_labels else 0)
            print(f"Identified {n_devices} device clusters")
        
        # Filter out noise points (-1)
        valid_idx = device_labels != -1
        X_valid = X[valid_idx]
        y_valid = device_labels[valid_idx]
        
        if len(np.unique(y_valid)) < 2:
            print("Not enough device clusters for classification")
            return None
        
        X_train, X_test, y_train, y_test = train_test_split(X_valid, y_valid, test_size=0.2, random_state=42)
        
        self.device_fingerprinter = lgb.LGBMClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42
        )
        
        self.device_fingerprinter.fit(X_train, y_train)
        
        train_acc = self.device_fingerprinter.score(X_train, y_train)
        test_acc = self.device_fingerprinter.score(X_test, y_test)
        
        print(f"Training accuracy: {train_acc:.4f}")
        print(f"Testing accuracy: {test_acc:.4f}")
        
        return self.device_fingerprinter
    
    def predict(self, X):
        """Make predictions with all models"""
        X_scaled = self.scaler.transform(X)
        
        results = {}
        
        if self.anomaly_detector:
            results['anomaly_scores'] = self.anomaly_detector.score_samples(X_scaled)
            results['is_anomaly'] = self.anomaly_detector.predict(X_scaled)
        
        if self.traffic_classifier:
            results['traffic_class'] = self.traffic_classifier.predict(X)
            results['traffic_class_proba'] = self.traffic_classifier.predict_proba(X)
        
        if self.performance_predictor:
            results['predicted_throughput'] = self.performance_predictor.predict(X)
        
        if self.device_fingerprinter:
            results['device_id'] = self.device_fingerprinter.predict(X)
            results['device_proba'] = self.device_fingerprinter.predict_proba(X)
        
        return results
    
    def analyze_realtime(self, pcap_file, report=True):
        """Real-time analysis of PCAP file"""
        print("\n" + "="*60)
        print("REAL-TIME WiFi TRAFFIC ANALYSIS")
        print("="*60)
        
        # Extract features
        extractor = PCAPFeatureExtractor()
        packet_features, flow_features = extractor.process_pcap(pcap_file)
        
        if not flow_features:
            print("No flows detected in PCAP file")
            return None
        
        # Prepare features
        X, ip_data = self.prepare_features(flow_features)
        
        # Make predictions
        results = self.predict(X)
        
        if report:
            self._print_analysis_report(results, flow_features, ip_data)
        
        return results
    
    def _print_analysis_report(self, results, flow_features, ip_data):
        """Print comprehensive analysis report"""
        print("\n" + "="*60)
        print("ANALYSIS REPORT")
        print("="*60)
        
        print(f"\nTotal flows analyzed: {len(flow_features)}")
        
        if 'is_anomaly' in results:
            anomaly_count = np.sum(results['is_anomaly'] == -1)
            print(f"\n--- Anomaly Detection ---")
            print(f"Anomalies detected: {anomaly_count}/{len(results['is_anomaly'])} ({anomaly_count/len(results['is_anomaly'])*100:.2f}%)")
            print(f"Average anomaly score: {np.mean(results['anomaly_scores']):.4f}")
            
            if anomaly_count > 0:
                anomaly_indices = np.where(results['is_anomaly'] == -1)[0]
                print(f"\nTop 5 anomalous flows:")
                top_anomalies = np.argsort(results['anomaly_scores'])[:5]
                for idx in top_anomalies:
                    if idx < len(flow_features):
                        flow = flow_features[idx]
                        print(f"  Flow {idx}: {flow.get('src_ip', 'N/A')} -> {flow.get('dst_ip', 'N/A')}, "
                              f"Score: {results['anomaly_scores'][idx]:.4f}")
        
        if 'traffic_class' in results:
            print(f"\n--- Traffic Classification ---")
            unique_classes, counts = np.unique(results['traffic_class'], return_counts=True)
            print(f"Identified {len(unique_classes)} traffic classes:")
            for cls, count in zip(unique_classes, counts):
                print(f"  Class {cls}: {count} flows ({count/len(results['traffic_class'])*100:.2f}%)")
        
        if 'predicted_throughput' in results:
            print(f"\n--- Performance Prediction ---")
            print(f"Average predicted throughput: {np.mean(results['predicted_throughput']):.2f} bytes/sec")
            print(f"Max predicted throughput: {np.max(results['predicted_throughput']):.2f} bytes/sec")
            print(f"Min predicted throughput: {np.min(results['predicted_throughput']):.2f} bytes/sec")
        
        if 'device_id' in results:
            print(f"\n--- Device Fingerprinting ---")
            unique_devices, counts = np.unique(results['device_id'], return_counts=True)
            print(f"Identified {len(unique_devices)} unique devices:")
            for dev, count in zip(unique_devices, counts):
                print(f"  Device {dev}: {count} flows ({count/len(results['device_id'])*100:.2f}%)")


def main():
    """Example usage"""
    
    # Initialize system
    print("Initializing Multi-Task WiFi Analyzer...")
    analyzer = MultiTaskWiFiAnalyzer()
    extractor = PCAPFeatureExtractor()
    
    # Example: Process PCAP file for training
    pcap_file = "sample_traffic.pcap"  # Replace with your PCAP file
    
    print(f"\nProcessing PCAP file: {pcap_file}")
    
    try:
        # Extract features
        packet_features, flow_features = extractor.process_pcap(pcap_file, max_packets=1000)
        
        if not flow_features:
            print("No flows detected. Please provide a valid PCAP file.")
            return
        
        # Prepare features
        X, ip_data = analyzer.prepare_features(flow_features)
        
        print(f"\nExtracted {X.shape[0]} flows with {X.shape[1]} features")
        
        # Train all models
        analyzer.train_anomaly_detector(X, contamination=0.1)
        analyzer.train_traffic_classifier(X)
        analyzer.train_performance_predictor(X)
        analyzer.train_device_fingerprinter(X)
        
        # Real-time analysis
        print("\n" + "="*60)
        print("Testing Real-Time Analysis")
        print("="*60)
        results = analyzer.analyze_realtime(pcap_file, report=True)
        
        print("\n" + "="*60)
        print("Analysis Complete!")
        print("="*60)
        
    except FileNotFoundError:
        print(f"\nError: PCAP file '{pcap_file}' not found.")
        print("\nTo use this system:")
        print("1. Capture WiFi traffic using Wireshark and save as .pcap")
        print("2. Update 'pcap_file' variable with your file path")
        print("3. Run the script again")
        print("\nExample usage:")
        print("  analyzer = MultiTaskWiFiAnalyzer()")
        print("  extractor = PCAPFeatureExtractor()")
        print("  packet_features, flow_features = extractor.process_pcap('your_file.pcap')")
        print("  X, ip_data = analyzer.prepare_features(flow_features)")
        print("  analyzer.train_anomaly_detector(X)")
        print("  results = analyzer.analyze_realtime('your_file.pcap')")


if __name__ == "__main__":
    main()
