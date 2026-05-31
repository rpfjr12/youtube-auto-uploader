# gui.py
import tkinter as tk
import threading
import time
from logger import LOG_FILE

def tail_log(n=20):
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            return lines[-n:]
    except Exception:
        return ["No logs yet\n"]

def gui_loop():
    root = tk.Tk()
    root.title("YouTube Auto Uploader")
    root.geometry("700x400")
    txt = tk.Text(root, wrap="none")
    txt.pack(fill="both", expand=True)
    def refresh():
        while True:
            lines = tail_log(50)
            txt.delete("1.0", "end")
            txt.insert("end", "".join(lines))
            time.sleep(3)
    t = threading.Thread(target=refresh, daemon=True)
    t.start()
    root.mainloop()

if __name__ == "__main__":
    gui_loop()
