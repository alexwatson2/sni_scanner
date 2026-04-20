#!/usr/bin/env python3
# SNI Scanner - Python version with ping check

import socket
import sys
import os
import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed

SCAN_PORTS = [443, 2053, 2083, 2087, 2096, 8443]
CONNECTION_TIMEOUT = 2
OUTPUT_FILE = "result.txt"
PING_TIMEOUT = 2  # timeout for ping in seconds

def is_private_ip(ip):
    return False 

def resolve_domain(domain):
    try:
        ips = socket.getaddrinfo(domain, None, socket.AF_INET)
        unique_ips = list(set(ip[4][0] for ip in ips))
        return unique_ips
    except socket.gaierror:
        return []

def check_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(CONNECTION_TIMEOUT)
            result = sock.connect_ex((ip, port))
            return result == 0
    except:
        return False

def ping_host(ip):
    """Check if host responds to ping (one time only)"""
    try:
        # Determine ping command based on OS
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        timeout_param = '-w' if platform.system().lower() == 'windows' else '-W'
        
        # Build ping command
        command = ['ping', param, '1', timeout_param, str(PING_TIMEOUT), ip]
        
        # Execute ping
        result = subprocess.run(command, 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL,
                               timeout=PING_TIMEOUT)
        
        return result.returncode == 0
    except:
        return False

def scan_target(target):
    parts = target.split('.')
    is_direct_ip = (len(parts) == 4 and all(p.isdigit() for p in parts))

    if is_direct_ip:
        ips = [target]
    else:
        ips = resolve_domain(target)

    if not ips:
        return None

    results = []
    any_open = False

    for ip in ips:
        # Check ping once for this IP
        ping_success = ping_host(ip)
        
        port_results = []
        for port in SCAN_PORTS:
            is_open = check_port(ip, port)
            port_results.append((port, is_open))
            if is_open:
                any_open = True

        results.append({
            'ip': ip,
            'ports': port_results,
            'ping': ping_success
        })

    return (target, ips, results, any_open)

def format_result_line(result_data):
    """فرمت کردن نتیجه برای ذخیره در فایل"""
    if result_data is None:
        return None
    
    target, ips, results, is_open = result_data
    lines = []
    
    for result in results:
        ip = result['ip']
        ping_status = result['ping']
        ping_symbol = '🟢' if ping_status else '🔴'  # Green circle if ping works, red if not
        
        port_str = ""
        for port, is_open_port in result['ports']:
            symbol = '✔' if is_open_port else '✖'
            port_str += f" {port}{symbol}"

        line = f"{ping_symbol} {target} -> {ip} ->{port_str}"
        
        if is_open:
            lines.append(f"[OK]   {line}")
        else:
            lines.append(f"[FAIL] {line}")
    
    return lines

def main():
    # باز کردن فایل خروجی برای نوشتن
    output_file_handle = open(OUTPUT_FILE, 'w', encoding='utf-8')
    
    try:
        if len(sys.argv) > 1:
            input_file = sys.argv[1]
        else:
            input_file = "targets.txt"

        if not os.path.exists(input_file):
            print(f"Error: File '{input_file}' not found")
            return

        targets = []
        with open(input_file, 'r') as f:
            for line in f:
                target = line.strip()
                if target:
                    targets.append(target)

        if not targets:
            print("No targets found in file")
            return

        print()
        print("=== Checking targets and ports ===")
        print("🟢 = Ping successful | 🔴 = Ping failed")
        print()
        
        # نوشتن هدر در فایل
        output_file_handle.write("=== SNI Scanner Results ===\n")
        output_file_handle.write(f"Total targets: {len(targets)}\n")
        output_file_handle.write("🟢 = Ping successful | 🔴 = Ping failed\n")
        output_file_handle.write("=" * 50 + "\n\n")

        results_data = []

        with ThreadPoolExecutor(max_workers=20) as executor:
            future_to_target = {executor.submit(scan_target, target): target for target in targets}

            for future in as_completed(future_to_target):
                result = future.result()
                if result is not None:
                    results_data.append(result)
                    
                    # چاپ در کنسول
                    lines = format_result_line(result)
                    if lines:
                        for line in lines:
                            print(line)
                            # ذخیره در فایل
                            output_file_handle.write(line + "\n")
                            output_file_handle.flush()

        # جداسازی نتایج
        ok_list = [r for r in results_data if r[3]]
        fail_list = [r for r in results_data if not r[3]]

        # نوشتن خلاصه در فایل
        output_file_handle.write("\n" + "=" * 50 + "\n")
        output_file_handle.write(f"SUMMARY:\n")
        output_file_handle.write(f"OK targets (with open ports): {len(ok_list)}\n")
        output_file_handle.write(f"FAIL targets (all ports closed): {len(fail_list)}\n")
        output_file_handle.write(f"Total valid targets: {len(results_data)}\n")

        if ok_list:
            print()
            print("=== OK (at least one open port) ===")
            print()
            output_file_handle.write("\n=== OK (at least one open port) ===\n\n")
            
            for result in ok_list:
                lines = format_result_line(result)
                if lines:
                    for line in lines:
                        print(line)
                        output_file_handle.write(line + "\n")

        if fail_list:
            print()
            print("=== FAIL (all ports closed) ===")
            print()
            output_file_handle.write("\n=== FAIL (all ports closed) ===\n\n")
            
            for result in fail_list:
                lines = format_result_line(result)
                if lines:
                    for line in lines:
                        print(line)
                        output_file_handle.write(line + "\n")

        print()
        print(f"\n[✓] Results saved to: {OUTPUT_FILE}")
        print(f"[✓] Total targets scanned: {len(results_data)} (resolve fails ignored)")

    finally:
        output_file_handle.close()

if __name__ == "__main__":
    main()