# Transfer and retention gate

Run with Python 3.10 or newer, using only the standard library:

```bash
python3 examples/03-building-blocks/14-learning-and-self-improvement/02-optimization-continual-learning-forgetting-and-evaluation/main.py
```

Expected output: baseline new=1, old=4; candidate new=4, old=3; promote=False; selected_version=1.

The mocked new parser improves one family and mistakes missing data for zero in another. Assertions verify that the retention gate keeps the baseline despite a better average. These fixed fixtures explain evaluation; they do not measure real model learning, statistical confidence or an actual held-out development process. No external calls or self-modification occur.
