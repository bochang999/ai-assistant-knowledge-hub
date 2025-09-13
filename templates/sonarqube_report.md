# SonarQube Final Verification Report Template (Mandatory Format)

```
# 🔍 SonarQube Final Verification Report ({Issue Number})

## 1. Quality Gate
- **Decision:** 🟢 Pass / 🔴 Failed
- **Details:** (Record major metrics such as coverage, duplication rate, security vulnerabilities)

## 2. Major Metrics
- **Reliability (Bugs):** A (0 New Bugs)
- **Security (Vulnerabilities):** A (0 New Vulnerabilities)
- **Maintainability (Code Smells):** A (0 New Code Smells)
- **Coverage:** 85% (> 80%)

## 3. Difference Analysis with Self-Review
- (Record Issues newly detected by SonarQube that were missed in AI assistant's preliminary review. If none, record "No differences")
- **Newly Detected Issue 1:**
  - **Type:** (Example: Bug, Code Smell)
  - **Content:** "Magic numbers should not be used."
  - **Location:** `file.ext` L10
  - **Consideration:** Hard-coded values that should be constants were used directly. In future self-reviews, need to pay attention to such hard-coded values.

## 4. Overall Decision and Recommended Response
- **Decision:** Approved / Needs Modification
- **Reason:** (Describe final decision reason based on Quality Gate results and difference analysis)
- **Recommended Response:** (If needs modification, list specific next actions)
```