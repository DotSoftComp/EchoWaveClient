import requests
import json
import sys

#BASE_URL = 'https://dotsoft.onrender.com'
BASE_URL = 'http://127.0.0.1:5000'

def CallServerChangePassword():
    # Open and read the JSON file
    with open("python/pythonChangePassword/userData.json", "r") as file:
        data = json.load(file)
    
    # Send a POST request with the loaded JSON data
    response = requests.post(f'{BASE_URL}/update_password', json=data)
    response = response.json()
    if response.get("error", None) != None:
        sys.stderr.write(f'Error : ' + response.get('error'))
    elif response.get("message", None) != None:
        print("message : " + response.get("message"))


if __name__ == "__main__":
    CallServerChangePassword()