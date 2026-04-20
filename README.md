# 🔍 SNI Port Scanner

A powerful multi-threaded Python tool for scanning SSL/TLS ports and checking connectivity across multiple targets. This scanner checks common HTTPS/SSL ports and includes ping verification to test host reachability.

## ✨ Features

- **Multi-threaded scanning** - Fast concurrent scanning of multiple targets
- **Ping verification** - Checks host reachability with visual indicators (🟢/🔴)
- **Port scanning** - Scans common SSL/TLS ports:
  - 443 (HTTPS)
  - 2053 (k8s)
  - 2083 (cPanel SSL)
  - 2087 (cPanel SSL)
  - 2096 (cPanel webmail SSL)
  - 8443 (Alternate HTTPS)
- **Domain resolution** - Automatically resolves domain names to IP addresses
- **Dual output** - Results displayed in console and saved to file
- **Cross-platform** - Works on Windows, Linux, and macOS

## 📋 Prerequisites

- Python 3.6 or higher
socket
sys
os
subprocess
platform


