#!/usr/bin/env python3
"""
ADB Wireless Connection Script
Automatically connects to Android devices over WiFi using ADB.

Requirements:
- Android Debug Bridge (ADB) installed
- USB debugging enabled on device
- Device initially connected via USB for authorization
"""

import subprocess
import re
import sys
import os
import platform
import shutil
from pathlib import Path
import time

class ADBWirelessConnector:
    def __init__(self):
        self.adb_path = self._find_adb_path()
        self.system = platform.system().lower()
        
    def _find_adb_path(self):
        """Find ADB executable in system PATH or common installation locations."""
        # First check if adb is in PATH
        adb_cmd = shutil.which("adb")
        if adb_cmd:
            return adb_cmd
            
        # Common ADB installation paths
        common_paths = []
        
        if platform.system().lower() == "windows":
            common_paths = [
                os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe"),
                os.path.expandvars(r"%PROGRAMFILES(X86)%\Android\android-sdk\platform-tools\adb.exe"),
                os.path.expandvars(r"%PROGRAMFILES%\Android\android-sdk\platform-tools\adb.exe"),
                r"C:\adb\adb.exe",
                r"C:\platform-tools\adb.exe"
            ]
        elif platform.system().lower() == "darwin":  # macOS
            common_paths = [
                os.path.expanduser("~/Library/Android/sdk/platform-tools/adb"),
                "/usr/local/bin/adb",
                "/opt/homebrew/bin/adb"
            ]
        else:  # Linux
            common_paths = [
                os.path.expanduser("~/Android/Sdk/platform-tools/adb"),
                "/usr/local/bin/adb",
                "/usr/bin/adb",
                "/opt/android-sdk/platform-tools/adb"
            ]
            
        # Check each common path
        for path in common_paths:
            if os.path.isfile(path) and os.access(path, os.X_OK):
                return path
                
        return None
    
    def _run_cmd(self, cmd, timeout=10):
        """Execute ADB command with proper error handling."""
        if not self.adb_path:
            raise FileNotFoundError("ADB not found. Please install Android SDK platform-tools.")
            
        # Replace 'adb' with full path if needed
        if cmd.startswith('adb '):
            cmd = cmd.replace('adb ', f'"{self.adb_path}" ', 1)
            
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=timeout
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        except subprocess.TimeoutExpired:
            return "", "Command timed out", 1
        except Exception as e:
            return "", str(e), 1
    
    def check_adb_setup(self):
        """Verify ADB installation and setup."""
        print("[*] Checking ADB setup...")
        
        if not self.adb_path:
            print("[-] ADB not found in PATH or common locations.")
            print("\n[!] Please install ADB:")
            if self.system == "windows":
                print("    - Download SDK Platform-Tools from: https://developer.android.com/studio/releases/platform-tools")
                print("    - Or install via Chocolatey: choco install adb")
            elif self.system == "darwin":
                print("    - Install via Homebrew: brew install android-platform-tools")
                print("    - Or download from: https://developer.android.com/studio/releases/platform-tools")
            else:
                print("    - Install via package manager: sudo apt install android-tools-adb")
                print("    - Or download from: https://developer.android.com/studio/releases/platform-tools")
            return False
            
        print(f"[+] ADB found at: {self.adb_path}")
        
        # Test ADB
        stdout, stderr, returncode = self._run_cmd("adb version")
        if returncode != 0:
            print(f"[-] ADB test failed: {stderr}")
            return False
            
        print(f"[+] ADB version: {stdout.split()[4] if len(stdout.split()) > 4 else 'Unknown'}")
        return True
    
    def check_devices(self):
        """Check for connected and authorized devices."""
        print("[*] Checking for connected devices...")
        stdout, stderr, returncode = self._run_cmd("adb devices")
        
        if returncode != 0:
            print(f"[-] Failed to list devices: {stderr}")
            return False
            
        lines = stdout.strip().split('\n')[1:]  # Skip header
        devices = [line.strip() for line in lines if line.strip()]
        
        if not devices:
            print("[-] No devices found.")
            print("[!] Please:")
            print("    1. Connect your device via USB")
            print("    2. Enable USB debugging in Developer Options")
            print("    3. Authorize the connection on your device")
            return False
            
        authorized_devices = []
        unauthorized_devices = []
        
        for device in devices:
            if '\tdevice' in device:
                authorized_devices.append(device.split('\t')[0])
            elif '\tunauthorized' in device:
                unauthorized_devices.append(device.split('\t')[0])
                
        if unauthorized_devices:
            print(f"[-] Found {len(unauthorized_devices)} unauthorized device(s):")
            for device in unauthorized_devices:
                print(f"    {device}")
            print("[!] Please authorize the connection on your device(s)")
            return False
            
        if not authorized_devices:
            print("[-] No authorized devices found.")
            return False
            
        print(f"[+] Found {len(authorized_devices)} authorized device(s):")
        for device in authorized_devices:
            print(f"    {device}")
        return True
    
    def get_device_ip(self):
        """Get device IP address from WiFi interface."""
        print("[*] Getting device IP address...")
        
        # Try different network interfaces
        interfaces = ['wlan0', 'wlan1', 'eth0', 'rmnet_data0']
        
        for interface in interfaces:
            stdout, stderr, returncode = self._run_cmd(f"adb shell ip -f inet addr show {interface}")
            
            if returncode == 0 and stdout:
                # Look for inet address
                match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)/\d+', stdout)
                if match:
                    ip = match.group(1)
                    # Skip localhost
                    if not ip.startswith('127.'):
                        print(f"[+] Found IP on {interface}: {ip}")
                        return ip
        
        # Fallback: try getprop
        stdout, stderr, returncode = self._run_cmd("adb shell getprop dhcp.wlan0.ipaddress")
        if returncode == 0 and stdout and not stdout.startswith('127.'):
            ip = stdout.strip()
            print(f"[+] Found IP via getprop: {ip}")
            return ip
            
        print("[-] Failed to get device IP address.")
        print("[!] Make sure your device is connected to WiFi")
        return None
    
    def enable_tcpip_mode(self, port=5555):
        """Enable TCP/IP mode on ADB."""
        print(f"[*] Enabling TCP/IP mode on port {port}...")
        stdout, stderr, returncode = self._run_cmd(f"adb tcpip {port}")
        
        if returncode != 0:
            print(f"[-] Failed to enable TCP/IP mode: {stderr}")
            return False
            
        print("[+] TCP/IP mode enabled")
        # Give device time to switch modes
        time.sleep(2)
        return True
    
    def connect_wireless(self, ip, port=5555, max_retries=3):
        """Connect to device wirelessly."""
        target = f"{ip}:{port}"
        print(f"[*] Connecting to {target}...")
        
        for attempt in range(max_retries):
            stdout, stderr, returncode = self._run_cmd(f"adb connect {target}", timeout=15)
            
            if returncode == 0:
                output = stdout.lower()
                if "connected" in output:
                    if "already connected" in output:
                        print(f"[+] Already connected to {target}")
                    else:
                        print(f"[+] Successfully connected to {target}")
                    return True
                    
            if attempt < max_retries - 1:
                print(f"[*] Connection attempt {attempt + 1} failed, retrying...")
                time.sleep(2)
            else:
                print(f"[-] Failed to connect after {max_retries} attempts")
                if stderr:
                    print(f"    Error: {stderr}")
                if stdout:
                    print(f"    Output: {stdout}")
                    
        return False
    
    def verify_wireless_connection(self):
        """Verify wireless connection is working."""
        print("[*] Verifying wireless connection...")
        stdout, stderr, returncode = self._run_cmd("adb devices")
        
        if returncode != 0:
            print(f"[-] Failed to verify connection: {stderr}")
            return False
            
        # Look for IP:port in devices list
        wireless_devices = [line for line in stdout.split('\n') if ':' in line and 'device' in line]
        
        if wireless_devices:
            print("[+] Wireless connection verified!")
            for device in wireless_devices:
                device_id = device.split('\t')[0]
                print(f"    Connected: {device_id}")
            return True
        else:
            print("[-] No wireless devices found")
            return False
    
    def run(self):
        """Main execution flow."""
        print("=" * 50)
        print("ADB Wireless Connection Script")
        print("=" * 50)
        
        # Check ADB setup
        if not self.check_adb_setup():
            return 1
            
        # Check for devices
        if not self.check_devices():
            return 1
            
        # Get device IP
        ip = self.get_device_ip()
        if not ip:
            return 1
            
        # Enable TCP/IP mode
        if not self.enable_tcpip_mode():
            return 1
            
        # Connect wirelessly
        if not self.connect_wireless(ip):
            return 1
            
        # Verify connection
        if not self.verify_wireless_connection():
            return 1
            
        print("\n[✓] Setup complete! You can now disconnect the USB cable.")
        print(f"[✓] Your device is accessible at {ip}:5555")
        print("\nTo disconnect later, use: adb disconnect")
        return 0

def main():
    """Entry point."""
    try:
        connector = ADBWirelessConnector()
        return connector.run()
    except KeyboardInterrupt:
        print("\n[!] Operation cancelled by user")
        return 1
    except Exception as e:
        print(f"\n[-] Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
