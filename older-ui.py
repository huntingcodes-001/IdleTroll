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
        if not window_active and time.time() - last_activity_time > 5:  # idle timeout
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

    # Matrix rain canvas
    canvas = tk.Canvas(root, bg='black', highlightthickness=0)
    canvas.pack(fill='both', expand=True)
    threading.Thread(target=matrix_rain, args=(canvas,), daemon=True).start()

    # Central glitch text
    glitch_label = tk.Label(root, text="💀 SYSTEM LOCKED 💀",
                            font=("Consolas", 42, "bold"),
                            fg="lime", bg="black")
    glitch_label.place(relx=0.5, rely=0.4, anchor='center')

    threading.Thread(target=glitch_text_effect, args=(glitch_label,), daemon=True).start()

    # Moving warning text
    threading.Thread(target=move_warning_text, args=(root,), daemon=True).start()
    threading.Thread(target=check_exit_hotkey, daemon=True).start()
    threading.Thread(target=key_blocker, daemon=True).start()

    disable_task_switching()
    root.mainloop()

def matrix_rain(canvas):
    letters = "abcdefghijklmnopqrstuvwxyz0123456789"
    font_size = 20
    cols = int(canvas.winfo_screenwidth() / font_size)
    drops = [0 for _ in range(cols)]

    while window_active:
        canvas.delete("matrix")
        for i in range(cols):
            char = random.choice(letters)
            x = i * font_size
            y = drops[i] * font_size

            canvas.create_text(x, y, text=char, fill="lime",
                               font=('Consolas', font_size, 'bold'), tags="matrix")

            drops[i] += 1
            if y > canvas.winfo_screenheight() and random.random() > 0.975:
                drops[i] = 0

        canvas.update()
        time.sleep(0.05)

def glitch_text_effect(label):
    glitch_colors = ['lime', 'green', 'red', 'cyan']
    while window_active:
        color = random.choice(glitch_colors)
        label.config(fg=color)
        time.sleep(0.1)

def move_warning_text(root):
    warning = tk.Label(root, text="⚠️ You left your system idle ⚠️",
                       font=("Consolas", 24, "bold"), fg="red", bg="black")
    warning.place(x=0, y=0)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    dx, dy = 4, 4
    x, y = 200, 150

    while window_active:
        x += dx
        y += dy

        if x <= 0 or x >= screen_width - 400:
            dx = -dx
        if y <= 0 or y >= screen_height - 50:
            dy = -dy

        warning.place(x=x, y=y)
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
