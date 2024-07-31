import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import os
import json

def calculate_ehp(*args):
    try:
        defense = float(defense_entry.get())
        shield = float(shield_entry.get())
        hp = float(hp_entry.get())

        defense_constant = 15000
        min_practical_dr = 0.40  # Minimum practical damage reduction (40%)
        high_dr_threshold = 0.65  # Threshold for considering DR as high (65%)

        def calculate_damage_reduction(def_value):
            return def_value / (def_value + defense_constant)

        def calculate_ehp_value(def_value, hp_value):
            dr = calculate_damage_reduction(def_value)
            return hp_value / (1 - dr) + shield

        current_dr = calculate_damage_reduction(defense)
        current_ehp = calculate_ehp_value(defense, hp)

        # Calculate HP efficiency
        hp_increment = hp * 0.01  # 1% increment for calculation
        ehp_with_more_hp = calculate_ehp_value(defense, hp + hp_increment)
        hp_efficiency = (ehp_with_more_hp - current_ehp) / hp_increment

        # Calculate Defense efficiency
        def_increment = defense * 0.01  # 1% increment for calculation
        ehp_with_more_def = calculate_ehp_value(defense + def_increment, hp)
        def_efficiency = (ehp_with_more_def - current_ehp) / def_increment

        def get_recommendation():
            if current_dr < min_practical_dr:
                return f"Prioritize increasing Defense. Current damage reduction ({current_dr*100:.2f}%) is too low for effective survivability."
            elif current_dr < high_dr_threshold:
                if def_efficiency > hp_efficiency * 1.2:
                    return f"Focus on increasing Defense for better damage reduction and EHP gain. (Defense efficiency: {def_efficiency:.2f}, HP efficiency: {hp_efficiency:.2f})"
                else:
                    return f"Balance Defense and HP increases. Aim for higher damage reduction while also increasing HP. (Defense efficiency: {def_efficiency:.2f}, HP efficiency: {hp_efficiency:.2f})"
            else:
                if hp_efficiency > def_efficiency:
                    return f"Prioritize increasing HP. Your damage reduction is already high, so HP will provide better EHP gains. (HP efficiency: {hp_efficiency:.2f}, Defense efficiency: {def_efficiency:.2f})"
                else:
                    return f"Focus on increasing HP, but don't neglect Defense entirely. Your damage reduction is good, but more Defense still provides slightly better gains. (Defense efficiency: {def_efficiency:.2f}, HP efficiency: {hp_efficiency:.2f})"

        recommendation = get_recommendation()

        result_label.config(
            text=f"Damage Reduction: {current_dr*100:.2f}%\n"
                 f"Current EHP: {current_ehp:.0f}\n"
                 f"Defense Efficiency: {def_efficiency:.2f} EHP/point\n"
                 f"HP Efficiency: {hp_efficiency:.2f} EHP/point\n"
                 f"Recommendation: {recommendation}"
        )
    except ValueError:
        result_label.config(text="Please enter valid numbers")

def save_preset():
    class ThemedDialog(simpledialog.Dialog):
        def __init__(self, parent, title=None):
            self.custom_style = ttk.Style()
            super().__init__(parent, title)

        def body(self, master):
            self.geometry("300x150")
            master.configure(bg=bg_color)
            self.configure(bg=bg_color)

            # Configure styles for the dialog
            self.custom_style.configure("Dialog.TLabel", background=bg_color, foreground=fg_color)
            self.custom_style.configure("Dialog.TEntry", fieldbackground=entry_bg, foreground=fg_color)
            self.custom_style.configure("Dialog.TButton", background=button_bg, foreground=fg_color)
            self.custom_style.map("Dialog.TButton", background=[("active", highlight_bg)])

            ttk.Label(master, text="Enter a name for this preset:", style="Dialog.TLabel").grid(row=0, column=0, padx=5, pady=5)
            self.e1 = ttk.Entry(master, width=30, style="Dialog.TEntry")
            self.e1.grid(row=1, column=0, padx=5, pady=5)
            return self.e1  # initial focus

        def buttonbox(self):
            box = ttk.Frame(self, style="Dialog.TFrame")

            ok_button = ttk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE, style="Dialog.TButton")
            ok_button.pack(side=tk.LEFT, padx=5, pady=5)
            cancel_button = ttk.Button(box, text="Cancel", width=10, command=self.cancel, style="Dialog.TButton")
            cancel_button.pack(side=tk.LEFT, padx=5, pady=5)

            self.bind("<Return>", self.ok)
            self.bind("<Escape>", self.cancel)

            box.pack()

        def apply(self):
            self.result = self.e1.get()

    name = ThemedDialog(root, title="Save Preset").result
    if name:
        preset = {
            "defense": defense_entry.get(),
            "shield": shield_entry.get(),
            "hp": hp_entry.get(),
        }
        presets[name] = preset
        save_presets_to_file()
        update_preset_menu()

