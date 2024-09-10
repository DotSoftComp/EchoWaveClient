import requests
import json
#BASE_URL = 'https://dotsoft.onrender.com'
BASE_URL = 'http://127.0.0.1:5000'

def SendMail():
    # Open and read the JSON file
    with open("python/databasePython/userId.json", "r") as file:
        data = json.load(file)
    
    # Send a POST request with the loaded JSON data
    response = requests.post(f'{BASE_URL}/SendRecoveryMail', json=data)

if __name__ == "__main__":
    SendMail()