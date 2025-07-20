import tkinter as tk
from tkinter import messagebox
from pypresence import Presence
import time
import threading
import os
import json
import webbrowser

class DiscordRPCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DS RPC")
        self.root.configure(bg="#2e2e2e")
        self.rpc = None
        self.connected = False

        self.config_path = os.path.join(os.path.expanduser('~'), 'Documents', 'discord_rpc_config.json')

        label_font = ("Segoe UI", 11, "bold")
        entry_font = ("Segoe UI", 11)
        button_font = ("Segoe UI", 10, "bold")
        fg_color = "#f0f0f0"
        bg_color = "#2e2e2e"
        entry_bg = "#3e3e3e"
        btn_color = "#4e8cff"

        header = tk.Label(root, text="Discord Custom Activity Setup", font=("Segoe UI", 14, "bold"), fg=fg_color, bg=bg_color)
        header.pack(pady=(10, 15))

        frame = tk.Frame(root, bg=bg_color)
        frame.pack(padx=20, pady=5)

        fields = [
            ("Client ID:", "client_id_entry"),
            ("Details:", "details_entry"),
            ("State:", "state_entry"),
            ("Large Image Key:", "large_image_key_entry"),
            ("Large Image Text:", "large_image_text_entry"),
            ("Small Image Key:", "small_image_key_entry"),
            ("Small Image Text:", "small_image_text_entry"),
        ]

        self.entries = {}
        for i, (label, attr_name) in enumerate(fields):
            tk.Label(frame, text=label, font=label_font, fg=fg_color, bg=bg_color).grid(row=i, column=0, sticky="e", pady=4)
            entry = tk.Entry(frame, font=entry_font, bg=entry_bg, fg=fg_color, insertbackground=fg_color, width=32, relief="flat")
            entry.grid(row=i, column=1, pady=4, padx=8)
            self.entries[attr_name] = entry

        button_frame = tk.Frame(root, bg=bg_color)
        button_frame.pack(pady=15)

        self.start_button = tk.Button(
            button_frame, text="▶ Connect & Update", font=button_font, bg=btn_color, fg="white",
            activebackground="#366ecc", relief="flat", padx=10, pady=5, command=self.start_rpc)
        self.start_button.pack(side="left", padx=10)

        self.stop_button = tk.Button(
            button_frame, text="■ Disconnect", font=button_font, bg="#cc4e4e", fg="white",
            activebackground="#a13c3c", relief="flat", padx=10, pady=5, command=self.stop_rpc, state=tk.DISABLED)
        self.stop_button.pack(side="left", padx=10)

        github_url = "https://github.com/d8-rpK/ds-custom-activity"
        github_button = tk.Button(
            root, text="💡 Help / GitHub", font=("Segoe UI", 9, "bold"),
            bg="#444", fg="white", activebackground="#555", relief="flat", padx=5, pady=3,
            command=lambda: webbrowser.open_new(github_url))
        github_button.pack(pady=(5, 10))

        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for key, entry in self.entries.items():
                        entry.insert(0, data.get(key.replace("_entry", ""), ""))
                print("✅ Config loaded from JSON.")
            except Exception as e:
                print(f"Error loading JSON config: {e}")

    def save_config(self, data):
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print("💾 Config saved to JSON.")
        except Exception as e:
            print(f"Error saving JSON config: {e}")

    def start_rpc(self):
        data = { key.replace("_entry", ""): entry.get().strip() for key, entry in self.entries.items() }

        if not data["client_id"]:
            messagebox.showerror("Error", "Please enter Client ID!")
            return

        self.save_config(data)

        def run_rpc():
            try:
                if not self.connected:
                    self.rpc = Presence(data["client_id"])
                    self.rpc.connect()
                    self.connected = True
                    self.stop_button.config(state=tk.NORMAL)
                    print("✅ Connected to Discord RPC!")

                self.rpc.update(
                    details=data["details"],
                    state=data["state"],
                    start=time.time(),
                    large_image=data["large_image_key"] or None,
                    large_text=data["large_image_text"] or None,
                    small_image=data["small_image_key"] or None,
                    small_text=data["small_image_text"] or None
                )
                print("✨ RPC updated!")
                messagebox.showinfo("Success", "RPC updated successfully!")
            except Exception as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", str(e))

        threading.Thread(target=run_rpc).start()

    def stop_rpc(self):
        if self.rpc and self.connected:
            try:
                self.rpc.clear()
                self.rpc.close()
                print("🛑 RPC disconnected.")
            except Exception as e:
                print(f"Error while disconnecting: {e}")
            finally:
                self.connected = False
                self.stop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = DiscordRPCApp(root)
    root.mainloop()
