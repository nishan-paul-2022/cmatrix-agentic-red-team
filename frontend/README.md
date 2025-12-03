# CMatrix Frontend

Modern web interface for CMatrix AI-powered cybersecurity agent system.

## 🛠️ Tech Stack

- **Next.js 16** - React framework with App Router
- **React 19** - Latest React with Server Components
- **TypeScript** - Type-safe development
- **Tailwind CSS 4** - Utility-first styling
- **Radix UI** - Accessible component primitives
- **Shadcn/ui** - Beautiful component library

## 🚀 Quick Start

### Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev
# or
make dev
```

### Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

## 📋 Available Commands

```bash
# Development
npm run dev              # Start dev server
make dev                 # Start dev server (Makefile)

# Code Quality
npm run quality          # Run all quality checks
npm run lint             # Run ESLint
npm run lint:fix         # Run ESLint with auto-fix
npm run format           # Format with Prettier
npm run typecheck        # TypeScript type checking

# Or use Makefile
make quality             # Run all quality checks
make lint-fix            # ESLint with auto-fix
make format              # Format code
make typecheck           # Type check
```

## 📚 Documentation

For comprehensive code quality, linting, and development workflows, see:
- **[Code Quality Guide](../docs/CODE_QUALITY_GUIDE.md)** - Complete guide to linting, formatting, and development workflows
- **[Makefile Commands](Makefile)** - Run `make help` for available commands

## 🔧 Configuration

- **ESLint**: `.eslintrc.json` - Next.js + TypeScript + Prettier compatible
- **Prettier**: `.prettierrc.json` - Code formatting with Tailwind class sorting
- **TypeScript**: `tsconfig.json` - Strict mode enabled
- **Next.js**: `next.config.mjs` - Framework configuration
