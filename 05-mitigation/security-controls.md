# Security Controls & Mitigation

## Overview

ICMP redirect attacks exploit a legacy routing feature that most modern networks do not need. The mitigations below range from disabling the vulnerable feature entirely to deploying monitoring and encryption layers.

---

## 1. Disable ICMP Redirect Acceptance (Primary Defense)

The most direct fix: configure all hosts to **ignore ICMP redirect messages**.

```bash
# Disable for all interfaces (temporary)
sysctl -w net.ipv4.conf.all.accept_redirects=0
sysctl -w net.ipv4.conf.default.accept_redirects=0

# Make permanent (add to /etc/sysctl.conf or /etc/sysctl.d/)
net.ipv4.conf.all.accept_redirects=0
net.ipv4.conf.default.accept_redirects=0
```

Apply with:
```bash
sysctl -p
```

> This is the default on most modern Linux distributions when acting as a router. For end hosts, it should be explicitly disabled.

---

## 2. Disable ICMP Redirect Sending on Routers

Routers should not send redirect messages unless specifically required:

```bash
sysctl -w net.ipv4.conf.all.send_redirects=0
```

In Docker/container environments, set via `sysctls` in `docker-compose.yml`:

```yaml
sysctls:
  - net.ipv4.conf.all.send_redirects=0
```

---

## 3. Static Routes / Route Pinning

Define critical routes statically to prevent the routing cache from being manipulated:

```bash
# Pin the route to the target subnet via the legitimate router
ip route add 192.168.60.0/24 via 10.9.0.11
```

Static routes are not overridden by ICMP redirects.

---

## 4. Network Monitoring & Anomaly Detection

| Technique | Description |
|-----------|-------------|
| **IDS/IPS rules** | Alert on unexpected ICMP type-5 messages from non-router sources |
| **Routing cache audits** | Periodically check `ip route show cache` for unexpected entries |
| **ARP/ICMP anomaly detection** | Tools like `arpwatch` or Suricata rules for spoofed redirect traffic |

Example Snort/Suricata rule concept:
```
alert icmp any any -> $HOME_NET any (msg:"ICMP Redirect"; itype:5; sid:1000001;)
```

---

## 5. Use Encrypted Protocols (Defense in Depth)

Even if traffic is redirected, encryption prevents payload modification:

| Protocol | Protection |
|----------|------------|
| **TLS/HTTPS** | Encrypts payload; modifications break the connection (MAC/integrity checks) |
| **SSH tunneling** | Encrypts all traffic over the tunnel |
| **IPsec** | Network-layer encryption with integrity verification |
| **VPNs** | Encapsulates traffic, preventing interception on the local network |

---

## 6. Network Segmentation

Limit attacker reach by segmenting the network:

- Place untrusted hosts in isolated VLANs
- Use firewall rules to prevent arbitrary hosts from sending ICMP messages on router subnets
- Implement 802.1X port authentication to control which devices join the network

---

## Summary

| Control | Effectiveness | Complexity |
|---------|--------------|------------|
| Disable `accept_redirects` | High — stops attack entirely | Low |
| Disable `send_redirects` | High — prevents legitimate redirects from being abused | Low |
| Static routes | High for known destinations | Medium |
| IDS/IPS monitoring | Medium — detects but doesn't prevent | Medium |
| TLS/IPsec encryption | High — neutralises payload modification | High |
| Network segmentation | Medium — reduces attack surface | High |

> The simplest and most effective mitigation is disabling ICMP redirect acceptance (`accept_redirects=0`) on all hosts that do not require dynamic route updates.
