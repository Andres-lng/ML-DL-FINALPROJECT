# ===================================================================
# setup-ec2.sh - Initial EC2 Setup Script
# ===================================================================
#!/bin/bash

echo "🔧 Setting up EC2 for TeleLink deployment"
echo "=========================================="

# Update system
echo "📦 Updating system packages..."
sudo yum update -y

# Install Docker
echo "🐳 Installing Docker..."
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose (optional, not needed for single container)
echo "🔧 Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Enable Docker on boot
sudo systemctl enable docker

# Install git
echo "📚 Installing Git..."
sudo yum install git -y

echo ""
echo "✅ EC2 setup complete!"
echo ""
echo "Next steps:"
echo "1. Log out and log back in (for Docker permissions)"
echo "2. Clone your repository"
echo "3. Run: bash deploy.sh"