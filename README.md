
## ADB Wireless IP Connection Script

A Python script to automatically set up wireless ADB connections for Android devices. No more USB cables needed after initial setup!

## Features

- 🔍 **Auto-detects ADB installation** across Windows, macOS, and Linux
- 📱 **Multiple device support** with proper device authorization checking  
- 🌐 **Smart IP detection** across different network interfaces
- 🔄 **Retry mechanism** for reliable connections
- ✅ **Connection verification** to ensure everything works
- 🛠️ **Comprehensive error handling** with helpful troubleshooting messages

## Prerequisites

### 1. Install ADB (Android Debug Bridge)

#### Windows
```bash
# Option 1: Using Chocolatey
choco install adb

# Option 2: Manual installation
# Download SDK Platform-Tools from:
# https://developer.android.com/studio/releases/platform-tools
```

#### macOS
```bash
# Using Homebrew
brew install android-platform-tools
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt install android-tools-adb
```

### 2. Enable Developer Options on Android
1. Go to **Settings** → **About Phone**
2. Tap **Build Number** 7 times
3. Go back to **Settings** → **Developer Options** 
4. Enable **USB Debugging**

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/adb-wireless-connector.git
cd adb-wireless-connector
```

2. Make the script executable (Linux/macOS):
```bash
chmod +x adb_wireless.py
```

## Usage

### Quick Start
1. Connect your Android device via USB
2. Run the script:
```bash
python adb_wireless.py
```
3. When prompted, authorize the connection on your device
4. Follow the on-screen instructions
5. Disconnect USB cable once wireless connection is established

### What the Script Does
1. ✅ Verifies ADB installation and setup
2. 📱 Checks for connected and authorized devices
3. 🌐 Detects your device's WiFi IP address
4. 🔌 Enables ADB TCP/IP mode on port 5555
5. 📡 Establishes wireless connection
6. ✅ Verifies the connection works

### Example Output
```
==================================================
ADB Wireless Connection Script
==================================================
[*] Checking ADB setup...
[+] ADB found at: /usr/local/bin/adb
[+] ADB version: 34.0.4
[*] Checking for connected devices...
[+] Found 1 authorized device(s):
    1A2B3C4D5E6F
[*] Getting device IP address...
[+] Found IP on wlan0: 192.168.1.100
[*] Enabling TCP/IP mode on port 5555...
[+] TCP/IP mode enabled
[*] Connecting to 192.168.1.100:5555...
[+] Successfully connected to 192.168.1.100:5555
[*] Verifying wireless connection...
[+] Wireless connection verified!
    Connected: 192.168.1.100:5555

[✓] Setup complete! You can now disconnect the USB cable.
[✓] Your device is accessible at 192.168.1.100:5555

To disconnect later, use: adb disconnect
```

## Troubleshooting

### "ADB not found"
- Install ADB using the methods above
- Ensure ADB is in your system PATH
- The script checks common installation locations automatically

### "No authorized devices found"
- Connect your device via USB first
- Enable USB debugging in Developer Options
- Authorize the connection when prompted on your device
- Try a different USB cable or port

### "Failed to get IP address"
- Make sure your device is connected to WiFi
- Check that both your computer and device are on the same network
- Some devices may use different network interface names

### "Failed to connect wirelessly"
- Ensure your device and computer are on the same WiFi network
- Some corporate/public networks may block ADB connections
- Try restarting the ADB server: `adb kill-server && adb start-server`
- Check if port 5555 is blocked by firewall

## Advanced Usage

### Using Different Ports
The script uses port 5555 by default, but you can modify it in the code:
```python
connector.enable_tcpip_mode(port=5556)  # Use port 5556 instead
```

### Multiple Devices
The script will work with the first authorized device found. For multiple devices, you may need to run it separately for each device.

### Disconnecting
```bash
# Disconnect specific device
adb disconnect 192.168.1.100:5555

# Disconnect all wireless devices
adb disconnect
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Android Developer Documentation for ADB reference
- Community contributions and feedback

---

**Note**: This tool is for development purposes. Ensure you understand the security implications of enabling wireless ADB debugging.
