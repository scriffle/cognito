# SEQUENTIAL GENERATION — MANDATORY

## The Rule

**Generate question files ONE AT A TIME. Never run multiple generation agents in parallel.**

Wait for each agent to finish and validate before launching the next.

## Why

Parallel agents hit API rate limits within minutes. When rate-limited mid-generation, the agent produces a partial JSON file that:

- Fails validation (Passed: 0/1)
- Contains truncated or missing question data
- Cannot be resumed — must be deleted and regenerated from scratch
- Wastes the entire token budget spent on that agent

This has happened three times across sessions, destroying 100+ files each time. The files look like they exist on disk but are incomplete garbage.

## The Correct Workflow

```
for each code in the batch:
    1. Launch ONE agent for that code
    2. Wait for it to complete
    3. Run: python3 questions/_validation/validate.py <file>
    4. Confirm Passed: 1/1
    5. Only then launch the next agent
```

## Batch Size

- **Maximum concurrent agents: 1**
- If the session has high token availability you may try 2, but never more
- If any agent fails with a rate limit error, drop back to 1 and add a pause between agents

## Recovery

If a file fails validation:
1. Delete it immediately — do not attempt to patch partial JSON
2. Regenerate from the skeleton file
3. Re-validate

## Anti-Drift Checklist

Before launching any generation agent, confirm:
- [ ] No other generation agent is currently running
- [ ] The previous file passed validation (Passed: 1/1)
- [ ] The skeleton file exists for the target code
- [ ] The output path does not already have a file (avoid overwrites)
