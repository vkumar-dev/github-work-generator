#!/bin/bash
# AI Work Generator Framework - Main Script
# Analyzes GitHub projects, generates ideas, and automates execution
#
# Usage:
#   ./workgenerator.sh                    # Terminal mode
#   USE_GUI=true ./workgenerator.sh       # GUI mode
#   WORKGENERATOR_APP_GUI=true ./workgenerator.sh  # App GUI mode
#   WG_SINGLE_RUN=true ./workgenerator.sh # Single run

set +e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Load configuration
if [[ -f "${SCRIPT_DIR}/config.sh" ]]; then
    source "${SCRIPT_DIR}/config.sh"
fi

# Default values (can be overridden by config.sh)
USE_GUI="${USE_GUI:-false}"
WORKGENERATOR_APP_GUI="${WORKGENERATOR_APP_GUI:-false}"
QWEN_BIN="${QWEN_BIN:-qwen}"
WG_SINGLE_RUN="${WG_SINGLE_RUN:-false}"
WG_SKIP_WAIT="${WG_SKIP_WAIT:-false}"
REST_SECONDS="${REST_SECONDS:-14400}"
GOAL="${GOAL:-Create impactful digital products}"
LOG_FILE="${LOG_FILE:-${SCRIPT_DIR}/workgenerator.log}"

# Initialize log file
> "$LOG_FILE"
exec > >(tee -a "$LOG_FILE") 2>&1

# Colors for terminal output
if [[ "$WORKGENERATOR_APP_GUI" == "true" ]]; then
    RED='' GREEN='' YELLOW='' BLUE='' CYAN='' WHITE='' MAGENTA='' NC='' BOLD=''
else
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    CYAN='\033[0;36m'
    WHITE='\033[1;37m'
    MAGENTA='\033[0;35m'
    NC='\033[0m'
    BOLD='\033[1m'
fi

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

header() {
    echo -e "${CYAN}${BOLD}$(printf '═%.0s' {1..75})${NC}"
    echo -e "  $1${NC}"
    echo -e "${CYAN}${BOLD}$(printf '═%.0s' {1..75})${NC}"
}

info() { echo -e "${BLUE}[INFO]${NC} $1" >&2; }
step() { echo -e "${CYAN}→${NC} $1" >&2; }
success() { echo -e "${GREEN}✓${NC} $1" >&2; }
error() { echo -e "${RED}✗${NC} $1" >&2; }
warn() { echo -e "${YELLOW}⚠${NC} $1" >&2; }

# =============================================================================
# INITIALIZATION
# =============================================================================

init_runtime_env() {
    # Load NVM if available
    if [[ -s "$HOME/.nvm/nvm.sh" ]]; then
        source "$HOME/.nvm/nvm.sh" >/dev/null 2>&1
    fi
    
    # Load Rust/Cargo if available
    if [[ -s "$HOME/.cargo/env" ]]; then
        source "$HOME/.cargo/env" >/dev/null 2>&1
    fi
}

resolve_ai_tool() {
    if command -v "$QWEN_BIN" >/dev/null 2>&1; then
        QWEN_BIN="$(command -v "$QWEN_BIN")"
        return 0
    fi

    # Fallback to qwen-code if qwen is specified
    if [[ "$QWEN_BIN" == "qwen" ]] && command -v qwen-code >/dev/null 2>&1; then
        QWEN_BIN="$(command -v qwen-code)"
        return 0
    fi

    return 1
}

