"""Minimal Ollama HTTP client.

Ollama is local-only in this project. The client calls /api/generate directly
and yields streamed response text chunks for progressive terminal output.
"""

from collections.abc import Iterator
import json

import httpx


class OllamaError(RuntimeError):
    """Raised when local Ollama cannot generate an explanation."""


class OllamaClient:
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "qwen3-coder:30b",
        timeout_seconds: float = 60.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds

    def stream_generate(self, prompt: str) -> Iterator[str]:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": 0.2,
            },
        }

        try:
            with httpx.stream(
                "POST",
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout_seconds,
            ) as response:
                if response.status_code == 404:
                    raise OllamaError(
                        f"Ollama model '{self.model}' was not found. "
                        f"Run: ollama pull {self.model}"
                    )
                response.raise_for_status()

                for line in response.iter_lines():
                    if not line:
                        continue
                    try:
                        item = json.loads(line)
                    except json.JSONDecodeError as exc:
                        raise OllamaError(
                            f"Ollama returned invalid streaming JSON: {line!r}"
                        ) from exc

                    if "error" in item:
                        message = item["error"]
                        if "model" in message.lower() and "not found" in message.lower():
                            raise OllamaError(
                                f"Ollama model '{self.model}' is missing. "
                                f"Run: ollama pull {self.model}"
                            )
                        raise OllamaError(f"Ollama returned an error: {message}")

                    chunk = item.get("response", "")
                    if chunk:
                        yield chunk

                    if item.get("done"):
                        break

        except httpx.ConnectError as exc:
            raise OllamaError(
                "Could not connect to local Ollama at "
                f"{self.base_url}. Start it with: ollama serve"
            ) from exc
        except httpx.TimeoutException as exc:
            raise OllamaError(
                "Timed out while waiting for Ollama. Check that Ollama is running "
                f"and that model '{self.model}' is available."
            ) from exc
        except httpx.HTTPStatusError as exc:
            raise OllamaError(
                f"Ollama HTTP request failed with status {exc.response.status_code}: "
                f"{exc.response.text}"
            ) from exc
