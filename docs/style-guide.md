# Style Guide

## Language

- Use simple, active English. Avoid overly complex sentences and marketing language.
- Define exact technical terms on first use. Do not use em dashes.

## Reader level

- Assume LLM and prompt familiarity, but no advanced software-system vocabulary.
- Explain API or Python details only when needed.

## Teach for understanding

- Start with a concrete situation before giving technical names.
- Introduce one concept at a time and reuse it in examples.
- Make a connected story, not disconnected definitions. Explain how to read every visual nearby.

## Chapter structure

- Personalize sections to the topic; omit empty placeholders.
- Do not create ASCII or text-based .md schemas. Generate visual cartoon illustrations for all diagrams.
- Wrap minimal implementations in `<details><summary>Expand minimal Python implementation</summary>...</details>` to keep code expandable on demand.
- End every unit with a clear next-unit navigation link.

## Architecture teaching order

1. State the problem.
2. Give a simple mental model.
3. Show the workflow or structure.
4. Add technical detail.
5. Show an example.
6. Explain limitations.
7. Add a short security preview linking to Pass 2.

Do not explain attacks, controls, or security tests in architecture chapters.

## Security teaching order

Start with the threat model. Map security items to Pass 1 components. Separate preventive, detective, and recovery controls.
