from scapy.all import sniff, TCP, UDP, ICMP

packet_count = 0

def packet_callback(packet):
    global packet_count
    packet_count += 1

    if TCP in packet:
        if packet[TCP].flags & 0x02:  # SYN flag
            print(f"{packet_count}. TCP SYN Packet: {packet.summary()}")
        elif packet[TCP].flags & 0x10:  # ACK flag
            print(f"{packet_count}. TCP ACK Packet: {packet.summary()}")
        else:
            print(f"{packet_count}. TCP Packet: {packet.summary()}")

    if ICMP in packet:
        print(f"{packet_count}. ICMP Packet: {packet.summary()}")

    elif UDP in packet:
        print(f"{packet_count}. UDP Packet: {packet.summary()}")

def start_sniffing():
    print("Starting packet capture...")
    sniff(prn=packet_callback, filter="ip", store=0)

if __name__ == "__main__":
    start_sniffing()
