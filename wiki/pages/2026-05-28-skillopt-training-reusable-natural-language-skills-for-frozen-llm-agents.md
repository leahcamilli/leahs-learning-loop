---
title: "SkillOpt: Training Reusable Natural-Language Skills for Frozen LLM Agents"
source: "https://github.com/microsoft/SkillOpt"
date: "2026-05-28"
tags: [llm, agents, prompt-optimization, python, evaluation, training-loops]
source_type: "github"
topics: [ai-agents, prompt-engineering, machine-learning]
kind: "deep-dive"
depth: 3
actionability: 2
---

## TL;DR

> SkillOpt improves frozen LLM agents by iteratively rewriting a reusable natural-language skill, validating each candidate, and saving the best version instead of changing model weights. This brings training-loop discipline—rollouts, feedback, gating, and checkpoints—to prompt and behavior optimization across hosted or closed-weight models.

## Key Takeaways

1. Treat the skill document as the learned artifact: SkillOpt produces a deployable `best_skill.md`, not a model checkpoint.
2. Use task trajectories to generate textual update signals; reflection analyzes successes, failures, and execution traces before the optimizer proposes revisions.
3. Gate candidate revisions on validation data so batch-specific improvements do not automatically replace the current or best skill.
4. Separate the frozen target model from the optimizer model; one executes tasks under the skill, while the other analyzes trajectories and proposes or ranks edits.
5. Implement benchmark-specific semantics in `skillopt/envs/<benchmark>/`—typically through `dataloader.py`, `adapter.py`, `rollout.py`, `evaluator.py` or `reflect.py`, and `skills/initial.md`—while reusing the common training engine.
6. Inspect `history.json`, versioned skill snapshots, step outputs, and `runtime_state.json` to compare experiments, diagnose updates, and resume interrupted runs.
7. Verify an experiment by diffing the benchmark's `initial.md` against `best_skill.md`, then evaluating the saved skill separately with `scripts/eval_only.py`.

## Overview

SkillOpt is a Python framework for improving LLM-based agents without fine-tuning model weights. Instead of updating parameters, it iteratively edits a natural-language skill document, evaluates the new behavior on task trajectories, and keeps only changes that pass validation gates. The result is a deployable `best_skill.md` artifact that can be reused with the same frozen model across future runs.

This matters for engineers building production agents who want some of the discipline of ML training loops—epochs, batching, scheduling, validation, checkpointing—but in prompt and behavior space rather than weight space. SkillOpt is especially relevant if you operate on proprietary APIs, use multiple model backends, or need benchmark-specific agent logic while preserving a common optimization pipeline.

## Key Concepts

- **Text-space optimization**: SkillOpt treats an agent's natural-language instruction document as the object being optimized. Instead of changing model weights, it rewrites and refines the skill text using task rollouts and feedback derived from agent trajectories. This makes optimization portable across closed-weight and hosted models.
- **Trajectory-driven reflection**: The system runs the target agent on benchmark tasks and records successes, failures, and execution traces. Reflection modules analyze these trajectories to infer what the current skill is missing or doing poorly. Those observations become the raw material for candidate skill updates.
- **Validation-gated updates**: SkillOpt does not accept every proposed rewrite. Candidate skill revisions are evaluated on validation data, and only improvements that meet gating criteria are promoted to the current or best skill. This reduces overfitting to the training batch and makes the optimization loop behave more like model selection in conventional ML.
- **Benchmark adapters and environments**: Each supported task domain—such as SearchQA, ALFWorld, DocVQA, OfficeQA, or SpreadsheetBench—implements its own adapter, dataloader, rollout, and often evaluator or reflection logic. This lets the framework keep a common optimization engine while handling domain-specific prompts, action formats, and scoring.
- **Optimizer stack for skill updates**: The optimizer package contains mechanisms such as rewrite, selection, clipping, scheduling, meta-skill generation, and slow updates. Together, these decide how many edits to propose, how aggressively to change the current skill, and when to synthesize broader strategy updates from accumulated evidence.
- **Artifact-centric training runs**: A run produces structured artifacts including `history.json`, per-step outputs, checkpoint state, versioned skill snapshots, and the final `best_skill.md`. This makes experiments resumable, inspectable, and easier to compare than ad hoc prompt tinkering.

## How It Works

SkillOpt is organized around a central training engine plus benchmark-specific environment modules.

At the top level, the entry points are `scripts/train.py` and `scripts/eval_only.py`. Training loads a YAML benchmark config from `configs/<benchmark>/default.yaml`, resolves CLI overrides such as model names and data split directory, and initializes the optimization loop. Evaluation-only mode skips optimization and applies an existing skill document to one or more dataset splits.

The core package structure is roughly:

