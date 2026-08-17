/**
 * MCP Server: PhoenixEngine PR Review Bundle
 *
 * Multi-layer analysis tool for pull requests:
 *   - Route contract drift detection
 *   - Frontend/backend endpoint mismatch validation
 *   - WebSocket protocol compatibility checking
 *   - Missing test matrix suggestions
 *
 * Callable via: npm run mcp:review -- 123
 * Resources: pr://123/summary, route:///api/graph/layout/contract
 * Tools: review_bundle({ pr_number: 123 })
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import {
  ListToolsRequestSchema,
  CallToolRequestSchema,
  Tool,
  TextContent,
} from "@modelcontextprotocol/sdk/types.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

import {
  analyzeRouteContractDrift,
  AnalyzedContractIssue,
} from "./analyzer/routeContract.js";
import {
  analyzeEndpointMismatch,
  AnalyzedEndpointMismatch,
} from "./analyzer/endpointDiff.js";
import {
  analyzeWSProtocolCompatibility,
  AnalyzedWSIssue,
} from "./analyzer/wsProtocol.js";
import {
  analyzeMissingTestMatrix,
  AnalyzedTestGap,
} from "./analyzer/testMatrix.js";

// ─────────────────────────────────────────────────────────────────────────────
// Type definitions
// ─────────────────────────────────────────────────────────────────────────────

export enum Severity {
  Low = "low",
  Medium = "medium",
  High = "high",
  Critical = "critical",
}

export interface ReviewBundle {
  pr_number: number;
  summary: string;
  risk_level: Severity;
  route_contract_drift: AnalyzedContractIssue[];
  endpoint_mismatch: AnalyzedEndpointMismatch[];
  ws_protocol_compatibility: AnalyzedWSIssue[];
  missing_test_matrix: AnalyzedTestGap[];
  generated_at: string;
  repository: string;
}

// ─────────────────────────────────────────────────────────────────────────────
// Review synthesis
// ─────────────────────────────────────────────────────────────────────────────

function getSeverityRank(severity: Severity): number {
  const ranks: Record<Severity, number> = {
    [Severity.Low]: 1,
    [Severity.Medium]: 2,
    [Severity.High]: 3,
    [Severity.Critical]: 4,
  };
  return ranks[severity];
}

function synthesizeReviewBundle(prNumber: number): ReviewBundle {
  const drift = analyzeRouteContractDrift(prNumber);
  const mismatch = analyzeEndpointMismatch(prNumber);
  const wsCompat = analyzeWSProtocolCompatibility(prNumber);
  const testGaps = analyzeMissingTestMatrix(prNumber);

  // Determine risk level based on severity distribution
  const allIssues = [
    ...drift.map((d) => d.severity),
    ...mismatch.map((m) => m.severity),
    ...wsCompat.map((w) => w.severity),
    ...testGaps.map((t) => t.severity),
  ];

  const maxSeverity = allIssues.reduce(
    (max, curr) => (getSeverityRank(curr) > getSeverityRank(max) ? curr : max),
    Severity.Low
  );

  const riskLevel =
    getSeverityRank(maxSeverity) >= 3 ? maxSeverity : Severity.Medium;

  const summary =
    `PR #${prNumber}: ` +
    `${drift.length} contract drifts, ` +
    `${mismatch.length} endpoint mismatches, ` +
    `${wsCompat.length} WS protocol issues, ` +
    `${testGaps.length} test gaps. ` +
    `Risk: ${riskLevel}.`;

  return {
    pr_number: prNumber,
    summary,
    risk_level: riskLevel,
    route_contract_drift: drift,
    endpoint_mismatch: mismatch,
    ws_protocol_compatibility: wsCompat,
    missing_test_matrix: testGaps,
    generated_at: new Date().toISOString(),
    repository: "Hydrogenesi/Phoenix-2.0-Apex-Edition",
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// MCP Server setup
// ─────────────────────────────────────────────────────────────────────────────

const server = new Server({
  name: "phoenixengine-review-bundle",
  version: "1.0.0",
});

// Tool: review_bundle
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "review_bundle",
        description:
          "Perform multi-layer PR review analysis: route contract drift, " +
          "frontend/backend endpoint mismatch, WebSocket protocol compatibility, " +
          "and missing test matrix suggestions.",
        inputSchema: {
          type: "object" as const,
          properties: {
            pr_number: {
              type: "integer",
              description: "The pull request number to analyze.",
            },
          },
          required: ["pr_number"],
        },
      } as Tool,
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request;

  if (name === "review_bundle") {
    const prNumber = (args as { pr_number?: number }).pr_number;
    if (typeof prNumber !== "number" || prNumber < 1) {
      return {
        content: [
          {
            type: "text" as const,
            text: "Error: pr_number must be a positive integer.",
          },
        ],
        isError: true,
      };
    }

    try {
      const bundle = synthesizeReviewBundle(prNumber);
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify(bundle, null, 2),
          },
        ],
        isError: false,
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text" as const,
            text: `Error analyzing PR #${prNumber}: ${String(error)}`,
          },
        ],
        isError: true,
      };
    }
  }

  return {
    content: [
      {
        type: "text" as const,
        text: `Unknown tool: ${name}`,
      },
    ],
    isError: true,
  };
});

// ─────────────────────────────────────────────────────────────────────────────
// Server transport
// ─────────────────────────────────────────────────────────────────────────────

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("PhoenixEngine Review Bundle MCP server started.");
}

main().catch(console.error);
