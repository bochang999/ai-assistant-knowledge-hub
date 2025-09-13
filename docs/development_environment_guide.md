# Development Environment Guide

## ⚡ Development Commands

```bash
# Current project examples:
briefcase dev                    # BeeWare development
http-server                      # Web development
git commit → AI-Gate automatic learning cycle

# Linear: Always use GraphQL API (CLI does not work)
curl -X POST "https://api.linear.app/graphql" -H "Authorization: $(cat ~/.linear-api-key)"
# Fixed team ID: $(cat ~/.linear-team-id) = "bochang's lab"
```

## 🔧 ESLint LSP - Termux Optimized Code Quality Management

**Adoption Reason**: TypeScript LSP times out in Termux environment - ESLint provides realistic solution

### Required Installation

```bash
# ESLint + daemon version (speed optimization)
npm install --save-dev eslint eslint_d vscode-langservers-extracted
```

### Configuration File Setup

**eslint.config.js**:
```javascript
export default [
    {
        languageOptions: {
            ecmaVersion: 2022,
            sourceType: "module",
            globals: {
                window: "readonly", document: "readonly", console: "readonly",
                localStorage: "readonly", history: "readonly", navigator: "readonly"
            }
        },
        rules: {
            "no-unused-vars": ["warn", { "args": "none" }],
            "no-undef": "error",
            "quotes": ["warn", "single", { "allowTemplateLiterals": true }]
        }
    }
];
```

### Practical Commands

```bash
# Real-time error checking
npx eslint script.js

# Auto-fix (quote unification, semicolons, etc.)
npx eslint script.js --fix

# Continuous monitoring mode
npx eslint script.js --watch
```

### Feature Constraint Acceptance

- ✅ **Gained**: High-speed error detection, auto-fix, practical development experience
- ❌ **Given up**: Advanced LSP features like find_definition, find_references
- 🎯 **Result**: Optimal solution under Termux constraints, significant development efficiency improvement

## Current Project Context Examples

- **Type**: Web→APK (HTML/CSS/JS → GitHub Actions → Signed APK)
- **Termux Role**: Code quality workbench (ESLint/basic editing)
- **CI/CD Role**: Complete build pipeline with all dependencies
- **Status**: GitHub Actions APK build functional, Termux lightweight editing ready