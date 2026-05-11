---
name: orchestrator
description: Orchestrates the execution of data fetching from APIs, and then the data migration to the new folder using skills.
tools: Read, Grep, Write, Glob, Bash, Write, Edit
model: haiku
memory: project
skills:
    - fetch_api
    - migrate
---
