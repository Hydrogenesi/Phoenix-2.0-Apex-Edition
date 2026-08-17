/**
 * PhoenixEngine WebSocket client — phoenix.cockpit.v1 protocol.
 *
 * Supports: connect → hello → subscribe → receive events → ping/pong.
 * Auto-reconnects on unexpected close (exponential backoff, max 30 s).
 */

import {
  SUBPROTOCOL,
  PROTOCOL_VERSION,
  helloFrame,
  subscribeFrame,
  pongFrame,
} from "./protocol";

export type WSMessage = Record<string, unknown>;
export type MessageHandler = (msg: WSMessage) => void;

const MAX_BACKOFF_MS = 30_000;

export class CockpitWSClient {
  private ws: WebSocket | null = null;
  private runId: string;
  private url: string;
  private handlers: MessageHandler[] = [];
  private reconnectDelay = 1_000;
  private closed = false;

  constructor(runId: string, baseUrl?: string) {
    this.runId = runId;
    const wsBase =
      baseUrl ??
      (location.protocol === "https:" ? "wss://" : "ws://") +
        location.host;
    this.url = `${wsBase}/ws/cockpit?run_id=${encodeURIComponent(runId)}`;
  }

  connect(): void {
    this.closed = false;
    this._open();
  }

  disconnect(): void {
    this.closed = true;
    this.ws?.close(1000, "client disconnect");
    this.ws = null;
  }

  onMessage(handler: MessageHandler): () => void {
    this.handlers.push(handler);
    return () => {
      this.handlers = this.handlers.filter((h) => h !== handler);
    };
  }

  send(msg: Record<string, unknown>): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(msg));
    }
  }

  subscribe(topics: string[]): void {
    this.send(subscribeFrame(topics));
  }

  private _open(): void {
    const ws = new WebSocket(this.url, SUBPROTOCOL);
    this.ws = ws;

    ws.onopen = () => {
      this.reconnectDelay = 1_000;
      this.send(
        helloFrame(`ui-${Math.random().toString(36).slice(2, 8)}`)
      );
    };

    ws.onmessage = (ev) => {
      let msg: WSMessage;
      try {
        msg = JSON.parse(ev.data) as WSMessage;
      } catch {
        return;
      }
      // Respond to ping automatically
      if (msg.type === "ping") {
        this.send(pongFrame());
        return;
      }
      for (const h of this.handlers) h(msg);
    };

    ws.onerror = () => {
      // onclose will handle reconnect
    };

    ws.onclose = (ev) => {
      if (this.closed || ev.code === 1000) return;
      setTimeout(() => {
        this.reconnectDelay = Math.min(
          this.reconnectDelay * 2,
          MAX_BACKOFF_MS
        );
        this._open();
      }, this.reconnectDelay);
    };
  }

  get runIdValue(): string {
    return this.runId;
  }

  /** Exposed for tests / diagnostics only. */
  get _protocolVersion(): string {
    return PROTOCOL_VERSION;
  }
}
