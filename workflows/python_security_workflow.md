# Python Security Integration Workflow

## 🔒 Automated Python Security Management System

This workflow integrates Python security validation into the existing ai-assistant-knowledge-hub Linear management system.

---

## Architecture Integration

### Phase 1: Pre-Execution Security Validation

**Integration Point**: Enhanced `smart-doit.sh` system
**Trigger**: Before any Python-related issue work begins

```bash
# Enhanced doit command with security validation
~/.linear-utils.sh get $ISSUE_ID
node ~/ai-assistant-knowledge-hub/security/security_context_injector.js $PROJECT_PATH

# Security validation exit codes:
# 0 = Safe to proceed or no Python detected
# 1 = High-risk patterns detected - manual review required
```

### Phase 2: Dynamic Context Injection

**Integration Point**: Claude context enhancement
**Trigger**: Real-time Python development detection

```bash
# Security context activation workflow
if [ $SECURITY_CONTEXT_ACTIVATED ]; then
    echo "🔒 Python Security Context Active"
    echo "📋 Security guidelines injected into Claude context"
    echo "⚠️ Code review required before implementation"
fi
```

### Phase 3: Linear Issue Security Tracking

**Integration Point**: Linear issue management and status updates
**Trigger**: Security context activation or violation detection

---

## Workflow Implementation

### 1. Enhanced doit Command Integration

**File**: `bin/security-aware-doit.sh`

```bash
#!/bin/bash
# Enhanced doit with Python security validation

set -euo pipefail

ISSUE_ID="$1"
INTERACTIVE_MODE="${2:-false}"

# Phase 1: Standard doit execution
echo "🔄 Executing standard doit workflow..."
doit "$ISSUE_ID" --interactive="$INTERACTIVE_MODE"

# Phase 2: Security context analysis
echo "🔒 Analyzing Python security context..."
PROJECT_PATH=$(jq -r '.project_path' temp/agent_issue_${ISSUE_ID}.json 2>/dev/null || echo ".")

SECURITY_RESULT=$(node ai-assistant-knowledge-hub/security/security_context_injector.js "$PROJECT_PATH")
SECURITY_EXIT_CODE=$?

# Phase 3: Handle security results
if [ $SECURITY_EXIT_CODE -eq 1 ]; then
    echo "🚨 HIGH-RISK PYTHON PATTERNS DETECTED"
    echo "📋 Manual security review required before proceeding"
    echo "🔒 Security context has been activated"

    # Add security warning to Linear issue
    ~/.linear-utils.sh comment "$ISSUE_ID" "🔒 **Security Review Required**: High-risk Python patterns detected. Security context activated. Manual review required before implementation."

    # Update issue status to indicate security review needed
    curl -X POST "https://api.linear.app/graphql" \
      -H "Authorization: $(cat ~/.linear-api-key)" \
      -d "{\"query\":\"mutation{issueUpdate(id:\\\"$(grep -o '\"id\":\"[^\"]*\"' temp/agent_issue_${ISSUE_ID}.json | cut -d'\"' -f4)\\\",input:{stateId:\\\"security-review-required\\\"})}\"}"
elif [ $SECURITY_EXIT_CODE -eq 0 ] && echo "$SECURITY_RESULT" | grep -q "SECURITY CONTEXT ACTIVATED"; then
    echo "⚠️ Python security context activated"
    echo "📋 Security guidelines are now active"

    # Add security notification to Linear issue
    ~/.linear-utils.sh comment "$ISSUE_ID" "⚠️ **Security Context Active**: Python security guidelines activated for this issue. Please follow secure coding practices."
fi

echo "✅ Security-aware doit completed"
```

### 2. Automatic Security Context Detection

**Integration**: Real-time project analysis

```javascript
// Auto-detection triggers (in security_context_injector.js)
const securityTriggers = {
    projectAnalysis: {
        pythonFiles: ['*.py', '*.pyx', '*.pyw'],
        configFiles: ['requirements.txt', 'setup.py', 'pyproject.toml'],
        frameworkIndicators: ['flask', 'django', 'fastapi', 'requests']
    },
    intentAnalysis: {
        keywords: ['web app', 'API', 'database', 'authentication', 'file upload'],
        riskPatterns: ['user input', 'file processing', 'crypto', 'subprocess']
    },
    realTimeDetection: {
        fileOperations: ['open()', 'subprocess.call()', 'eval()'],
        importStatements: ['import os', 'import subprocess', 'import pickle'],
        stringPatterns: ['SQL', 'password', 'secret', 'token']
    }
};
```

### 3. Linear Issue Security Workflow

**Security Status Management**:

