#!/bin/bash
#
# UauthAPIX - Quick Setup Script
# This script sets up UauthAPIX on your system
#

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              UauthAPIX Setup Script                          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "🔍 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Found Python $PYTHON_VERSION"

# Check pip
echo ""
echo "🔍 Checking pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi
echo "✅ pip3 is available"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt --quiet

echo "✅ Dependencies installed"

# Make script executable
echo ""
echo "🔧 Making script executable..."
chmod +x uauthapix.py
echo "✅ Script is now executable"

# Test installation
echo ""
echo "🧪 Testing installation..."
if python3 uauthapix.py --help > /dev/null 2>&1; then
    echo "✅ Installation successful!"
else
    echo "❌ Installation test failed"
    exit 1
fi

# Print success message
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              Setup Complete! 🎉                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Quick Start:"
echo ""
echo "  # View help"
echo "  python3 uauthapix.py --help"
echo ""
echo "  # Basic test"
echo "  python3 uauthapix.py api-spec.json --base-url https://api.example.com"
echo ""
echo "  # Full security scan"
echo "  python3 uauthapix.py api-spec.json --base-url https://api.example.com --test-all -vv"
echo ""
echo "📖 Documentation: README.md"
echo "⚡ Quick Reference: QUICKSTART.md"
echo ""
echo "Happy testing! 🔒🛡️"
echo ""
