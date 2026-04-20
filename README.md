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
- Create a targets.txt file with your targets (one per line):
google.com
github.com
1.1.1.1
192.168.1.100
example.com
- ## Run the scanner:
python sni_scanner.py targets.txt
🔴 Output Example 🟢 
=== Checking targets and ports ===
🟢 = Ping successful | 🔴 = Ping failed

[OK]   🟢 google.com -> 142.250.185.46 -> 443✔ 2053✖ 2083✖ 2087✖ 2096✖ 8443✖
[OK]   🟢 github.com -> 140.82.112.3 -> 443✔ 2053✖ 2083✖ 2087✖ 2096✖ 8443✖
[FAIL] 🔴 192.168.1.100 -> 192.168.1.100 -> 443✖ 2053✖ 2083✖ 2087✖ 2096✖ 8443✖

=== SUMMARY ===
OK targets (with open ports): 2
FAIL targets (all ports closed): 1
Total valid targets: 3

[✓] Results saved to: result.txt

📊 Output Format
Console Output

🟢 - Host responds to ping

🔴 - Host does not respond to ping

✔ - Port is open

✖ - Port is closed

[OK] - At least one port is open

[FAIL] - All ports are closed

File Output

All results are automatically saved to result.txt with the same format as console output, including summary statistics.

  ⚙️ Configuration
    You can modify the following parameters in the script:
    SCAN_PORTS = [443, 2053, 2083, 2087, 2096, 8443]  # Ports to scan
    CONNECTION_TIMEOUT = 2  # Connection timeout in seconds
    PING_TIMEOUT = 2  # Ping timeout in seconds
    OUTPUT_FILE = "result.txt"  # Output filename
    MAX_WORKERS = 100  # Maximum concurrent threads

🎯 Use Cases

Security auditing - Check which SSL/TLS ports are exposed

Network monitoring - Verify service availability across multiple hosts

CDN testing - Check edge server connectivity

Server migration - Verify port configurations

Penetration testing - Initial reconnaissance (authorized only)

⚠️ Important Notes

Ping behavior:

    Some servers block ICMP packets, showing 🔴 even if the host is online

    Ping is only sent once per IP to minimize network traffic

Rate limiting:

    The scanner uses 100 concurrent threads by default

    Adjust max_workers if you encounter rate limiting or network issues

Legal use:

    Only scan targets you own or have permission to test

    Unauthorized scanning may violate laws and terms of service



🐛 Troubleshooting

Issue: "No targets found in file"

Solution: Ensure targets.txt exists and contains targets (one per line)
Issue: "File 'targets.txt' not found"

Solution: Create the file or specify a custom input file path
Issue: Ping always shows 🔴 on Windows

Solution: Windows Firewall may block ICMP. This is normal and doesn't affect port scanning.
Issue: Slow scanning

Solution: Reduce CONNECTION_TIMEOUT or decrease max_workers value



📁 File Structure

sni-scanner/
├── sni_scanner.py      # Main scanner script
├── targets.txt         # Input targets (create this)
├── result.txt          # Output results (auto-generated)
└── README.md          # This file

🔧 Advanced Usage Examples

Scan specific IP range

# Create targets.txt with IPs
for i in {1..254}; do echo "192.168.1.$i" >> targets.txt; done
python3 sni_scanner.py

Combine with other tools
# Extract domains from a file and scan
grep -oP 'https?://\K[^/]+' urls.txt > targets.txt
python3 sni_scanner.py

⭐ Support
If you find this tool useful, please give it a star on GitHub!


    

