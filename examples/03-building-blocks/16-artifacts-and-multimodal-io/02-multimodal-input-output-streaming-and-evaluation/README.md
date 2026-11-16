# Interruption and late tool results

Requires Python 3.10+ with only its standard library. Run from repository root:

```bash
python3 examples/03-building-blocks/16-artifacts-and-multimodal-io/02-multimodal-input-output-streaming-and-evaluation/main.py
```

Expected: the uninterrupted task completes. The interrupted trace retains a completed reservation, verifies the mocked ledger, delivers the current acknowledgement and remains incomplete with `needs_resolution=True`. Obsolete speech is absent from the final text.

The event reducer uses a local ordered sequence, turn IDs and an operation ID. An interruption changes intent and stops old output; it does not erase the pending tool. A late result is retained and compared with the corrected goal. The final acknowledgement reports an unresolved release rather than falsely claiming success. Tests check late-result handling, partial-only traces, a dropped connection before tool completion, old-turn playback, sequence gaps and mismatched operations.

These are application teaching events, not OpenAI or A2A messages. All speech, tool results, playback and ledger checks are mocked. The script neither emits audio nor executes reservations, cancellations or compensation. It does not measure latency, recognition, buffering or network reliability. Production delivery may duplicate, reorder or lose events; this example detects gaps and requires state recovery instead of implementing a transport protocol.
