# Hentai Sync [![CodeFactor](https://www.codefactor.io/repository/github/pedro-anthony/hentai-sync/badge/main)](https://www.codefactor.io/repository/github/pedro-anthony/hentai-sync/overview/main)
Shamelessly grab images from any image-based subreddit (i.e porn) and dump everything to a personal Google Drive folder.

## Setup
 - Login to [Google Cloud Console](https://console.cloud.google.com/)
- Create a new epic application, setup the oAuth consent screen
- Enable the Google Drive API and create new credentials
- Download your credentials, rename them to "client_secrets.json" and put the file in the project root folder
- Since your app is (most-likely) not verified, ensure you put the email for the account holding the Drive folder in the whitelist.
## Config
- Login to [Reddit](https://old.reddit.com)
- Create a new application, script type
- Create a "config.json" file, based on the example with your new Reddit application's secrets.
- Run the program, a local webserver window serving the login page will open, promptly follow the on-screen instructions.

