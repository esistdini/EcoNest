import requests
import time

def get_location():
    try:
        response = requests.get('https://ipinfo.io/json')
        response.raise_for_status()
        data = response.json()
        location = data['loc'].split(',')
        latitude = location[0]
        longitude = location[1]
        return latitude, longitude
    except requests.RequestException as e:
        print(f"Error fetching location: {e}")
        return None, None

def get_weather(latitude, longitude):
    try:
        url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true'
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        if 'current_weather' in weather_data:
            temperature = weather_data['current_weather']['temperature']
            return temperature
        else:
            raise ValueError("Unexpected response format. 'current_weather' key is missing.")
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    except ValueError as e:
        print(e)
        return None

def main():
    while True:
        latitude, longitude = get_location()
        if latitude is None or longitude is None:
            print("Failed to get location. Skipping weather check.")
        else:
            temperature = get_weather(latitude, longitude)
            if temperature is not None:
                if temperature < 15:
                    with open("temperature_status.txt", "w") as f:
                        f.write("Cold")
                else:
                    with open("temperature_status.txt", "w") as f:
                        f.write("Warm")
            else:
                print("Failed to get weather data. Skipping temperature status update.")
        time.sleep(3600)

if __name__ == "__main__":
    main()
