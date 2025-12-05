import requests
import json
from datetime import datetime

def hole_buchdaten(isbn):
    
    try:
        
        url = f"https://openlibrary.org/api/books"
        
        # Parameters to send to API
        params ={
            'bibkeys': f'ISBN:{isbn}', # Which ISBN to search   
            'format': 'json', # Response format is JSON
            'jscmd': 'data'   # We want only book data
                        
        }
        print(f'API-Anfrage wird gesendet')
        
        # API request
         ## Send GET request to API (with 10 second timeout)
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()     # Control HTTP Errors
        
        #  Convert JSON response to Python dictionary
        data = response.json() 
        book_key = f'ISBN:{isbn}'
        
        #Check if book exists in API response
        if book_key not in data:
           print('Das Buch mit dieser ISBN-Nummer konnte nicht gefunden werden.')
           return None
        #Get the book data   
        book_data= data[book_key]
        
        
    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}")
        return None
        
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {e}" )
        return None
    except Exception as e:
        print(f"Unknown Error: {e}")
        return None
    
    
def buche_automatisch_ein(isbn, barcode):
    try:
        from database import fuege_buch_hinzu
        
        #Get book information from the API
        buchdaten=hole_buchdaten(isbn)
        
        if not buchdaten: 
            print("Cannot get book information")
            return False
        # Add book to database
        success = fuege_buch_hinzu(
            isbn=buchdaten['isbn'],
            titel= buchdaten['titel'],
            author = buchdaten['autor'],
            barcode= barcode,
        
        )
    except ImportError: 
        print("Database module not found")