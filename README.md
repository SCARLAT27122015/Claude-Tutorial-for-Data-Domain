# Lessons Learned: Claude Code Masterclass (Data Domain Edition)

This repository documents the key technical takeaways and hands-on practices implemented while following the Claude Code course. The focus was on transitioning from standard LLM interactions to **agentic workflows** within a terminal-native environment.

## 🚀 Core Concepts & Takeaways

### 1. Terminal-Native Agentic AI
Unlike web-based LLMs, Claude Code operates directly within the shell. This provides the "hands" necessary to interact with the local operating system, execute commands, and manage files without manual intervention.
*   **Practice:** Set up a dedicated environment (e.g., EC2/local) to allow Claude to perform full-cycle development—from file creation to execution—using its built-in toolset.

### 2. Claude Agentic Architecture & Sub-Agents
Claude Code is an orchestration of the Claude model combined with advanced system tools. It enables "Agentic Behavior," where the AI doesn't just suggest code but executes the plan.
*   **Practice:** Experimented with building **sub-agents** to delegate complex, multi-step tasks. Instead of providing single prompts, I assigned high-level objectives (e.g., "Build a PySpark pipeline and organize it into a specific folder structure") and observed the agent handle the directory creation and file generation autonomously.

### 3. Skills & Skills 2.0
Skills are the mechanism for extending Claude's capabilities. While standard skills cover basic file operations, **Skills 2.0** and customized skills allow for project-specific automation and standardization.
*   **Practice:** Defined custom instructions and reusable logic within the `.claude.md` configuration file. This ensures that the agent adheres to specific coding standards and project architectures (like Data Engineering best practices) consistently.

### 4. Model Context Protocol (MCP)
MCP is a game-changer for data-heavy workflows. It allows Claude Code to connect to external data sources and tools via local or hosted servers, providing the model with "eyes" into specific datasets.
*   **Practice:** Configured and connected to **MCP servers**. This enabled the agent to query data and access specialized tools (like SQL databases or local file indexers) as part of its reasoning process.

### 5. Automated Hooks
Hooks allow for the execution of scripts based on specific events (e.g., before or after a tool call) without requiring LLM tokens for the execution itself.
*   **Practice:** Implemented **pre-scripts and post-scripts**. Specifically, I practiced creating hooks for automated notifications and logging, ensuring that every time a script was generated or a test failed, a local notification was triggered.

## 🛠 Summary of Hands-on Exercises
*   **Architecture Mapping:** Visualized the flow between the LLM, the Claude Code tools, and the terminal.
*   **Automation Pipeline:** Built a workflow where Claude Code manages the lifecycle of a Python/PySpark script using hooks.
*   **Context Integration:** Successfully linked local MCP servers to provide domain-specific context to the agent.

IMPORTANT: Create a .env file with your anthropic API key and set the environment variable `ANTHROPIC_API_KEY` to enable the agentic features of Claude Code.


---


*Based on the Claude Code Course by Ansh Lamba.*