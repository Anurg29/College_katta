#!/bin/bash

echo "🎯 TechKatta - Easy Setup Script"
echo "=================================="
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH (for Apple Silicon Macs)
    if [[ $(uname -m) == 'arm64' ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    
    echo "✅ Homebrew installed!"
else
    echo "✅ Homebrew already installed"
fi

echo ""
echo "📦 Installing databases..."
echo ""

# Install MySQL
if ! command -v mysql &> /dev/null; then
    echo "📥 Installing MySQL..."
    brew install mysql
    brew services start mysql
    echo "✅ MySQL installed and started"
else
    echo "✅ MySQL already installed"
fi

# Install MongoDB
if ! command -v mongod &> /dev/null; then
    echo "📥 Installing MongoDB..."
    brew tap mongodb/brew
    brew install mongodb-community@6.0
    brew services start mongodb-community@6.0
    echo "✅ MongoDB installed and started"
else
    echo "✅ MongoDB already installed"
fi

# Install Redis
if ! command -v redis-server &> /dev/null; then
    echo "📥 Installing Redis..."
    brew install redis
    brew services start redis
    echo "✅ Redis installed and started"
else
    echo "✅ Redis already installed"
fi

echo ""
echo "🎉 All dependencies installed!"
echo ""
echo "⏳ Waiting 5 seconds for databases to start..."
sleep 5

echo ""
echo "🔧 Setting up MySQL database..."
echo ""

# Create MySQL database and user
mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS techkatta CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'techkatta_user'@'localhost' IDENTIFIED BY 'techkatta_pass';
GRANT ALL PRIVILEGES ON techkatta.* TO 'techkatta_user'@'localhost';
FLUSH PRIVILEGES;
EOF

echo "✅ MySQL database 'techkatta' created!"
echo ""
echo "=================================="
echo "✨ Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Run: cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
echo "2. Run: uvicorn app.main:app --reload"
echo "3. In a new terminal: cd frontend && npm install && npm run dev"
echo ""
echo "Then visit: http://localhost:5173"
echo ""