```bash
# Security workflow states
SECURITY_STATES = {
    "no-security-needed": "No Python development detected",
    "security-context-active": "Security guidelines activated",
    "security-review-required": "High-risk patterns - manual review needed",
    "security-approved": "Security review completed - safe to proceed",
    "security-violation": "Security violation detected - immediate attention required"
}

# Automatic status updates based on security analysis
update_security_status() {
    local issue_id="$1"
    local security_level="$2"

    case "$security_level" in
        "critical"|"high")
            set_issue_status "$issue_id" "security-review-required"
            ;;
        "medium"|"low")
            set_issue_status "$issue_id" "security-context-active"
            ;;
        "none")
            # No security status change needed
            ;;
    esac
}
```

### 4. Security Compliance Tracking

**Linear Comments Integration**:

```bash
# Automatic security compliance logging
log_security_compliance() {
    local issue_id="$1"
    local analysis_result="$2"

    # Extract key security metrics
    local risk_level=$(echo "$analysis_result" | jq -r '.analysis.riskLevel')
    local patterns_count=$(echo "$analysis_result" | jq -r '.analysis.detectedPatterns | length')
    local context_type=$(echo "$analysis_result" | jq -r '.analysis.recommendedContext')

    # Generate compliance report
    local compliance_report="## 🔒 Security Compliance Report

**Risk Level**: $risk_level
**Patterns Detected**: $patterns_count
**Security Context**: $context_type
**Timestamp**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")

### Security Checklist
- [ ] Input validation implemented
- [ ] SQL injection prevention verified
- [ ] File path traversal protection confirmed
- [ ] Error handling security reviewed
- [ ] Cryptographic functions validated

**Next Action**: $(get_next_security_action "$risk_level")"

    # Add to Linear issue
    ~/.linear-utils.sh comment "$issue_id" "$compliance_report"
}

get_next_security_action() {
    case "$1" in
        "critical") echo "🚨 Immediate security review required before any code generation" ;;
        "high") echo "⚠️ Security review recommended before implementation" ;;
        "medium") echo "📋 Follow security guidelines during development" ;;
        "low") echo "✅ Basic security awareness sufficient" ;;
        *) echo "ℹ️ No specific security action required" ;;
    esac
}
```

---

## Integration Commands

### Setup Security System

```bash
# Make security context injector executable
chmod +x ai-assistant-knowledge-hub/security/security_context_injector.js

# Test security system
node ai-assistant-knowledge-hub/security/security_context_injector.js .

# Integrate with existing doit system
cp bin/smart-doit.sh bin/smart-doit.sh.backup
# Enhance smart-doit.sh with security integration
```

### Manual Security Analysis

```bash
# Analyze specific project for security context
security-analyze() {
    local project_path="${1:-.}"
    echo "🔒 Analyzing $project_path for Python security context..."
    node ai-assistant-knowledge-hub/security/security_context_injector.js "$project_path"
}

# Force security context activation
security-activate() {
    local context_type="${1:-HIGH_RISK_SECURITY_CONTEXT}"
    export PYTHON_SECURITY_CONTEXT="$context_type"
    echo "🔒 Security context '$context_type' activated"
}
```

### Security Monitoring

```bash
# Monitor security violations across all issues
security-monitor() {
    echo "🔍 Security monitoring across all active issues..."
    for issue_file in temp/agent_issue_BOC-*.json; do
        if [ -f "$issue_file" ]; then
            issue_id=$(basename "$issue_file" .json | sed 's/agent_issue_//')
            echo "Checking $issue_id..."
            # Security analysis logic here
        fi
    done
}
```

---

## Emergency Security Response

### Critical Security Violation Protocol

```bash
# Emergency response for critical security violations
security-emergency() {
    local issue_id="$1"
    local violation_type="$2"

    echo "🚨 SECURITY EMERGENCY: $violation_type detected in $issue_id"

    # Immediately halt any automated processes
    touch "temp/security_halt_${issue_id}"

    # Update Linear issue with emergency status
    ~/.linear-utils.sh comment "$issue_id" "🚨 **SECURITY EMERGENCY**: $violation_type detected. All automated processes halted. Manual intervention required immediately."

    # Set issue to emergency review status
    curl -X POST "https://api.linear.app/graphql" \
      -H "Authorization: $(cat ~/.linear-api-key)" \
      -d "{\"query\":\"mutation{issueUpdate(id:\\\"$(get_issue_linear_id $issue_id)\\\",input:{stateId:\\\"security-emergency\\\"})}\"}"

    echo "🔒 Emergency protocols activated. Issue $issue_id requires immediate manual review."
}
```

---

## Success Metrics

### Security Effectiveness Tracking

- **Vulnerability Prevention**: Number of potential security issues caught before implementation
- **Context Activation Rate**: Percentage of Python projects with activated security context
- **Compliance Rate**: Percentage of issues following security guidelines
- **Response Time**: Time from security violation detection to resolution

### Integration Health

- **doit Integration**: Seamless security validation in existing workflow
- **Linear Integration**: Automatic security status and comment management
- **Claude Context**: Effective security guideline injection and adherence
- **Developer Experience**: Minimal friction while maintaining security standards

---

**🎯 Goal**: Zero Python security vulnerabilities in AI-generated code through proactive, automated, and integrated security management.
