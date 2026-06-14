"""Small local web UI for AI inspection results.

This UI is intentionally lightweight. Kafbat UI shows Kafka topics/messages;
this page shows the deterministic findings and streamed Ollama explanation for
the same predefined demo transactions used by the producer.
"""

from __future__ import annotations

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from urllib.parse import parse_qs, urlparse

from pydantic import ValidationError

from banking_ai.config import load_settings
from banking_ai.graph import inspect_with_graph
from banking_ai.models import BankingTransaction
from banking_ai.ollama_client import OllamaClient, OllamaError
from banking_ai.producer import DEMO_TRANSACTIONS
from banking_ai.rules import inspect_transaction_rules


HTML_PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Banking AI Inspection Results</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f8fafc;
      --panel: #ffffff;
      --text: #111827;
      --muted: #4b5563;
      --line: #d1d5db;
      --accent: #0f766e;
      --warning: #b45309;
      --danger: #b91c1c;
      --ok: #15803d;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
    }
    header {
      padding: 24px 32px 16px;
      border-bottom: 1px solid var(--line);
      background: var(--panel);
    }
    h1 { margin: 0 0 8px; font-size: 24px; }
    p { margin: 0; color: var(--muted); }
    main {
      display: grid;
      grid-template-columns: minmax(280px, 360px) minmax(0, 1fr);
      gap: 20px;
      padding: 24px 32px;
    }
    section, aside {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
    }
    label { display: block; font-weight: 700; margin-bottom: 8px; }
    select, button {
      width: 100%;
      min-height: 40px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fff;
      color: var(--text);
      font: inherit;
    }
    button {
      margin-top: 12px;
      background: var(--accent);
      color: #fff;
      border-color: var(--accent);
      font-weight: 700;
      cursor: pointer;
    }
    button:disabled { opacity: .6; cursor: wait; }
    dl {
      display: grid;
      grid-template-columns: 120px 1fr;
      gap: 8px 12px;
      margin: 16px 0 0;
    }
    dt { color: var(--muted); }
    dd { margin: 0; font-weight: 600; }
    .status {
      display: inline-block;
      margin-top: 8px;
      padding: 4px 8px;
      border-radius: 999px;
      font-weight: 800;
      font-size: 13px;
    }
    .normal { color: var(--ok); background: #dcfce7; }
    .suspicious { color: var(--danger); background: #fee2e2; }
    ul { padding-left: 20px; }
    pre {
      white-space: pre-wrap;
      word-break: break-word;
      min-height: 220px;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #f9fafb;
      line-height: 1.45;
    }
    .hint { margin-top: 12px; font-size: 14px; color: var(--warning); }
    @media (max-width: 760px) {
      main { grid-template-columns: 1fr; padding: 16px; }
      header { padding: 20px 16px 12px; }
    }
  </style>
</head>
<body>
  <header>
    <h1>Banking AI Inspection Results</h1>
    <p>Choose a predefined transaction and stream the local Ollama explanation in the browser.</p>
  </header>
  <main>
    <aside>
      <label for="transaction">Demo transaction</label>
      <select id="transaction"></select>
      <button id="inspect">Inspect with local AI</button>
      <div id="transaction-details"></div>
      <p class="hint">Kafka messages are visible in Kafbat UI. This page focuses on the inspection result and streamed AI text.</p>
    </aside>
    <section>
      <h2>Inspection</h2>
      <div id="status"></div>
      <h3>Rule findings</h3>
      <ul id="findings"></ul>
      <h3>AI explanation</h3>
      <pre id="ai-output"></pre>
      <h3>Reviewer check</h3>
      <p id="reviewer-check"></p>
    </section>
  </main>
  <script>
    const select = document.querySelector("#transaction");
    const button = document.querySelector("#inspect");
    const details = document.querySelector("#transaction-details");
    const findings = document.querySelector("#findings");
    const status = document.querySelector("#status");
    const aiOutput = document.querySelector("#ai-output");
    const reviewerCheck = document.querySelector("#reviewer-check");
    let transactions = [];
    let source = null;

    function renderTransaction(tx) {
      details.innerHTML = `
        <dl>
          <dt>Account</dt><dd>${tx.account_id}</dd>
          <dt>Amount</dt><dd>${tx.amount} ${tx.currency}</dd>
          <dt>Merchant</dt><dd>${tx.merchant}</dd>
          <dt>Country</dt><dd>${tx.country}</dd>
          <dt>Type</dt><dd>${tx.transaction_type}</dd>
        </dl>
      `;
    }

    function renderFindings(items) {
      findings.innerHTML = "";
      if (!items.length) {
        findings.innerHTML = "<li>none</li>";
        return;
      }
      for (const item of items) {
        const li = document.createElement("li");
        li.textContent = `${item.rule_id}: ${item.reason}`;
        findings.appendChild(li);
      }
    }

    async function loadTransactions() {
      const response = await fetch("/api/transactions");
      transactions = await response.json();
      for (const tx of transactions) {
        const option = document.createElement("option");
        option.value = tx.transaction_id;
        option.textContent = `${tx.transaction_id} - ${tx.merchant} - ${tx.amount} ${tx.currency}`;
        select.appendChild(option);
      }
      renderTransaction(transactions[0]);
    }

    select.addEventListener("change", () => {
      const tx = transactions.find((item) => item.transaction_id === select.value);
      renderTransaction(tx);
    });

    button.addEventListener("click", () => {
      if (source) source.close();
      button.disabled = true;
      status.innerHTML = "";
      findings.innerHTML = "";
      aiOutput.textContent = "";
      reviewerCheck.textContent = "";

      source = new EventSource(`/api/inspect?transaction_id=${encodeURIComponent(select.value)}`);
      source.addEventListener("rules", (event) => {
        const data = JSON.parse(event.data);
        status.innerHTML = `<span class="status ${data.suspicious ? "suspicious" : "normal"}">${data.suspicious ? "SUSPICIOUS" : "NORMAL"}</span>`;
        renderFindings(data.findings);
      });
      source.addEventListener("token", (event) => {
        aiOutput.textContent += JSON.parse(event.data);
      });
      source.addEventListener("final", (event) => {
        const data = JSON.parse(event.data);
        reviewerCheck.textContent = data.reviewer_check;
        button.disabled = false;
        source.close();
      });
      source.addEventListener("error-message", (event) => {
        aiOutput.textContent += `\\n${JSON.parse(event.data)}`;
        button.disabled = false;
        source.close();
      });
      source.onerror = () => {
        button.disabled = false;
      };
    });

    loadTransactions();
  </script>
</body>
</html>
"""


class ResultsUiHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send_html()
            return
        if parsed.path == "/api/transactions":
            self._send_transactions()
            return
        if parsed.path == "/api/inspect":
            self._stream_inspection(parse_qs(parsed.query).get("transaction_id", [""])[0])
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def log_message(self, format: str, *args: object) -> None:
        print(f"results-ui: {format % args}")

    def _send_html(self) -> None:
        body = HTML_PAGE.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_transactions(self) -> None:
        body = json.dumps(DEMO_TRANSACTIONS).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _stream_inspection(self, transaction_id: str) -> None:
        try:
            transaction = _find_transaction(transaction_id)
        except ValueError as exc:
            self.send_error(HTTPStatus.NOT_FOUND, str(exc))
            return

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

        settings = load_settings()
        client = OllamaClient(settings.ollama_base_url, settings.ollama_model)
        findings = inspect_transaction_rules(transaction)
        self._send_event(
            "rules",
            {
                "suspicious": bool(findings),
                "findings": [finding.model_dump() for finding in findings],
            },
        )

        try:
            result = inspect_with_graph(
                transaction,
                ollama_client=client,
                stream_writer=lambda chunk: self._send_event("token", chunk),
            )
        except OllamaError as exc:
            self._send_event("error-message", f"Ollama error: {exc}")
            return

        self._send_event(
            "final",
            {
                "status": result.status,
                "reviewer_check": result.reviewer_check,
            },
        )

    def _send_event(self, event: str, data: object) -> None:
        payload = json.dumps(data)
        message = f"event: {event}\ndata: {payload}\n\n".encode("utf-8")
        self.wfile.write(message)
        self.wfile.flush()


def _find_transaction(transaction_id: str) -> BankingTransaction:
    for item in DEMO_TRANSACTIONS:
        if item["transaction_id"] == transaction_id:
            return BankingTransaction.model_validate(item)
    raise ValueError(f"Unknown transaction_id: {transaction_id}")


def run(host: str = "127.0.0.1", port: int = 8081) -> None:
    server = ThreadingHTTPServer((host, port), ResultsUiHandler)
    print(f"Results UI: http://{host}:{port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Results UI.")
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
