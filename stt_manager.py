from __future__ import annotations

import sys
from typing import Optional
import os

try:
    import speech_recognition as sr  # type: ignore
except ImportError:
    sr = None  # type: ignore

# Optional offline Vosk recognizer (https://alphacephei.com/vosk/)
try:
    from vosk import Model, KaldiRecognizer  # type: ignore
except ImportError:  # pragma: no cover
    Model = None  # type: ignore
    KaldiRecognizer = None  # type: ignore

# Optional sounddevice for mic capture when PyAudio khong san sang
try:
    import sounddevice as sd  # type: ignore
except ImportError:  # pragma: no cover
    sd = None  # type: ignore

class STTManager:
    """High-level wrapper around SpeechRecognition for Vietnamese."""

    def __init__(self) -> None:
        """Khoi tao STTManager voi cac duong fallback linh hoat."""
        # Trang thai
        self._available: bool = False
        self._use_speech_recog: bool = False  # speech_recognition + PyAudio
        self._use_vosk: bool = False          # Vosk (offline)
        self._use_sounddevice: bool = False   # Thu am truc tiep bang sounddevice -> Vosk

        # ---------------------------------------------------------
        # 1) Thu speech_recognition + PyAudio neu kha dung
        # ---------------------------------------------------------
        if sr is not None:
            try:
                self.recognizer = sr.Recognizer()  # type: ignore[arg-type]
                self.microphone = sr.Microphone()  # type: ignore[attr-defined]
                self._use_speech_recog = True
                self._available = True
            except Exception as exc:
                print(f"[STT] PyAudio microphone init failed: {exc}", file=sys.stderr)

        # ---------------------------------------------------------
        # 2) Tai model Vosk (offline) – duoc su dung cho ca 2 nhan dang
        # ---------------------------------------------------------
        self.vosk_model = None  # type: ignore
        if Model is not None:
            model_path_candidates = [
                "models/vosk-vi",
                "vosk-model-small-vi-0.22",
                os.path.join(os.path.dirname(__file__), "vosk-model-small-vi-0.22"),
            ]
            for path in model_path_candidates:
                if os.path.isdir(path):
                    try:
                        self.vosk_model = Model(path)  # type: ignore
                        self._use_vosk = True
                        break
                    except Exception as exc:
                        print(f"[STT] Cannot load Vosk model from {path}: {exc}", file=sys.stderr)

        # ---------------------------------------------------------
        # 3) Neu chua co mic (PyAudio) nhung co Vosk + sounddevice, dung fallback
        # ---------------------------------------------------------
        if not self._available and self.vosk_model is not None and sd is not None:
            self._use_sounddevice = True
            self._available = True
            print("[STT] Using sounddevice + Vosk offline mode", file=sys.stderr)

        if not self._available:
            print("[STT] No microphone backend available (PyAudio or sounddevice).", file=sys.stderr)

    # ------------------------------------------------------------------
    def is_available(self) -> bool:
        return self._available

    def listen(self, prompt: str | None = None, timeout: int = 5) -> str:
        """Nghe tu microphone va tra ve chuoi tieng Viet."""
        if not self._available:
            return ""

        if prompt:
            print(prompt)

        # -----------------------------------------------
        # 1) speech_recognition + PyAudio (online/offline)
        # -----------------------------------------------
        if self._use_speech_recog:
            try:
                with self.microphone as source:  # type: ignore
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)  # type: ignore[arg-type]
                    audio = self.recognizer.listen(source, timeout=timeout)

                # Thu offline Vosk truoc neu model san sang
                if self._use_vosk and self.vosk_model is not None:
                    try:
                        import json
                        sample_rate = 16000
                        rec = KaldiRecognizer(self.vosk_model, sample_rate)  # type: ignore
                        raw_pcm = audio.get_raw_data(convert_rate=sample_rate, convert_width=2)  # type: ignore[attr-defined]
                        rec.AcceptWaveform(raw_pcm)
                        result = json.loads(rec.Result())
                        text = result.get("text", "")
                        if text:
                            return text
                    except Exception as exc:
                        print(f"[STT] Vosk recognition failed: {exc}", file=sys.stderr)

                # Fallback Google (can Internet)
                return self.recognizer.recognize_google(audio, language="vi-VN")  # type: ignore[attr-defined]
            except Exception as exc:
                print(f"[STT] Recognition failed: {exc}", file=sys.stderr)
                return ""

        # -----------------------------------------------
        # 2) Fallback: sounddevice + Vosk (offline)
        # -----------------------------------------------
        if self._use_sounddevice and self.vosk_model is not None:
            return self._listen_with_sounddevice(duration=timeout + 3)

        return ""

    # ------------------------------------------------------------------
    def _listen_with_sounddevice(self, duration: int = 6) -> str:
        """Record *duration* seconds with sounddevice and recognise via Vosk."""
        if sd is None or self.vosk_model is None:
            return ""
        try:
            import json
            sample_rate = 16000
            print("[STT] Recording via sounddevice...", file=sys.stderr)
            audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
            sd.wait()
            rec = KaldiRecognizer(self.vosk_model, sample_rate)  # type: ignore
            rec.AcceptWaveform(audio.tobytes())
            result = json.loads(rec.Result())
            return result.get("text", "")
        except Exception as exc:
            print(f"[STT] sounddevice recording failed: {exc}", file=sys.stderr)
            return "" 