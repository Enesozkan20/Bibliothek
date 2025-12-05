import requests
import json
from datetime import datetime

def hole_buchdaten(isbn):
    
    try:
        
        url = f"https://openlibrary.org/api/books"
        
        params ={
            'bibkeys': f'ISBN:{isbn}',
            'format': 'json',
            'jscmd': 'data'      
        }
        print(f'API-Anfrage wird gesendet')
        
        # API request
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()     # Control HTTP Errors
        
        # Parse JSON-Daten
        data = response.json() 
        book_key = f'ISBN:{isbn}'
        
        if book_key not in data:
           print('')
    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}")
        return None
        
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {e}" )
        return None
    except Exception as e:
        print(f"Unbekannter Fehler{e}")
        return None