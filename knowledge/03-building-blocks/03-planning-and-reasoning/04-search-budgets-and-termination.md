<!--
---
title: Search, budgets, and termination
unit_id: P1-03-03-04
summary: Explains deliberate reasoning via tree and graph search over candidate thoughts,
  multi-dimensional search budgets, heuristic pruning, and deterministic termination
  protocols.
prerequisites:
- Read [Reflection, evaluation, and replanning](03-reflection-evaluation-and-replanning.md).
learning_objectives:
- Differentiate between linear autoregressive generation, Tree of Thoughts (ToT),
  and Graph of Thoughts (GoT) exploration.
- Apply heuristic evaluation functions to score candidate reasoning branches and prune
  unpromising paths.
- Configure multi-dimensional execution budgets covering search depth, token consumption,
  wall-clock latency, and branching factor.
- Implement deterministic termination state transitions including goal satisfaction,
  budget exhaustion, cycle detection, and human escalation.
source_records:
- p1-03-03-04-yao-tree-of-thoughts-2023
- p1-03-03-04-besta-graph-of-thoughts-2024
- p1-03-03-04-anthropic-agent-budgets-2024
- p1-03-03-04-langchain-budget-termination-2024
visual_assets: []
example_paths:
- examples/03-building-blocks/03-planning-and-reasoning/04-search-budgets-and-termination/tree_search_budget_governor.py
pass: architecture
learning_path: main
status: complete
last_reviewed: '2026-08-24'
---
-->

# Search, budgets, and termination

## Why this matters

When humans tackle complex mathematical proofs, strategic chess positions, or architectural refactoring, they do not commit blindly to the very first idea that enters their mind. Instead, they imagine multiple possibilities, look several steps ahead, evaluate the merits of each path, backtrack when hitting dead ends, and stop when a proven solution is reached or time runs out.

Standard language model prompting operates in a strictly left-to-right, feed-forward sequence. Once a model begins generating a path, it cannot easily explore alternative branches in parallel or backtrack to earlier decision points. **Search, budget, and termination mechanisms** equip autonomous agents with deliberate problem-solving capabilities (Yao et al., 2023; Besta et al., 2024; Anthropic, 2024; LangChain, 2024). By structuring reasoning as a tree or graph search governed by strict token and depth budgets, agents can explore complex solution spaces methodically without getting trapped in infinite execution loops.

## Simple mental model

Think of a navigator planning an overland expedition through mountainous terrain:

1. **The search frontier:** at each crossroads, the navigator identifies several viable trails rather than walking blindly down the first path.
2. **Heuristic evaluation:** the navigator assesses each trail using topographical maps, weather forecasts, and elevation gain to estimate the likelihood of reaching the summit.
3. **Pruning and backtracking:** dangerous or blocked paths are pruned immediately. If a trail ends at a cliff, the expedition backtracks to the previous intersection.
4. **The expedition budget:** the team has finite rations, battery power, and daylight. Every detour consumes part of the budget.
5. **Deterministic stopping rules:** the expedition halts when the summit is reached, when night falls (timeout), when rations run out (budget exhaustion), or when circular tracks indicate the team is lost (cycle detection).

Managing both exploration and resources ensures the expedition discovers optimal routes without becoming stranded.

## Position in the agent workflow

Search and budgeting sit at the strategic core of agent reasoning. In single-step or linear workflows (such as basic ReAct or Plan-and-Execute), action selection proceeds along a single line. In deliberate reasoning architectures, the agent maintains an active search frontier of candidate subtasks and partial trajectories.

The search governor orchestrates this exploration. It queries the model to expand promising nodes, invokes heuristic evaluators to score intermediate states, and tracks resource consumption. When a candidate path meets the goal criteria or when safety budgets are depleted, the governor terminates the search and returns either the validated solution or a graceful fallback.

## How it works

Deliberate search and execution budgeting operate across four interconnected components:

### 1. The search frontier and thought generation

A **thought** is a coherent intermediate reasoning step, such as a decomposed equation, a proposed database query, or an initial API call strategy (Yao et al., 2023). Given a current state, the agent generates multiple candidate next thoughts:

- **Breadth-First Search (BFS):** Explores all candidate thoughts at the current depth before advancing deeper. This approach provides broad coverage but incurs high token overhead.
- **Depth-First Search (DFS):** Pursues a single promising line of thought deeply, backtracking to alternative branches only when a dead end or constraint violation occurs.
- **Beam Search:** Retains only the top-*k* highest-scoring candidate paths at each step, discarding lower-quality branches to keep memory usage bounded.

