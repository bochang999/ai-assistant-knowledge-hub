# General Issue Workflow

## Overview
This is the default workflow for issues that don't fall into specific categories like build errors, UI problems, or API issues.

## Phase 1: Issue Analysis and Setup

### 1.1 Issue Understanding
- Read issue title and description thoroughly
- Identify the project context from issue metadata
- Extract key requirements and acceptance criteria
- Determine the scope and complexity

### 1.2 Status Management
- Automatically update issue status to "In Progress"
- Use Linear GraphQL API with fixed state IDs:
  - IN_PROGRESS_ID="1cebb56e-524e-4de0-b676-0f574df9012a"

### 1.3 Project Context Setup
- Navigate to correct project directory based on project_map.json
- Review project structure and existing codebase
- Understand relevant technologies and frameworks in use

## Phase 2: Investigation and Fact-Gathering

### 2.1 Current State Analysis
- Examine existing implementation (if applicable)
- Identify related files and components
- Document current behavior vs. expected behavior

### 2.2 Technical Assessment
- Review code patterns and conventions
- Check for similar implementations in the codebase
- Identify potential technical constraints or dependencies

### 2.3 Requirements Clarification
- Break down complex requirements into smaller tasks
- Identify any missing information or assumptions
- Plan implementation approach

## Phase 3: Implementation

### 3.1 Planning
- Create implementation plan with clear steps
- Consider impact on existing functionality
- Plan for testing and validation

### 3.2 Code Implementation
- Follow project coding standards and patterns
- Implement features incrementally
- Write clean, maintainable code

### 3.3 Testing and Validation
- Test implemented functionality
- Verify requirements are met
- Check for regressions or side effects

## Phase 4: Documentation and Completion

### 4.1 Code Review
- Review implementation for quality and standards
- Ensure proper error handling
- Verify security considerations

### 4.2 Documentation
- Update relevant documentation
- Add inline comments where necessary
- Document any new patterns or decisions

### 4.3 Linear Issue Completion
- Add comprehensive completion comment to Linear issue
- Include:
  - Summary of work completed
  - Key implementation details
  - Any relevant commit hashes
  - Testing results
- Update issue status to "In Review" using GraphQL API:
  - IN_REVIEW_ID="33feb1c9-3276-4e13-863a-0b93db032a0f"

## Phase 5: Follow-up and Integration

### 5.1 Git Management
- Create appropriate git commits with descriptive messages
- Follow project commit message conventions
- Ensure all changes are properly tracked

### 5.2 Knowledge Sharing
- Update project knowledge base if applicable
- Share learnings or new patterns discovered
- Document any workflow improvements

## Emergency Patterns
- When stuck: Review similar issues in Linear history
- For technical blockers: Consult project documentation and existing patterns
- For scope creep: Document additional requirements as separate issues

## Tools and Commands
- Linear API: Always use GraphQL endpoint with stored credentials
- Project navigation: Use project_map.json for directory resolution
- Status updates: Use predefined state IDs for consistency

---
*This workflow provides a structured approach for general issue resolution while maintaining consistency with the ai-assistant-knowledge-hub system.*
