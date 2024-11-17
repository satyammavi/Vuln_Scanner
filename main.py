import os
from banner import generate_banner
import subprocess
import socket
import ipaddress
import json
import xml.etree.ElementTree as ET
from utility import find_local_ip, find_subnet_range, ip_range
from scanner import scan_subnet, scan_specific_ip
from monitor import start_sniffing  # Imported sniffer function

def save_result_to_file(scan_result, file_type="txt"):
    """Saves scan results to a file in the script's directory."""
    file_type = file_type.strip('.').lower()  # Normalize file type input
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the script's directory
    file_name = os.path.join(script_dir, f"scan_result.{file_type}")  # Save in the script's directory

    try:
        if file_type == "txt":
            with open(file_name, "w") as f:
                f.write(str(scan_result))  # Ensure result is a string

        elif file_type == "json":
            # Ensure scan_result is JSON-serializable
            with open(file_name, "w") as f:
                f.write(json.dumps(scan_result, indent=4))

        elif file_type == "xml":
            # Convert non-string results to a string for XML saving
            if not isinstance(scan_result, str):
                scan_result = str(scan_result)
            root = ET.Element("ScanResult")
            ET.SubElement(root, "Result").text = scan_result
            tree = ET.ElementTree(root)
            tree.write(file_name)
        
        else:
            print("Unsupported file type. Please choose .txt, .json, or .xml.")
            return
        
        print(f"Results successfully saved to {file_name}")

    except Exception as e:
        print(f"Error saving the file: {e}")

if __name__ == "__main__":
    generate_banner()

    while True:
        local_ip = find_local_ip()

        if local_ip:
            print(f"Your local IP Address is: {local_ip}")
            subnet = find_subnet_range(local_ip)
            print(f"The calculated CIDR notation is: {subnet}")
            ip_range(subnet)

            # Ask users for their choice of scan
            print("\nChoose a scan option:\n")
            print("1. Scan all active hosts for open ports")
            print("2. Scan all active hosts for the first 1000 ports and determine the running services")
            print("3. Scan all hosts on all open ports to determine if any running services have vulnerabilities")
            print("4. Scan all active hosts for the first 1000 ports to identify if any services have vulnerabilities")
            print("5. Monitor network traffic (Packet Sniffing)")
            print("6. Scan a specific IP address for open ports")
            choice = input("Enter your choice (1/2/3/4/5/6): ")

            if choice == "1":
                print("\nScanning all active hosts for open ports...")
                scan_result = scan_subnet(subnet)

            elif choice == "2":
                print("\nScanning all active hosts for the first 1000 ports to determine running services...")
                scan_result = scan_subnet(subnet, ports="1-1000")

            elif choice == "3":
                print("\nScanning all active hosts on all ports for vulnerabilities...")
                scan_result = scan_subnet(subnet, script="vuln")

            elif choice == "4":
                print("\nScanning all active hosts on the first 1000 ports for vulnerabilities...")
                scan_result = scan_subnet(subnet, ports="1-1000", script="vuln")

            elif choice == "5":
                print("\nMonitoring network traffic using packet sniffing...")
                start_sniffing()
                continue  # Skip the rest of the loop for sniffing

            elif choice == "6":
                specific_ip = input("\nEnter the specific IP address to scan: ")
                print(f"\nScanning specific IP: {specific_ip} for open ports...")
                scan_result = scan_specific_ip(specific_ip)

            else:
                print("Invalid choice.")
                scan_result = None

            if scan_result:
                print("\nScan Results:\n")
                print(scan_result)

                # Ask the user to save the result to a file
                save_choice = input("Do you want to save the results? (yes/no): ")
                if save_choice.lower() == "yes":
                    file_type = input("Enter file type to save (.txt, .json, .xml): ").lower()
                    save_result_to_file(scan_result, file_type)
            else:
                print("Scan failed or no vulnerabilities found.")

        else:
            print("Unable to retrieve local IP address.")

        print()
        run_again = input("Do you want to run the program again? (yes/no): ")
        if run_again.lower() != 'yes':
            break
