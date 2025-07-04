from __future__ import annotations

import sys
from typing import Optional

try:
    import speech_recognition as sr  # type: ignore
except ImportError:
    sr = None  # type: ignore

class STTManager:
    """High-level wrapper around SpeechRecognition for Vietnamese."""

    def __init__(self) -> None:
        if sr is None:
            print("[STT] speech_recognition package not available.", file=sys.stderr)
            self._available = False
            return

        try:
            self.recognizer = sr.Recognizer()  # type: ignore[arg-type]
            # Use default microphone; handle errors gracefully
            self.microphone = sr.Microphone()  # type: ignore[attr-defined]
            self._available = True
        except Exception as exc:
            print(f"[STT] Microphone init failed: {exc}", file=sys.stderr)
            self._available = False

    # ------------------------------------------------------------------
    def is_available(self) -> bool:
        return self._available

    def listen(self, prompt: str | None = None, timeout: int = 5) -> str:
        """Listen through the default mic and return recognised Vietnamese text."""
        if not self._available:
            return ""

        if prompt:
            print(prompt)
        try:
            with self.microphone as source:  # type: ignore
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)  # type: ignore[arg-type]
                audio = self.recognizer.listen(source, timeout=timeout)
            text = self.recognizer.recognize_google(audio, language="vi-VN")  # type: ignore[attr-defined]
            return text
        except Exception as exc:
            print(f"[STT] Recognition failed: {exc}", file=sys.stderr)
            return "" 