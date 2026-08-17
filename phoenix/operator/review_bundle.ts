/**
 * PhoenixEngine Operator: Review Bundle
 *
 * Wraps the MCP review_bundle tool for use in the OperatorModePipeline.
 * Allows automated PR analysis during the operator's review stage.
 *
 * Usage:
 *   const op = new ReviewBundleOperator();
 *   const result = await op.analyze(prNumber);
 *   ctx.review_analysis = result;
 */

export interface ReviewAnalysis {
  pr_number: number;
  risk_level: "low" | "medium" | "high" | "critical";
  drift_count: number;
  mismatch_count: number;
  ws_issue_count: number;
  test_gap_count: number;
  recommendations: string[];
  blocking_issues: string[];
}

export class ReviewBundleOperator {
  private mcp_tool = "review_bundle";

  /**
   * Analyze a PR using the MCP review_bundle tool.
   * Returns structured analysis and recommendations.
   */
  async analyze(prNumber: number): Promise<ReviewAnalysis> {
    // In a real implementation, this would invoke the MCP tool.
    // For now, we provide a placeholder that calls the analysis functions.
    
    const { synthesizeReviewBundle } = await import(
      "../mcp/tools/review_bundle/index.ts"
    );

    const bundle = synthesizeReviewBundle(prNumber);

    const blockingIssues = [
      ...bundle.endpoint_mismatch
        .filter((m: { severity: string }) => m.severity === "high")
        .map((m: { endpoint: string; issue: string }) => 
          `Endpoint ${m.endpoint}: ${m.issue}`
        ),
      ...bundle.ws_protocol_compatibility
        .filter((w: { severity: string }) => w.severity === "high")
        .map((w: { opcode: string; issue: string }) =>
          `WS ${w.opcode}: ${w.issue}`
        ),
    ];

    const recommendations = [
      ...bundle.route_contract_drift
        .map((d: { route: string; recommendation?: string }) => 
          d.recommendation || `Review route ${d.route}`
        ),
      ...bundle.missing_test_matrix
        .filter((t: { severity: string }) => t.severity === "high")
        .map((t: { area: string; suggestion: string }) => 
          `[${t.area}] ${t.suggestion}`
        ),
    ];

    return {
      pr_number: prNumber,
      risk_level: bundle.risk_level as "low" | "medium" | "high" | "critical",
      drift_count: bundle.route_contract_drift.length,
      mismatch_count: bundle.endpoint_mismatch.length,
      ws_issue_count: bundle.ws_protocol_compatibility.length,
      test_gap_count: bundle.missing_test_matrix.length,
      recommendations,
      blocking_issues: blockingIssues,
    };
  }

  /**
   * Format analysis for display in operator logs.
   */
  formatSummary(analysis: ReviewAnalysis): string {
    return `
╔═══════════════════════════════════════════════════════════════════════════════╗
║                   PR REVIEW BUNDLE ANALYSIS                                   ║
║                         PR #${analysis.pr_number}                                        ║
╚═══════════════════════════════════════════════════════════════════════════════╝

RISK LEVEL: ${analysis.risk_level.toUpperCase()}

ISSUE SUMMARY:
  • Route Contract Drift:      ${analysis.drift_count}
  • Endpoint Mismatches:       ${analysis.mismatch_count}
  • WS Protocol Issues:        ${analysis.ws_issue_count}
  • Missing Tests:             ${analysis.test_gap_count}

BLOCKING ISSUES:
${analysis.blocking_issues.length > 0 
  ? analysis.blocking_issues.map(i => `  ⚠️  ${i}`).join('\n')
  : '  ✅ None'}

RECOMMENDATIONS:
${analysis.recommendations.slice(0, 5).map(r => `  → ${r}`).join('\n')}
${analysis.recommendations.length > 5 ? `  ... and ${analysis.recommendations.length - 5} more` : ''}
    `;\n  }\n}

export default ReviewBundleOperator;
