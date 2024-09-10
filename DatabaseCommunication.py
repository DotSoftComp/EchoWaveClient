import requests
import json
#BASE_URL = 'https://dotsoft.onrender.com'
BASE_URL = 'http://127.0.0.1:5000'

def CheckIdValidity():
    # Open and read the JSON file
    with open("python/databasePython/userId.json", "r") as file:
        data = json.load(file)
    
    # Send a POST request with the loaded JSON data
    response = requests.post(f'{BASE_URL}/checkIdValidity', json=data)
    
    # Check if the request was successful
    print("server response is : ")
    print(response.json())
    
    # Return the JSON content of the response
    with open('python/temp/id.json', "w") as file:
        json.dump(response.json(), file, indent=4)

if __name__ == "__main__":
    CheckIdValidity()