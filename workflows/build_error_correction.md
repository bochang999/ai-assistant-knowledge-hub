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

## Phase 5: Deployment Preparation and Final Report

**Purpose**: Reflect implemented code in shared repository and start CI/CD pipeline

**AI Assistant Execution Items**:
1. **Summarize implementation content from Phase 4**
2. **Execute git commit and git push.** In commit message, include summary of modification content
   ```
   Example: git commit -m "🔧 {Issue Number} fix: (summary of modification content)"
   ```
3. **Post comment following "Completion Report Template" below as final report to Linear Issue**
   - **Important**: Set Issue status to "In Review" at this point to mark completion