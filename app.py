import tkinter as tk
import threading
import random
import time
import keyboard
import mouse
import ctypes
import os

last_activity_time = time.time()
window_active = False
root = None
alt_pressed = False

def update_last_activity(event=None):
    global last_activity_time
    last_activity_time = time.time()

def monitor_idle_time():
    global window_active
    while True:
        if not window_active and time.time() - last_activity_time > 5:  # idle 5 secs for demo
            start_prank_window()
        time.sleep(1)

def start_prank_window():
    global root, window_active, alt_pressed
    window_active = True
    alt_pressed = False

    root = tk.Tk()
    root.title("💀 System Locked 💀")
    root.attributes('-fullscreen', True)
    root.configure(bg='black')
    root.attributes('-topmost', True)
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    root.config(cursor="none")

    label = tk.Label(root, text="💀 SYSTEM LOCKED 💀\nPress ALT + SHIFT + F to unlock",
                     font=("Segoe UI", 36, "bold"), fg="lime", bg="black")
    label.pack(expand=True)

    threading.Thread(target=move_window, daemon=True).start()
    threading.Thread(target=check_exit_hotkey, daemon=True).start()
    threading.Thread(target=key_blocker, daemon=True).start()

    disable_task_switching()
    root.mainloop()

def move_window():
    global root
    prank_label = tk.Label(root, text="😈 You left your system idle 😈",
                           font=("Segoe UI", 26, "bold"), fg="red", bg="black")
    prank_label.place(x=0, y=0)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    dx, dy = 5, 5
    x, y = 100, 100

    while window_active:
        x += dx
        y += dy

        if x <= 0 or x >= screen_width - 400:
            dx = -dx
        if y <= 0 or y >= screen_height - 50:
            dy = -dy

        prank_label.place(x=x, y=y)
        time.sleep(0.02)

def key_blocker():
    def on_key(event):
        global alt_pressed
        if event.event_type == 'down':
            if event.name == 'alt':
                alt_pressed = True
            else:
                if not alt_pressed:
                    os.system('rundll32.exe user32.dll,LockWorkStation')
                    return False

    keyboard.hook(on_key)

def check_exit_hotkey():
    global window_active, root
    while window_active:
        if (keyboard.is_pressed('alt') and
            keyboard.is_pressed('shift') and
            keyboard.is_pressed('f')):
            enable_task_switching()
            window_active = False
            root.destroy()
            break
        time.sleep(0.05)

def disable_task_switching():
    user32 = ctypes.WinDLL('user32')
    user32.BlockInput(True)

def enable_task_switching():
    user32 = ctypes.WinDLL('user32')
    user32.BlockInput(False)

def listen_activity():
    keyboard.on_press(update_last_activity)
    mouse.hook(lambda e: update_last_activity())
    keyboard.wait()

if __name__ == "__main__":
    threading.Thread(target=monitor_idle_time, daemon=True).start()
    threading.Thread(target=listen_activity, daemon=True).start()
    while True:
        time.sleep(1)
