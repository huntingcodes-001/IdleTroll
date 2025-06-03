import tkinter as tk
import threading
import random
import time
import keyboard
import mouse

last_activity_time = time.time()
window_active = False
root = None

def update_last_activity(event=None):
    global last_activity_time
    last_activity_time = time.time()

def monitor_idle_time():
    global window_active
    while True:
        if not window_active and time.time() - last_activity_time > 30:  # 5 minutes
            start_prank_window()
        time.sleep(1)

def move_window():
    global root
    while window_active:
        x = root.winfo_x()
        y = root.winfo_y()

        target_x = random.randint(0, root.winfo_screenwidth() - 300)
        target_y = random.randint(0, root.winfo_screenheight() - 100)

        while abs(x - target_x) > 2 or abs(y - target_y) > 2:
            if x < target_x:
                x += min(5, target_x - x)
            elif x > target_x:
                x -= min(5, x - target_x)

            if y < target_y:
                y += min(5, target_y - y)
            elif y > target_y:
                y -= min(5, y - target_y)

            root.geometry(f"+{x}+{y}")
            root.update()
            time.sleep(0.01)

def start_prank_window():
    global root, window_active
    window_active = True
    root = tk.Tk()
    root.title("Microsoft Windows")
    root.geometry("300x100")
    root.resizable(False, False)
    root.attributes('-topmost', True)
    root.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable close

    label = tk.Label(root, text="LOL", font=("Segoe UI", 14))
    label.pack(pady=20)

    threading.Thread(target=move_window, daemon=True).start()
    threading.Thread(target=check_exit_hotkey, daemon=True).start()

    root.mainloop()

def check_exit_hotkey():
    global window_active, root
    while window_active:
        if keyboard.is_pressed('alt') and keyboard.is_pressed('shift') and keyboard.is_pressed('f'):
            window_active = False
            root.destroy()
            break
        time.sleep(0.1)

def listen_activity():
    keyboard.on_press(update_last_activity)
    mouse.on_move(lambda e: update_last_activity())
    mouse.on_click(lambda e: update_last_activity())
    mouse.on_wheel(lambda e: update_last_activity())
    keyboard.wait()  # Keeps thread alive

if __name__ == "__main__":
    threading.Thread(target=monitor_idle_time, daemon=True).start()
    threading.Thread(target=listen_activity, daemon=True).start()
    while True:
        time.sleep(1)
