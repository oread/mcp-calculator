# MCP-Tools Docker Deployment Guide

## Quick Start

### 1. Prerequisites

- Docker installed (version 20.10+)
- Docker Compose installed (version 2.0+)
- MCP endpoint token

### 2. Configuration

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` and set your values:

```bash
# Required
MCP_ENDPOINT=wss://api.xiaozhi.me/mcp/?token=YOUR_TOKEN_HERE

# Optional (for Dataverse tool)
DATAVERSE_URL=https://yourorg.crm.dynamics.com
CLIENT_ID=your-azure-ad-client-id
CLIENT_SECRET=your-azure-ad-client-secret
TENANT_ID=your-azure-ad-tenant-id
```

### 3. Build the Image

```bash
docker build -t mcp-tools .
```

### 4. Run Individual Tools

Run a specific tool:

```bash
# Calculator
docker run -e MCP_ENDPOINT="your-endpoint-url" mcp-tools calculator.py

# Dataverse
docker run -e MCP_ENDPOINT="your-endpoint-url" \
  -e DATAVERSE_URL="your-dataverse-url" \
  -e CLIENT_ID="your-client-id" \
  -e CLIENT_SECRET="your-client-secret" \
  -e TENANT_ID="your-tenant-id" \
  mcp-tools dataverse.py

# VNExpress
docker run -e MCP_ENDPOINT="your-endpoint-url" mcp-tools vnexpress.py

# Zing MP3
docker run -e MCP_ENDPOINT="your-endpoint-url" mcp-tools zingmp3.py
```

### 5. Run All Tools with Docker Compose

Start all tools:

```bash
docker-compose up -d
```

View logs:

```bash
docker-compose logs -f
```

Stop all tools:

```bash
docker-compose down
```

## Container Management

### View Running Containers

```bash
docker ps
```

### View Container Logs

```bash
# Individual container
docker logs mcp-calculator
docker logs mcp-dataverse
docker logs mcp-vnexpress
docker logs mcp-zingmp3

# Follow logs
docker logs -f mcp-calculator
```

### Stop/Start Containers

```bash
# Stop
docker stop mcp-calculator

# Start
docker start mcp-calculator

# Restart
docker restart mcp-calculator
```

### Remove Containers

```bash
# Remove specific container
docker rm mcp-calculator

# Remove all stopped containers
docker container prune
```

## Advanced Configuration

### Custom Network

Create a custom network:

```bash
docker network create mcp-custom-network
```

Run container on custom network:

```bash
docker run --network mcp-custom-network \
  -e MCP_ENDPOINT="your-endpoint-url" \
  mcp-tools calculator.py
```

### Volume Mounting

Mount configuration files:

```bash
docker run -v $(pwd)/mcp_config.json:/app/mcp_config.json \
  -e MCP_ENDPOINT="your-endpoint-url" \
  mcp-tools
```

### Resource Limits

Limit CPU and memory:

```bash
docker run --cpus="0.5" --memory="256m" \
  -e MCP_ENDPOINT="your-endpoint-url" \
  mcp-tools calculator.py
```

## Docker Compose Advanced

### Run Specific Services

```bash
# Only calculator and dataverse
docker-compose up -d calculator dataverse
```

### Scale Services

```bash
# Run multiple instances
docker-compose up -d --scale calculator=3
```

### Custom Compose File

Create `docker-compose.override.yml`:

```yaml
version: '3.8'

services:
  calculator:
    environment:
      - CUSTOM_VAR=value
    ports:
      - "8080:8080"
```

### Health Checks

Add to docker-compose.yml:

```yaml
services:
  calculator:
    healthcheck:
      test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## Production Deployment

### Build for Production

```bash
docker build -t mcp-tools:v1.0.0 .
docker tag mcp-tools:v1.0.0 your-registry/mcp-tools:v1.0.0
```

### Push to Registry

```bash
# Docker Hub
docker push your-registry/mcp-tools:v1.0.0

# Azure Container Registry
az acr login --name yourregistry
docker push yourregistry.azurecr.io/mcp-tools:v1.0.0
```

### Deploy to Cloud

#### Azure Container Instances

```bash
az container create \
  --resource-group myResourceGroup \
  --name mcp-calculator \
  --image yourregistry.azurecr.io/mcp-tools:v1.0.0 \
  --environment-variables MCP_ENDPOINT="your-endpoint-url" \
  --command-line "python mcp_pipe.py calculator.py"
```

#### AWS ECS

Create task definition and service using your registry.

#### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-calculator
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mcp-calculator
  template:
    metadata:
      labels:
        app: mcp-calculator
    spec:
      containers:
      - name: mcp-calculator
        image: mcp-tools:v1.0.0
        command: ["python", "mcp_pipe.py", "calculator.py"]
        env:
        - name: MCP_ENDPOINT
          valueFrom:
            secretKeyRef:
              name: mcp-secrets
              key: endpoint
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs mcp-calculator

# Check container status
docker inspect mcp-calculator
```

### Connection Issues

- Verify MCP_ENDPOINT is correct
- Check network connectivity
- Ensure firewall allows WebSocket connections

### Memory Issues

```bash
# Check resource usage
docker stats mcp-calculator

# Increase memory limit
docker run --memory="512m" ...
```

### Permission Issues

```bash
# Run as specific user
docker run --user $(id -u):$(id -g) ...
```

## Monitoring

### Basic Monitoring

```bash
# Resource usage
docker stats

# Container events
docker events
```

### Integration with Monitoring Tools

- Prometheus: Use Docker metrics exporter
- Grafana: Create dashboards for container metrics
- ELK Stack: Collect and analyze logs

## Backup and Restore

### Backup Configuration

```bash
# Backup environment file
cp .env .env.backup

# Backup volumes
docker run --rm -v mcp-data:/data -v $(pwd):/backup \
  alpine tar czf /backup/mcp-data-backup.tar.gz /data
```

### Restore Configuration

```bash
# Restore environment
cp .env.backup .env

# Restore volumes
docker run --rm -v mcp-data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/mcp-data-backup.tar.gz -C /
```

## Security Best Practices

1. **Use Environment Variables**: Never hardcode secrets in images
2. **Scan Images**: Use `docker scan mcp-tools` to check for vulnerabilities
3. **Non-Root User**: Run containers as non-root user
4. **Network Segmentation**: Use custom networks to isolate containers
5. **Update Regularly**: Keep base images and dependencies updated
6. **Secrets Management**: Use Docker secrets or external vaults

## Performance Optimization

1. **Multi-Stage Builds**: Reduce image size
2. **Layer Caching**: Order Dockerfile commands efficiently
3. **Resource Limits**: Set appropriate CPU and memory limits
4. **Health Checks**: Implement proper health check endpoints
5. **Logging**: Use JSON logging driver for better performance

## Support

For issues and questions:
- Check container logs: `docker logs <container-name>`
- Review Docker documentation: https://docs.docker.com
- Open an issue on the project repository
