# Container Setup

## Docker Lab Setup

```bash
# Download and extract the lab archive
unzip Labsetup.zip
cd Labsetup

# Build container images
docker-compose build

# Start all containers in detached mode
docker-compose up -d

# Shut everything down when done
docker-compose down
```

---

## Container Access

```bash
# List all running containers
docker ps

# Open a shell into a specific container (short ID works)
docker exec -it <container_id> /bin/bash
```

---

## Attacker Container

- A shared folder is mounted between host and container:
  - Host path: `./volumes`
  - Container path: `/volumes`
- Write scripts on the host inside `./volumes`, then run them from `/volumes` inside the attacker container.

---

## Victim Container Configuration

The victim must be configured to **accept ICMP redirects** (disabled by default on modern Ubuntu). This is set in `docker-compose.yml`:

```yaml
sysctls:
  - net.ipv4.conf.all.accept_redirects=1
```

---

## Malicious Router Configuration

The malicious router must **not send its own redirects** — we spoof them from the attacker instead:

```yaml
sysctls:
  - net.ipv4.conf.all.send_redirects=0
  - net.ipv4.conf.default.send_redirects=0
  - net.ipv4.conf.eth0.send_redirects=0
```

---

## Important Note on Container Environments

In container environments, the victim must be **actively sending traffic** (e.g., `ping 192.168.60.5`) before sending the ICMP redirect. The enclosed packet in the redirect must match the type and destination of the victim's current outgoing traffic for the redirect to be accepted by the kernel.
