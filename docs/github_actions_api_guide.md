# GitHub Actions Error Detail Information Retrieval (BOC-46 Compliant)

## Phase 1: Actions Execution History Retrieval

```bash
curl -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/[OWNER]/[REPO]/actions/runs
# Output: run_id, status, conclusion, head_sha, created_at
```

## Phase 2: Failed Job Detail Retrieval

```bash
# (Identify run_id in Phase 1)
curl -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/[OWNER]/[REPO]/actions/runs/[RUN_ID]/jobs
# Output: name, status, conclusion, started_at, completed_at for each step
```

## Phase 3: Actual Log File Retrieval (Authentication Required)

**Personal Access Token (classic) Required Scopes:**
- repo (Full control of private repositories)
- workflow (Update GitHub Action workflows)
- admin:repo_hook (Full control of repository hooks)
- read:org (Read org and team membership) ← GitHub CLI required

```bash
echo 'YOUR_TOKEN' | gh auth login --with-token
gh run view [RUN_ID] --repo [OWNER]/[REPO] --log
```

## Phase 4: Information Required for Analysis

Information obtainable from the above APIs:
- ✅ **Failed Step Identification**: steps with conclusion="failure"
- ✅ **Execution Time Analysis**: started_at → completed_at
- ✅ **Impact Scope Confirmation**: Check if subsequent step status is skipped
- ✅ **Change History Confirmation**: Check corresponding commit content from head_sha
- ✅ **Actual Error Content Confirmation**: Get specific error messages with gh run view --log

## Proven Example (pwa-to-apk-template)

- **Run ID: 17510369988** → Step 6: Install Dependencies failed → Stopped in 13 seconds
- **Run ID: 17510939777** → Actual error content: package-lock.json sync error confirmed
- **Root Cause**: `npm ci` requires package.json and package-lock.json sync