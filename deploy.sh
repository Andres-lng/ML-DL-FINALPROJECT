echo "🚀 TeleLink Single Container Deployment"
echo "========================================="

# Stop and remove old container
echo "📦 Stopping old container..."
docker stop telelink 2>/dev/null || true
docker rm telelink 2>/dev/null || true

# Remove old image
echo "🗑️  Removing old image..."
docker rmi telelink:latest 2>/dev/null || true

# Build new image
echo "🔨 Building Docker image..."
docker build -t telelink:latest .

# Run container
echo "🎯 Starting container..."
docker run -d \
  --name telelink \
  -p 80:8000 \
  --restart unless-stopped \
  --memory="800m" \
  --cpus="0.9" \
  telelink:latest

# Wait for health check
echo "⏳ Waiting for container to be healthy..."
sleep 10

# Check status
echo "✅ Deployment complete!"
docker ps | grep telelink

echo ""
echo "🌐 Access your application at:"
echo "   http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo ""
echo "📊 Container stats:"
docker stats --no-stream telelink
