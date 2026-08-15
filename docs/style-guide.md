# Style Guide

## Language

- Use simple, direct, active English. Avoid overly complex sentences and unnecessary academic jargon.
- Keep exact technical terms. Define them clearly with familiar analogies on first use.
- Avoid marketing language and em dashes.

## Reader level

- Assume LLM and prompt familiarity, but no software-system vocabulary.
- Explain model, API, or Python details only when needed.

## Teach for understanding

- Start with a concrete situation. Explain the ordinary idea before its technical name.
- Introduce and define one technical term at a time, then reuse it in examples.
- Do not trade essential explanation for brevity. Use prose, tables, or visuals to clarify mechanisms.
- Make a connected story, not a list of disconnected definitions.
- Explain how to read every visual nearby.

## Chapter structure

- Personalize sections to the chapter topic. Include optional sections only when they provide substantive technical value.
- Do not add placeholder text or artificial questions.
- Do not create ASCII or text-based .md schemas. Generate visual cartoon illustrations for all diagrams and flows.
- End every unit with a clear navigation link or button to the next sequential unit to ensure smooth reading progression.

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
