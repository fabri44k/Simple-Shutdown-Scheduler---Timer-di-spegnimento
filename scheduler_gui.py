from datetime import datetime, timedelta
import os
import time
import tkinter as tk
from threading import Thread
from win10toast import ToastNotifier

def show_notification():
    toast.show_toast(
    "Avviso",
    "1 Minuto allo spegnimento del pc",
    duration = 5,
    threaded = True,
    )

def get_remaining_time(hour, minute, sec):
    now = datetime.now()
    input_time = now.replace(hour = hour, minute = minute, second = sec)
    diff = input_time - now
    return diff.total_seconds()

def start_shutdown():
    global input_text
    input_text = name.get()
    while True:
        try:
            ore, minuti = map(int, input_text.split('.'))
            break
        except ValueError:
            log_text.delete(1.0, tk.END)
            log_text.insert(tk.END, "Input non valido")
            return
    while True:
        try:
            sec_value = str(int(get_remaining_time(ore, minuti, 0)))
            break
        except ValueError:
            log_text.delete(1.0, tk.END)
            log_text.insert(tk.END, "Input non valido")
            return
    
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    
    COMMAND = "shutdown /s /t " + sec_value
    os.system(COMMAND)
    
    
    def countdown():
        for i in range(int(sec_value) - 2, 0, -1):
            remaining_time = f"Ore: {i // 3600} Minuti: {(i % 3600) // 60} Secondi: {i % 60}"
            if i == 60:
                show_notification()
            if i == 10:
                show_notification()
            log_text.delete(1.0, tk.END)
            log_text.insert(tk.END, remaining_time)
            time.sleep(1)
    countdown_thread = Thread(target = countdown)
    countdown_thread.start()

def stop_shutdown():
    os.system("shutdown /a")
    time.sleep(2)
    window.destroy()

toast = ToastNotifier()
window = tk.Tk()
window.title("Scheduler")
label = tk.Label(text="Seleziona l'orario di spegnimento (formato ore.minuti) ", font=("Arial", 12))
name = tk.StringVar()
text_field = tk.Entry(window, width = 10, textvariable = name)
start_button = tk.Button(window, text = " Avvia ", command = start_shutdown)
stop_button = tk.Button(window, text = " Stop ", command = stop_shutdown, state = tk.DISABLED)
log_text = tk.Text(window, height = 2, width = 30, font=("Arial", 12))
log_text.grid(column=0, row=2, columnspan=2, padx=10, pady=10)
label.grid(column = 0, row = 0)
text_field.grid(column = 1, row = 0)
start_button.grid(column = 0, row = 1)
stop_button.grid(column = 1, row = 1, padx = 20)
x_center = (window.winfo_screenwidth() - window.winfo_reqwidth()) / 2
y_center = (window.winfo_screenheight() - window.winfo_reqheight()) / 2
window.geometry("+%d+%d" % (x_center, y_center))
window.mainloop()