check_dependencies() {
    local missing=()

    if ! command -v gh >/dev/null 2>&1; then
        missing+=("gh (GitHub CLI)")
    fi

    if [[ ${#missing[@]} -gt 0 ]]; then
        error "Missing dependencies: ${missing[*]}"
        echo ""
        echo "Install GitHub CLI: https://cli.github.com/"
        return 1
    fi

    if ! gh auth status >/dev/null 2>&1; then
        error "GitHub CLI not authenticated"
        echo ""
        echo "Run: gh auth login"
        return 1
    fi

    if ! resolve_ai_tool; then
        warn "AI tool '$QWEN_BIN' not found. Install or configure QWEN_BIN."
    fi

    return 0
}

# =============================================================================
# PORTFOLIO STATE
# =============================================================================

load_portfolio_state() {
    local portfolio_file="${SCRIPT_DIR}/portfolio-state.md"
    
    if [[ -f "$portfolio_file" ]]; then
        cat "$portfolio_file"
    else
        cat <<'EOF'
Portfolio State
===============

Financial Context:
- Available capital: ${{AVAILABLE_CAPITAL:-0}}
- Emergency fund: ${{EMERGENCY_FUND:-0}}
- Borrowing capacity: ${{MAX_BORROWING:-0}}

Constraints:
- Prefer ideas that can start with zero or minimal spend
- Focus on digital products (apps, tools, libraries, content)
- Leverage existing skills and technology stack

Technology Stack:
- Primary: ${TECH_STACK:-Python, JavaScript, Shell}

Target Audience:
- ${TARGET_AUDIENCE:-Developers, creators, small teams}
EOF
    fi
}

# =============================================================================
# GITHUB ANALYSIS
# =============================================================================

analyze_github() {
    header "GitHub Analysis"
    step "Fetching repository data..."

    local repos
    repos=$(gh repo list --limit 100 --json name,description,starCount,forkCount,updatedAt,primaryLanguage,isPrivate 2>/dev/null)

    if [[ -z "$repos" ]]; then
        error "Failed to fetch repository data"
        return 1
    fi

    step "Analyzing traffic and trends..."

    # Generate analysis summary
    cat <<EOF
GitHub Repository Analysis
==========================

$(echo "$repos" | jq -r '.[] | "- \(.name): \(.starCount // 0) ⭐, \(.forkCount // 0) 🔱, \(.primaryLanguage.name // "Unknown")"' 2>/dev/null || echo "No repositories found")

Focus Areas:
- High-traffic repositories for improvement opportunities
- Under-maintained projects with potential
- Technology gaps in current portfolio
- Trending topics in your domain

EOF

    echo "$repos"
}

# =============================================================================
# AI IDEA GENERATION
# =============================================================================

generate_idea() {
    local github_analysis="$1"
    local iteration="${2:-1}"
    
    step "Generating idea #${iteration}..."

    # Load prompts
    source "${SCRIPT_DIR}/prompts/load-prompts.sh" 2>/dev/null || true

    local portfolio_state
    portfolio_state=$(load_portfolio_state)

    # Create prompt for AI
    local prompt
    prompt=$(cat <<EOF
Using GitHub CLI and AI analysis:

Goal: ${GOAL}

Portfolio State:
${portfolio_state}

GitHub Analysis:
${github_analysis}

Generate ONE high-impact digital product idea (app, code library, tool, art, book, etc.) 
that leverages GitHub deployment and existing code tools.

Format your response as:
---
**PROJECT IDEA #${iteration}**

## Title
[2-4 word name]

## Description
[1-2 sentences describing the project]

## Why This Is A Good Idea
[Market fit, timing, unique advantages]

## Implementation Overview
[High-level technical approach]

## Estimated Impact
[Potential users, revenue, or value]

## Effort Required
[Time estimate: Low/Medium/High]
---

Respond only with the formatted idea, nothing else.
EOF
)

    # Call AI tool
    local response
    if command -v "$QWEN_BIN" >/dev/null 2>&1; then
        response=$(echo "$prompt" | "$QWEN_BIN" -y 2>/dev/null)
    else
        # Fallback: generate template
        response=$(cat <<EOF
---
**PROJECT IDEA #${iteration}**

## Title
[AI Tool Not Available - Manual Input]

## Description
Configure QWEN_BIN in config.sh to enable AI idea generation.

## Why This Is A Good Idea
Manual idea entry mode.

## Implementation Overview
User-defined implementation plan.

## Estimated Impact
To be determined.

## Effort Required
To be determined.
---
EOF
)
    fi

    echo "$response"
}

# =============================================================================
# USER DECISION INTERFACE
# =============================================================================

get_user_decision() {
    local idea="$1"
    
    echo ""
    header "Decision Time"
    echo ""
    echo "$idea"
    echo ""
    echo -e "${CYAN}${BOLD}Options:${NC}"
    echo "  [Y] Yes     - Execute this idea"
    echo "  [N] No      - Skip and generate new idea"
    echo "  [P] Pass    - Skip for now, try again later"
    echo "  [I] Improve - Refine idea with user input"
    echo "  [Q] Quit    - Exit the program"
    echo ""

    if [[ "$WG_SKIP_WAIT" == "true" ]]; then
        info "Auto-skipping (WG_SKIP_WAIT=true)"
        echo "pass"
        return
    fi

    local choice
    read -p "Your choice (Y/N/P/I/Q): " -n 1 -r choice
    echo ""

    case $choice in
        [Yy]) echo "yes" ;;
        [Nn]) echo "no" ;;
        [Pp]) echo "pass" ;;
        [Ii]) echo "improve" ;;
        [Qq]) echo "quit" ;;
        *) echo "invalid" ;;
    esac
}

get_user_improvements() {
    echo ""
    header "Improve Idea"
    echo ""
    echo "Enter your suggestions (press Enter twice to finish):"
    echo ""

    local improvements=""
    local line
    while IFS= read -r line; do
        [[ -z "$line" ]] && break
        improvements="${improvements}${line}"$'\n'
    done

    echo "$improvements"
}

# =============================================================================
# IMPLEMENTATION PLANNING
# =============================================================================

