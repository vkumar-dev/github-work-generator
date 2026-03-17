# AI Agent Implementation Guide

> **For AI Coding Agents:** This document provides everything you need to implement the GitHub Work Generator framework in a new repository or project.

---

## 🎯 Your Mission

Implement a **GitHub Work Generator** - an AI-powered automation framework that:

1. Analyzes GitHub repositories using `gh cli`
2. Generates project ideas using AI
3. Presents ideas via GUI/terminal interface
4. Executes approved ideas through automated workflows
5. Rests between cycles for sustainable automation

---

## 📋 Implementation Steps

### Phase 1: Setup & Configuration

```markdown
## Task 1.1: Project Scaffolding
- Create a new repository for the GitHub Work Generator
- Set up the directory structure:
  ```
  github-work-generator/
  ├── workgenerator.sh          # Main orchestration script
  ├── workgenerator-desktop.py  # PyQt5 GUI (optional)
  ├── config.example.sh         # Configuration template
  ├── prompts/                  # AI prompt templates
  │   ├── github-analysis.prompt.md
  │   ├── idea-generation.prompt.md
  │   ├── implementation-plan.prompt.md
  │   └── load-prompts.sh
  ├── docs/                     # GitHub Pages documentation
  ├── .github/workflows/        # GitHub Actions
  ├── README.md
  ├── LICENSE
  └── .gitignore
  ```

## Task 1.2: Configuration System
- Create `config.example.sh` with template variables:
  - `GOAL` - User's primary objective
  - `QWEN_BIN` - AI CLI command (qwen, ollama, etc.)
  - `REST_SECONDS` - Rest period between cycles
  - `USE_GUI` - Enable/disable GUI mode
  - `TECH_STACK` - Preferred technologies
  - `GITHUB_USERNAME` - GitHub user (auto-detect if empty)
- Add validation for required dependencies (gh, AI tool)
```

### Phase 2: Core Implementation

```markdown
## Task 2.1: GitHub Analysis Module
- Implement `analyze_github()` function using `gh cli`:
  - Fetch repository list with `gh repo list`
  - Get traffic data with `gh api repos/{owner}/{repo}/traffic/...`
  - Analyze stars, forks, recent activity
  - Identify trends and opportunities
- Output structured analysis for AI consumption

## Task 2.2: AI Integration Module
- Implement AI prompt loading system
- Create `generate_idea()` function:
  - Load portfolio state
  - Load GitHub analysis
  - Call AI with structured prompt
  - Parse and format AI response
- Support multiple AI backends (qwen, ollama, custom)
- Add retry logic with exponential backoff

## Task 2.3: Decision Interface
- Implement user decision flow:
  - Display generated idea
  - Accept: YES / NO / PASS / IMPROVE / QUIT
  - Handle each decision type appropriately
- Add single-run mode for automation
- Add auto-skip mode for testing
```

### Phase 3: User Interfaces

```markdown
## Task 3.1: Terminal Interface (Required)
- Color-coded output using ANSI escape codes
- Progress indicators and status messages
- Interactive prompts for decisions
- Logging to file and stdout

## Task 3.2: Desktop GUI (Optional - PyQt5)
- Create `workgenerator-desktop.py`:
  - Main window with split layout
  - Live terminal output panel
  - Decision buttons (Approve/Reject/Pass/Improve)
  - Status indicators (Phase, Task, Connection)
  - Portfolio state display
- Style with dark theme and glow effects
- Handle backend process communication

## Task 3.3: Web Interface (Optional)
- Create `workgenerator-web.html`:
  - Single-page application
  - WebSocket or polling for live updates
  - Responsive design
  - Decision interface
```

### Phase 4: Execution & Automation

```markdown
## Task 4.1: Implementation Planning
- Implement `generate_plan()` function:
  - Take approved idea + user improvements
  - Call AI to generate task breakdown
  - Output JSON array of tasks with:
    - Task ID and description
    - Estimated effort
    - Dependencies
    - Success criteria
    - Commands to execute

## Task 4.2: Task Execution
- Implement `execute_plan()` function:
  - Iterate through tasks
  - Execute shell commands
  - Track progress
  - Handle errors gracefully
- Integration with task runners (Ralph, Make, etc.)
- Auto-commit and push options

## Task 4.3: State Management
- Implement state persistence:
  - `.workgenerator_config` - iteration, status
  - `.ideas_log.json` - idea history
  - `.pending_tasks.json` - pending tasks
- Load state on startup
- Save state after each decision
```

### Phase 5: Documentation & Deployment

