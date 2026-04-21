# Memory Bank - Universal Agent Rules

> This file applies to all AI coding agents working on this project.
> Read this file and all files under `docs/memory-bank/` at the start of every session.

## File Structure

| File | Purpose |
|------|---------|
| `RULES.md` | This file - rules (immutable, do not modify) |
| `projectbrief.md` | Project scope, vision, requirements |
| `productContext.md` | Product context, user flows, UX decisions |
| `systemPatterns.md` | Architecture, design patterns, technical decisions |
| `techContext.md` | Tech stack, dependencies, dev environment |
| `activeContext.md` | Active work, recent changes, current decisions |
| `progress.md` | Completed work, in-progress items, known issues |

## Supplemental Files

These files are maintained as supporting project context and planning history:

| File | Purpose |
|------|---------|
| `decisionLog.md` | Historical architecture and implementation decisions |
| `roadmap.md` | Forward-looking planning and milestone tracking |

## Required Protocols

### Session Start
1. Check that `docs/memory-bank/` directory exists
2. Read ALL `.md` files in `docs/memory-bank/`
3. Understand active work from `activeContext.md`
4. Understand current status from `progress.md`

### Update Triggers

| Event | File(s) to Update |
|-------|-------------------|
| Feature completed | `activeContext.md` + `progress.md` |
| Architecture decision made | `systemPatterns.md` |
| New dependency added | `techContext.md` |
| Bug fix / error resolved | `activeContext.md` |
| User preference learned | `activeContext.md` |
| Branch / task changed | `activeContext.md` |

### Session End
1. What changed in this session?
2. What decisions were made?
3. What are the next steps?
4. Ask the user: "Should I update the memory bank?"

## Update Rules
- **DO NOT** modify `RULES.md` - ever
- **DO NOT** modify `projectbrief.md` unless the user explicitly asks
- **DO NOT** write sensitive information (API keys, passwords, tokens) to any file
- Use date stamps: `[YYYY-MM-DD]`
- Keep each file under 500 lines
- Do not duplicate information across files

## Commands

| Command | Action |
|---------|--------|
| `memory bank update` / `memory bank güncelle` | Review and update ALL memory bank files |
| `memory bank status` / `memory bank durumu` | Show current status summary |
| `memory bank read` / `memory bank oku` | Read all files and present full context |
