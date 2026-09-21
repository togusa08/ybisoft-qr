
import io
import threading
import numpy as np
import cv2
import qrcode
import keyboard
import win32clipboard # type: ignore 
from mss import MSS
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

HOTKEY = "ctrl+shift+q"

BG = "#000000"
FG = "#ffffff"
ACCENT = "#1a1a1a"
ACCENT_ACTIVE = "#333333"


def dark_theme():
    style = ttk.Style()
    style.theme_use("clam")  
    style.configure("Dark.TFrame", background=BG)
    style.configure("Dark.TLabel", background=BG, foreground=FG)
    style.configure("Dark.TButton", background=ACCENT, foreground=FG, borderwidth=0, focusthickness=0)
    style.map("Dark.TButton", background=[("active", ACCENT_ACTIVE)])
    style.configure("Dark.TEntry", fieldbackground=ACCENT, foreground=FG, insertcolor=FG, borderwidth=0)
    return style


def copy_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()


def copy_image_to_clipboard(img: Image.Image):
    output = io.BytesIO()
    img.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]  
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()


def capture_screen():
    with MSS() as sct:
        monitor = sct.monitors[1]  # primary monitor
        raw = sct.grab(monitor)
        img = np.array(raw)  
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img


def decode_qr(img):
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    return data if data else None


def scan_and_decode():
    scan_win.withdraw()
    gen_win.withdraw()
    scan_win.after(150, _do_scan)


def _do_scan():
    img = capture_screen()
    scan_win.deiconify()
    gen_win.deiconify()
    data = decode_qr(img)
    scan_result_var.set(data if data else "QR code not detected")


def copy_result():
    copy_clipboard(scan_result_var.get())


current_qr_image = None  


def generate_qr():
    global current_qr_image
    text = gen_entry.get().strip()
    if not text:
        return

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    current_qr_image = img

    display_img = img.resize((170, 170))
    photo = ImageTk.PhotoImage(display_img)
    gen_image_label.config(image=photo)
    gen_image_label.image = photo  


def copy_generated_image():
    if current_qr_image is not None:
        copy_image_to_clipboard(current_qr_image)


def scan_widget(root_):
    win = tk.Toplevel(root_)
    win.configure(bg=BG)
    win.attributes("-topmost", True)
    win.overrideredirect(True)  

    frame = ttk.Frame(win, style="Dark.TFrame", padding=12)
    frame.pack(fill="both", expand=True)

    global scan_result_var
    scan_result_var = tk.StringVar(value="Press 'Capture & Scan' to read a QR code")

    ttk.Label(frame, text="Scan", style="Dark.TLabel", font=("Segoe UI", 10, "bold")).grid(
        column=0, row=0, columnspan=2, sticky="w", pady=(0, 8)
    )
    ttk.Button(frame, text="x", width=3, style="Dark.TButton", command=win.withdraw).grid(
        column=2, row=0, sticky="e"
    )

    ttk.Label(frame, textvariable=scan_result_var, style="Dark.TLabel", wraplength=250).grid(
        column=0, row=1, columnspan=3, sticky="w", pady=(0, 10)
    )

    ttk.Button(frame, text="Capture && Scan", style="Dark.TButton", command=scan_and_decode).grid(
        column=0, row=2, sticky="w", padx=(0, 6)
    )
    ttk.Button(frame, text="Copy Result", style="Dark.TButton", command=copy_result).grid(
        column=1, row=2, sticky="w"
    )

    return win


def generate_widget(root_):
    win = tk.Toplevel(root_)
    win.configure(bg=BG)
    win.attributes("-topmost", True)
    win.overrideredirect(True)

    frame = ttk.Frame(win, style="Dark.TFrame", padding=12)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Generate", style="Dark.TLabel", font=("Segoe UI", 10, "bold")).grid(
        column=0, row=0, columnspan=2, sticky="w", pady=(0, 8)
    )
    ttk.Button(frame, text="x", width=3, style="Dark.TButton", command=win.withdraw).grid(
        column=2, row=0, sticky="e"
    )

    global gen_entry, gen_image_label
    gen_entry = ttk.Entry(frame, width=26, style="Dark.TEntry")
    gen_entry.grid(column=0, row=1, columnspan=3, sticky="we", pady=(0, 8))

    ttk.Button(frame, text="Generate QR", style="Dark.TButton", command=generate_qr).grid(
        column=0, row=2, sticky="w", padx=(0, 6)
    )
    ttk.Button(frame, text="Copy Image", style="Dark.TButton", command=copy_generated_image).grid(
        column=1, row=2, sticky="w"
    )

    gen_image_label = ttk.Label(frame, style="Dark.TLabel")
    gen_image_label.grid(column=0, row=3, columnspan=3, pady=(10, 0))

    return win


def toggle_widgets():
    for w in (scan_win, gen_win):
        if w.state() == "withdrawn":
            w.deiconify()
        else:
            w.withdraw()


def hotkey_callback():
    root.after(0, toggle_widgets)


def start_hotkey_listener():
    keyboard.add_hotkey(HOTKEY, hotkey_callback)


#main
root = tk.Tk()
root.withdraw()  

dark_theme()

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

scan_win = scan_widget(root)
scan_win.geometry(f"290x150+{screen_w - 620}+20")

gen_win = generate_widget(root)
gen_win.geometry(f"290x290+{screen_w - 310}+20")

threading.Thread(target=start_hotkey_listener, daemon=True).start()

root.mainloop()
