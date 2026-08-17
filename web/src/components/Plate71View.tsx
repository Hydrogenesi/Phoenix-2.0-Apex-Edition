import { useCallback, useEffect, useRef, useState } from "react";

interface Plate71ViewProps {
  /** If provided, POST this layout to the SVG endpoint instead of using SAMPLE_GRAPH. */
  layout?: Record<string, unknown> | null;
  /** Poll interval in ms.  Set to 0 to disable polling. */
  pollMs?: number;
}

type LoadState = "idle" | "loading" | "ok" | "error";

/**
 * Fetches the Plate71 SVG from /api/plate71/svg and renders it inline.
 *
 * The backend's Plate71SVGBuilder escapes all user-supplied content via _esc(),
 * so it is safe to inject the server response via dangerouslySetInnerHTML.
 */
export function Plate71View({ layout = null, pollMs = 0 }: Plate71ViewProps) {
  const [svg, setSvg] = useState<string | null>(null);
  const [state, setState] = useState<LoadState>("idle");
  const [error, setError] = useState<string | null>(null);
  // Tracks the most-recent AbortController so the refresh button can abort
  // any in-progress fetch and start a fresh one.
  const ctrlRef = useRef<AbortController | null>(null);

  const fetchSvg = useCallback(
    async (signal?: AbortSignal) => {
      setState("loading");
      try {
        let res: Response;
        if (layout) {
          res = await fetch("/api/plate71/svg", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(layout),
            signal,
          });
        } else {
          res = await fetch("/api/plate71/svg", { signal });
        }
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const text = await res.text();
        setSvg(text);
        setState("ok");
        setError(null);
      } catch (err) {
        if ((err as { name?: string }).name === "AbortError") return;
        setError(err instanceof Error ? err.message : String(err));
        setState("error");
      }
    },
    [layout]
  );

  useEffect(() => {
    const ctrl = new AbortController();
    ctrlRef.current = ctrl;
    fetchSvg(ctrl.signal);
    let timerId: ReturnType<typeof setInterval> | undefined;
    if (pollMs > 0) {
      timerId = setInterval(() => fetchSvg(ctrl.signal), pollMs);
    }
    return () => {
      ctrl.abort();
      ctrlRef.current = null;
      if (timerId !== undefined) clearInterval(timerId);
    };
  }, [fetchSvg, pollMs]);

  function handleRefresh() {
    // Abort any ongoing fetch first, then start a new one with a fresh signal.
    ctrlRef.current?.abort();
    const ctrl = new AbortController();
    ctrlRef.current = ctrl;
    fetchSvg(ctrl.signal);
  }

  return (
    <div className="plate71-viewer">
      <button
        className="plate71-viewer__refresh"
        onClick={handleRefresh}
        title="Refresh SVG"
      >
        ↺ refresh
      </button>

      {state === "loading" && !svg && (
        <div className="plate71-viewer__loading">Loading Plate71…</div>
      )}

      {state === "error" && (
        <div className="plate71-viewer__error">⚠ {error}</div>
      )}

      {svg && (
        /* Server escapes all user content — safe to inject. */
        <div dangerouslySetInnerHTML={{ __html: svg }} />
      )}
    </div>
  );
}
