import sqlite3
import csv
from datetime import datetime, timedelta

def erstelle_datenbank():
    conn = sqlite3.connect('bibliothek.db')
    c = conn.cursor() 
    
    c.execute(''' CREATE TABLE IF NOT EXISTS buecher
               (id INTEGER PRIMARY KEY,
                  isbn TEXT,
                  titel TEXT,
                  autor TEXT,
                  barcode TEXT UNIQUE,
                  verfuegbar BOOLEAN)
              ''')
    
    c.execute(''' CREATE TABLE IF NOT EXISTS schueler
               (id INTEGER PRIMARY KEY,
                  name TEXT,
                  klasse TEXT,
                  barcode TEXT UNIQUE,
                  email TEXT)
              ''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS ausleihen
              (id INTEGER PRIMARY KEY,
                  buch_id INTEGER,
                  schueler_id INTEGER,
                  ausleihdatum DATE,
                  rueckgabedatum DATE,
                  faellig_am DATE,
                  FOREIGN KEY(buch_id) REFERENCES buecher(id), 
                  FOREIGN KEY(schueler_id) REFERENCES schueler(id))    
              ''')
    
    conn.commit()
    conn.close()
    print("Datenbank erfolgreich erstellt")
    
    

def fuege_buch_hinzu(isbn, titel, autor, barcode):
    conn = sqlite3.connect('bibliothek.db')
    c = conn.cursor()
    
    try:
     c.execute('''INSERT INTO buecher (isbn, titel, autor, barcode)
               VALUES(?,?,?,?)''', (isbn, titel, autor, barcode))   
     print(f"Buch '{titel}' erfolgreich hinzugefügt!")
     return True 
 
    except sqlite3.IntegrityError:
        print("Fehler: Barcode bereits vergeben!")
        return False
    
    finally:
        conn.close()
    
if __name__ == "__main__":
    erstelle_datenbank()
    
    fuege_buch_hinzu("978-3-123-45678-9", "Python für Anfänger", "Max Mustermann", "B000001")
    