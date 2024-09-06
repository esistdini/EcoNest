import tkinter as tk
import json
import time
import os

class PriceCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Price Calculator")
        self.label = tk.Label(self, text="Calculating Price...", font=("Arial", 16))
        self.label.pack(pady=20)
        self.price_per_hour = 1000
        self.start_time = time.time()
        self.load_runtime_data()
        self.update_price()

    def load_runtime_data(self):
        self.total_runtime = 0
        if os.path.exists("runtime_data.json"):
            try:
                with open("runtime_data.json", "r") as f:
                    data = json.load(f)
                    self.total_runtime = data.get("total_runtime", 0)
                    self.last_update_time = data.get("last_update_time", time.time())
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error reading runtime_data.json: {e}")
                self.last_update_time = time.time()
        else:
            self.last_update_time = time.time()

    def save_runtime_data(self):
        data = {
            "total_runtime": self.total_runtime,
            "last_update_time": self.last_update_time
        }
        try:
            with open("runtime_data.json", "w") as f:
                json.dump(data, f)
        except IOError as e:
            print(f"Error writing runtime_data.json: {e}")

    def calculate_price(self):
        try:
            with open("commands.json", "r") as f:
                commands = json.load(f)
                fan_status = commands.get("fan", "OFF")
                light_status = commands.get("light", "OFF")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading commands.json: {e}")
            fan_status = "OFF"
            light_status = "OFF"

        current_time = time.time()
        elapsed_time = (current_time - self.last_update_time) / 3600
        self.total_runtime += elapsed_time
        self.last_update_time = current_time
        self.save_runtime_data()
        total_price = 0
        if fan_status == "ON":
            total_price += self.total_runtime * self.price_per_hour
        if light_status == "ON":
            total_price += self.total_runtime * self.price_per_hour
        return total_price

    def update_price(self):
        price = self.calculate_price()
        self.label.config(text=f"Current Price: ${price:.2f}")
        self.after(1000, self.update_price)

if __name__ == "__main__":
    app = PriceCalculator()
    app.mainloop()
