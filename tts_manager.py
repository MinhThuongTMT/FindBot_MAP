from __future__ import annotations

import os
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional

# First, try to load the offline engine.  This works if the user has a Vietnamese
# voice installed in the OS (e.g. `Microsoft Hai` on Windows 10+ or any 3rd-party
# voice) and the `pyttsx3` package is available.
try:
    import pyttsx3  # type: ignore
except ImportError:  # pragma: no cover – will hit on systems without pyttsx3
    pyttsx3 = None  # type: ignore

# gTTS fallback – requires internet access.
try:
    from gtts import gTTS  # type: ignore
    from pygame import mixer  # Re-use pygame audio backend already initialised in the app
except ImportError:  # pragma: no cover
    gTTS = None  # type: ignore
    mixer = None  # type: ignore

class TTSManager:
    """High-level Vietnamese Text-To-Speech wrapper."""

    def __init__(self) -> None:
        self._engine: Optional[object] = None
        self._use_pyttsx3: bool = False
        self._initialized: bool = False

        # Attempt to initialise an offline voice first.
        if pyttsx3 is not None:
            try:
                engine = pyttsx3.init()
                found_vi = False
                for voice in engine.getProperty("voices"):
                    lang_list = getattr(voice, "languages", [])
                    # Normalise language codes to str for comparison
                    lang_list_str = [l.decode() if isinstance(l, bytes) else str(l) for l in lang_list]
                    if (
                        any(lang.lower().startswith("vi") for lang in lang_list_str)
                        or "vietnam" in voice.name.lower()
                        or "vi_" in voice.id.lower()
                    ):
                        engine.setProperty("voice", voice.id)
                        found_vi = True
                        break

                if found_vi:
                    # Reduce speaking rate a little for clarity.
                    rate = engine.getProperty("rate")
                    engine.setProperty("rate", int(rate * 0.9))
                    self._engine = engine
                    self._use_pyttsx3 = True
                    self._initialized = True
                else:
                    # No Vietnamese voice available -> dispose engine and fallback
                    engine.stop()
                    del engine
            except Exception as exc:  # pragma: no cover
                # Fallback will be attempted below.
                print(f"[TTS] pyttsx3 initialisation failed: {exc}", file=sys.stderr)

        # pyttsx3 not available or failed – try gTTS.
        if not self._initialized and gTTS is not None and mixer is not None:
            try:
                if not mixer.get_init():
                    mixer.init()
                # Nothing else to do now; we will generate mp3s on demand.
                self._use_pyttsx3 = False
                self._initialized = True
            except Exception as exc:  # pragma: no cover
                print(f"[TTS] pygame.mixer init failed for gTTS fallback: {exc}", file=sys.stderr)

        if not self._initialized:
            print(
                "[TTS] No available TTS backend. Please install 'pyttsx3' for offline "
                "usage or 'gTTS' & 'pygame' for online fallback.",
                file=sys.stderr,
            )

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def is_available(self) -> bool:
        """Return *True* if at least one backend is ready to use."""
        return self._initialized

    def speak(self, text: str) -> None:
        """Speak *text* in Vietnamese.  Falls back gracefully if no TTS available."""
        if not text:
            return

        if not self._initialized:
            # Nothing we can do – silently ignore to avoid crashing the app.
            return

        try:
            if self._use_pyttsx3 and self._engine is not None:
                # OFFLINE path.
                self._engine.say(text)  # type: ignore[attr-defined]
                self._engine.runAndWait()  # type: ignore[attr-defined]
            else:
                # ONLINE fallback using Google TTS.
                self._speak_with_gtts(text)
        except Exception as exc:  # pragma: no cover
            print(f"[TTS] Speaking failed: {exc}", file=sys.stderr)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _speak_with_gtts(self, text: str) -> None:
        if gTTS is None or mixer is None:
            return  # Should not happen as we guard earlier.

        temp_path: Optional[Path] = None
        try:
            tts = gTTS(text=text, lang="vi")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                temp_path = Path(tmp_file.name)
                tts.save(str(temp_path))

            sound = mixer.Sound(str(temp_path))
            channel = sound.play()
            # Wait until sound finishes – prevents premature deletion.
            while channel.get_busy():
                time.sleep(0.1)

        finally:
            # Clean up the temp file.
            try:
                if temp_path is not None and temp_path.exists():
                    os.unlink(temp_path)
            except Exception:
                pass 