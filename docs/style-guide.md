# Style Guide

## Language

- Use simple, precise, active English. Keep one main idea per paragraph.
- Define terms and expand acronyms on first use. Use terms consistently.
- Avoid marketing language and em dashes.

## Reader level

- Assume LLM and prompt familiarity, but no software-system vocabulary.
- Explain model, API, or Python details only when needed.

## Teach for understanding

- Start with a concrete situation. Explain the ordinary idea before its technical name.
- Introduce, define, and motivate one new term at a time, then reuse it in the example.
- Do not trade essential explanation for brevity. Use prose, tables, or visuals when they improve understanding.
- Make a connected story, not a list of definitions. Explain the question before a formula, diagram, JSON example, or acronym.
- Explain how to read every visual nearby.

## Architecture teaching order

1. State the problem.
2. Give a simple mental model.
3. Show the workflow or structure.
4. Add technical detail.
5. Show an example.
6. Explain limitations.
7. Add a short security preview that links to Pass 2.

Do not explain attacks, controls, recovery, or security tests in an architecture chapter.

## Security teaching order

Start with the threat model. Map each security item to Pass 1 architecture. Separate preventive, detective, and recovery controls.

## Formatting

- Use descriptive headings and tables for comparisons.
- Use code only when useful. Give every visual alt text and a caption.
- Split large files into focused chapters.

## Claims

Distinguish definitions, official guidance, research results, implementation choices, project opinions, and open questions.

## Current field terminology

Map current terms to the architecture already taught. Define the mechanism first, state its maturity, and do not treat popularity as evidence.
