# GitHub Work Generator - AI Agent Implementation Prompt

> **Copy and paste this entire prompt into your AI coding agent** (Claude, Cursor, Copilot, etc.) to implement the GitHub Work Generator framework.

---

## 🎯 Implementation Request

**Project:** GitHub Work Generator  
**Repository:** https://github.com/vkumar-dev/github-work-generator  
**Type:** AI-powered automation framework for GitHub project generation  

---

## 📋 What I Need You to Build

Implement a **GitHub Work Generator** - an intelligent automation framework that:

1. **Analyzes** my GitHub repositories using `gh cli`
2. **Generates** high-impact project ideas using AI (qwen, ollama, etc.)
3. **Presents** ideas via terminal or GUI interface
4. **Executes** approved ideas through automated workflows
5. **Rests** 4 hours between cycles for sustainable automation

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Work Generator                     │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   GitHub     │  │     AI       │  │   Decision   │      │
│  │  Analysis    │→ │  Generation  │→ │   Interface  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         ↓                  ↓                  ↓              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Traffic    │  │  Planning    │  │  Execution   │      │
│  │   Analytics  │  │  Generation  │  │   (Tasks)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Directory Structure to Create

```
github-work-generator/
├── workgenerator.sh              # Main bash script (REQUIRED)
├── workgenerator-desktop.py      # PyQt5 GUI (optional)
├── config.example.sh             # Configuration template
├── prompts/
│   ├── github-analysis.prompt.md
│   ├── idea-generation.prompt.md
│   ├── implementation-plan.prompt.md
│   └── load-prompts.sh
├── docs/
│   ├── index.html                # GitHub Pages
│   ├── styles.css
│   └── script.js
├── .github/workflows/
│   └── deploy-pages.yml
├── README.md
├── AGENT.md                      # This file
├── LICENSE
└── .gitignore
```

---

## 🔧 Implementation Tasks

### Task 1: Core Script (workgenerator.sh)

Create the main bash script with these functions:

```bash
#!/bin/bash
# GitHub Work Generator - Main Script

# Configuration loading
# - Load config.sh if exists
# - Set defaults for all variables

# Dependency checking
# - Check for gh cli (required)
# - Check for AI tool (qwen, ollama, etc.)
# - Check for Python (optional, for GUI)

# GitHub Analysis
# - gh repo list --json name,description,starCount,forkCount,updatedAt
# - Parse and format repository data
# - Identify trends and opportunities

# AI Idea Generation
# - Load prompts from prompts/ directory
# - Call AI with structured prompt
# - Parse AI response

# User Decision Interface
# - Display generated idea
# - Accept: YES / NO / PASS / IMPROVE / QUIT
# - Handle each decision type

# Implementation Planning
# - Generate task breakdown from idea
# - Output JSON array of tasks

# Task Execution
# - Execute tasks sequentially
# - Track progress
# - Handle errors

# State Management
# - Save/load iteration state
# - Log ideas and decisions
# - Persist pending tasks

# Main Loop
# - Run analysis → generate → decide → execute → rest → repeat
```

**Key Requirements:**
- Use ANSI colors for terminal output
- Log all actions to `workgenerator.log`
- Support environment variable overrides
- Handle Ctrl+C gracefully
- Save state after each decision

---

### Task 2: Configuration System (config.example.sh)

Create a comprehensive configuration template:

```bash
#!/bin/bash
# GitHub Work Generator - Configuration Template

# Primary goal (be specific for better AI suggestions)
GOAL="Create impactful digital products that generate value"

# AI Configuration
QWEN_BIN="qwen"                    # AI CLI command
AI_TEMPERATURE="0.7"
AI_MAX_TOKENS="2048"

# Workflow Configuration
REST_SECONDS=14400                 # 4 hours
WG_SINGLE_RUN=false
WG_SKIP_WAIT=false

# UI Configuration
USE_GUI=false
WORKGENERATOR_APP_GUI=false

# Technology Preferences
TECH_STACK="Python, JavaScript, Shell"
TARGET_AUDIENCE="Developers, creators"

# GitHub Configuration
GITHUB_USERNAME=""                 # Auto-detect if empty
ANALYZE_REPOS=""                   # All repos if empty

# Logging
LOG_LEVEL="INFO"
DEBUG=false
```

---

### Task 3: AI Prompts (prompts/)

Create three prompt templates:

**prompts/github-analysis.prompt.md:**
```markdown
Using gh CLI:

Goal: {{GOAL}}
Portfolio State: {{PORTFOLIO_STATE}}

Analyze GitHub for high-impact opportunities to build digital products.

Return: 5-10 trending projects with:
- Traffic metrics (stars, forks, activity)
- Technology stack
- Gaps and opportunities
- Product potential

Format: Bullet points with clear sections.
```

