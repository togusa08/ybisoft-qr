# QR CODE Tool 

A lightweight Windows desktop utility for scanning and generating QR codes through widgets.

## Overview

QR Tool provides two independent floating widgets:

* **Scan** captures the current screen and decodes a  QR code
* **Generate** creates a QR code 

## Features

### Features

* **Screen Capture & Decode**
  
  * Detects and decodes visible QR codes using OpenCV.

* **QR Code Generation**

  * Converts typed text, URLs, or other data into QR code images on the fly.

* **Clipboard Integration**

  * Copies decoded QR text to the system clipboard.
  * Copies generated QR images to the Windows clipboard.

* **Global Hotkey**

  * `Ctrl + SHift + Q` toggles both widgets.
  
### Extra Features

* **Dual Floating Widgets**

  * Separate **Scan** and **Generate** panels.
  * Both remain above other windows.

* **Zero Disk Writes**

  * Screenshots are processed entirely in memory.
  * Generated QR images are kept in memory.
  * No temporary image files are required.

---

## System Slice

### Frontend

Built with Python's `tkinter` and `ttk`.

feature:

* Widget layout
* User input
* Dark theme styling
* Always-on-top floating windows
* QR preview rendering

### Backend

Stack:

* **mss** — screen capture
* **OpenCV (`cv2`)** — QR detection and decoding
* **Pillow (`PIL`)** — image conversion
* **qrcode** — QR code generation

### Data & Integration

* **pywin32 (`win32clipboard`)** — writing image data to the Windows clipboard
* **tkinter clipboard** — copying decoded text
* **keyboard** — registering and listening for the global hotkey

---

## Application Flow

### Scan Flow

```text
User presses "Scan"
        ↓
mss captures the screen
        ↓
Screenshot remains in memory
        ↓
Convert capture to NumPy array
        ↓
OpenCV QRCodeDetector
        ↓
QR data extracted
        ↓
Display decoded text
        ↓
Optional: Copy text to clipboard
```

### Generate Flow

```text
User enters text or URL
        ↓
qrcode generates QR image
        ↓
Image remains in memory
        ↓
Pillow handles image conversion
        ↓
Display QR preview
        ↓
Optional: Copy image to clipboard
```

### Toggle Flow

```text
Ctrl + Alt + Q
        ↓
Global keyboard listener
        ↓
Toggle Scan widget
        ↓
Toggle Generate widget
```

---

## Design Goals

simple,small,light-weight:
1. **In-memory processing** instead of temporary files.
2. **Computer vision** for practical QR detection.
3. **Native  integration** through the Windows clipboard.
4. **Global input ** through system-wide hotkeys.
5. **Floating  UI** using lightweight tkinter widgets.
