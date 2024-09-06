import tkinter as tk
import json
import math

class FanGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fan GUI")
        self.canvas = tk.Canvas(self, width=400, height=400, bg="white")
        self.canvas.pack()
        self.angle = 0
        self.animation_id = None
        self.update_fan_status()

    def draw_fan(self):
        self.canvas.delete("all")
        self.canvas.create_oval(150, 150, 250, 250, fill="gray", outline="black", width=2)
        self.canvas.create_oval(190, 190, 210, 210, fill="black")
        blade_length = 100
        for i in range(0, 360, 45):
            self.draw_fan_blade(i, blade_length)

    def draw_fan_blade(self, angle, length):
        rad = math.radians(angle + self.angle)
        x0 = 200
        y0 = 200
        x1 = x0 + length * math.cos(rad)
        y1 = y0 + length * math.sin(rad)
        self.canvas.create_line(x0, y0, x1, y1, width=8, fill="black")

    def update_fan(self):
        if self.check_fan_command() == "ON":
            self.angle = (self.angle + 5) % 360
            self.draw_fan()
            self.animation_id = self.canvas.after(50, self.update_fan)
        else:
            if self.animation_id:
                self.canvas.after_cancel(self.animation_id)
                self.animation_id = None
            self.draw_fan()

    def check_fan_command(self):
        try:
            with open("commands.json", "r") as f:
                commands = json.load(f)
                return commands.get("fan", "OFF")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading commands.json: {e}")
            return "OFF"

    def update_fan_status(self):
        self.update_fan()
        self.after(1000, self.update_fan_status)

if __name__ == "__main__":
    app = FanGUI()
    app.mainloop()
