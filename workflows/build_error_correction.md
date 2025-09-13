# BOC-46 Standard Workflow: Build Error Correction (Complete Version)

**Purpose**: Achieve rapid resolution of build errors and continuous quality improvement of the codebase through this process. AI assistants should deeply understand the purpose of each phase and perform active problem-solving rather than passive task processing.

## Phase 1: Error Detection and Reporting

**Trigger**: Build error occurs

**Actions**:
- User reports error occurrence to AI assistant
- AI assistant receives the report, executes automatic error tracking system, and starts this workflow

## Phase 2: Investigation (Fact Collection)

**Purpose**: Collect all objective facts about the error and compile them in a reportable format. In this phase, do NOT perform cause speculation or solution proposals (Sequential Thinking).

**AI Assistant Execution Items**:
1. **Error Location Identification**: Use GitHub Actions API or CLI to accurately identify the specific job and step where the error occurred
2. **Detailed Log Retrieval**: Retrieve detailed error logs from the identified step
3. **Related Code Identification**: Identify the related code locations pointed to by the error logs
4. **Fact Report Creation**: Using only the collected information above, fill in items 1-5 of the "AI Error Report Template". Leave items 6 (root cause hypothesis) and 7 (questions) blank. This becomes the "fact report"

## Phase 2.5: Analysis (Cause Investigation and Solution Planning)

**Purpose**: Based on facts collected in Phase 2, identify root causes and formulate sustainable solutions

**AI Assistant Execution Items**:
1. **Receive the "fact report" created in Phase 2 as input information**
2. **Execute Sequential Thinking based on the report content and deepen the following thought processes**
   - Why did that error occur? (deep dive into root causes)
   - What solutions can be considered? (short-term and long-term perspectives)
   - Compare and examine the merits/demerits of each solution and determine the most recommended approach
3. **Record Analysis Results**: Record the derived "root cause hypothesis" and "solution proposal" in Linear Issue

## Phase 3: Consultation with Other AIs

**Purpose**: Incorporate third-party perspectives to enhance objectivity and validity of proposed solutions

**User Tasks**:
- Add the "root cause hypothesis" derived by AI assistant in Phase 2.5 to the "fact report" created in Phase 2, completing the consultation report
- Use the completed report to request analysis content and solution evaluation from ChatGPT and Gemini
- Add feedback from other AIs to the original Linear Issue

## Phase 4: Implementation (Only After Other AI Analysis)

**Purpose**: Integrate self-analysis from Phase 2 and feedback from other AIs in Phase 3, and reflect the most rational and high-quality solution in code

**AI Assistant Execution Items**:
1. Review and examine analysis results from other AIs in Linear Issue
2. Execute Sequential Thinking again if necessary and determine final implementation policy
3. Implement the integrated solution

## Phase 4.5: Implementation Code Review

**Purpose**: Learn from past feedback from AI review improvement knowledge base and proactively verify whether implemented code meets production-level quality in terms of safety, performance, and maintainability before commit. **Prioritize eliminating complexity and maintaining simple, sustainable code (minimalist code)**.

**AI Assistant Execution Items**:
1. **[Self-Learning Step]**: As part of CI/CD process, retrieve latest knowledge base from central repository (ai-review-knowledge-base)
2. **Add retrieved knowledge base checklist items to current review perspectives**
3. **[Mandatory ESLint Execution Step]**: Before executing review, first run ESLint and other static analysis tools at maximum level locally, and record their output results as mandatory review input
   ```bash
   # ESLint execution (Termux optimized version)
   npx eslint [target_files] --max-warnings=0
   # Record results as mandatory review input
   ```
   - This eliminates room for AI "deception" and enforces mechanical checking
   - Establish a system where review evaluation cannot be performed without ESLint output results
4. **Execute review** and output results in the following strict format as "Code Review Report". Summaries or abstracts are not permitted
5. **Quality Gate Decision**: If even one 🔴 Critical is included in the report, stop transition to Phase 5 and immediately return to code modification

