
import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
import os
from datetime import datetime

root = tk.Tk()
root.title("File Integrity Monitor")
root.geometry("850x650")
root.configure(bg="#101722")
root.resizable(False, False)

selected_file = ""
original_hash = ""
monitoring = False
check_count = 0
alert_count = 0

def calculate_hash(path):
    sha256 = hashlib.sha256()
    with open(path, "rb") as file:
        for data in iter(lambda: file.read(4096), b""):
            sha256.update(data)
    return sha256.hexdigest()

def log(message):
    activity_box.config(state="normal")
    activity_box.insert("end", datetime.now().strftime("%H:%M:%S") + "  " + message + "\n")
    activity_box.see("end")
    activity_box.config(state="disabled")

def select_file():
    global selected_file
    path = filedialog.askopenfilename(title="Select a file to monitor")
    if path:
        selected_file = path
        file_label.config(text=os.path.basename(path), fg="#4DD0E1")
        path_label.config(text=path)
        status_label.config(text="FILE SELECTED", fg="#4DD0E1")
        log("Selected: " + os.path.basename(path))

def register_hash():
    global original_hash, monitoring, check_count, alert_count
    if not selected_file:
        messagebox.showwarning("No file", "Please select a file first.")
        return
    try:
        original_hash = calculate_hash(selected_file)
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "stored_hash.txt"), "w") as file:
            file.write(original_hash)
        monitoring = False
        check_count = 0
        alert_count = 0
        checks_label.config(text="0")
        alerts_label.config(text="0")
        original_box.config(state="normal")
        original_box.delete("1.0", "end")
        original_box.insert("1.0", original_hash)
        original_box.config(state="disabled")
        current_box.config(state="normal")
        current_box.delete("1.0", "end")
        current_box.insert("1.0", original_hash)
        current_box.config(state="disabled")
        status_label.config(text="BASELINE REGISTERED", fg="#49D99B")
        log("Trusted SHA-256 baseline registered.")
        log("Keep stored_hash.txt protected.")
    except (OSError, PermissionError) as error:
        messagebox.showerror("File error", str(error))

def check_integrity():
    global check_count, monitoring, alert_count
    if not monitoring:
        return
    try:
        current_hash = calculate_hash(selected_file)
        check_count += 1
        checks_label.config(text=str(check_count))
        current_box.config(state="normal")
        current_box.delete("1.0", "end")
        current_box.insert("1.0", current_hash)
        current_box.config(state="disabled")

        if current_hash != original_hash:
            monitoring = False
            alert_count += 1
            alerts_label.config(text=str(alert_count))
            status_label.config(text="MODIFICATION DETECTED", fg="#FF6262")
            log("Possible file modification detected.")
            messagebox.showwarning("Security Alert", "Possible file modification detected.")
            return
        status_label.config(text="INTEGRITY VERIFIED", fg="#49D99B")
        log("File integrity verified.")
    except OSError as error:
        monitoring = False
        status_label.config(text="FILE ACCESS ERROR", fg="#FF6262")
        log("Could not read file: " + str(error))
        return
    root.after(5000, check_integrity)

def start_monitoring():
    global monitoring
    if not selected_file or not original_hash:
        messagebox.showwarning("Setup required", "Select a file and register its original hash first.")
        return
    if not os.path.isfile(selected_file):
        messagebox.showerror("File missing", "The selected file no longer exists.")
        return
    if monitoring:
        return
    monitoring = True
    status_label.config(text="MONITORING...", fg="#4DD0E1")
    log("Monitoring started. Checks run every 5 seconds.")
    check_integrity()

def stop_monitoring():
    global monitoring
    monitoring = False
    status_label.config(text="MONITORING STOPPED", fg="#F4BD50")
    log("Monitoring stopped.")

def make_label(parent, text, color="#8FA7BE", size=10, bold=False):
    return tk.Label(parent, text=text, bg="#101722", fg=color, font=("Segoe UI", size, "bold" if bold else "normal"))