```markdown
## Task 5.1: README.md
- Project overview and features
- Quick start guide (3 steps)
- Configuration reference
- Usage examples
- Architecture diagram
- Contributing guidelines

## Task 5.2: GitHub Pages Site
- Create `docs/index.html`:
  - Hero section with terminal demo
  - Features grid
  - Quick start section
  - Documentation links
  - Use cases/examples
  - Footer with links
- Add `docs/styles.css` (dark theme)
- Add `docs/script.js` (interactions)

## Task 5.3: GitHub Actions
- Create `.github/workflows/deploy-pages.yml`:
  - Deploy docs on push to main
  - Use actions/configure-pages
  - Use actions/upload-pages-artifact
  - Use actions/deploy-pages
```

---

## 🔧 Technical Requirements

### Dependencies

| Tool | Purpose | Required |
|------|---------|----------|
| `bash` (v4.0+) | Main scripting | Yes |
| `gh` (GitHub CLI) | GitHub API access | Yes |
| `python3` | GUI mode | Optional |
| `PyQt5` | Desktop GUI | Optional |
| AI CLI (qwen, ollama) | AI generation | Yes* |

*Can work in manual mode without AI

### Environment Variables

```bash
# Required
QWEN_BIN="qwen"              # AI CLI command

# Optional
USE_GUI="false"              # Enable GUI mode
WORKGENERATOR_APP_GUI="false" # Embedded app GUI
WG_SINGLE_RUN="false"        # Run once and exit
WG_SKIP_WAIT="false"         # Skip user confirmation
REST_SECONDS="14400"         # 4 hours rest
LOG_LEVEL="INFO"             # DEBUG, INFO, WARN, ERROR
```

---

## 📁 File Templates

### workgenerator.sh (Skeleton)

```bash
#!/bin/bash
set +e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load config
[[ -f "${SCRIPT_DIR}/config.sh" ]] && source "${SCRIPT_DIR}/config.sh"

# Defaults
QWEN_BIN="${QWEN_BIN:-qwen}"
REST_SECONDS="${REST_SECONDS:-14400}"
GOAL="${GOAL:-Create impactful digital products}"

# Main loop
main_loop() {
    while true; do
        # 1. Analyze GitHub
        # 2. Generate idea
        # 3. Get user decision
        # 4. Execute or rest
        sleep "$REST_SECONDS"
    done
}

main_loop
```

### Prompt Template (prompts/idea-generation.prompt.md)

```markdown
# Idea Generation Prompt

```
Using gh CLI:

Goal: {{GOAL}}
Portfolio State: {{PORTFOLIO_STATE}}
GitHub Analysis: {{GITHUB_ANALYSIS}}

Generate ONE high-impact digital product idea.

Format:
---
**PROJECT IDEA #{{ITERATION}}**
## Title
## Description
## Why This Is A Good Idea
## Implementation Overview
## Estimated Impact
## Effort Required
---
```
```

---

## ✅ Acceptance Criteria

The implementation is complete when:

- [ ] `./workgenerator.sh` runs without errors
- [ ] GitHub analysis fetches real repository data
- [ ] AI generates formatted project ideas
- [ ] User can approve/reject/pass/improve ideas
- [ ] Implementation plans are generated as JSON
- [ ] State persists across restarts
- [ ] GUI mode works (if implemented)
- [ ] Documentation is complete
- [ ] GitHub Pages deploys automatically

---

## 🚀 Quick Start for Agents

**Copy and paste this prompt into your AI coding agent:**

```
I need you to implement the GitHub Work Generator framework.

Repository: https://github.com/vkumar-dev/github-work-generator

This is an AI-powered automation framework that:
1. Analyzes GitHub repos using gh cli
2. Generates project ideas using AI
3. Shows ideas via GUI/terminal
4. Executes approved ideas automatically
5. Rests between cycles

Implementation files are in the repo above. Your tasks:

1. Clone the repository
2. Read AGENT.md for implementation guide
3. Read prompts/*.prompt.md for AI templates
4. Implement workgenerator.sh with:
   - GitHub analysis using gh cli
   - AI idea generation
   - User decision interface
   - Task planning and execution
   - State persistence
5. Optionally implement workgenerator-desktop.py (PyQt5)
6. Create docs/ for GitHub Pages
7. Test the implementation

Start by reading the existing files, then implement step by step.
Ask me questions if you need clarification.
```

---

## 📞 Support

If you encounter issues during implementation:

1. Check existing files in the repository for reference
2. Review the prompt templates in `prompts/`
3. Consult the README.md for usage examples
4. Open an issue on GitHub for clarification

---

**Repository:** https://github.com/vkumar-dev/github-work-generator  
**License:** MIT  
**Author:** vkumar-dev
