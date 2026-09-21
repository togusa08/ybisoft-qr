# Ybisoft QR Tool — Scan & Generate

A lightweight Windows overlay tool with two floating widgets:
- **Scan**: capture your screen and decode a QR code from it
- **Generate**: type or paste text/a link and generate a QR code image

Everything happens in memory — no screenshots or generated images are saved to disk. Results are copied straight to your clipboard.

## Features

- 🔍 Capture your screen and decode any visible QR code
- 🧩 Generate a QR code from typed text or a link
- 📋 Copy scanned text or the generated QR image directly to the clipboard
- ⌨️ Global hotkey (`Ctrl+Shift+Q`) to show/hide both widgets
- 🖤 Simple dark-themed floating widgets, no transparency

## Requirements

- Windows
- Python 3.9+

```bash
pip install mss opencv-python qrcode[pil] pillow pywin32 keyboard
```

## Usage

```bash
python qr_tool_v2.py
```

- Click **Capture & Scan** to grab your screen and decode any QR code on it
- Click **Copy Result** to copy the decoded text to your clipboard
- Type text/a link into the Generate widget and click **Generate QR**
- Click **Copy Image** to copy the generated QR code image to your clipboard
- Press `Ctrl+Alt+Q` anytime to show or hide both widgets

> Note: the global hotkey may require running the script as Administrator to be caught while other elevated applications have focus.

## How it works

- Screen capture uses [`mss`](https://pypi.org/project/mss/) for fast, in-memory screenshots
- QR decoding uses OpenCV's `cv2.QRCodeDetector`
- QR generation uses the [`qrcode`](https://pypi.org/project/qrcode/) library
- Copying the generated image to the clipboard uses `pywin32`'s `win32clipboard`, since Windows only accepts images in `CF_DIB` (device-independent bitmap) format
