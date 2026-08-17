/**
 * CLI entry point for review bundle tool.
 * Writes result to review-bundle-result.json for GitHub Action consumption.
 */

import { writeFileSync } from "fs";
import { resolve } from "path";

interface ReviewBundleResult {
  pr_number: number;
  summary: string;
  risk_level: string;
  route_contract_drift: Array<{ route: string; issue: string; severity: string }>;
  endpoint_mismatch: Array<{ endpoint: string; issue: string; severity: string }>;
  ws_protocol_compatibility: Array<{ opcode: string; issue: string; severity: string }>;
  missing_test_matrix: Array<{ area: string; suggestion: string; severity: string }>;
}

async function main() {
  const prNumber = parseInt(process.argv[2] || process.env.PR_NUMBER || "0");
  if (!prNumber) {
    console.error("Error: PR number not provided");
    process.exit(1);
  }

  // Import the MCP server module
  const { synthesizeReviewBundle } = await import("./index.ts");
  
  try {
    const bundle = synthesizeReviewBundle(prNumber);
    const result: ReviewBundleResult = {
      pr_number: bundle.pr_number,
      summary: bundle.summary,
      risk_level: bundle.risk_level,
      route_contract_drift: bundle.route_contract_drift,
      endpoint_mismatch: bundle.endpoint_mismatch,
      ws_protocol_compatibility: bundle.ws_protocol_compatibility,
      missing_test_matrix: bundle.missing_test_matrix,
    };

    const outputPath = resolve("./review-bundle-result.json");
    writeFileSync(outputPath, JSON.stringify(result, null, 2));
    console.log(`Review bundle written to ${outputPath}`);
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error("Error generating review bundle:", error);
    process.exit(1);
  }
}

main();
