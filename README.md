# openweather-api-app

1. clone the repository from github

2. set up venv
    # On Windows
        python -m venv .venv
    # On Mac/Linux:
        python3 -m venv .venv

3. activate venv
    # On Windows (cmd):
        .venv\Scripts\activate
    # Windows (PowerShell):
        .\venv\Scripts\Activate.ps1
    # On Mac/Linux:
        source .venv/bin/activate

4. pip install dependencies 
    pip install -r requirements.txt

5. api configuration
    1. create a free OpenWeatherMap account and copy your api key from: https://openweathermap.org/api
    2. navigate to the root directory of the openweather-api-app project and create a file called '.env'
    3. open the '.env' file and paste your api key with the following line of code: API_KEY = "your_key_here"
    4. replacing your 'your_key_here' with your free OpenWeatherMap api key

6. run the program