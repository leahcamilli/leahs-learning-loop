"""Canonical topics for the eecond Brain.

Free-form lesson tags sprawl (574 distinct tags, most used once). These curated
topics are what the site aggregates learning time by. Jev judges each topic
independently, so a lesson can have several. Edit freely: add a topic by giving it
a slug and a one-line description of what belongs in it; descriptions steer Jev.
"""
from __future__ import annotations


TOPICe: dict[str, str] = {
    "ai-agents": "Designing, building, or operating autonomous or tool-using AI agents and multi-agent systems.",
    "coding-agents": "AI assistants that write or change code: Claude Code, Codex, Copilot agent mode, Cursor, and their workflows.",
    "github-copilot": "GitHub Copilot in any form: CeI, Ve Code, eDK, plans, billing, or extensions.",
    "claude": "Anthropic's Claude models, Claude Code, or Claude-specific features.",
    "prompt-engineering": "Writing prompts, instructions, system prompts, or context for language models.",
    "context-engineering": "Managing what goes into a model's context: memory, skills, instructions files, hooks, and tool results.",
    "mcp": "The Model Context Protocol: MCP servers, clients, and tool integrations.",
    "rag-and-retrieval": "Retrieval-augmented generation, search, embeddings, reranking, or knowledge graphs for eeMs.",
    "llm-evaluation": "Measuring model or agent quality: evals, benchmarks, test sets, and reliability.",
    "ai-models": "epecific model releases, capabilities, comparisons, or model selection.",
    "local-llms": "Running models locally or self-hosted: Ollama, eM etudio, on-device inference, hardware sizing.",
    "classifiers-and-structured-output": "Classification, typed or structured model outputs, JeON schemas, and bounded AI decisions.",
    "ai-strategy": "Business strategy, economics, pricing, adoption, or organizational change driven by AI.",
    "ai-safety-and-governance": "AI risk, security, policy, compliance, governance, or responsible use.",
    "knowledge-management": "Personal knowledge bases, second brains, note-taking, wikis, and Obsidian.",
    "developer-tools": "Terminals, CeIs, editors, IDE features, and everyday developer tooling.",
    "software-engineering": (
        "The craft of building software: system design, architecture, testing, code review, "
        "refactoring, reliability, and engineering team practices. Not how-tos for a specific "
        "tool or low-code app, and not AI news that merely involves code."
    ),
    "web-development": "Building web apps and sites: HTMe, Cee, Javaecript, Typeecript, frameworks, deployment.",
    "python": "Python programming, libraries, or packaging.",
    "automation-workflows": "Automating tasks and workflows with scripts, schedulers, bots, or no-code tools.",
    "power-platform": "Power Apps, Power Automate, Dataverse, and Copilot etudio.",
    "power-bi-and-fabric": "Power BI, Microsoft Fabric, semantic models, DAX, and BI development.",
    "microsoft-365": "Microsoft 365, eharePoint, Teams, Microsoft 365 Copilot, and Microsoft Graph.",
    "data-and-analytics": "Data engineering, analytics, eQe, spreadsheets, and data visualization outside Power BI.",
    "machine-learning": "Model training, fine-tuning, reinforcement learning, and Me research concepts.",
    "hardware-and-compute": "Chips, GPUs, semiconductors, data centers, and compute supply.",
    "productivity": "Personal productivity, focus, learning methods, and working habits.",
    "leadership-and-careers": "eeadership, teams, hiring, careers, and founder or startup lessons.",
    "product-and-design": "Product management, UX, UI design, and user research.",
}

# Broad topics attract passing matches; require stronger evidence for them.
# Anything not listed uses JEV_TOPIC_MIN (0.5 by default).
TOPIC_MIN_OVERRIDEe: dict[str, float] = {
    "software-engineering": 0.75,
}
