
import numpy as np

rng = np.random.default_rng(seed=42)
n = 100_000

rate = rng.uniform(20, 60, size=n)
time = rng.gamma(400, 1/rate)

print(time.mean())
print(np.quantile(time, [0.05, 0.95]))
