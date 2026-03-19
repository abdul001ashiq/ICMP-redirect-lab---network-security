# ICMP Redirect Attack Lab

> Network Security |  Docker Environment

---

## Attribution

This project is based on the **ICMP Redirect Attack Lab** from [SEED Labs](https://seedsecuritylabs.org/) (Dr. Wenliang Du) and lab materials by Mohamed Anis Aguida, licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). I completed this lab as coursework and documented my approach and observations here.

---

## Summary

Demonstrated a **Man-in-the-Middle (MITM) attack** using spoofed ICMP redirect messages to reroute victim traffic through an attacker-controlled machine, then intercept and modify TCP payloads in transit — all within a containerized lab environment.

---

## Lab Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Overview](01-overview/lab-overview.md) | Goals, background, and concepts covered |
| 02 | [Environment](02-environment/container-setup.md) | Docker setup, network topology, container config |
| 03 | [Attack Scenario](03-attack-scenario/icmp-redirect-attack.md) | ICMP redirect & MITM implementation |
| 04 | [Verification](04-verification/wireshark-analysis.md) | Packet capture, routing table, results |
| 05 | [Mitigation](05-mitigation/security-controls.md) | Defenses and security controls |

---

## Quick Reference

| Role             | IP Address                        | Subnet           |
|------------------|-----------------------------------|------------------|
| Attacker         | 10.9.0.105                        | 10.9.0.0/24      |
| Victim           | 10.9.0.5                          | 10.9.0.0/24      |
| Malicious Router | 10.9.0.111                        | 10.9.0.0/24      |
| Router           | 10.9.0.11 / 192.168.60.11         | Both subnets     |
| Target Host      | 192.168.60.5                      | 192.168.60.0/24  |

**Tools:** Python 3, Scapy, netcat, Docker

---

## License

Licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). See [LICENSE](LICENSE).

---

## Disclaimer

This repository contains my own implementation, analysis, and documentation of the SEED ICMP Redirect Lab. The original lab instructions are not redistributed here.
