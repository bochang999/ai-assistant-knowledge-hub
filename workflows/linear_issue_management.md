# Linear Issue Automatic Management System

## 🔄 Linear Issue Automatic Management System

```bash
# Issue work flow (automatic execution):
1. Issue reading start → status: "In Progress"
2. Work execution and code implementation
3. Work completion → content and code recording → status: "In Review"
→ Complete automatic management without permission required
```

## 📋 Linear Status Management Rules

**At Start**: Automatically change to "In Progress" when confirming Issue
**At Completion**: Change to "In Review" after recording work content and code
**When Adding**: Must change to "In Review" after adding comments (mandatory automatic execution)

**Implementation Method**:
```bash
# Status update GraphQL
mutation { issueUpdate(id: "$issue_id", input: { stateId: "$state_id" }) }

# State IDs (fixed values):
IN_PROGRESS_ID="1cebb56e-524e-4de0-b676-0f574df9012a"
IN_REVIEW_ID="33feb1c9-3276-4e13-863a-0b93db032a0f"
```

## 🤖 Automatic Execution Commands

```bash
# When starting Issue
curl -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $(cat ~/.linear-api-key)" \
  -d '{"query":"mutation{issueUpdate(id:\"$ISSUE_ID\",input:{stateId:\"1cebb56e-524e-4de0-b676-0f574df9012a\"})}"}'

# When completing Issue / When adding (mandatory)
curl -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $(cat ~/.linear-api-key)" \
  -d '{"query":"mutation{issueUpdate(id:\"$ISSUE_ID\",input:{stateId:\"33feb1c9-3276-4e13-863a-0b93db032a0f\"})}"}'
```

## 🔄 Mandatory Process When Adding Linear Comments

**Important Rule**: When adding comments to Linear issue, immediately execute verification system afterwards

```bash
# 1. Add comment (using ~/.linear-utils.sh)
~/.linear-utils.sh comment BOC-XX "Comment content"

# 2. Immediately verify afterwards (absolutely mandatory execution)
~/.linear-utils.sh get BOC-XX

# 3. Verification check: Confirm latest comment existence
# Verify if latest createdAt time matches addition time
# If mismatch, respond as emergency automation system failure
```

**Application Cases**:
- Work completion comments
- Additional reports and analysis results
- Error correction reports
- Progress updates
- Technical insight additions

## Integration with Linear API

**Always use GraphQL API** (CLI does not work)
```bash
curl -X POST "https://api.linear.app/graphql" -H "Authorization: $(cat ~/.linear-api-key)"
# Fixed team ID: $(cat ~/.linear-team-id) = "bochang's lab"
```