### 2. Heuristic state evaluation and pruning

To navigate the search space efficiently, the agent evaluates intermediate thoughts using a **state evaluator**. The evaluator scores candidate nodes based on logical consistency, alignment with the initial goal, and constraint compliance (Yao et al., 2023). Candidates scoring below a predefined threshold are pruned immediately, preventing the agent from wasting computation on flawed paths.

### 3. Multi-dimensional execution budgets

Unbounded search leads to runaway latency, astronomical API bills, and memory exhaustion. Production architectures enforce four complementary budget constraints (Anthropic, 2024; LangChain, 2024):

- **Maximum search depth:** Caps the maximum number of sequential reasoning steps (for example, depth $<= 5$).
- **Token consumption ceiling:** Establishes a hard limit on the total input and output tokens consumed across all generated branches.
- **Wall-clock timeout:** Terminates execution if search time exceeds an absolute duration (such as 30 seconds).
- **Branching factor cap:** Restricts the number of candidate children generated from any single parent node.

### 4. Graph transformations and aggregation

Beyond simple trees, **Graph of Thoughts (GoT)** enables arbitrary directed acyclic graph operations (Besta et al., 2024). Agents can combine complementary ideas from two separate branches (aggregation), refine a promising node in place (transformation), or loop back to previous stable states while preserving verified intermediate insights.

## Main variants

1. **Tree of Thoughts (ToT):** Formulates reasoning as a tree where each node represents a partial solution and branches represent candidate next steps evaluated via lookahead and backtracking (Yao et al., 2023).
2. **Graph of Thoughts (GoT):** Generalizes tree search to arbitrary graph topologies, supporting thought merging, feedback loops, and multi-path synthesis (Besta et al., 2024).
3. **Monte Carlo Tree Search (MCTS) Agents:** Uses statistical rollout simulations and value networks to navigate large, stochastic decision trees in complex multi-step environments.
4. **Bounded Workflow Governors:** Embeds strict timeout counters, token monitors, and recursion limiters into deterministic execution frameworks like LangGraph (LangChain, 2024).

## Minimal implementation

The following Python snippet demonstrates a bounded Tree of Thoughts search governor enforcing maximum depth, token limits, heuristic pruning, and deterministic termination. The [full runnable example](../../../examples/03-building-blocks/03-planning-and-reasoning/04-search-budgets-and-termination/tree_search_budget_governor.py) simulates an end-to-end security verification task exploring alternative analysis paths.

<details>
<summary>Expand minimal Python implementation</summary>

```python
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, Tuple

class TerminationReason(Enum):
    SUCCESS = auto()
    BUDGET_EXCEEDED = auto()
    NO_VIABLE_PATHS = auto()

@dataclass
class SearchNode:
    node_id: str
    thought: str
    depth: int
    score: float

@dataclass
class SearchBudget:
    max_depth: int = 3
    max_tokens: int = 1500

class TreeSearchGovernor:
    def __init__(self, budget: SearchBudget):
        self.budget = budget
        self.tokens_used = 0

    def evaluate_and_prune(self, candidate: SearchNode) -> bool:
        # Prune low-scoring dead ends immediately
        return candidate.score >= 0.5

    def search(self, root_goal: str) -> Tuple[TerminationReason, Optional[SearchNode]]:
        root = SearchNode("0", root_goal, depth=0, score=1.0)
        frontier = [root]

        while frontier:
            frontier.sort(key=lambda n: n.score, reverse=True)
            current = frontier.pop(0)

            if current.score >= 0.99 and current.depth >= 2:
                return TerminationReason.SUCCESS, current

            if current.depth >= self.budget.max_depth or self.tokens_used >= self.budget.max_tokens:
                return TerminationReason.BUDGET_EXCEEDED, current

            # Generate and evaluate candidate child thoughts
            children = [
                SearchNode(f"{current.node_id}.1", "Valid parameterized query check", current.depth + 1, 0.95),
                SearchNode(f"{current.node_id}.2", "Bypass authentication filter", current.depth + 1, 0.1),
            ]
            self.tokens_used += 200

            for child in children:
                if self.evaluate_and_prune(child):
                    frontier.append(child)

        return TerminationReason.NO_VIABLE_PATHS, None
```

</details>

Run [tree_search_budget_governor.py](../../../examples/03-building-blocks/03-planning-and-reasoning/04-search-budgets-and-termination/tree_search_budget_governor.py) to inspect the complete search trace, including node expansion, score evaluation, branch pruning, token accounting, and optimal path selection.

## Data flow and state changes

