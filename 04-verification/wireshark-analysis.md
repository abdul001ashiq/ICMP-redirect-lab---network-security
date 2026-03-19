# Verification & Analysis

## Results Summary

The ICMP redirect attack was **successfully executed**:

- The victim's traffic was redirected through the malicious router via spoofed ICMP redirects.
- TCP payloads were intercepted and modified in transit.
- The target host received the altered data while the victim was unaware of any modification.

---

## Task 1 Verification Screenshots

Screenshots for Task 1.A, 1.B, and 1.C are in **[task1/](task1/)**:
- **Task 1.A:** [task1a-ip-route-show-cache.png](task1/task1a-ip-route-show-cache.png) — victim's `ip route show cache` confirming the redirect.
- **Task 1.B:** [task1b-traceroute.png](task1/task1b-traceroute.png) — traceroute showing traffic via `10.9.0.11` (redirect to offline host ignored).
- **Task 1.C (Scenario 1):**
  - [Task 1c Scenario 1 Cache Results.png](task1/Task 1c Scenario 1 Cache Results.png) — routing cache confirming redirect via malicious router with `send_redirects=1`.
  - [Task 1c Scenario 1 Pinging Host.png](task1/Task 1c Scenario 1 Pinging Host.png) — ping output where the victim explicitly sees the ICMP redirect message.
- **Task 1.C (Scenario 2):**
  - [Task 1c Scenario 2 Pinging Host.png](task1/Task 1c Scenario 2 Pinging Host.png) — ping output with `send_redirects=0`, no redirect message shown.
  - [Task 1c Scenario 2 Traceroute.png](task1/Task 1c Scenario 2 Traceroute.png) — traceroute still showing traffic via `10.9.0.111` even though no redirect is visible to the victim.

---

## Phase 1 Verification — Routing Redirection

### Traceroute Confirmation (Fig 1.2)

![Fig 1.2 — Traceroute showing redirection through malicious router](../assets/screenshots/lab-report-phase1.png)

**Fig 1.2** — When the attack was launched, packets were redirected through the malicious router. This is evident in the traceroute to host `192.168.60.5` from the victim (`10.9.0.5`): the first hop is now `10.9.0.111` (malicious router) instead of `10.9.0.11` (legitimate router).

---

### Routing Cache Confirmation (Fig 1.3)

```
root@8cbd077ea1f2:/# ip route show cache
192.168.60.5 via 10.9.0.111 dev eth0
    cache <redirected> expires 239sec
root@8cbd077ea1f2:/#
```

**Fig 1.3** — Running `ip route show cache` on the victim confirms that traffic to `192.168.60.5` is now flowing via the malicious router (`10.9.0.111`). The `<redirected>` tag confirms the route was set by an ICMP redirect message.

---

## Observations & Findings

| Finding | Explanation |
|---------|-------------|
| **Redirect to non-existing host fails** | Redirecting to an offline IP (`10.9.0.76`) does not work — the victim's kernel validates gateway reachability before accepting the redirect. See [Task 1.B](../03-attack-scenario/icmp-redirect-attack.md#task-1b--redirect-to-a-non-existing-machine). |
| **`send_redirects` configuration matters** | When the malicious router has `send_redirects=1`, the victim's traceroute reveals the redirect path. Keeping it at `0` prevents this. |
| **One-direction capture is sufficient** | Capturing only victim → host traffic and modifying it in that direction fully achieves the MITM goal. |
| **IP filter > MAC filter** | Using the victim's IP in the sniff filter is more reliable than MAC address filtering in Docker container environments. |
| **Payload length must be preserved** | TCP sequence numbers depend on payload size — replacing with a different-length string breaks the stream. Same-length substitution keeps the connection intact. |

---

## Task 2 — MITM Verification (IP Forwarding Behaviour)

### Code Snapshots

Script screenshots are stored under `assets/screenshots/scripts/`:

- [Task 1a code](../assets/screenshots/scripts/Task 1a code.png) — ICMP redirect script for Task 1.A (baseline redirect to malicious router).
- [Task 1b code](../assets/screenshots/scripts/Task 1b code.png) — variant for Task 1.B where `icmp.gw` points to a non-existing/offline host.
- [Task 1c code](../assets/screenshots/scripts/Task 1c code.png) — script used for Task 1.C when toggling `send_redirects`.
- [Task 2 code (a)](../assets/screenshots/scripts/Task 2 code (a).png) and [Task 2 code (b)](../assets/screenshots/scripts/Task 2 code (b).png) — MITM sniff-and-spoof variants used for Task 2.

### Runtime Evidence — IP Forwarding = 0

When `net.ipv4.ip_forward=0` on the malicious router, packets are forced through the user-space sniff-and-spoof script:

- [Launching attack from attacker container](task 2/IP FORWARDING IS 0/lauching attack from attacker container.png) — shows the attack script being started.
- [Task 2 host side](task 2/IP FORWARDING IS 0/Task 2 host side.png) — netcat server output on the host, receiving the **modified** payload.
- [Task 2 victim side](task 2/IP FORWARDING IS 0/Task 2 victim side.png) — victim’s netcat client output, unaware that its message is being altered in transit.

### Runtime Evidence — IP Forwarding = 1

When `net.ipv4.ip_forward=1`, the kernel forwards packets directly and the user-space MITM logic is bypassed:

- [Task 2 netcat client](task 2/IP FORWARDING IS 1/task 2 netcat client.png) — victim’s client talking to the server with normal payloads.
- [Task 2 netcat server (1)](task 2/IP FORWARDING IS 1/Task 2 netcat server(1).png) and [Task 2 netcat server (2)](task 2/IP FORWARDING IS 1/task 2 netcat server(2).png) — server side output showing **unmodified** messages.
- [Task 2 malicious router container](task 2/Task 2 malicious router container .png) — behaviour on the malicious router when toggling IP forwarding on and off.

These screenshots collectively confirm that the MITM attack only works reliably when kernel IP forwarding is disabled and all transit traffic passes through the sniff-and-spoof script.

---

## Adding Further Screenshots

Place additional Wireshark or terminal screenshots in this folder and reference them here:

```
04-verification/
├── packet-capture.png         ← tcpdump/Wireshark showing traffic on malicious router
├── routing-table-change.png   ← victim routing cache before/after
└── wireshark-analysis.md
```
