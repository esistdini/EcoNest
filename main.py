import subprocess
import time
import json
import os
import speech_recognition as sr

def start_gui_scripts():
    subprocess.Popen(['pythonw', 'components/fan_gui.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
    subprocess.Popen(['pythonw', 'components/light_bulb_gui.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
    subprocess.Popen(['pythonw', 'components/price_calculator.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
    subprocess.Popen(['pythonw', 'components/face_detection.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)

def update_commands(fan_status, light_status):
    commands = {
        "fan": fan_status,
        "light": light_status
    }
    try:
        with open("commands.json", "w") as file:
            json.dump(commands, file)
    except IOError as e:
        print(f"Error writing to commands.json: {e}")

def get_temperature_status():
    subprocess.call(['python', 'components/check_weather.py'])
    if os.path.exists("temperature_status.txt"):
        with open("temperature_status.txt", "r") as file:
            status = file.read().strip()
        return status
    return "Warm"

def get_face_status():
    if os.path.exists("face_status.txt"):
        with open("face_status.txt", "r") as file:
            status = file.read().strip()
        return status
    return "NoFaceDetected"

def process_voice_command(command):
    command = command.lower()
    if "fan" in command:
        if "on" in command:
            update_commands("ON", None)
            print("Voice command: Turning on the fan.")
        elif "off" in command:
            update_commands("OFF", None)
            print("Voice command: Turning off the fan.")
    elif "light" in command:
        if "on" in command:
            update_commands(None, "ON") 
            print("Voice command: Turning on the light.")
        elif "off" in command:
            update_commands(None, "OFF")
            print("Voice command: Turning off the light.")

def listen_for_commands():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        print("Listening for commands...")
        while True:
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio)
                print(f"Command : {command}")
                process_voice_command(command)
            except sr.UnknownValueError:
                print("Can\'t Understand!")
            except sr.RequestError as e:
                print(f"Sorry, there was an error : {e}")

def main():
    start_gui_scripts()
    subprocess.Popen(['python', '-c', 'from main import listen_for_commands; listen_for_commands()'])
    while True:
        temperature_status = get_temperature_status()
        face_status = get_face_status()
        if face_status == "FaceDetected":
            if temperature_status == "Cold":
                print("Temperature is below 15°C, not turning on the fan...")
                update_commands("OFF", "ON")
            else:
                print("Face detected, turning on the fan and light...")
                update_commands("ON", "ON")
        else:
            print("No face detected, turning off the fan and light...")
            update_commands("OFF", "OFF")
        time.sleep(1)

if __name__ == "__main__":
    main()
