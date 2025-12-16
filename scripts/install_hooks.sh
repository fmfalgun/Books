#!/bin/bash
chmod +x .githooks/*
git config core.hooksPath .githooks
echo "[+] Git hooks installed"

