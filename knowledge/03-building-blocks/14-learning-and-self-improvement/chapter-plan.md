# Learning and Self-Improvement Plan

## Section purpose

Separate the mechanisms by which agents adapt during or across runs.

## Learning outcomes

Explain reflection, feedback-based refinement, experience storage, skill libraries, prompt optimization, test-time adaptation, continual learning, and weight updates; evaluate improvement and forgetting.

## Prerequisites

[Multi-agent systems](../13-multi-agent-systems/chapter-plan.md), memory, and evaluation.

## Planned child chapters

Main path:

1. `01-adaptation-taxonomy.md`
2. `02-reflection-feedback-and-self-refinement.md`

Deep dives:

3. `03-experience-memory-and-skill-libraries.md`
4. `04-prompt-and-policy-optimization.md`
5. `05-continual-learning-weight-updates-and-forgetting.md`

Main path resumes:

6. `06-evaluating-improvement.md`

## Required concepts

Feedback, reflection, refinement, experience, skill, curriculum, transfer, plasticity, retention, catastrophic forgetting, prompt update, policy update, and weight update.

## Concepts explicitly out of scope

Speculation about recursive self-improvement and unverified autonomous training.

## Recommended teaching order

Define mechanisms, cover inference-time feedback, add durable experience and skills, distinguish optimization from training, then test transfer and forgetting.

## Required diagrams or visuals

Adaptation taxonomy and feedback-data lifecycle.

## Recommended examples

A mocked refinement loop and versioned skill record; no self-modifying production system.

## Sources

Authoritative source categories: Peer-reviewed primary research and reproducible benchmark work.

Candidate primary sources:

- [Reflexion](https://papers.neurips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html)
- [Self-Refine](https://papers.neurips.cc/paper_files/paper/2023/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html)
- [Voyager](https://arxiv.org/abs/2305.16291)
- [Large Language Models as Optimizers](https://proceedings.iclr.cc/paper_files/paper/2024/hash/3339f19c5fcee3ad74502947a32be9e6-Abstract-Conference.html)
- [AgentCL](https://arxiv.org/abs/2606.02461)

## Connections to later security chapters

[Retrieval, memory, and data security](../../07-security-by-component-and-workflow-stage/02-retrieval-memory-and-data/chapter-plan.md) and [end-to-end attack paths](../../07-security-by-component-and-workflow-stage/07-end-to-end-attack-paths/chapter-plan.md).

## Open questions

Which improvements generalize beyond the tasks that generated the feedback?

## Completion criteria

Every claimed improvement identifies mechanism, evaluation baseline, transfer test, retention test, and rollback path.
