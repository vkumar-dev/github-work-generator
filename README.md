# GitHub Work Generator

🚀 **AI-powered automation framework that analyzes your GitHub projects, generates actionable ideas, and automates execution.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/vkumar-dev/github-work-generator)](https://github.com/vkumar-dev/github-work-generator/stargazers)

> **Note:** This project is not affiliated with GitHub Inc. GitHub is a registered trademark of GitHub, Inc.

---

## 📖 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Architecture](#architecture)
- [Customization](#customization)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The GitHub Work Generator is an intelligent automation framework that:

1. **Analyzes** your project portfolio using GitHub CLI
2. **Generates** high-impact project ideas using AI
3. **Presents** ideas via GUI or terminal interface
4. **Executes** approved ideas through automated workflows
5. **Learns** from outcomes to improve future suggestions

Perfect for developers, creators, and teams looking to maximize productivity through AI-driven decision making.

---

## ✨ Features

- 🔍 **GitHub Analysis** - Automatically analyze your repositories for opportunities
- 💡 **AI Idea Generation** - Get context-aware project suggestions
- 🖥️ **Multiple UI Options** - Terminal, TUI, GUI, or web interface
- 🔄 **Automated Execution** - Integrate with task runners for implementation
- 📊 **Traffic Analytics** - Make data-driven decisions
- ⏰ **Smart Scheduling** - Configurable rest periods between cycles
- 🎨 **Customizable Prompts** - Tailor AI behavior to your needs
- 📝 **State Persistence** - Never lose progress with automatic state saving

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/vkumar-dev/ai-work-generator-framework.git
cd ai-work-generator-framework

# Install dependencies (optional, for GUI mode)
pip install -r requirements.txt

# Configure your settings
cp config.example.sh config.sh
# Edit config.sh with your preferences

# Run in terminal mode
./workgenerator.sh

# Or run with GUI (requires PyQt5)
USE_GUI=true ./workgenerator.sh
```

---

## 📦 Installation

### Prerequisites

- **Bash** (v4.0+)
- **GitHub CLI** (`gh`)
- **Python 3** (for GUI mode)
- **AI CLI Tool** (e.g., `qwen`, `ollama`, or custom)

### Step 1: Install GitHub CLI

```bash
# Ubuntu/Debian
sudo apt install gh

# macOS
brew install gh

# Authenticate
gh auth login
```

### Step 2: Clone the Repository

```bash
git clone https://github.com/vkumar-dev/ai-work-generator-framework.git
cd ai-work-generator-framework
```

### Step 3: Install Optional Dependencies

```bash
# For GUI mode (PyQt5)
pip install -r requirements.txt

# For web mode (optional)
# No additional dependencies needed
```

### Step 4: Configure AI Tool

The framework works with any AI CLI tool. Configure in `config.sh`:

```bash
# Example: Using Qwen
QWEN_BIN="qwen"

# Example: Using Ollama
QWEN_BIN="ollama run llama2"

# Example: Custom AI endpoint
QWEN_BIN="curl -X POST https://your-ai-api.com/generate -d"
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `QWEN_BIN` | `qwen` | AI CLI command |
| `USE_GUI` | `false` | Enable popup GUI |
| `WORKGENERATOR_APP_GUI` | `false` | Enable embedded app GUI |
| `WG_SINGLE_RUN` | `false` | Run once and exit |
| `WG_SKIP_WAIT` | `false` | Skip user confirmation |
| `REST_SECONDS` | `14400` | Rest period between cycles (4h) |

### Configuration File

Create `config.sh` from the example:

```bash
cp config.example.sh config.sh
```

Edit with your settings:

```bash
# Your primary goal
GOAL="Create impactful digital products"

# Financial constraints (optional)
AVAILABLE_CAPITAL=0
EMERGENCY_FUND=0
MAX_BORROWING=0

# Preferred technologies
TECH_STACK="Python, JavaScript, Shell"

# Target audience
TARGET_AUDIENCE="Developers, creators, small teams"
```

---

## 💻 Usage

### Terminal Mode (Default)

```bash
./workgenerator.sh
```

### GUI Mode

```bash
USE_GUI=true ./workgenerator.sh
```

### App GUI Mode (Embedded)

```bash
WORKGENERATOR_APP_GUI=true ./workgenerator.sh
```

### Single Run Mode

```bash
WG_SINGLE_RUN=true ./workgenerator.sh
```

### Web Interface

```bash
# Open workgenerator-web.html in your browser
# Requires local web server or GitHub Pages
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Work Generator                         │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   GitHub     │  │     AI       │  │   Decision   │      │
│  │  Analysis    │→ │  Generation  │→ │   Interface  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         ↓                  ↓                  ↓              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Traffic    │  │  Planning    │  │  Execution   │      │
│  │   Analytics  │  │  Generation  │  │   (Ralph)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
         ↓                  ↓                  ↓
    gh CLI commands    AI Prompts       Task Runner
```

### Core Components

| Component | Description |
|-----------|-------------|
| `workgenerator.sh` | Main orchestration script |
| `workgenerator-desktop.py` | PyQt5 GUI interface |
| `workgenerator-tui.sh` | Terminal UI mode |
| `workgenerator-web.html` | Web interface |
| `prompts/` | AI prompt templates |
| `config.example.sh` | Configuration template |

---

## 🎨 Customization

### Custom Prompts

Edit prompts in the `prompts/` directory:

```bash
prompts/
├── github-analysis.prompt.md    # Repository analysis
├── idea-generation.prompt.md    # Idea creation
├── implementation-plan.prompt.md # Task planning
└── load-prompts.sh              # Prompt loader
```

### Example: Custom Analysis Prompt

```markdown
# GitHub Analysis
```
Using gh CLI:
Goal: {{GOAL}}
Portfolio State: {{PORTFOLIO_STATE}}

Analyze for opportunities in: {{FOCUS_AREA}}
Return: {{NUM_IDEAS}} project ideas with:
- Traffic metrics
- Technology gaps
- Implementation complexity
Format: {{OUTPUT_FORMAT}}
```
```

### Integration Points

- **GitHub CLI**: Customize queries in `github-analysis.prompt.md`
- **AI Backend**: Swap AI provider in `config.sh`
- **Task Runner**: Integrate custom executors (Ralph, Make, etc.)
- **UI**: Modify interfaces or create new ones

---

## 📚 Examples

### Example 1: Developer Portfolio Optimization

```bash
# Goal: Build developer tools
GOAL="Create tools that help developers save time"

# The framework will:
# 1. Analyze your repos for common pain points
# 2. Suggest tooling improvements
# 3. Generate implementation plans
```

### Example 2: Content Creation Pipeline

```bash
# Goal: Generate technical content
GOAL="Create educational content about emerging technologies"

# The framework will:
# 1. Identify trending topics in your repos
# 2. Suggest article/video topics
# 3. Create content outlines
```

### Example 3: Product Development

```bash
# Goal: Build revenue-generating products
GOAL="Launch SaaS products with market fit"

# The framework will:
# 1. Analyze market gaps via GitHub trends
# 2. Suggest product ideas
# 3. Create MVP roadmaps
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
git clone https://github.com/vkumar-dev/ai-work-generator-framework.git
cd ai-work-generator-framework

# Run tests (if available)
./run-tests.sh

# Lint code
./lint.sh
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with ❤️ using GitHub CLI and AI
- Inspired by automation-first development workflows
- Thanks to all contributors and users!

---

## 📞 Support

- **Documentation**: https://vkumar-dev.github.io/github-work-generator
- **Issues**: https://github.com/vkumar-dev/github-work-generator/issues
- **Discussions**: https://github.com/vkumar-dev/github-work-generator/discussions

---

<div align="center">

**Made with [AI](https://qwen.ai) + [GitHub](https://github.com)**

[⬆ Back to Top](#ai-work-generator-framework)

</div>
