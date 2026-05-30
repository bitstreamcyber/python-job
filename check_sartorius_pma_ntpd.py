"""
Sartorius Evolution PMA - USB Connection Checker
Detects if the scale is connected by scanning for "PMA USB Serial" in Device Manager.
Requires: pip install pyserial pywin32
"""

import sys
import time

def check_device_connected():
    """Check if the Sartorius PMA USB Serial device is connected."""
    try:
        import winreg
    except ImportError:
        print("ERROR: This script must be run on Windows.")
        sys.exit(1)

    device_found = False
    device_info = []

    # Search through Device Manager registry entries
    reg_paths = [
        r"SYSTEM\CurrentControlSet\Enum\USB",
        r"SYSTEM\CurrentControlSet\Enum\USBSER",
    ]

    for reg_path in reg_paths:
        try:
            base_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
            num_subkeys = winreg.QueryInfoKey(base_key)[0]

            for i in range(num_subkeys):
                try:
                    subkey_name = winreg.EnumKey(base_key, i)
                    subkey = winreg.OpenKey(base_key, subkey_name)
                    num_devices = winreg.QueryInfoKey(subkey)[0]

                    for j in range(num_devices):
                        try:
                            device_key_name = winreg.EnumKey(subkey, j)
                            device_key = winreg.OpenKey(subkey, device_key_name)

                            try:
                                friendly_name, _ = winreg.QueryValueEx(device_key, "FriendlyName")
                                if "PMA USB Serial" in friendly_name or "PMA" in friendly_name:
                                    device_found = True
                                    device_info.append(friendly_name)
                            except FileNotFoundError:
                                pass

                            try:
                                dev_desc, _ = winreg.QueryValueEx(device_key, "DeviceDesc")
                                if "PMA USB Serial" in dev_desc or "PMA" in dev_desc:
                                    device_found = True
                                    device_info.append(dev_desc)
                            except FileNotFoundError:
                                pass

                            winreg.CloseKey(device_key)
                        except (OSError, WindowsError):
                            continue

                    winreg.CloseKey(subkey)
                except (OSError, WindowsError):
                    continue

            winreg.CloseKey(base_key)
        except (OSError, WindowsError):
            continue

    # Also check via serial ports (pyserial)
    com_port = check_via_serial_ports()

    return device_found, list(set(device_info)), com_port


def check_via_serial_ports():
    """Use pyserial to list COM ports and find PMA device."""
    try:
        from serial.tools import list_ports
        ports = list_ports.comports()
        for port in ports:
            desc = (port.description or "").upper()
            name = (port.name or "").upper()
            hwid = (port.hwid or "").upper()
            if "PMA" in desc or "PMA" in hwid:
                return port.device  # e.g. "COM3"
        return None
    except ImportError:
        return None  # pyserial not installed


def print_status(device_found, device_info, com_port):
    """Print a clean status report to the terminal."""
    print("=" * 50)
    print("  Sartorius Evolution PMA - Connection Status")
    print("=" * 50)

    if device_found or com_port:
        print("  STATUS : ✔  CONNECTED")
        if device_info:
            for info in device_info:
                print(f"  Device : {info}")
        if com_port:
            print(f"  COM Port: {com_port}")
    else:
        print("  STATUS : ✘  NOT CONNECTED")
        print("  The Sartorius PMA USB Serial device was not found.")
        print("  • Make sure the USB cable is plugged in.")
        print("  • Check Device Manager for driver issues.")

    print("=" * 50)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Check if Sartorius Evolution PMA scale is connected via USB."
    )
    parser.add_argument(
        "--watch", "-w",
        action="store_true",
        help="Keep monitoring and refresh every 5 seconds (Ctrl+C to stop)."
    )
    parser.add_argument(
        "--interval", "-i",
        type=int,
        default=5,
        help="Refresh interval in seconds when using --watch (default: 5)."
    )
    args = parser.parse_args()

    if args.watch:
        print("Monitoring mode — press Ctrl+C to stop.\n")
        try:
            while True:
                found, info, port = check_device_connected()
                print_status(found, info, port)
                print(f"  Next check in {args.interval}s...\n")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")
    else:
        found, info, port = check_device_connected()
        print_status(found, info, port)


if __name__ == "__main__":
    main()
