# Editorial Review

Automated checks can verify structure, links, and metadata. They cannot determine whether a chapter is accurate, proportionate, understandable, or safe to apply. Editorial review supplies that missing judgment.

## Review layers

### Author review

The author checks the chapter against its plan, prerequisites, source records, examples, and visuals. The author removes repetition, defines terms on first use, and makes uncertainty visible.

### Independent technical review

A reviewer who did not write the chapter checks the system model, source interpretation, code behavior, and limitations. Security chapters should be reviewed by someone with relevant defensive engineering or research experience before a stable release presents them as guidance.

### Reader review

A reader from the intended audience checks whether the chapter can be followed in sequence without hidden prerequisites. Reader feedback should identify the first confusing sentence, diagram, or transition rather than only giving a general impression.

## Chapter checklist

- The opening states why the concept matters and what the reader will learn.
- New terms are defined before they carry an argument.
- Paragraphs make one main point and use concrete subjects and verbs.
- Architecture, control flow, data flow, and trust boundaries are not conflated.
- Important claims have nearby citations whose source records state exact support and limitations.
- Time-sensitive claims include versions or dates and were rechecked.
- Examples teach the claimed behavior, run without secrets, and expose their limitations.
- Visual labels are legible, technically consistent with the prose, and explained in text.
- Alternative text communicates the instructional purpose, not every decorative detail.
- Security language distinguishes a control, mitigation, assumption, and residual risk.
- Absolute terms such as `prevents`, `guarantees`, `safe`, and `optimal` are either proven in the stated scope or replaced with bounded language.
- The summary and next link match the published learning path.

## Cross-chapter review

Before a release, review related chapters as a group. Check terminology, duplicated explanations, conflicting definitions, prerequisite order, link direction, and whether examples reuse the same conceptual model. Record deferred findings in release notes or issues rather than hiding them.

## Recording review

Pull requests should name the review type performed and any reviewer. Release tracking should list highlighted chapters that received independent review and material that remains author-reviewed only. A review date signals when the check happened, not permanent correctness.
