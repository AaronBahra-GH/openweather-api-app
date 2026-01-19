from sre_parse import State
from PyQt6.QtCore import QThread, pyqtSignal
import gzip
import json

class CityLoader(QThread):
    
    finished = pyqtSignal(list) # declare pyqtSignal can only carry the list datatype
    
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        
    def run(self):
        try:
            with gzip.open(self.file_path, 'rt', encoding='utf-8') as file:
                cities_data = json.load(file) 
                
                #formatted_cities = [f"{city['name']}, {city['country']}" for city in cities_data] # for every city in the list, return 'name' and'country'
                formatted_cities = [] # for every city in the list, return 'name' and'country'
                
                # USE FOR LOOP TO IMPLEMENT FILTER FOR US CITIES TO INCLUDE STATES DUE TO CITIES HAVING THE SAME NAME
                for city in cities_data:
                    name = city['name']
                    state = city['state']
                    country = city['country']
                    
                    if country == "US":
                        formatted_cities.append(f"{name}, {state}, {country}")
                    else:
                        formatted_cities.append(f"{name}, {country}")
                
                formatted_cities.sort(key=len) # sort list by ascending length
                
                self.finished.emit(formatted_cities) # when finished return/send formatted_cities
                
        except Exception as e:
            self.finished.emit([]) # send an empty list