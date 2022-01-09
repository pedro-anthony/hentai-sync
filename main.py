import os
import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import praw
import shutil
import requests
from colorama import Fore

#clear the screen
os.system('cls' if os.name == 'nt' else 'clear')

# Open configuration file and parse the data
with open('config.json') as data_file:
    config = json.load(data_file)

print('Configuration file loaded.')

gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("user_credentials.json")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("user_credentials.json")

drive = GoogleDrive(gauth)

print('Authention Successful.') 

reddit = praw.Reddit(
    client_id=config['client_id'],
    client_secret=config['client_secret'],
    user_agent=config['user_agent'],
)

subreddit = reddit.subreddit('hentai')

# Grab first 50 "hot" posts
def get_images():
    for submission in subreddit.hot(limit=50):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png') or submission.url.endswith('.gif'):
            print(Fore.GREEN,'Downloading: ' + submission.url)
            r = requests.get(submission.url, stream=True)
            if r.status_code == 200:
                with open('images/' + submission.url.split('/')[-1], 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                print(Fore.YELLOW, 'File downloaded successfully.', Fore.RESET, '\n')
            else:
                print('Error downloading: ' + submission.url)

# Wipe the images/ folder
def wipe_directory():
    for filename in os.listdir('images'):
        file_path = os.path.join('images', filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

# Upload the images to Google Drive
def upload_images():
    for filename in os.listdir('images'):
        file_path = os.path.join('images', filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            print(Fore.GREEN, 'Uploading: ' + file_path)
            file1 = drive.CreateFile({'title': filename, 'parents': [{'id': config['folder_id']}]})
            file1.SetContentFile(file_path)
            file1.Upload()
            print(Fore.YELLOW, 'Uploaded: ' + file_path, Fore.RESET, '\n')

# Wipe all images in the google drive folder
def full_wipe():
    for file1 in drive.ListFile({'q': "'" + config['folder_id'] + "' in parents and trashed=false"}).GetList():
        file1.Delete()

print('Obtained Reddit instance.')

print("""
Welcome to Hentai Sync!

Please input the index of the desired operation.

""")

options = ["1. Get images", "2. Upload images", "3. Wipe local cache", "4. Complete cycle", "5. Wipe remote images", "6. Exit"]
colors = [Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.BLUE, Fore.RED, Fore.MAGENTA]

for i in range(len(options)):
    print(colors[i] + options[i] + Fore.RESET)

def menu():
    while True:
        try:
            choice = int(input("> "))
            if choice == 1:
                get_images()
            elif choice == 2:
                upload_images()
            elif choice == 3:
                wipe_directory()
            elif choice == 4:
                get_images()
                upload_images()
                wipe_directory()
                break
            elif choice == 5:
                full_wipe()
                break
            elif choice == 6:
                exit()
            else:
                print("Invalid input.")
        except ValueError:
            print("Invalid input.")

menu()