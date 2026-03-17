# Implementation Plan Prompt

```
Create a detailed, executable implementation plan for:

{{IDEA}}

{{USER_IMPROVEMENTS}}

Requirements:
- Break down into discrete, actionable tasks
- Each task should be independently verifiable
- Include dependencies between tasks
- Estimate effort for each task
- Define clear success criteria

Output Format (JSON array):
[
  {
    "id": 1,
    "title": "Task title",
    "description": "Detailed task description",
    "estimated_hours": 2,
    "dependencies": [],
    "success_criteria": "How to verify completion",
    "commands": ["shell commands to execute"],
    "files": ["files to create/modify"]
  }
]

Prioritize:
1. Setup and scaffolding
2. Core functionality
3. Testing and validation
4. Documentation
5. Deployment
```
