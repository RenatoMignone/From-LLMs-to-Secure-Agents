<!--
---
title: Data, control, and trust boundaries
unit_id: P1-00-02
summary: Separates information from instructions and shows where a system must reconsider
  its assumptions.
prerequisites:
- Read [Reader contract and system map](01-reader-contract-and-system-map.md).
learning_objectives:
- Distinguish data from control in one structured message.
- Trace data flow and control flow through a simple application.
- Mark a trust boundary and name the assumption that changes there.
source_records:
- p1-00-02-rfc-8259-json
- p1-00-02-rfc-9110-http-semantics
visual_assets: []
example_paths: []
pass: architecture
learning_path: main
status: complete
last_reviewed: '2026-08-10'
---
-->

# Data, control, and trust boundaries

## Why this matters

Imagine you ask a travel assistant to draft a day trip, then press **Save itinerary**. The same message can contain the place you chose, the date, and the request to save it. Those are not the same kind of thing. The place and date describe the trip. The request tells the software what to try next.

Making that distinction is a practical way to read an agent system. It stops a sentence such as “the agent sent the itinerary” from hiding three different questions: what information was moved, which part decided to act, and which other system received the request. This chapter gives names to those questions before [agent foundations](../01-agent-foundations/chapter-plan.md) adds an agent to the story. The [project guide](../chapter-plan.md) shows how this prerequisite chapter fits into the whole guide.

## Simple mental model

Think of a restaurant order slip. `Vegetable pizza` is **data**: it is the thing being discussed. `Place order` is **control**: it tells the kitchen workflow what should happen. The slip may also name a table, a payment method, and a person allowed to approve a refund. A single slip can therefore carry data, a request for action, and information used to decide whether the action is allowed.

Software messages work the same way. **Data flow** is the movement of values between components. **Control flow** is the movement of a decision, trigger, or command that changes what a component does next. The two often travel together, but separating them lets you trace a system without guessing.

| Part of a travel request | Role | Question to ask |
| --- | --- | --- |
| `destination: "Florence"` | Data | What value is being discussed? |
| `date: "2026-09-12"` | Data | What value will be remembered or sent on? |
| `action: "save_itinerary"` | Control | What action is requested? |
| `actor_id: "maya"` | Context for a decision | Who is asking? |
| `permission: "itineraries:write"` | Context for a decision | Is this actor allowed to cause that action? |

The last two fields are neither proof nor permission by themselves. They are inputs that the receiving application must evaluate. The next prerequisite chapter explains how requests change remembered state and create observable events.

## Position in the agent workflow

Use the system-context diagram in the previous chapter as the map. A user, an application process, a store, and an external service are the named components. Label each arrow twice: first with the data that crosses it, then with the control meaning, if any.

For the itinerary story, a browser sends the application the chosen destination and a request to save it. The application writes the itinerary to its store. It might later ask a map service to calculate travel times. The write moves data into durable state. The map request also directs another system to perform work. The same arrow can carry both a destination and an instruction such as “calculate route.”

## How it works

### A structured message is a container, not a decision

An application often receives a web request through the Hypertext Transfer Protocol, or **HTTP**. HTTP gives shared meanings to requests and responses; it does not decide what an application's fields mean. [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) defines HTTP as a stateless application-level protocol.

The contents are often written in JavaScript Object Notation, or **JSON**. JSON is a text format for structured data. It can group named values into an object, which makes a message easier for a person and a program to inspect. [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259.html) defines JSON's structure, but not the meaning or authority of its fields.

```json
{
  "actor_id": "maya",
  "action": "save_itinerary",
  "itinerary": {
    "destination": "Florence",
    "date": "2026-09-12"
  }
}
```

Read the message in two passes. In the data pass, `destination` and `date` describe an itinerary. In the control pass, `action` asks the application to save it. `actor_id` says who claims to be asking. It does not turn the request into an allowed action. The application needs its own rules and records to decide that.

### A boundary marks a changed assumption

A **trust boundary** is a line in a diagram where an assumption must be checked again. It is a teaching and design term, not a claim that one side is safe and the other is unsafe. The useful question is: *what no longer follows automatically after this line?*

For example, the application may regard a value in its own store as having passed its normal checks. When it receives the same-looking value from a browser, it cannot make that assumption. When it sends a request to a map service, the map service has its own account, rules, availability, and records. Each crossing changes which component is responsible for interpreting the message and deciding whether to act.

| Crossing | Assumption to reconsider | Ordinary consequence |
| --- | --- | --- |
| Browser to application | The message was supplied by the application's user interface. | Interpret its fields and decide whether the requested action is allowed. |
| Application to its store | The running process still has the current version of the itinerary. | Decide what should be read or written. |
| Application to map service | The other service shares the application's rules and account. | Send only the request that service needs and interpret its response separately. |

This is why a boundary belongs on the diagram, not only in a security document. It makes the system's assumptions visible while its ordinary workflow is still simple.

