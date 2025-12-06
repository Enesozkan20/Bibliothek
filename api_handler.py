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
        book_data = data[book_key]
        
        result = {
            'titel': book_data.get('title', 'Unknown Title'), 
            'autor': ','.join([author['name'] for author in book_data.get('authors', []) ]) if book_data.get('authors') else 'Unknown Author',
            'jahr': book_data.get('publish_date', 'Unknown'),
            # Book cover image URL (large size)
            'cover_url':book_data.get('cover',{}).get('large', '') if book_data.get('cover') else '',
            'isbn':isbn    
        }
        
        print(f"Book found: {result['titel']}")
        return result # THIS WAS MISSING
    
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
            autor = buchdaten['autor'],
            barcode= barcode,
        )
        
        #Check if succesful
        if success:
            print(f"Book added succesfully: {buchdaten['titel']}")
        else: 
            print("Cannot add book to database")
            return False
        
    except ImportError: 
        print("Database module not found")
        return False
    
    
def test_api():
  # Test function for API
  
   print("=== API TEST STARTING ===")
   
   test_isbns=[
        "9780140328721",  # Matilda - Roald Dahl
        "9780439064873",  # Harry Potter
        "9780000000000"   # Invalid ISBN
   ]
   
   # Test each ISBN
   for isbn in test_isbns:
       print(f"\n ISBN: {isbn}")
       buchdaten = hole_buchdaten(isbn)
       
       if buchdaten:
           print(f"Title: {buchdaten['titel']}")
           print(f"Author: {buchdaten['autor']}")
           print(f"Year: {buchdaten['jahr']}")
        
       else:
           print("Book not found")
           
           
def test_automatische_buchereinfügung():
    print("\n   Automatic book adding test   ")   
    buche_automatisch_ein("9780140328721", "B000100") 
    
       
if __name__ =="__main__":
    test_api()
    test_automatische_buchereinfügung()