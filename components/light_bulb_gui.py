import tkinter as tk
import json

class LightBulbGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Light Bulb GUI")
        self.canvas = tk.Canvas(self, width=200, height=300, bg="white")
        self.canvas.pack()
        self.draw_bulb(off=True)
        self.update_light_status()

    def draw_bulb(self, off=True):
        self.canvas.delete("all")
        self.canvas.create_oval(75, 150, 125, 200, fill="gray", outline="black")
        self.canvas.create_oval(50, 50, 150, 150, fill="lightyellow", outline="black")
        if not off:
            self.canvas.create_oval(80, 70, 120, 110, outline="yellow", width=3, tags="glow")
            self.canvas.create_line(100, 80, 100, 120, fill="yellow", width=3)
            self.canvas.create_line(90, 95, 110, 95, fill="yellow", width=3)
            self.canvas.create_line(100, 100, 85, 105, fill="yellow", width=3)
            self.canvas.create_line(100, 100, 115, 105, fill="yellow", width=3)

    def check_light_command(self):
        try:
            with open("commands.json", "r") as f:
                commands = json.load(f)
                return commands.get("light", "OFF")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading commands.json: {e}")
            return "OFF"

    def update_light_status(self):
        if self.check_light_command() == "ON":
            self.draw_bulb(off=False)
        else:
            self.draw_bulb(off=True)
        self.after(1000, self.update_light_status)

if __name__ == "__main__":
    app = LightBulbGUI()
    app.mainloop()