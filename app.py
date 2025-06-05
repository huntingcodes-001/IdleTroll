import tkinter as tk
import threading
import time
import keyboard
import mouse
import os

last_activity_time = time.time()
idle_timeout = 5
window_active = False
alt_pressed = False

def start_lock_screen():
    global lock_root, lock_label, window_active, dx, dy, x, y, alt_pressed

    window_active = True
    alt_pressed = False

    lock_root = tk.Tk()
    lock_root.title("💀 System Locked 💀")
    lock_root.attributes("-fullscreen", True)
    lock_root.configure(bg="#000000")
    lock_root.attributes("-topmost", True)
    lock_root.config(cursor="none")

    screen_width = lock_root.winfo_screenwidth()
    screen_height = lock_root.winfo_screenheight()

    lock_label = tk.Label(lock_root,
                          text="💀 SYSTEM LOCKED 💀\nPress ALT + SHIFT + F to Unlock",
                          fg="#00FF00", bg="#000000",
                          font=("Consolas", 48, "bold"),
                          justify="center")
    lock_label.place(relx=0.5, rely=0.5, anchor="center")

    x, y = screen_width // 3, screen_height // 3
    dx, dy = 5, 5

    threading.Thread(target=move_label, daemon=True).start()
    threading.Thread(target=focus_enforcer, daemon=True).start()
    threading.Thread(target=key_blocker, daemon=True).start()
    threading.Thread(target=exit_hotkey, daemon=True).start()

    lock_root.mainloop()

def move_label():
    global x, y, dx, dy, window_active
    while window_active:
        screen_width = lock_root.winfo_screenwidth()
        screen_height = lock_root.winfo_screenheight()

        x += dx
        y += dy

        if x <= 0 or x >= screen_width - 600:
            dx = -dx
        if y <= 0 or y >= screen_height - 200:
            dy = -dy

        lock_label.place(x=x, y=y)
        time.sleep(0.02)

def focus_enforcer():
    while window_active:
        try:
            lock_root.attributes("-topmost", True)
            lock_root.focus_force()
        except:
            pass
        time.sleep(0.05)

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

def exit_hotkey():
    global window_active
    while window_active:
        if keyboard.is_pressed('alt') and keyboard.is_pressed('shift') and keyboard.is_pressed('f'):
            window_active = False
            lock_root.destroy()
        time.sleep(0.05)

def listen_activity():
    global last_activity_time
    mouse.hook(lambda e: update_last_activity())
    keyboard.hook(lambda e: update_last_activity())

def update_last_activity():
    global last_activity_time
    last_activity_time = time.time()

def idle_check_loop():
    global last_activity_time
    while True:
        if time.time() - last_activity_time > idle_timeout:
            start_lock_screen()
            last_activity_time = time.time()
        time.sleep(1)

threading.Thread(target=listen_activity, daemon=True).start()
idle_check_loop()
