# FINDBOT - NGON LUA PTIT

**He thong dinh vi sieu thi thong minh su dung Python, Pygame va cong nghe nhan dang giong noi**

---

## 1. Tong quan du an

FindBot la mot ung dung mo phong (game/simulation) giup nguoi dung tim duong ngan nhat den cac ke hang trong sieu thi 2D. He thong ket hop thuat toan A* pathfinding, nhan dang giong noi (STT) va tong hop giong noi (TTS) de tao trai nghiem tuong tac tu nhien.

---

## 2. Kien truc va thanh phan chinh

```
FindBot_Map/
├─ findbot_main.py          # Vong lap chinh, giao dien Pygame
├─ enhanced_pathfinding.py  # Thuat toan A* toi uu
├─ supermarket_board.py     # Layout sieu thi va du lieu ke hang
├─ stt_manager.py           # Speech-to-Text su dung SpeechRecognition + Vosk
├─ tts_manager.py           # Text-to-Speech su dung pyttsx3 hoac gTTS
├─ sound_manager.py         # Phat am thanh feedback bang Pygame mixer
├─ pathfinding.py           # A* co ban (tham khao)
└─ README.md
```

### 2.1 findbot_main.py
* Tao cua so Pygame 1280x720, ve ban do sieu thi va duong di.
* Nhan input ban phim / giong noi, goi EnhancedPathFinder de tinh toan lo trinh.
* Ket xuat huong dan dang van ban, doc bang TTS va hien thi tren man hinh.

### 2.2 EnhancedPathFinder
* Cai dat thuat toan A* voi heuristic Manhattan.
* Su dung `heapq` de duyet nut nhanh (O(V log V)).
* Ho tro tranh va cham ke hang, tuong va gioi han ban do.

### 2.3 STTManager
* Du dua tren thu vien `speech_recognition`.
* Ho tro 2 backend:
  * **Vosk offline** – mo hinh Vietnamese 22k nho (< 50 MB).
  * **Google Web Speech** – can ket noi Internet (du phong).
* Tra ve chuoi ASCII khong dau de de xu ly key mapping.

### 2.4 TTSManager
* Lua chon **pyttsx3 offline** (Windows SAPI, macOS NSSpeech, espeak) hoac **gTTS online**.
* Tu dong luu file .mp3 tam thoi va phat qua `pygame.mixer` de tranh dung dong thoi audio engine.

### 2.5 SoundManager
* Tao feedback "beep", "success" bang sine wave (`numpy` + `pygame.sndarray`).
* Co the tat/bat bang phim `M`.

---

## 3. Cong nghe su dung va cach tich hop

| Nhom | Thu vien | Muc dich | Cach su dung |
|------|----------|----------|--------------|
| Do hoa & Game Loop | **pygame** | Ve ban do, xu ly su kien, phat am thanh | `pip install pygame` – tao Surface, blit, update 60 FPS |
| Xu ly du lieu | **numpy** | Tao tin hieu am thanh sine wave, tinh toan ma tran | Duoc import trong `sound_manager.py` va `findbot_main.py` |
| Pathfinding | thu vien tieu chuan **heapq**, **math** | Hang doi uu tien, tinh khoang cach | Co san trong Python 3, khong can cai dat |
| STT | **speech_recognition**, **vosk** | Chuyen am thanh thanh chu | `speech_recognition.Recognizer().listen()` + `KaldiRecognizer` |
| TTS | **pyttsx3**, **gTTS** | Doc huong dan bang giong noi | Khoi tao engine va save/play mp3 |
| Am thanh | **pygame.mixer** | Phat file .wav / .mp3 | Khoi tao `pygame.mixer.init()` va `mixer.Sound.play()` |

*Moi thu vien deu duoc ghi ro trong file `requirements.txt` (tao o buoc cai dat).* 

---

## 4. Cai dat

```bash
# 1. Tao virtualenv (khuyen khich)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Cai dat phu thuoc
pip install -r requirements.txt

# 3. Tai model Vosk (lan dau tien)
mkdir -p models && cd models
curl -L -o vosk-model.zip "https://alphacephei.com/vosk/models/vosk-model-small-vi-0.3.zip"
unzip vosk-model.zip && rm vosk-model.zip
cd ..

# 4. Chay ung dung
python findbot_main.py
```

**Chu y:** Tren Windows, can cai Visual C++ Build Tools de build pyttsx3. Neu su dung gTTS thi can Internet.

---

## 5. Cach su dung nhanh

1. Khoi dong ung dung => Ban do sieu thi xuat hien.
2. Nhan phim so (1-9,0) hoac chu cai (Q-P) de chon ke hang.
3. Hoac bam phim `V` de kich hoat che do lenh giong noi, noi: "ke 3".
4. Bot tinh toan duong di, to mau vang va doc huong dan.
5. Bam `ESC` de huy, `M` de bat/tat am thanh.

---

## 6. Thong so ky thuat & hieu nang

* Thuat toan: 100% tim duong ngan nhat, 4 huong, heuristic Manhattan.
* Thoi gian tinh toan trung binh: < 1 ms / duong di (ban do 35x28).
* FPS: ~60 tren may tinh thong dung.
* RAM them: ~50 MB bao gom model Vosk.

---

## 7. Phat trien tuong lai

* Ho tro keo tha chuot de danh dau diem bat dau/ket thuc tuy y.
* Che do multiplayer – so sanh duong di giua nhieu nguoi.
* Tich hop database san pham voi gia, khuyen mai.
* Export huong dan thanh QR / PDF.

---

## 8. Dong gop

Pull request va issue rat duoc hoan nghenh!

1. Fork repository.
2. Tao nhanh moi: `git checkout -b feature/my-awesome-feature`.
3. Commit theo quy tac Conventional Commits.
4. Tao PR va mo ta ro rang.

---

## 💡 Nếu bạn thích dự án này, hãy ⭐️ trên GitHub nhé! 

### 📩 Liên hệ:  
[tranminhthuong08082003@gmail.com](mailto:tranminhthuong08082003@gmail.com)
