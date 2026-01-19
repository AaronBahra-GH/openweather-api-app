# openweather-api-app

## 1. Clone the repository from GitHub

## 2. Set up venv
#### On Windows
        python -m venv .venv
#### On Mac/Linux:
        python3 -m venv .venv

## 3. Activate venv
#### On Windows (cmd):
        .venv\Scripts\activate
#### Windows (PowerShell):
        .\venv\Scripts\Activate.ps1
#### On Mac/Linux:
        source .venv/bin/activate

## 4. Install dependencies 
    pip install -r requirements.txt

## 5. Api configuration
1. Create a free OpenWeatherMap account and copy your api key from: https://openweathermap.org/api
2. Navigate to the root directory of the /openweather-api-app project and create a file called '.env'
3. Open the '.env' file and paste your api key with the following line of code: API_KEY = "your_key_here"
4. Replace your 'your_key_here' with your free OpenWeatherMap api key

## 6. Run the program
Run the program :)
