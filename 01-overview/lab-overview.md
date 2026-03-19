# Lab Overview

## Objective

Demonstrate a **Man-in-the-Middle (MITM) attack** in which an attacker intercepts traffic between a victim and a target host, modifies the data in transit, and forwards it — all without the victim's knowledge.

The mechanism used to achieve this is **ICMP redirect message spoofing**, which tricks the victim into routing its traffic through the attacker's controlled machine.

---

## Background

### The MITM Goal

In a MITM attack, the attacker positions themselves between two communicating parties. All traffic passes through the attacker, who can read, modify, or drop packets. The core challenge is convincing the victim to route their traffic through the attacker in the first place.

### ICMP Redirect as the Vector

Routers use ICMP redirect messages (type 5) to inform hosts that a better route exists for a given destination. An attacker can **spoof** these messages: by pretending to be the legitimate router, the attacker tells the victim to send future packets to a different gateway — the attacker's machine.

Once traffic flows through the malicious router, the attacker can intercept and modify it before forwarding it to the intended destination.

---

## Concepts Covered

- IP and ICMP protocol mechanics
- Routing tables and routing cache
- Packet sniffing and spoofing (Scapy)
- TCP payload modification
- Container-based network lab environments (Docker)

---

## Two-Phase Approach

| Phase | Goal | Technique |
|-------|------|-----------|
| 1 | Redirect victim's traffic through malicious router | Spoofed ICMP redirect messages |
| 2 | Intercept and modify traffic in transit | Sniff-and-spoof with Scapy |

---

## Lab Context

> This lab was completed in a university-provided VM/Docker environment. Access has since been removed. The scripts and documentation reflect the implementation approach used during the lab.

See the [environment setup](../02-environment/container-setup.md) for full topology and configuration details.
