# AI Work Generator Framework - Prompt Loader
# Sources all prompt templates for use in the main script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPTS_DIR="${SCRIPT_DIR}/prompts"

# Load prompt templates
load_prompt() {
    local prompt_name="$1"
    local prompt_file="${PROMPTS_DIR}/${prompt_name}.prompt.md"
    
    if [[ -f "$prompt_file" ]]; then
        cat "$prompt_file"
    else
        echo "Prompt file not found: $prompt_file" >&2
        echo ""
    fi
}

# Export for use in other scripts
export -f load_prompt
export PROMPTS_DIR
