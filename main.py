import sys
import requests
import os
from dotenv import load_dotenv
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QCompleter
from PyQt6.QtCore import QLine, QStringListModel, Qt
from PyQt6.QtGui import QIcon
from city_loader import CityLoader

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Declare components
        self.city_label = QLabel(self)
        self.temperature_label = QLabel(self)
        self.temperature_button = QPushButton(self)   
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.city_input = QLineEdit(self)
        self.city_model = QStringListModel(self)
        self.city_completer = QCompleter(self.city_model, self)
        self.submit_button = QPushButton(self)
        self.error_label = QLabel(self)
        
        # Config and Style
        self._setup_ui()
        self._apply_styleSheet()
        self.load_city_data()
        
    def _setup_ui(self):
        """
        setup ui and component properties.
        """
        self.setWindowTitle("Weather App")
        self.setWindowIcon(QIcon("resources/chiikawa.jpg"))
        self.setGeometry(550, 350, 400, 400)
        
        # qcompleter config
        self.city_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive) # case insensitive
        #self.city_completer.setFilterMode(Qt.MatchFlag.MatchContains) # autofill filter
        self.city_completer.setFilterMode(Qt.MatchFlag.MatchStartsWith)
        #self.city_completer.setCompletionMode(QCompleter.CompletionMode.InlineCompletion) # autofill suggestions
        self.city_completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.city_input.setCompleter(self.city_completer) # attach city_completer to city_input
        
        # widget properties and alignment
        self.city_input.setPlaceholderText("Enter a City...")
        self.submit_button.setText("Get forecast")
        
        self.emoji_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temperature_button.setCheckable(True) # button will be checkable
        self.temperature_button.setChecked(False) # will initially be unchecked (for displaying celsius)
        self.temperature_button.setEnabled(False) # disable temp unit button until needed
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.city_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # layout
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        
        # hbox components (emoji and temp)
        hbox.addWidget(self.emoji_label)
        hbox.addWidget(self.temperature_label)
        hbox.addWidget(self.temperature_button)
        hbox.addStretch(1)
        
        # add all components to vbox
        vbox.addWidget(self.city_label)
        vbox.addLayout(hbox)
        vbox.addWidget(self.error_label)
        vbox.addWidget(self.description_label)
        vbox.addStretch(1)     
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.submit_button)
        self.setLayout(vbox)
        
        # set object name for style sheet
        self.city_label.setObjectName("city_label")
        self.emoji_label.setObjectName("emoji_label")
        self.temperature_label.setObjectName("temperature_label")
        self.temperature_button.setObjectName("temperature_button")
        self.description_label.setObjectName("description_label")
        self.error_label.setObjectName("error_label")
        self.city_input.setObjectName("city_input")
        self.submit_button.setObjectName("submit_button")
        
        # Connections / call methods
        self.submit_button.clicked.connect(self.get_weather)
        self.city_input.returnPressed.connect(self.get_weather) # ENTER 
        self.temperature_button.toggled.connect(self.update_temperature_unit)
        
        self.setFocus()

    def _apply_styleSheet(self):
        """
        apply css styling from style.qss
        """
        try:
            with open('resources/style.qss', 'r') as file:
                style = file.read()
                self.setStyleSheet(style)
        except FileNotFoundError:
            print("Warning:\n resources/style.qss not found")
        except PermissionError:
            print("Permission Error:\naccess denied")
        except:
            print("Error")
    
    def load_city_data(self):
        """
        helper method starts a background thread to load and parse the city data.
        connects to update_city_suggestion() upon completion.
        """
        self.loader_thread = CityLoader('data/city.list.min.json.gz')
        
        self.loader_thread.finished.connect(self.update_city_suggestion)
        
        self.loader_thread.start()
        
    def update_city_suggestion(self, formatted_cities):
        self.city_model.setStringList(formatted_cities) 
        self.city_completer.setModel(self.city_model)
    
    def get_weather(self): 
        city_name = self.city_input.text()
        url = (f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={os.getenv('API_KEY')}") # api request - uses "API_KEY" from .env file using os.getenv()
        
        try:
            response = requests.get(url) # returns the API request as an object
            response.raise_for_status() # check response and raise an exception if needed
            api_data = response.json() # convert API request object into json format so that its readable
            
            if api_data["cod"] == 200: # successful api response code
                self.display_weather(api_data)
                
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorised:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not Found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP Error Occurred:\n{http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")

    def display_error(self, message):
        """
        clear and disable ui components to display an error from get_weather()  
        """
        self.error_label.setText(message)
        self.city_label.clear()
        self.emoji_label.clear()
        self.temperature_label.clear()
        self.temperature_button.setText("")
        self.temperature_button.setEnabled(False) # disable temperature converter button
        self.description_label.clear()

    def display_weather(self, data: dict):
        city_name = data["name"]
        self.city_temp_k = data["main"]["temp"] # variable accessible in other methods
        weather_id = data["weather"][0]["id"] # 'weather' is a list of 1 item, so we need to get index 0 before getting the 'id' 
        weather_description = data["weather"][0]["description"] # 'weather' is a list of 1 item, so we get index 0 before getting the 'description'
        
        self.error_label.setText("")
        self.city_label.setText(f"{city_name}")
        self.emoji_label.setText(self.get_weather_emoji(weather_id)) # set emoji_label's text to the returned value of the get_weather_emoji() method
        self.description_label.setText(f"{weather_description}")
        
        self.temperature_button.setEnabled(True) # enable temperature button
        self.update_temperature_unit()

    def update_temperature_unit(self):
        if self.temperature_button.isChecked():
            city_temp = (self.city_temp_k - 273.15) * 9/5 + 32 # fahrenheit
            
            self.temperature_button.setText("°F")
        else:
            city_temp = self.city_temp_k - 273.15 # celsius
            self.temperature_button.setText("°C")
            
        self.temperature_label.setText(f"{city_temp:.0f}")
    
    @staticmethod
    def get_weather_emoji(weather_id):
        match weather_id:                       # https://openweathermap.org/weather-conditions
            case _ if 200 <= weather_id <= 232: # thunderstorm
                return "⛈️"
            case _ if 300 <= weather_id <= 321: # drizzle
                return "🌦️"
            case _ if 500 <= weather_id <= 531: # rain
                return "🌧️"
            case _ if 600 <= weather_id <= 622: # snow
                return "🌨️"
            case _ if 700 <= weather_id <= 781: # fog
                return "🌫️"
            case 762:                           # volcanic
                return "🌋" 
            case 771:                           # squall
                return "💨"
            case 781:                           # tornado
                return "🌪️" 
            case 800:                           # clear sky
                return "☀️"
            case _ if 801 <= weather_id <= 804: # cloudy
                return "☁️"
            case _:
                return "🌡️"

def configure():
    load_dotenv() # load .env file that contains API_KEY
    
def main():
    configure()
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()