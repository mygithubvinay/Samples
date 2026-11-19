# Web Portal

Pages: `/` (Home), `/about` (About), `/contact` (Contact)

## Run locally (no Docker)
```bash
npm install
npm run dev        # http://localhost:5173
```

## Run with Docker
```bash
docker build -t web-portal .
docker run -d --name web-portal -p 80:80 --restart unless-stopped web-portal
```
Open http://localhost (or http://<server-public-ip>).

## Make it reachable from anywhere
1. Run the container on a server with a public IP (AWS EC2, Azure VM, DigitalOcean, etc.).
2. Open inbound port 80 (and 443 for HTTPS) in the cloud firewall / security group.
3. Point a domain's A record to the server IP.
4. Add HTTPS (e.g. Caddy or nginx + Let's Encrypt, or put it behind Cloudflare).

Alternatively, push the image to a registry and deploy it on a managed service
(AWS App Runner / ECS, Azure Container Apps, Google Cloud Run) — these give you a
public HTTPS URL automatically.