header = tk.Frame(root, bg="#101722")
header.pack(fill="x", padx=28, pady=(22, 14))
tk.Label(header, text="🛡", font=("Segoe UI Emoji", 28), bg="#101722", fg="#4DD0E1").pack(side="left", padx=(0, 12))
tk.Label(header, text="FILE INTEGRITY MONITOR", font=("Segoe UI", 20, "bold"), bg="#101722", fg="#E5F3FF").pack(anchor="w")
make_label(header, "SHA-256  •  INTEGRITY PROTECTION", size=9).pack(anchor="w")

metrics = tk.Frame(root, bg="#101722")
metrics.pack(fill="x", padx=28, pady=8)

def metric_card(title, value):
    card = tk.Frame(metrics, bg="#192536", padx=16, pady=12)
    card.pack(side="left", fill="both", expand=True, padx=(0, 10))
    make_label(card, title, size=9).pack(anchor="w")
    label = tk.Label(card, text=value, font=("Segoe UI", 20, "bold"), bg="#192536", fg="#FFFFFF")
    label.pack(anchor="w")
    return label

files_label = metric_card("SELECTED FILE", "01")
checks_label = metric_card("INTEGRITY CHECKS", "0")
alerts_label = metric_card("ALERTS", "0")

panel = tk.Frame(root, bg="#192536", padx=18, pady=14)
panel.pack(fill="x", padx=28, pady=10)
make_label(panel, "MONITORED FILE", size=9).pack(anchor="w")
file_label = tk.Label(panel, text="No file selected", bg="#192536", fg="#FFFFFF", font=("Segoe UI", 13, "bold"))
file_label.pack(anchor="w", pady=(5, 2))
path_label = tk.Label(panel, text="Choose an important file to begin.", bg="#192536", fg="#8FA7BE", font=("Segoe UI", 9), wraplength=750, justify="left")
path_label.pack(anchor="w")

buttons = tk.Frame(panel, bg="#192536")
buttons.pack(fill="x", pady=(12, 0))

def make_button(text, command, color):
    return tk.Button(buttons, text=text, command=command, bg=color, fg="white", activebackground=color, activeforeground="white", relief="flat", font=("Segoe UI", 10, "bold"), padx=14, pady=9, cursor="hand2")

make_button("Select File", select_file, "#087E9B").pack(side="left", padx=(0, 8))
make_button("Register Original Hash", register_hash, "#176B4D").pack(side="left", padx=(0, 8))
make_button("Start Monitoring", start_monitoring, "#2456A6").pack(side="left", padx=(0, 8))
make_button("Stop", stop_monitoring, "#6C3540").pack(side="left")

status_panel = tk.Frame(root, bg="#192536", padx=18, pady=12)
status_panel.pack(fill="x", padx=28, pady=8)
make_label(status_panel, "INTEGRITY STATUS", size=9).pack(anchor="w")
status_label = tk.Label(status_panel, text="READY — SELECT A FILE", bg="#192536", fg="#8FA7BE", font=("Segoe UI", 13, "bold"))
status_label.pack(anchor="w", pady=(4, 0))

hash_panel = tk.Frame(root, bg="#192536", padx=18, pady=12)
hash_panel.pack(fill="x", padx=28, pady=8)

make_label(hash_panel, "ORIGINAL SHA-256 HASH", size=9).pack(anchor="w")
original_box = tk.Text(hash_panel, height=1, bg="#101722", fg="#49D99B", font=("Consolas", 9), relief="flat", wrap="none")
original_box.pack(fill="x", pady=(4, 10))
original_box.config(state="disabled")

make_label(hash_panel, "CURRENT SHA-256 HASH", size=9).pack(anchor="w")
current_box = tk.Text(hash_panel, height=1, bg="#101722", fg="#4DD0E1", font=("Consolas", 9), relief="flat", wrap="none")
current_box.pack(fill="x", pady=(4, 0))
current_box.config(state="disabled")

log_panel = tk.Frame(root, bg="#192536", padx=18, pady=10)
log_panel.pack(fill="both", expand=True, padx=28, pady=(4, 18))
make_label(log_panel, "ACTIVITY LOG", size=9).pack(anchor="w")
activity_box = tk.Text(log_panel, height=4, bg="#101722", fg="#C8D6E5", font=("Consolas", 9), relief="flat", state="disabled")
activity_box.pack(fill="both", expand=True, pady=(6, 0))

root.mainloop()
