#!/bin/bash

# Frontend Setup Script for Next.js with TypeScript

set -e

echo "🎨 Setting up Next.js Frontend..."
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check Node version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18+ is required. Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js $(node -v) detected"
echo ""

# Create Next.js app if package.json doesn't exist
if [ ! -f "package.json" ]; then
    echo "📦 Creating Next.js application..."
    npx create-next-app@latest . \
        --typescript \
        --tailwind \
        --eslint \
        --app \
        --src-dir \
        --import-alias "@/*" \
        --no-git
    
    echo "✅ Next.js application created"
else
    echo "📦 Installing dependencies..."
    npm install
fi

echo ""
echo "📦 Installing additional dependencies..."

# Install required dependencies
npm install \
    @tanstack/react-query \
    zustand \
    react-hook-form \
    zod \
    date-fns \
    lucide-react

# Install shadcn/ui
echo ""
echo "🎨 Setting up shadcn/ui..."
npx shadcn-ui@latest init -y

# Install commonly used shadcn components
echo ""
echo "📦 Installing shadcn/ui components..."
npx shadcn-ui@latest add button input card dialog dropdown-menu toast form label select textarea

echo ""
echo "✅ Frontend dependencies installed!"
echo ""

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "📝 Creating .env.local..."
    cat > .env.local << 'EOF'
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws

# Environment
NODE_ENV=development
EOF
    echo "✅ .env.local created"
fi

echo ""
echo "======================================"
echo "✅ Frontend setup complete!"
echo "======================================"
echo ""
echo "📍 Next steps:"
echo "   1. Start development: npm run dev"
echo "   2. Visit: http://localhost:3000"
echo "   3. Start building components in src/app/"
echo ""
echo "🐳 Docker:"
echo "   • Uncomment frontend service in docker-compose.yml"
echo "   • Run: docker-compose up -d frontend"
echo ""
echo "📚 Documentation:"
echo "   • Next.js: https://nextjs.org/docs"
echo "   • shadcn/ui: https://ui.shadcn.com"
echo "   • TanStack Query: https://tanstack.com/query"
echo ""