- `skillopt/engine/trainer.py`: orchestrates the end-to-end training loop.
- `skillopt/config.py`: loads and flattens runtime configuration.
- `skillopt/model/`: abstracts model backends such as Azure OpenAI, OpenAI/Codex-style, Claude, and local Qwen via vLLM.
- `skillopt/envs/<benchmark>/`: benchmark-specific data loading, prompt adaptation, rollout execution, evaluation, and sometimes reflection logic.
- `skillopt/gradient/`: derives update signals from trajectories, including reflection and aggregation.
- `skillopt/optimizer/`: turns feedback into edited skill documents, applies scheduling and clipping, and manages update modes like slow updates or meta-skills.
- `skillopt/evaluation/gate.py`: implements the logic that decides whether a candidate skill should be accepted.

A typical data flow during training looks like this:

1. **Load config and dataset split**
   - Training expects `train/`, `val/`, and `test/` directories under a split root.
   - Each benchmark's `dataloader.py` defines the exact JSON schema it expects.

2. **Initialize the environment adapter**
   - The selected benchmark module converts raw task items into prompts, tool calls, or action spaces appropriate for that domain.
   - For example, SearchQA and DocVQA are mostly QA-style rollouts, while ALFWorld and SpreadsheetBench involve more complex interaction loops.

3. **Start from an initial skill document**
   - Most environments ship an initial skill under `skillopt/envs/<benchmark>/skills/initial.md`.
   - This file is the current policy-like instruction set for the frozen target model.

4. **Run rollouts on training items**
   - The environment's `rollout.py` executes tasks using the current skill plus benchmark prompts.
   - Some environments also have `reflect.py` modules that produce richer task-specific feedback from trajectories.

5. **Aggregate failure/success signals into edit proposals**
   - `skillopt/gradient/reflect.py` and `skillopt/gradient/aggregate.py` help transform traces into textual guidance.
   - The optimizer then uses prompt templates in `skillopt/prompts/`—such as analyst, merge, ranking, and rewrite prompts—to draft candidate skill modifications.

6. **Apply optimization controls**
   - Modules like `optimizer/rewrite.py`, `select.py`, `clip.py`, and `scheduler.py` control how edits are proposed and constrained.
   - `lr_autonomous.py` suggests there is a learned or model-guided notion of learning-rate-like step sizing in text space.
   - `slow_update.py` and `meta_skill.py` add higher-level consolidation passes over accumulated experience.

7. **Validate and gate**
   - Candidate skill revisions are evaluated on validation data.
   - `evaluation/gate.py` decides whether the new skill should replace the current one and whether it becomes the best-known skill artifact.

8. **Persist artifacts and resume state**
   - Each step writes snapshots into `outputs/<run_name>/skills/` and detailed step artifacts into `outputs/<run_name>/steps/step_XXXX/`.
   - `runtime_state.json` supports resuming interrupted runs.
   - `history.json` records step-wise training progress.

The model backend layer is important because SkillOpt separates the **optimizer model** from the **target model**. The target model is the frozen agent being improved through better skill text. The optimizer model is the model that analyzes trajectories, ranks edits, and proposes rewrites. In practice, they may be the same deployment, but the architecture allows them to differ.

Benchmark code follows a clear pattern. For example, a benchmark folder often contains:

- `adapter.py`: transforms task items and runtime context into the benchmark-specific prompt/interaction format.
- `dataloader.py`: loads and normalizes JSON task items.
- `rollout.py`: executes inference or multi-step agent interaction.
- `evaluator.py`: scores the final answer or behavior.
- `reflect.py`: generates domain-specific diagnostic feedback when generic reflection is insufficient.
- `prompts/`: benchmark-local prompt templates layered on top of framework-global prompts.
- `skills/initial.md`: seed skill document.

This design is especially visible in environments like SpreadsheetBench, which includes `codegen_agent.py`, `react_agent.py`, and `executor.py`. That indicates the benchmark is not just single-turn generation; it may synthesize code, run it, and score outcomes, while SkillOpt still optimizes the instruction document guiding those agents.

The WebUI in `skillopt_webui/app.py` is optional but useful for monitoring runs. It sits beside the training system rather than inside it, reading the generated artifacts to visualize progress. That reinforces the repository's experiment-driven workflow: run training, inspect step outputs, compare skill versions, and deploy the best validated skill file.

A practical mental model is: **SkillOpt is an MLOps-style trainer for prompts/skills**. The dataset lives in JSON splits, environment code defines task semantics, rollouts generate trajectories, reflection converts them into textual gradients, optimizer modules rewrite the skill, validation gates prevent regressions, and the output is a versioned markdown skill file rather than updated neural weights.

## Training Exercise

