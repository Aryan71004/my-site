
import { NextRequest, NextResponse } from "next/server";
import { saveLatest, type CandidateSummary } from "@/lib/simulator-store";

export const runtime = "nodejs";

type Game = {
  probeId?: string;
  type: string;
  scenario?: string;
  upPct: number;
  downPct: number;
  horizonYears: number;
  buyIn: number;
  candidateFractions: number[];
};

function quantile(sorted: number[], p: number): number {
  const index = (sorted.length - 1) * p;
  const lower = Math.floor(index);
  const upper = Math.ceil(index);
  if (lower === upper) return sorted[lower];
  return (
    sorted[lower] * (upper - index) +
    sorted[upper] * (index - lower)
  );
}

function simulate(
  game: Game,
  fraction: number,
  trials = 20_000
): CandidateSummary {
  const balances: number[] = [];

  const upFactor = 1 + (game.upPct / 100) * fraction;
  const downFactor = 1 - (game.downPct / 100) * fraction;

  for (let i = 0; i < trials; i++) {
    let balance = game.buyIn;

    for (let year = 0; year < game.horizonYears; year++) {
      balance *= Math.random() < 0.5 ? upFactor : downFactor;
    }

    balances.push(balance);
  }

  balances.sort((a, b) => a - b);

  const losses = balances.filter((balance) => balance < game.buyIn).length;

  return {
    fraction,
    p5: quantile(balances, 0.05),
    p25: quantile(balances, 0.25),
    median: quantile(balances, 0.5),
    p75: quantile(balances, 0.75),
    p95: quantile(balances, 0.95),
    probLoss: losses / trials,
  };
}

export async function POST(request: NextRequest) {
  try {
    const game = (await request.json()) as Game;

    if (
      game.type !== "investment-game" ||
      !Number.isFinite(game.upPct) ||
      !Number.isFinite(game.downPct) ||
      !Number.isInteger(game.horizonYears) ||
      game.horizonYears <= 0 ||
      !Number.isFinite(game.buyIn) ||
      game.buyIn <= 0 ||
      !Array.isArray(game.candidateFractions) ||
      game.candidateFractions.length === 0 ||
      game.candidateFractions.some(
        (fraction) =>
          typeof fraction !== "number" ||
          !Number.isFinite(fraction) ||
          fraction < 0 ||
          fraction > 1
      )
    ) {
      return NextResponse.json(
        { error: "Invalid investment game" },
        { status: 400 }
      );
    }

    const candidates = game.candidateFractions.map((fraction) =>
      simulate(game, fraction)
    );

    const best = candidates.reduce((current, candidate) =>
      candidate.median > current.median ? candidate : current
    );

    const recommendedFraction = best.fraction;
    const medianFinalBalance = best.median;
    const probLoss = best.probLoss;

    const reasoning =
      `Of the ${candidates.length} stake fractions simulated, ` +
      `staking ${(recommendedFraction * 100).toFixed(0)}% ` +
      `each year produced the highest median final balance ` +
      `of $${medianFinalBalance.toFixed(0)} after ` +
      `${game.horizonYears} years. ` +
      `About ${(probLoss * 100).toFixed(1)}% of simulated ` +
      `investors ended below their original buy-in.`;

    const answer = {
      recommendedFraction,
      medianFinalBalance,
      probLoss,
      reasoning,
    };

    await saveLatest(game, answer, candidates);

    return NextResponse.json(answer);
  } catch (error) {
    console.error("Simulator error:", error);

    return NextResponse.json(
      { error: "Simulator failed" },
      { status: 500 }
    );
  }
}
