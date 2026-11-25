
import { NextResponse } from "next/server";
import { saveLatest, type GroupMeans } from "@/lib/causality-store";

/**
 * Challenge 4: Causality Audit Service
 * Run-along: Causality Auditor
 *
 * Identifies fork, pipe, collider, or direct causal structures.
 * Calculates naive and stratified effects.
 * Saves the latest result for the /causality page.
 */

type Structure = "fork" | "pipe" | "collider" | "direct";

type Row = {
  x: 0 | 1;
  z: 0 | 1;
  y: number;
};

// An effect of at least 0.35 in either direction is visible.
const VISIBLE = 0.35;

// Calculate the average of a list of numbers.
const mean = (ys: number[]) =>
  ys.reduce((a, b) => a + b, 0) / ys.length;

// Average outcome for X = 0 and X = 1.
function groupMeans(label: string, rows: Row[]): GroupMeans {
  const y0 = rows.filter((r) => r.x === 0).map((r) => r.y);
  const y1 = rows.filter((r) => r.x === 1).map((r) => r.y);

  return {
    label,
    n0: y0.length,
    mean0: mean(y0),
    n1: y1.length,
    mean1: mean(y1),
  };
}

// Naive effect: difference in averages without considering Z.
function naiveEffect(rows: Row[]): number {
  const g = groupMeans("all", rows);
  return g.mean1 - g.mean0;
}

// Stratified effect: calculate within each Z group,
// then weight the differences by each group's size.
function stratifiedEffect(rows: Row[]): number {
  let weighted = 0;

  for (const z of [0, 1]) {
    const slice = rows.filter((r) => r.z === z);
    const g = groupMeans(`z=${z}`, slice);

    weighted += (g.mean1 - g.mean0) * slice.length;
  }

  return weighted / rows.length;
}

// Classify the causal structure using domain facts
// and the naive versus stratified effects.
function classifyStructure(
  facts: {
    zTiming: "before-x" | "after-x";
    zInfluencesX: boolean;
  },
  naive: number,
  stratified: number
): Structure | null {
  const naiveVisible = Math.abs(naive) >= VISIBLE;
  const stratifiedVisible = Math.abs(stratified) >= VISIBLE;

  // Fork: Z exists before X and influences X.
  // Z is a common cause of treatment and outcome.
  if (facts.zTiming === "before-x" && facts.zInfluencesX) {
    return "fork";
  }

  // Pipe: X affects Z, which affects Y.
  // The overall effect disappears after controlling for Z.
  if (
    facts.zTiming === "after-x" &&
    naiveVisible &&
    !stratifiedVisible
  ) {
    return "pipe";
  }

  // Collider: Z is a common effect.
  // Conditioning on Z creates an apparent relationship.
  if (
    facts.zTiming === "after-x" &&
    !naiveVisible &&
    stratifiedVisible
  ) {
    return "collider";
  }

  // Direct: the effect remains after stratification,
  // or the third variable does not influence X.
  return "direct";
}

// API endpoint: POST /api/causality/decide
export async function POST(req: Request) {
  const probe = await req.json().catch(() => null);

  // Check that the request contains the required fields.
  if (
    !probe ||
    !Array.isArray(probe.dataset) ||
    !probe.context?.domainFacts
  ) {
    return NextResponse.json(
      {
        error:
          "expected a JSON probe with `context.domainFacts` and a `dataset` list",
      },
      { status: 400 }
    );
  }

  const rows: Row[] = probe.dataset;
  const ctx = probe.context;

  // Calculate the two effects.
  const naive = naiveEffect(rows);
  const stratified = stratifiedEffect(rows);

  // Identify the causal structure.
  const structure = classifyStructure(
    ctx.domainFacts,
    naive,
    stratified
  );

  if (structure === null) {
    return NextResponse.json(
      {
        error:
          "Could not classify the causal structure",
      },
      { status: 501 }
    );
  }

  // Determine whether the relationship is causal.
  const causal =
    structure === "pipe" || structure === "direct"
      ? true
      : structure === "fork"
        ? Math.abs(stratified) >= VISIBLE
        : false;

  // Decide whether stratification is appropriate.
  const advice =
    structure === "fork" ? "stratify" : "do-not-stratify";

  // Explain the classification.
  const z = `The third variable (${ctx.zLabel})`;

  const why: Record<Structure, string> = {
    fork:
      `${z} was set before ${ctx.xLabel} and steered it, ` +
      `so it is a common cause. Comparing within each of its ` +
      `levels blocks that path`,

    pipe:
      `${z} comes after ${ctx.xLabel}, and the gap disappears ` +
      `within its levels, so it is how ${ctx.xLabel} works. ` +
      `The overall gap is the effect`,

    collider:
      `${z} comes after both, there is no overall gap, ` +
      `and a gap appears only within its levels, so it is ` +
      `a common effect. Splitting by it creates a false pattern`,

    direct:
      `${z} did not steer ${ctx.xLabel}, and the gap is ` +
      `the same overall and within its levels, ` +
      `so it is a bystander`,
  };

  // Build the JSON response required by the grader.
  const answer = {
    structure,
    causal,
    advice,
    stratifiedEffect: Number(stratified.toFixed(4)),
    reasoning:
      `Naive effect ${naive.toFixed(2)}, ` +
      `stratified effect ${stratified.toFixed(2)}. ` +
      `${why[structure]}. ` +
      `Verdict: ${causal ? "causal" : "not causal"}.`,
  };

  // Build the summary for the /causality page.
  const summary = {
    naive,
    stratified,
    groups: [
      groupMeans("All data", rows),

      groupMeans(
        `${ctx.zLabel}: ${ctx.z0}`,
        rows.filter((r) => r.z === 0)
      ),

      groupMeans(
        `${ctx.zLabel}: ${ctx.z1}`,
        rows.filter((r) => r.z === 1)
      ),
    ],
  };

  // Save the latest result without storing all 240 rows.
  await saveLatest(
    { ...probe, dataset: undefined },
    answer,
    summary
  );

  // Return the result to the grader.
  return NextResponse.json(answer);
}
