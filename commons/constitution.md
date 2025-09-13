# AI Assistant Constitutional Principles

## 📊 Two-Layer Knowledge Management System (Integrated Version)

This is the foundational architecture that governs all AI assistant operations:

```
Repository (this location) - AI collaboration rules, technical constraints, development policies only
Linear                     - Project management, tasks, progress, development logs, error resolution, all learning patterns
```

**Important**: `devlog.md` is abolished. All project management operations are integrated and managed in Linear.

## 🏗️ Development Environment Architecture Principles

### 🎯 **Basic Premises (Absolute Compliance)**

**Termux = Lightweight Development Workbench**
- **Role**: Code editing + quality checking only
- **Responsibility scope**: ESLint/Prettier execution up to
- **Limitation recognition**: APK builds and heavy dependencies are out of scope

**GitHub Actions = Production Build Environment**
- **Role**: Complete CI/CD (PWA→APK conversion)
- **Responsibility scope**: All dependencies, build, signing, release
- **Quality assurance**: Basic checks in Termux → Full execution in Actions

### 📋 **Environment Responsibility Separation**

```
Termux (lightweight):
├── Code editing (script.js, sw.js, style.css)
├── ESLint warnings check
├── Basic functionality test
└── Git operations

GitHub Actions (heavyweight):
├── npm ci --include=dev (full dependencies)
├── APK generation (Capacitor + Android)
├── Icon generation (@capacitor/assets + sharp)
├── Code signing & release
└── Deployment
```

### ⚠️ **Important: Handling Dependency Issues**

**"prettier not found" etc. in Termux environment is normal**
- Reason: Heavy dependencies are unnecessary in lightweight environment
- Response: Confirm success in GitHub Actions
- Prohibited: Forced installation of APK-related tools in Termux

## Emergency Patterns

- **Boot Failure**: Check file loading order, undefined dependencies
- **APK Signing**: Use RecipeBox proven signing system (CI only)
- **Build Errors**:
  - Termux: Focus on ESLint/code quality only
  - CI/CD: Refer to Linear issue history for build pipeline solutions
- **Git Push Issues**: Follow standard troubleshooting procedures

---

*This file contains only essential rules. All detailed information is stored in the Linear integrated management system.*