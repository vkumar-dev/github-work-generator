# AI Work Generator Framework - Prompts

This directory contains AI prompt templates used by the framework.

## Available Prompts

| Prompt | Description |
|--------|-------------|
| `github-analysis.prompt.md` | Analyzes GitHub repositories for opportunities |
| `idea-generation.prompt.md` | Generates project ideas based on analysis |
| `implementation-plan.prompt.md` | Creates executable task plans |

## Usage

Prompts are automatically loaded by `load-prompts.sh` and used throughout the framework.

### Customizing Prompts

1. Edit the prompt files to match your needs
2. Use template variables like `{{GOAL}}`, `{{PORTFOLIO_STATE}}`, etc.
3. Test changes with `WG_SINGLE_RUN=true ./workgenerator.sh`

### Template Variables

| Variable | Description |
|----------|-------------|
| `{{GOAL}}` | Your primary objective from config |
| `{{PORTFOLIO_STATE}}` | Current project/financial state |
| `{{GITHUB_ANALYSIS}}` | Output from GitHub analysis |
| `{{ITERATION}}` | Current cycle number |
| `{{IDEA}}` | Approved project idea |
| `{{USER_IMPROVEMENTS}}` | User refinement suggestions |

## Adding New Prompts

Create a new `.prompt.md` file and update `load-prompts.sh`:

```bash
# In load-prompts.sh
load_github_analysis_prompt() {
    cat "${PROMPTS_DIR}/github-analysis.prompt.md"
}
```

## Best Practices

- Keep prompts focused and specific
- Include clear output format requirements
- Use examples where helpful
- Test prompts with your AI tool of choice
