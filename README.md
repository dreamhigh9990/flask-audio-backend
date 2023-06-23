## Requirements
1. Python & MongoDB
    - MongoDB (download here: https://www.mongodb.com/try/download/community)
    - Python 3.9.x (download here: https://www.python.org/downloads/release/python-397/)

2. Extract ffmpeg-4.4.1-essentials_build.7z file into c drive.
    - Register 'C:\ffmpeg-4.4.1-essentials_build\bin' as System Path variable.
    - Confirm that ffmpeg command is enabled on console.

3. pipenv install resemblyzer

## Further configuration
1. You can configure the app manually by editing the `api/main/config/config.cfg` file.

2. You need to install following packages.
    pipenv install flask

3. And then you run the project following command. 
    pipenv run python api/run.py

## Auth tokens

There is a very basic front-end example in place within the `/web` directory. It demonstrates making a few API calls (User Add and User Login).

A successful login request will return two tokens: `AccessToken` and `RefreshToken`. These should be saved to localStorage and used to set the `AccessToken` and `RefreshToken` request headers for all protected routes (e.g. `GET /user/`).

You can refresh the `AccessToken` when it returns as expired by submitting a request to `GET /user/auth/`.