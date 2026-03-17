#!/bin/bash
# AI Work Generator Framework - Configuration Template
# Copy this file to config.sh and customize for your needs

# =============================================================================
# GOAL CONFIGURATION
# =============================================================================

# Your primary objective (be specific for better AI suggestions)
GOAL="Create impactful digital products that generate value"

# =============================================================================
# FINANCIAL CONTEXT (Optional - for revenue-focused ideas)
# =============================================================================

# Available capital for projects
AVAILABLE_CAPITAL=0

# Emergency fund reserve
EMERGENCY_FUND=0

# Maximum borrowing capacity
MAX_BORROWING=0

# =============================================================================
# AI CONFIGURATION
# =============================================================================

# AI CLI command (supports qwen, ollama, custom endpoints)
QWEN_BIN="qwen"

# AI model parameters (adjust based on your AI tool)
AI_TEMPERATURE="0.7"
AI_MAX_TOKENS="2048"

# =============================================================================
# WORKFLOW CONFIGURATION
# =============================================================================

# Rest period between cycles (in seconds)
# Default: 14400 = 4 hours
REST_SECONDS=14400

# Enable single run mode (exit after one cycle)
WG_SINGLE_RUN=false

# Skip user confirmation (auto-execute)
WG_SKIP_WAIT=false

# =============================================================================
# UI CONFIGURATION
# =============================================================================

# Enable GUI mode (requires PyQt5)
USE_GUI=false

# Enable embedded app GUI
WORKGENERATOR_APP_GUI=false

# =============================================================================
# TECHNOLOGY PREFERENCES
# =============================================================================

# Preferred tech stack for implementations
TECH_STACK="Python, JavaScript, Shell, HTML/CSS"

# Target audience for your products
TARGET_AUDIENCE="Developers, creators, small teams"

# Focus areas (comma-separated)
FOCUS_AREA="developer tools, automation, content creation"

# =============================================================================
# GITHUB CONFIGURATION
# =============================================================================

# GitHub username (leave empty to auto-detect)
GITHUB_USERNAME=""

# Repositories to analyze (leave empty for all)
ANALYZE_REPOS=""

# Minimum stars for trend analysis
MIN_STARS=0

# =============================================================================
# EXECUTION CONFIGURATION
# =============================================================================

# Task runner (ralph, make, custom script, or empty for manual)
TASK_RUNNER=""

# Auto-push commits
AUTO_PUSH=true

# Auto-create pull requests
AUTO_PR=false

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

# Log level (DEBUG, INFO, WARN, ERROR)
LOG_LEVEL="INFO"

# Log file location
LOG_FILE="./workgenerator.log"

# Enable debug logging
DEBUG=false

# =============================================================================
# ADVANCED SETTINGS
# =============================================================================

# Retry attempts for AI calls
AI_RETRY_COUNT=3

# Retry delay (seconds)
AI_RETRY_DELAY=2

# Timeout for AI calls (seconds)
AI_TIMEOUT=120

# =============================================================================
# END OF CONFIGURATION
# =============================================================================