**prompts/idea-generation.prompt.md:**
```markdown
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

**prompts/implementation-plan.prompt.md:**
```markdown
Create implementation plan for:

{{IDEA}}

User Improvements: {{USER_IMPROVEMENTS}}

Output JSON array of tasks:
[
  {
    "id": 1,
    "title": "Task title",
    "description": "Description",
    "estimated_hours": 2,
    "dependencies": [],
    "success_criteria": "How to verify",
    "commands": ["shell commands"]
  }
]
```

---

### Task 4: Desktop GUI (workgenerator-desktop.py) - Optional

Create a PyQt5 application with:

- **Main window** (1460x940, dark theme)
- **Left panel:**
  - Header with title and status HUD
  - Spotlight frame (current task display with glow effect)
  - Transcript list (scrolling message log)
- **Right panel:**
  - Portfolio state card
  - Decision card (Approve/Reject/Pass/Improve buttons)
  - Improvement card (text input for feedback)
  - Control panel (stop backend button)
- **Backend integration:**
  - Run workgenerator.sh as subprocess
  - Parse stdout for events
  - Send decisions via stdin

**Styling:**
- Dark blue background (#07111f)
- Cyan/green accent colors
- Rounded corners (24px)
- Glow effects on active elements
- Monospace fonts for code

---

### Task 5: Documentation Site (docs/)

Create GitHub Pages site:

**docs/index.html:**
- Navigation bar (fixed, blur effect)
- Hero section (title, subtitle, terminal demo, stats)
- Features grid (8 cards)
- Quick Start section (3 steps with code blocks)
- Documentation section (4 cards with links)
- Examples section (3 use cases)
- Footer (links, license, credits)

**docs/styles.css:**
- CSS variables for colors
- Dark theme (#07111f background)
- Gradient accents (cyan → green → yellow)
- Responsive grid layouts
- Smooth animations
- Mobile-friendly breakpoints

**docs/script.js:**
- Smooth scroll for nav links
- Scroll-based navbar styling
- Intersection Observer for animations
- Copy-to-clipboard for code blocks
- Console welcome message

---

### Task 6: GitHub Actions (.github/workflows/)

Create deployment workflow:

```yaml
name: Deploy GitHub Pages

on:
  push:
    branches: [main]
    paths: ['docs/**']
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with:
          path: './docs'
      - uses: actions/deploy-pages@v4
```

---

### Task 7: README.md

Create comprehensive documentation:

```markdown
# GitHub Work Generator

🚀 AI-powered automation framework that analyzes your GitHub projects, 
generates actionable ideas, and automates execution.

## Features
- GitHub Analysis
- AI Idea Generation
- Multiple UI Options (Terminal, GUI, Web)
- Automated Execution
- Smart Scheduling

## Quick Start
1. Clone: git clone https://github.com/vkumar-dev/github-work-generator
2. Configure: cp config.example.sh config.sh && nano config.sh
3. Run: ./workgenerator.sh

## Configuration
[Table of all options]

## Usage
[Terminal, GUI, and web mode examples]

## Architecture
[Diagram and component description]

## Contributing
[Guidelines]

## License
MIT
```

---

## ✅ Acceptance Criteria

Your implementation is complete when:

- [ ] `./workgenerator.sh --help` shows usage
- [ ] `./workgenerator.sh` runs without errors
- [ ] GitHub analysis fetches real data via `gh cli`
- [ ] AI generates properly formatted ideas
- [ ] User can make decisions (Y/N/PASS/IMPROVE)
- [ ] Implementation plans are valid JSON
- [ ] State persists in `.workgenerator_config`
- [ ] Logs written to `workgenerator.log`
- [ ] GUI mode launches (if implemented)
- [ ] GitHub Pages deploys automatically
- [ ] README documents all features

---

## 🚀 How to Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vkumar-dev/github-work-generator
   cd github-work-generator
   ```

2. **Read existing files:**
   - `AGENT.md` - Implementation guide
   - `prompts/*.prompt.md` - AI templates
   - `config.example.sh` - Configuration

3. **Implement step by step:**
   - Start with `workgenerator.sh` (core logic)
   - Add prompts (AI templates)
   - Add config system
   - Add GUI (optional)
   - Add documentation

4. **Test frequently:**
   ```bash
   WG_SINGLE_RUN=true ./workgenerator.sh
   ```

5. **Ask questions** if you need clarification on any requirement.

---

## 📞 Reference

- **Repository:** https://github.com/vkumar-dev/github-work-generator
- **Documentation:** https://vkumar-dev.github.io/github-work-generator
- **License:** MIT
- **Author:** vkumar-dev

---

**Ready to begin? Start by cloning the repository and reading the existing files!**
