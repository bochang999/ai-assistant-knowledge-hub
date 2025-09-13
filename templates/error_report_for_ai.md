# AI Error Report Template

```markdown
# What I want to consult: Solving build errors that occurred in {Project Name}

## 1. Purpose / What I want to do
(Example: In the PWA build process, I am trying to automatically generate apk files for Android applications.)

---

## 2. Problem Overview
(Example: When executing build on GitHub Actions, an error occurred in the keystore password setting step and the build failed.)

---

## 3. Error Message
**Step where error occurred:**
`(Example: Setup Keystore from GitHub Secrets)`

**Error log:**
(Please paste the core part of the error message here. If it's too long, extract about 10-20 lines from where the error starts.)

---

## 4. Related Code
**File name:**
`(Example: .github/workflows/build-apk.yml)`

**Code (around problem area):**
```yaml
# (Paste about 10 lines before and after the code suspected to be the cause of the error)
```

---

## 5. Environment
- Execution environment: (Example: GitHub Actions (Ubuntu 22.04))
- Related tools and versions:
  - (Example: Java (Temurin) 17)
  - (Example: Node.js 20.x)

---

## 6. What has been tried / What is known
**Root cause hypothesis:**
(Example: As a result of Phase 2 analysis, I believe the root cause is that Java's keytool command does not accept empty passwords.)

**Tried solutions:**
(Example: I tried setting a dummy string as the password, but got a different error.)

---

## 7. Questions
- Is this root cause analysis valid?
- What do you think is the approach closest to best practices for solving this problem?
- (Add specific questions if any)
```