## Main variants

The same reading method works even when the connection changes.

| Connection shape | Data flow | Control flow |
| --- | --- | --- |
| One local component calls another | Values passed in memory | A function call asks the receiving component to run now. |
| Browser calls a web application | An HTTP request carries values | The request method and application fields express the requested work. |
| Application publishes to a queue | A message waits for another process | The published event triggers work later. |
| Application calls a vendor service | Request values cross organisations or accounts | The call asks the service to perform its own operation. |

These are descriptions, not a ranking of safety. A local call can still be important, and a vendor call can still be tightly limited. The boundary tells readers where to ask again about identity, meaning, and responsibility.

## Minimal implementation

Before writing code, state the small decision in plain language:

```text
receive request
separate requested action from itinerary data
look up whether the actor may save an itinerary
if allowed, write the itinerary and return a response
otherwise, return a refusal without writing it
```

This is pseudocode, not a complete program. Its important feature is order: the application identifies the requested control action before it changes its remembered data. It also makes one limit clear. A field named `permission` in an incoming message is only data until the application checks it against a source it trusts for that decision.

## Framework implementations

No framework is required here. Frameworks use labels such as *route*, *handler*, *webhook*, or *tool call*. Translate each label into the same questions: which component received what data, what control request arrived with it, and where does a trust assumption change? This keeps framework vocabulary from obscuring the workflow.

## Data flow and state changes

Data flow alone does not say that anything changed. The application can receive `Florence`, look up information, and reply without saving anything. A state change happens only when the application updates what it remembers, such as writing the itinerary to its store.

Control flow alone does not promise that an action completed. An application can request a route calculation from a map service and receive a timeout. In later diagrams, keep the two questions separate: “what values moved?” and “what action was requested or triggered?” The next chapter adds the third question: “what state changed, and what event records that change?”

## Trust boundaries

Draw a trust boundary around the part whose rules you are currently discussing. Then label every connection that crosses it with the smallest useful set of facts: the sender, the receiver, the data, and the requested action. If the connection can cause an effect outside the boundary, name that effect too.

This is not detailed security analysis. It is inventory. Later, the [threat model](../06-threat-model/chapter-plan.md) will use the inventory to discuss assets, actors, authority, boundaries, and side effects. For now, a well-labelled boundary prevents us from assigning every decision to the vague phrase “the system.”

## Reliability failures

An ordinary failure can blur data and control if the diagram does not separate them. The application may send a route request, lose the response, and be unable to tell the user whether the map service completed it. The request was sent; that does not prove the route was calculated. Likewise, a response that says “saved” is only useful if the application's state really contains the itinerary.

This chapter does not prescribe retries, queues, or recovery. It supplies a reading habit for the reliability material: record what was requested, what was observed, and what state changed as different facts.

## Worked example

Return to the JSON request above. Suppose Maya is permitted to save itineraries. The application can write the destination and date to its store, then reply that the itinerary was saved. The data change is the new stored itinerary. The control decision is that `save_itinerary` was allowed and carried out.

Now change only `actor_id` to an identity that lacks permission. The destination is still ordinary data and the action is still a request. What changes is the application's decision: it returns a refusal and leaves the stored itinerary unchanged. This tiny comparison is the core distinction: receiving an instruction is not the same as accepting it.

## Limitations and trade-offs

Data and control are an explanatory separation, not a property that every protocol labels perfectly. A field can serve both roles. For example, a `destination` can be travel data for one component and an address that directs delivery work for another. Explain the component and purpose before deciding which role matters in a diagram.

Trust boundaries are also relative to the question being asked. A team may draw one boundary around a whole application when teaching the user journey, then draw smaller boundaries around its store and vendor integrations when planning a deployment. Neither drawing is the whole truth. Each should state the assumptions it is meant to expose.

## Security preview

Security work later will ask whether data crossing a boundary is handled as expected and whether a control request has the authority to cause its intended side effect. This chapter does not assess attacks or prescribe controls. It only makes the components, requests, and changed assumptions visible for the [threat model](../06-threat-model/chapter-plan.md).

## Open research questions

Where should a later reliability chapter introduce retries: immediately after the first delayed workflow, or in a short optional branch? The answer depends on whether readers need delivery guarantees before they can trace the next main-path workflow.

## Key takeaways

- Data describes the thing a system is discussing. Control asks the system to take its next action.
- One message can carry both, plus facts used to decide whether the request is allowed.
- A message format such as JSON gives structure, not meaning, truth, or authority.
- A trust boundary marks where an assumption must be reconsidered. Label what crosses it and who decides what happens next.

## References

- [RFC 8259: The JavaScript Object Notation (JSON) Data Interchange Format](https://www.rfc-editor.org/rfc/rfc8259.html)
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html)

---

[Next Unit: Requests, events, state, and side effects →](03-requests-events-state-and-side-effects.md)
