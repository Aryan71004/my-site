import numpy as np

rng = np.random.default_rng(seed=42)
n = 100_000

rate = rng.uniform(20, 60, size=n)  # parent first: patients per week
time = rng.gamma(400, 1/rate)       # child second: one time for each simulated rate

for i in range(10):
    print(i + 1, round(rate[i], 1), round(time[i], 1))


print((time > 15).mean())
print(time.mean())
print(np.quantile(time, [0.05, 0.95]))


# Run-along 2: Promo Day -> Arrivals

rng = np.random.default_rng(seed=3)
n = 100_000

promo = rng.binomial(1, 0.5, size=n)  # parent: 1 = promo day
lam = np.where(promo == 1, 60, 30)     # 60 on promo days, 30 otherwise
arrivals = rng.poisson(lam)            # child: one draw per row

print(arrivals.mean())
print((arrivals >= 50).mean())
print(((arrivals >= 40) & (arrivals <= 50)).mean())


# Run-along 3a: Two stores' total demand

rng = np.random.default_rng(seed=8)

store_a = rng.normal(220, 30, size=n)
store_b = rng.normal(160, 20, size=n)

total = store_a + store_b

print(np.quantile(total, 0.95))



# Run-along 3b: Flight 246

rng = np.random.default_rng(seed=7)
n = 100_000

demand = rng.poisson(190, size=n)
sold = np.minimum(demand, 182)
shows = rng.binomial(sold, 0.93)

print((shows >= 175).mean())
print((shows > 175).mean())



# Skill Test Question 2

rng = np.random.default_rng(seed=0)
n = 100_000

big_client = rng.binomial(1, 0.41, size=n)
lam = np.where(big_client == 1, 50, 30)
x = rng.poisson(lam)

print("Question 2:", x.mean())
