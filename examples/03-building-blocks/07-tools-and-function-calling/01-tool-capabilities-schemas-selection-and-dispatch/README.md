# Direct dispatch and code aggregation

Run `python3 main.py` for dispatcher validation, then `python3 programmatic_tools.py` for aggregation through the same dispatcher. Both are offline standard-library examples.

The aggregation example returns a 5,000-cent quote for two lamps and whether stock was sufficient at lookup time. It preserves missing-product and malformed-quantity failures. It never reserves stock. Reads are separate observations, not one atomic snapshot.

No model, generated-code sandbox or provider API is implemented. The scripts do not establish a latency, cost or context-size improvement.
