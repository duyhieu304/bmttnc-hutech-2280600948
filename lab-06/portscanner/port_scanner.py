import socket
from scapy.all import *

# Danh sách các cổng thường gặp
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3389]

def scan_common_ports(target_domain, timeout=2):
    open_ports = []

    try:
        target_ip = socket.gethostbyname(target_domain)
    except socket.gaierror:
        print("Invalid domain name or network error.")
        return []

    for port in COMMON_PORTS:
        response = sr1(IP(dst=target_ip)/TCP(dport=port, flags="S"),
                       timeout=timeout, verbose=0)

        if response and response.haslayer(TCP) and response[TCP].flags == 0x12:
            open_ports.append(port)
            send(IP(dst=target_ip)/TCP(dport=port, flags="R"), verbose=0)  # Đóng kết nối

    return open_ports

def main():
    target_domain = input("Enter the target domain: ")

    open_ports = scan_common_ports(target_domain)

    if open_ports:
        print("Open common ports:")
        print(open_ports)
    else:
        print("No open common ports found.")

if __name__ == "__main__":
    main()