Run a minimal end-to-end experiment on a tiny SearchQA-style dataset, inspect the generated artifacts, and verify that SkillOpt is optimizing a skill document rather than a model checkpoint.

1. **Install and configure**

```bash
git clone https://github.com/microsoft/SkillOpt.git
cd SkillOpt
pip install -e .
cp .env.example .env
source .env
```

Set one backend, for example Azure OpenAI:

```bash
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_API_KEY="your-key"
```

2. **Create a tiny dataset split**

```bash
mkdir -p data/searchqa_tiny/{train,val,test}
```

Create `data/searchqa_tiny/train/items.json`:

```json
[
  {
    "id": "q1",
    "question": "Who wrote Pride and Prejudice?",
    "context": "[DOC] Pride and Prejudice is a novel by Jane Austen.",
    "answers": ["Jane Austen"]
  },
  {
    "id": "q2",
    "question": "What planet is known as the Red Planet?",
    "context": "[DOC] Mars is often called the Red Planet.",
    "answers": ["Mars"]
  }
]
```

Copy similar files to validation and test:

```bash
cp data/searchqa_tiny/train/items.json data/searchqa_tiny/val/items.json
cp data/searchqa_tiny/train/items.json data/searchqa_tiny/test/items.json
```

3. **Run a short training job**

```bash
python scripts/train.py \
  --config configs/searchqa/default.yaml \
  --split_dir data/searchqa_tiny \
  --azure_openai_endpoint "$AZURE_OPENAI_ENDPOINT" \
  --optimizer_model gpt-5.5 \
  --target_model gpt-5.5 \
  --num_epochs 1 \
  --batch_size 2 \
  --workers 1 \
  --out_root outputs/searchqa_tiny_run
```

4. **Inspect the output structure**

Look at the produced files:

```bash
find outputs/searchqa_tiny_run -maxdepth 3 -type f | sort
```

Focus on these artifacts:

- `best_skill.md`
- `history.json`
- `skills/skill_vXXXX.md`
- `steps/step_XXXX/...`

5. **Compare initial and optimized skills**

Open the benchmark's seed skill and the generated best skill:

```bash
diff -u skillopt/envs/searchqa/skills/initial.md outputs/searchqa_tiny_run/best_skill.md || true
```

Write down:
- What instructions were added or removed?
- Do the changes target answer formatting, evidence use, or error avoidance?
- Does the edit seem grounded in the training examples?

6. **Run evaluation-only on the saved skill**

```bash
python scripts/eval_only.py \
  --config configs/searchqa/default.yaml \
  --skill outputs/searchqa_tiny_run/best_skill.md \
  --split all \
  --split_dir data/searchqa_tiny \
  --azure_openai_endpoint "$AZURE_OPENAI_ENDPOINT"
```

7. **Extension exercise: add a new benchmark field mapping**

Open `skillopt/envs/searchqa/dataloader.py` and inspect how it expects items to be structured. Then modify your dataset to include one malformed example and observe where loading or rollout fails. This is a good way to understand the boundary between generic training logic and benchmark-specific environment code.

8. **Reflection question**

After the run, answer: if you wanted to support a new benchmark, which files would you need first?

A strong answer should mention at least:
- `configs/<benchmark>/default.yaml`
- `skillopt/envs/<benchmark>/dataloader.py`
- `adapter.py`
- `rollout.py`
- `evaluator.py` or `reflect.py`
- `skills/initial.md`

The goal of this exercise is not just to run the tool, but to observe that the primary learned artifact is a markdown skill document, backed by validation and experiment traces.

## Test Yourself

<details><summary>What does SkillOpt optimize, and what artifact does a successful run produce?</summary>

It optimizes a natural-language skill document while leaving the target model's weights frozen. The primary deployable artifact is the best validation-approved version saved as `best_skill.md`.

</details>

<details><summary>Why does SkillOpt evaluate proposed skill rewrites on validation data before accepting them?</summary>

Validation gating helps prevent a rewrite that merely fits the current training batch from replacing a more reliable skill. A candidate is promoted only when it satisfies the configured improvement criteria.

</details>

<details><summary>What is the minimum structure needed to add a new benchmark?</summary>

The lesson recommends a benchmark config plus an environment containing a dataloader, adapter, rollout logic, evaluator or reflection logic, and an initial skill document. These pieces define the data schema, task interaction, scoring or diagnosis, and starting behavior while the shared engine handles optimization.

</details>

## Further Reading

- [SkillOpt Project Documentation](https://microsoft.github.io/SkillOpt/)
- [SkillOpt Paper on arXiv](https://arxiv.org/abs/2605.23904)
- [SkillOpt GitHub Repository](https://github.com/microsoft/SkillOpt)
- [ALFWorld: Aligning Text and Embodied Environments](https://alfworld.github.io/)