1. **Root initialization:** The search governor initializes the root node with the user goal and resets resource meters.
2. **Frontier queuing:** The root node is placed on the priority frontier queue.
3. **Node expansion:** The governor pops the highest-ranked node and prompts the model to generate branching candidate thoughts.
4. **Heuristic evaluation:** Each child candidate is scored by the evaluation rubric or external environment checks.
5. **Pruning filter:** Candidates failing score thresholds are discarded; viable candidates are added to the search frontier.
6. **Budget verification:** The governor decrements remaining tokens and checks elapsed time against hard limits.
7. **Termination dispatch:** When a verified target state is discovered or when a budget constraint is reached, search terminates and the final status is emitted.

## Trust boundaries

- **Candidate thoughts to execution boundary:** Candidate thoughts generated during tree exploration must remain sandboxed. The runtime must not execute side-effecting actions (such as database writes or emails) until a path is finalized and approved.
- **Evaluator integrity:** Heuristic evaluators must operate independently of the generator to prevent adversarial inputs from inflating candidate quality scores.
- **Budget enforcement authority:** Budget counters must be enforced by the host runtime, not by the model itself. A model cannot be trusted to self-report when it should time out or stop.

## Reliability failures

- **Combinatorial explosion:** Without aggressive pruning, branching factors cause search trees to grow exponentially, exhausting memory and token limits within few steps.
- **Heuristic misalignment:** If the evaluation heuristic favors superficial eloquence over technical correctness, the agent may pursue dead ends while pruning genuinely correct solutions.
- **Premature pruning:** Overly aggressive score thresholds can inadvertently prune valid solutions early in the search tree before their full utility becomes apparent.
- **Infinite loop cycles:** When exploring cyclic graphs, an agent may cycle between identical partial states unless explicit visited-state hashing is enforced.

## Limitations and trade-offs

- **High latency:** Tree search multiplies model calls, increasing response times from hundreds of milliseconds to several tens of seconds.
- **Significant token costs:** Generating and evaluating multiple branches across several depths dramatically increases API billing costs compared to linear ReAct loops.
- **Orchestration complexity:** Managing frontier priority queues, state snapshots, and backtracking requires complex state machine infrastructure.

## Security preview

In Pass 2, search and budget architectures are evaluated against **Denial of Service (DoS), Resource Exhaustion Attacks, and Frontier Poisoning**. Attackers craft inputs designed to induce high-branching combinatorial explosion, exhaust API budgets, or poison heuristic evaluators to force runaway execution. We analyze deterministic resource sandboxing, token rate limiters, and cycle detection defenses in [Instructions, context, and model security](../../07-security-by-component-and-workflow-stage/01-instructions-context-and-models/chapter-plan.md).

## Open research questions

- How can agents learn optimal dynamic branching factors that scale up for genuinely hard problems while staying minimal for straightforward tasks?
- What formal methods can prove that a search heuristic is admissible, guaranteeing that the best solution found is globally optimal?

## Key takeaways

- Tree of Thoughts (ToT) and Graph of Thoughts (GoT) extend linear generation with deliberate branching, lookahead, and backtracking.
- Heuristic evaluation functions score intermediate states to prune low-quality branches before computation is wasted.
- Multi-dimensional execution budgets (depth, tokens, wall-clock time, branching factor) prevent runaway agent loops.
- Deterministic termination states guarantee that the agent halts cleanly when goals are satisfied or when resource limits are reached.

## References

- Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T. L., Cao, Y., & Narasimhan, K. *Tree of Thoughts: Deliberate Problem Solving with Large Language Models*. Advances in Neural Information Processing Systems (NeurIPS), 2023. [arXiv:2305.10601](https://arxiv.org/abs/2305.10601).
- Besta, M., Blach, N., Kubicek, A., Gerstenberger, R., Gianinazzi, L., et al. *Graph of Thoughts: Solving Elaborate Problems with Large Language Models*. AAAI Conference on Human Computation and Crowdsourcing, 2024. [arXiv:2308.09687](https://arxiv.org/abs/2308.09687).
- Anthropic. *Building Effective Agents: Managing Search Trees and Execution Budgets*. Anthropic Research, 2024. [Anthropic Research](https://www.anthropic.com/research/building-effective-agents).
- LangChain Community. *Timeouts, Recursion Limits, and Termination in LangGraph Workflows*. LangGraph Documentation, 2024. [LangGraph Workflows](https://docs.langchain.com/oss/python/langgraph/workflows-agents).

---

[Next Unit: Run, thread, and event models →](../04-state-and-lifecycle/chapter-plan.md)
