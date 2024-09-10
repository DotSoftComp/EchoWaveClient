import sys
import os
import requests
from Common import *
from ClientUtilities import *
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import time
import shutil
from datetime import datetime

BASE_URL = 'http://127.0.0.1:5000'
#BASE_URL = 'https://dotsoft.onrender.com'

SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']


def CallServerPdfCreator():
    print("start making data")
    #not usable : only instagram is used in the beta test
    #CreateOauthToken()
    data = GenerateParameters()

    with open("python/token.json", 'r') as file:
        data['gootoken'] = file.read()

    #different route of the server
    accessRoute = ["GetWeekDailyInteractionFoll", "GetDailyHourInteractionFoll"]
    accessAuthorization = [
         'InstagramBaseInformation',
         'InstagramVideos',
         'InstagramGraphAge',
         'InstagramGraphGender',
         'InstagramGraphCity',
         'InstagramGraphCountry',
         
         
    ]
    
    canUseRoute = data['saveFile']['bilData']
    data['insightData'] = "null"
    instagramData = requests.post(f'{BASE_URL}/GetInstagramData', json=data)
    data['insightData'] = instagramData.json()

    for i in range(0, len(canUseRoute)):
        if canUseRoute[i] == True:
            if i < len(accessAuthorization):
                accessRoute.append(accessAuthorization[i])

    print(f"\n\n\ndifferent route : {accessRoute} from {data['saveFile']}")
    #find the actual directory to save new Data
    directory = GetDirectoryHighIndex()
    dataFileName = f"python/localSaveData/{directory}"
    
    #init the directories
    RemoveAllFilesInDirectory()
    os.makedirs(f"python/localSaveData/{directory}")

    for i in range(0, len(accessRoute)):
        response = requests.post(f'{BASE_URL}/{accessRoute[i]}', json=data)
        time.sleep(2)
        if response.status_code == 200:
            GetResponseFromServer(response, dataFileName)
        elif response.status_code == 400:
             # Use BeautifulSoup to parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find the custom message, assuming it's within a <p> tag
            custom_message = soup.find('p').get_text()
            # Extract and print the main content (ignoring the tags)
            shutil.rmtree(dataFileName)
            raise Exception(custom_message)
        else:
            print(f"Error: {response.status_code} during ./{accessRoute[i]}")
            shutil.rmtree(dataFileName)
            return

    MergeAllPdfsInOrder(f'python/bilan/{data["fileName"]}.pdf')

    #create time
    # Get the current date and time
    current_time = datetime.now()
    # Extract day, month, and year
    timeData = {}
    timeData["day"] = current_time.day
    timeData["month"] = current_time.month
    timeData["year"] = current_time.year
    with open(dataFileName + "/time.json", 'w') as timeFile:
        json.dump(timeData, timeFile, indent=4)


def GetResponseFromServer(response, name):
    try:

        # Extracting content disposition from response headers
        contentDispo = response.headers['Content-Disposition']
        # Extracting the filename
        filename = contentDispo.split('filename=')[1]
        filePath = f'python/temp/{filename}'
 
        # Write the response content to a local file
        with open(filePath, 'wb' ) as f:
            f.write(response.content)
        print(f"File downloaded: {filePath}")

        returnedValue = response.headers.get('TxtData')
        if response.headers.get('TxtDataName') == "specialAge":
            menFile = f'{name}/menAgeData.json'
            womenFile = f'{name}/womenAgeData.json'
            total = f'{name}/totalAgeData.json'

            menData = ""
            womenData = ""
            totalData = ""
            currentTarget = "total"

            for word in returnedValue.split(" "):
                if word == "men":
                    currentTarget = "men"
                    continue
                if word == "women":
                    currentTarget = "women"
                    continue

                if currentTarget == "men":
                    menData +=  word + " " 
                if currentTarget == "women":
                    womenData +=  word + " " 
                if currentTarget == "total":
                    totalData += word + " "

            with open(total, "w") as file:
                file.write(totalData)
            with open(menFile, "w") as file:
                file.write(menData)
            with open(womenFile, "w") as file:
                file.write(womenData)
        elif returnedValue != "NULL":
            name = f'{name}/{response.headers.get("TxtDataName")}.json'
            with open(name, 'w') as saveFile:
                    saveFile.write(returnedValue)

            print(returnedValue)

    except KeyError:
        print("Error: Content-Disposition header not found in response")



def CreateOauthToken(credentials_file='python/ytbCredential.json', token_file='python/token.json', scopes=SCOPES):
    creds = None
    # Check if token file exists and load existing credentials
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scopes)

    # If there are no valid credentials available, let the user log in.
    if not creds or not creds.valid:
        # Start the OAuth flow to get new credentials
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_file, scopes)
        creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    return creds

if __name__ == "__main__":
    CallServerPdfCreator()
