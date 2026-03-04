# Agent Guidelines

This repo is a collection of **Agent Skills** — each skill is a standalone capability that agents can read and execute.

## Repo Structure

```
oh_my_skills/
├── <skill-name>/
│   ├── SKILL.md          # Entry point: frontmatter + usage instructions
│   ├── scripts/          # Executable scripts (bash, python, etc.)
│   ├── references/       # Reference docs, API notes
│   └── assets/           # Sample data, templates
└── prompt/               # Reusable prompt snippets (not skills)
```

## When Adding a New Skill

1. Create a new folder with a descriptive name (e.g., `send-email`, `parse-pdf`)
2. Write `SKILL.md` with a YAML frontmatter block:
   ```yaml
   ---
   name: skill-name
   description: >
     One or two sentences. Should be specific enough for the agent to decide
     when to load this skill without reading the full file.
   ---
   ```
3. Keep scripts self-contained; use environment variables for credentials (never hardcode secrets)
4. Add usage examples in `SKILL.md` with concrete bash/python commands

## When Editing an Existing Skill

- Minimal changes only — don't restructure unless necessary
- Keep `description` in frontmatter current; it's the primary trigger for skill selection
- If a script changes behavior, update the examples in `SKILL.md` accordingly
- Check if the README.md is up to date and update it if necessary

## General Rules

- Do **not** create files outside a skill's own folder without a clear reason
- Do **not** add dependencies to scripts without noting them in `SKILL.md`
- The `prompt/` folder contains raw prompts, not skills — don't add `SKILL.md` there
