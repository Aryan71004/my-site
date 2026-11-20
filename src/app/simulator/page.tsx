
import { loadLatest } from "@/lib/simulator-store";

export const metadata = {
  title: "Decision Simulator",
};

export const dynamic = "force-dynamic";

export default async function SimulatorPage() {
  const latest = await loadLatest();

  if (!latest) {
    return (
      <main style={{ padding: "40px", maxWidth: "1000px", margin: "auto" }}>
        <h1>Decision Simulator</h1>
        <p>No simulation results yet.</p>
        <p>Run the decision API to generate your first recommendation.</p>
        <img
          src="/images/dag.png"
          alt="Investment decision DAG"
          data-simulator="dag"
          style={{ width: "100%", maxWidth: "700px" }}
        />
      </main>
    );
  }

  const { problem, answer, candidates } = latest;

  const recommendedFraction = Number(answer.recommendedFraction);
  const medianFinalBalance = Number(answer.medianFinalBalance);
  const probLoss = Number(answer.probLoss);

  const maxMedian = Math.max(
    1,
    ...candidates.map((c) => c.median)
  );

  return (
    <main
      style={{
        maxWidth: "1000px",
        margin: "auto",
        padding: "40px 20px",
      }}
    >
      <h1>Decision Simulator</h1>

      <p>
        Explore investment decisions using Monte Carlo simulation.
        Compare candidate stake fractions and find the one that
        produces the highest median final balance.
      </p>

      <hr style={{ margin: "30px 0" }} />

      <h2>Recommended Decision</h2>

      <div style={{ display: "grid", gap: "16px" }}>
        <div>
          <h3>Recommended Stake Fraction</h3>
          <p data-simulator="recommended-fraction">
            {recommendedFraction}
          </p>
          <p>
            Stake {(recommendedFraction * 100).toFixed(0)}%
            of the balance each year.
          </p>
        </div>

        <div>
          <h3>Median Final Balance</h3>
          <p data-simulator="median-final">
            {medianFinalBalance.toFixed(2)}
          </p>
        </div>

        <div>
          <h3>Probability of Loss</h3>
          <p data-simulator="prob-loss">
            {probLoss}
          </p>
          <p>
            {(probLoss * 100).toFixed(1)}% of simulated
            investors finish below their original buy-in.
          </p>
        </div>
      </div>

      <h2>Why This Decision?</h2>
      <p>{String(answer.reasoning ?? "")}</p>

      <hr style={{ margin: "30px 0" }} />

      <h2>Latest Investment Game</h2>

      <ul>
        <li>Buy-in: ${Number(problem.buyIn).toLocaleString()}</li>
        <li>Heads gain: {problem.upPct}%</li>
        <li>Tails loss: {problem.downPct}%</li>
        <li>Duration: {problem.horizonYears} years</li>
      </ul>

      <h2>Candidate Stake Comparison</h2>

      <p>
        Each bar represents the median final balance
        for one candidate fraction.
      </p>

      <div style={{ display: "grid", gap: "20px" }}>
        {candidates.map((candidate) => (
          <div key={candidate.fraction}>
            <p>
              <strong>
                {(candidate.fraction * 100).toFixed(0)}% stake
              </strong>
              {" — "}
              ${candidate.median.toLocaleString(undefined, {
                maximumFractionDigits: 0,
              })}
            </p>

            <div
              style={{
                background: "#e5e7eb",
                height: "24px",
                borderRadius: "6px",
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  width: `${Math.max(
                    0,
                    (candidate.median / maxMedian) * 100
                  )}%`,
                  height: "100%",
                  background:
                    candidate.fraction === recommendedFraction
                      ? "#16a34a"
                      : "#2563eb",
                }}
              />
            </div>

            <p>
              Probability of loss:{" "}
              {(candidate.probLoss * 100).toFixed(1)}%
            </p>
          </div>
        ))}
      </div>

      <hr style={{ margin: "30px 0" }} />

      <h2>Decision DAG</h2>

      <p>
        The diagram shows how the chosen stake fraction,
        initial wealth, and annual coin flips determine
        the investor's final balance.
      </p>

      <img
        src="/images/dag.png"
        alt="Investment-game decision DAG"
        data-simulator="dag"
        style={{
          width: "100%",
          maxWidth: "900px",
          height: "auto",
        }}
      />
    </main>
  );
}
