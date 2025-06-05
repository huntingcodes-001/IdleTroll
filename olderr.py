import tkinter as tk
import threading
import random
import time
import keyboard
import mouse
import ctypes

last_activity_time = time.time()
window_active = False
root = None

def update_last_activity(event=None):
    global last_activity_time
    last_activity_time = time.time()

def monitor_idle_time():
    global window_active
    while True:
        if not window_active and time.time() - last_activity_time > 3:  # 5 mins
            start_prank_window()
        time.sleep(1)

def start_prank_window():
    global root, window_active
    window_active = True
    root = tk.Tk()
    root.title("System Locked")
    root.attributes('-fullscreen', True)
    root.configure(bg='black')
    root.attributes('-topmost', True)
    root.protocol("WM_DELETE_WINDOW", lambda: None)

    label = tk.Label(root, text="💀 SYSTEM LOCKED 💀\nPress ALT + SHIFT + F to unlock",
                     font=("Segoe UI", 28), fg="lime", bg="black")
    label.pack(expand=True)

    prank_label = tk.Label(root, text="😈 You left your system idle 😈",
                           font=("Segoe UI", 20), fg="red", bg="black")
    prank_label.place(x=0, y=0)

    threading.Thread(target=move_label_smooth, args=(prank_label,), daemon=True).start()
    threading.Thread(target=check_exit_hotkey, daemon=True).start()

    disable_task_switching()

    root.mainloop()

def move_label_smooth(label):
    global root, window_active
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    w, h = 350, 50  # approx size of label

    x, y = random.randint(0, screen_w - w), random.randint(0, screen_h - h)
    dx, dy = 5, 5  # speed

    while window_active:
        x += dx
        y += dy

        if x <= 0 or x + w >= screen_w:
            dx = -dx
        if y <= 0 or y + h >= screen_h:
            dy = -dy

        label.place(x=x, y=y)
        time.sleep(0.01)

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
        time.sleep(0.1)

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
