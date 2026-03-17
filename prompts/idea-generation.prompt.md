# Idea Generation Prompt

```
Using gh CLI:

Goal: {{GOAL}}
Portfolio State:
{{PORTFOLIO_STATE}}
GitHub Analysis:
{{GITHUB_ANALYSIS}}

Generate ONE high-impact digital product idea (app, code library, tool, 
art, book, etc.) that leverages GitHub deployment and existing code tools.

Consider:
- Market fit and timing
- Technical feasibility with current stack
- Potential for revenue or value creation
- Alignment with user's goals and constraints

Format:
---
**PROJECT IDEA #{{ITERATION}}**

## Title
[2-4 word descriptive name]

## Description
[1-2 sentences describing the project]

## Why This Is A Good Idea
[Market fit, timing, unique advantages, potential impact]

## Implementation Overview
[High-level technical approach, key technologies]

## Estimated Impact
[Potential users, revenue, or value creation]

## Effort Required
[Time estimate: Low (< 1 week) / Medium (1-4 weeks) / High (> 1 month)]
---

Respond only with the formatted idea, nothing else.
```