generate_plan() {
    local idea="$1"
    local improvements="$2"

    step "Generating implementation plan..."

    local prompt
    if [[ -n "$improvements" ]]; then
        prompt=$(cat <<EOF
Create a detailed implementation plan for:

${idea}

User Improvements:
${improvements}

Break down into executable tasks with:
- Task description
- Estimated time
- Dependencies
- Success criteria

Format as JSON array of tasks.
EOF
)
    else
        prompt=$(cat <<EOF
Create a detailed implementation plan for:

${idea}

Break down into executable tasks with:
- Task description
- Estimated time
- Dependencies
- Success criteria

Format as JSON array of tasks.
EOF
)
    fi

    # Call AI tool for planning
    if command -v "$QWEN_BIN" >/dev/null 2>&1; then
        echo "$prompt" | "$QWEN_BIN" -y 2>/dev/null
    else
        echo '[]'
    fi
}

# =============================================================================
# EXECUTION
# =============================================================================

execute_plan() {
    local plan="$1"

    header "Execution"
    step "Starting implementation..."

    if [[ -n "$TASK_RUNNER" ]] && command -v "$TASK_RUNNER" >/dev/null 2>&1; then
        info "Using task runner: $TASK_RUNNER"
        # Execute via task runner
        echo "$plan" | "$TASK_RUNNER"
    else
        info "No task runner configured. Plan saved for manual execution."
        echo "$plan" > "${SCRIPT_DIR}/.pending_tasks.json"
        success "Plan saved to .pending_tasks.json"
    fi
}

# =============================================================================
# STATE MANAGEMENT
# =============================================================================

save_state() {
    local iteration="$1"
    local idea="$2"
    local status="$3"

    local state_file="${SCRIPT_DIR}/.workgenerator_config"
    
    cat > "$state_file" <<EOF
iteration=${iteration}
last_idea_timestamp=$(date +%s)
last_status=${status}
EOF

    # Log idea
    local idea_log="${SCRIPT_DIR}/.ideas_log.json"
    echo "{\"iteration\": ${iteration}, \"timestamp\": $(date +%s), \"status\": \"${status}\", \"idea\": $(echo "$idea" | jq -Rs '.' 2>/dev/null || echo '""')}" >> "$idea_log"
}

load_state() {
    local state_file="${SCRIPT_DIR}/.workgenerator_config"
    
    if [[ -f "$state_file" ]]; then
        source "$state_file"
        echo "${iteration:-0}"
    else
        echo "0"
    fi
}

# =============================================================================
# MAIN LOOP
# =============================================================================

main_loop() {
    header "AI Work Generator Framework"
    info "Goal: ${GOAL}"
    info "Rest period: ${REST_SECONDS}s between cycles"
    echo ""

    # Check dependencies
    if ! check_dependencies; then
        error "Dependency check failed. Please install required tools."
        exit 1
    fi

    success "All dependencies OK"
    echo ""

    local iteration
    iteration=$(($(load_state) + 1))

    while true; do
        header "Cycle #${iteration}"

        # Step 1: GitHub Analysis
        local github_analysis
        github_analysis=$(analyze_github)

        # Step 2: Generate Idea
        local idea
        idea=$(generate_idea "$github_analysis" "$iteration")

        # Step 3: Get User Decision
        local decision
        decision=$(get_user_decision "$idea")

        case $decision in
            yes)
                success "Idea approved!"
                local plan
                plan=$(generate_plan "$idea" "")
                execute_plan "$plan"
                save_state "$iteration" "$idea" "approved"
                ;;
            no)
                warn "Idea rejected"
                save_state "$iteration" "$idea" "rejected"
                ;;
            pass)
                info "Skipping for now"
                save_state "$iteration" "$idea" "passed"
                ;;
            improve)
                local improvements
                improvements=$(get_user_improvements)
                success "Generating refined plan..."
                local plan
                plan=$(generate_plan "$idea" "$improvements")
                execute_plan "$plan"
                save_state "$iteration" "$idea" "improved"
                ;;
            quit)
                info "Exiting..."
                save_state "$iteration" "$idea" "quit"
                exit 0
                ;;
            *)
                warn "Invalid choice"
                ;;
        esac

        # Single run mode
        if [[ "$WG_SINGLE_RUN" == "true" ]]; then
            info "Single run mode - exiting"
            exit 0
        fi

        # Rest period
        info "Resting for ${REST_SECONDS} seconds..."
        sleep "$REST_SECONDS"

        iteration=$((iteration + 1))
    done
}

# =============================================================================
# ENTRY POINT
# =============================================================================

# Initialize
init_runtime_env

# Check for GUI mode
if [[ "$USE_GUI" == "true" ]]; then
    if [[ -f "${SCRIPT_DIR}/workgenerator-desktop.py" ]]; then
        python3 "${SCRIPT_DIR}/workgenerator-desktop.py"
        exit $?
    else
        warn "GUI script not found. Falling back to terminal mode."
    fi
fi

# Check for App GUI mode
if [[ "$WORKGENERATOR_APP_GUI" == "true" ]]; then
    if [[ -f "${SCRIPT_DIR}/workgenerator-desktop.py" ]]; then
        python3 "${SCRIPT_DIR}/workgenerator-desktop.py"
        exit $?
    else
        warn "GUI script not found. Falling back to terminal mode."
    fi
fi

# Run main loop
main_loop