def load_preset(name):
    preset = presets.get(name)
    if preset:
        defense_entry.delete(0, tk.END)
        defense_entry.insert(0, preset["defense"])
        shield_entry.delete(0, tk.END)
        shield_entry.insert(0, preset["shield"])
        hp_entry.delete(0, tk.END)
        hp_entry.insert(0, preset["hp"])
        calculate_ehp()  # Automatically calculate when loading a preset

def save_presets_to_file():
    with open("presets.json", "w") as f:
        json.dump(presets, f)

def load_presets_from_file():
    global presets
    try:
        with open("presets.json", "r") as f:
            presets = json.load(f)
    except FileNotFoundError:
        presets = {}

def update_preset_menu():
    preset_menu["menu"].delete(0, "end")
    for name in presets:
        preset_menu["menu"].add_command(label=name, command=lambda n=name: load_preset(n))

root = tk.Tk()
root.title("Descendant EHP Calculator")

root.geometry("375x350")
root.resizable(False, False)

script_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(script_dir, "calculate.ico")
root.iconbitmap(icon_path)

style = ttk.Style()
style.theme_use("clam")

bg_color = "#2E2E2E"
fg_color = "#FFFFFF"
entry_bg = "#3E3E3E"
button_bg = "#4A4A4A"
highlight_bg = "#5A5A5A"

style.configure("TFrame", background=bg_color)
style.configure("TLabel", background=bg_color, foreground=fg_color)
style.configure("TEntry", fieldbackground=entry_bg, foreground=fg_color)
style.configure("TButton", background=button_bg, foreground=fg_color)
style.map("TButton", background=[("active", highlight_bg)])

style.configure("TMenubutton", background=button_bg, foreground=fg_color, arrowcolor=fg_color)
style.map("TMenubutton", background=[("active", highlight_bg)])

root.configure(bg=bg_color)

main_frame = ttk.Frame(root, padding="20 20 20 0")
main_frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(main_frame, text="Defense:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
defense_entry = ttk.Entry(main_frame)
defense_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

ttk.Label(main_frame, text="Shield:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
shield_entry = ttk.Entry(main_frame)
shield_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

ttk.Label(main_frame, text="HP:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
hp_entry = ttk.Entry(main_frame)
hp_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

result_label = ttk.Label(main_frame, text="Enter values to calculate EHP", wraplength=335)
result_label.grid(row=3, column=0, columnspan=2, pady=10)

save_preset_button = ttk.Button(main_frame, text="Save Preset", command=save_preset)
save_preset_button.grid(row=4, column=0, pady=10)

preset_var = tk.StringVar(root)
preset_var.set("Load Preset")
preset_menu = ttk.OptionMenu(main_frame, preset_var, "Load Preset")
preset_menu.grid(row=4, column=1, pady=10)

main_frame.columnconfigure(1, weight=1)

defense_entry.bind("<KeyRelease>", calculate_ehp)
shield_entry.bind("<KeyRelease>", calculate_ehp)
hp_entry.bind("<KeyRelease>", calculate_ehp)

load_presets_from_file()
update_preset_menu()

root.mainloop()