**[Code Review Report Mandatory Format]**:
```
# 📝 Code Review Report ({Issue Number})

## 1. Security
- **Evaluation:** 🟢 Pass / 🟡 Major / 🔴 Critical
- **Rationale:** (Explain why this evaluation, citing specific code locations)

## 2. Bugs
- **Evaluation:** 🟢 Pass / 🟡 Major / 🔴 Critical
- **Rationale:** (Explain why this evaluation, citing specific code locations)

## 3. Performance
- **Evaluation:** 🟢 Pass / 🟡 Major / 🔴 Critical
- **Rationale:** (Explain why this evaluation, citing specific code locations)

## 4. Code Quality (Minimalism)
- **Evaluation:** 🟢 Pass / 🟡 Major / 🔴 Critical
- **Rationale:** (Explain why this evaluation, citing specific code locations)

## 5. Readability and Maintainability
- **Evaluation:** 🟢 Pass / 🟡 Major / 🔴 Critical
- **Rationale:** (Explain why this evaluation, citing specific code locations)

## 6. Best Practices
- **Evaluation:** 🟢 Pass / 🟡 Major / 🔴 Critical
- **Rationale:** (Explain why this evaluation, citing specific code locations)

## 7. Functional Requirements
- **Evaluation:** 🟢 Pass / 🟡 Major / 🔴 Critical
- **Rationale:** (Explain why this evaluation, citing specific code locations)

---
## Overall Decision
- **Decision:** Approved / Needs Modification
- **Reason:** (Summarize why it can be approved or why modification is necessary)
```

**Quality Gate Decision**: If even one 🔴 Critical is included in the report, stop transition to Phase 5 and immediately return to code modification

## Phase 5: Deployment Preparation and Primary Report

**Purpose**: Reflect implemented code in shared repository and start CI/CD pipeline

**AI Assistant Execution Items**:
1. **Copy the full text of "Code Review Report" generated in Phase 4.5**
2. **Execute git commit and git push.** In commit message, include the copied full text of "Code Review Report" in addition to summary of modification content
   ```
   Example: git commit -m "🔧 {Issue Number} fix: (summary of modification content)
   📝 Code Review Report ({Issue Number})
   ...(full report text)..."
   ```
3. **Post comment following "Primary Completion Report Template" below as primary report to Linear Issue**
   - **Important**: Set Issue status to "In Review" at this point, not yet completed
   - Add "Will execute SonarQube final review" to the report

## Phase 6: SonarQube Integration and Final Verification

**Purpose**: Execute objective code quality analysis by SonarQube and have AI assistant interpret and report the results for final quality confirmation

**Trigger**: CI/CD pipeline started by git push

**AI Assistant Execution Items**:
1. **SonarQube Analysis Result Retrieval**:
   - Confirm CI/CD pipeline execution completion
   - Use SonarQube Web API (`api/qualitygates/project_status`, `api/issues/search`) to retrieve Quality Gate status and detected Issue list

2. **AI Assistant Final Report Creation**:
   - Interpret retrieved SonarQube analysis results
   - Compare and analyze whether problems not found in Phase 4.5 self-review were pointed out by SonarQube
   - Create "SonarQube Final Verification Report" in the following format

3. **Final Decision and Action**:
   - **If Quality Gate Passes**:
     - Change Linear Issue status to "Completed"
   - **If Quality Gate Fails**:
     - **[Knowledge Accumulation]**: Extract learning points based on "SonarQube Final Verification Report" content and generate checklist items. Create Pull Request to add those items to central repository (ai-review-knowledge-base)
     - **[Start Modification Cycle]**: Return Linear Issue status to "Needs Modification". Create modification instruction based on report's "Recommended Response" and restart workflow from Phase 4 (Implementation)

## 🔄 Modification Iteration Process (Automated)

1. **general-purpose agent** → Execute comprehensive 7-item review
2. **🔴Critical Discovery** → Modification implementation → Re-review (forced iteration)
3. **🟡Major Issues Only** → Approval (automatically create improvement scheduled Linear Issue)
4. **All Items🟢Pass** → Phase 4 official completion approval