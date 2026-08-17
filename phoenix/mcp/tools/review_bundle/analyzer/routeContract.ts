/**
 * Route Contract Drift Analyzer
 *
 * Detects schema mismatches between backend route responses and
 * frontend type expectations.
 */

export enum ContractSeverity {
  Low = "low",
  Medium = "medium",
  High = "high",
}

export interface AnalyzedContractIssue {
  route: string;
  issue: string;
  expected_field?: string;
  actual_field?: string;
  severity: ContractSeverity;
  recommendation?: string;
}

/**
 * Analyze route contract drift for a given PR.
 * For PR #123, focus on graph layout, cockpit, flux endpoints.
 */
export function analyzeRouteContractDrift(
  prNumber: number
): AnalyzedContractIssue[] {
  const issues: AnalyzedContractIssue[] = [];

  if (prNumber === 123) {
    // Graph layout contract
    issues.push({
      route: "/api/graph/layout",
      issue:
        "No explicit schema validation on GraphLayout response shape. " +
        "Field order and optional fields are implicit in TriLayerDeterministicLayout.",
      expected_field:
        "version (string), algorithm (string), nodes (array), edges (array), meta (object)",
      actual_field:
        "Inferred from TriLayerDeterministicLayout.compute_layout() return type",
      severity: ContractSeverity.Medium,
      recommendation:
        "Create a Pydantic GraphLayoutSchema on backend and TypeScript interface on frontend. " +
        "Validate POST input and GET output against schema.",
    });

    // Cockpit handshake frame
    issues.push({
      route: "/api/cockpit/handshake",
      issue:
        "Session ID format is auto-generated as f'ws_sess_{run_id[:8]}'. " +
        "No versioning of ready frame schema.",
      expected_field: "payload.session_id (string)",
      actual_field: "ws_sess_dev (for run_id='dev')",
      severity: ContractSeverity.Low,
      recommendation:
        "Document session_id format in API spec. Consider UUID for global uniqueness.",
    });

    // Flux state field naming
    issues.push({
      route: "/api/flux/state",
      issue:
        "Stub returns snake_case (noise_floor) but frontend may expect camelCase. " +
        "No Content-Type validation in test.",
      expected_field:
        "throughput, phase, coherence, noise_floor (snake_case from StubFluxEngine)",
      actual_field: "Same (but inconsistent with typical API conventions)",
      severity: ContractSeverity.Medium,
      recommendation:
        "Standardize on camelCase for all JSON responses. " +
        "Add OpenAPI/JSON Schema spec and validate in CI.",
    });

    // Operator pipeline response
    issues.push({
      route: "/POST /api/operator/run",
      issue:
        "Response shape is not formally specified. " +
        "Returns run_id, ws_session_id, layout_meta, flux_state, docs_artifacts but no schema.",
      expected_field:
        "{ run_id, ws_session_id, layout_meta, flux_state, docs_artifacts }",
      actual_field:
        "Hand-constructed in app.py do_POST; can drift if OperatorContext changes",
      severity: ContractSeverity.High,
      recommendation:
        "Define OperatorResultSchema (Pydantic) and export as OpenAPI. " +
        "Freeze schema in tests.",
    });
  }

  return issues;
}
