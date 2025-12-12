import sqlite3
import csv
from datetime import datetime, timedelta


def erstelle_datenbank():
    conn = sqlite3.connect('bibliothek.db')
    c = conn.cursor() 
    
    c.execute(''' CREATE TABLE IF NOT EXISTS buecher
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  isbn TEXT,
                  titel TEXT,
                  autor TEXT,
                  barcode TEXT UNIQUE,
                  verfuegbar BOOLEAN)
              ''')
    
    c.execute(''' CREATE TABLE IF NOT EXISTS schueler
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  klasse TEXT,
                  barcode TEXT,
                  email TEXT)
              ''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS ausleihen
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
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
     conn.commit()
     return True 
 
    except sqlite3.IntegrityError:
        print("Fehler: Barcode bereits vergeben!")
        return False
    
    finally:
        conn.close()
    
def lade_schueler_aus_csv(dateipfad):
    conn = sqlite3.connect('bibliothek.db')
    c = conn.cursor()
    try:
        with open(dateipfad,'r', encoding="utf-8") as file:
           reader = csv.reader(file)
           next(reader)      # Header überspringen

           for row in reader:
               name,klasse,barcode,email=row
               c.execute('''INSERT INTO schueler (name,klasse,barcode,email)
               VALUES(?,?,?,?)''', (name,klasse,barcode,email))
               
               
        conn.commit()
    
    except sqlite3.IntegrityError:
        print(f"Übersprungen – Barcode bereits vorhanden: {barcode}")
        
    finally:
        conn.close()
 

def suche_buch(suchebegriff):
    conn = sqlite3.connect('bibliothek.db')
    c = conn.cursor()
    
    c.execute('''SELECT * FROM buecher WHERE titel LIKE ? OR autor LIKE ? OR isbn LIKE ?''',(f'%{suchebegriff}%',f'%{suchebegriff}%',f'%{suchebegriff}%'))
    
    buecher= c.fetchall()
    conn.commit()
    conn.close()
    return buecher

## BUECHER    
def loesche_buch(buch_id):
   conn = sqlite3.connect('bibliothek.db')
   c = conn.cursor()  
   
   try:
        # Check the loan records for this book.
       c.execute('''SELECT * FROM ausleihen WHERE buch_id = ? AND ruecgabedatum IS NULL''', (buch_id,))
       aktive_ausleihen=c.fetchall()
       
       if aktive_ausleihen:
           print(" Das Buch ist derzeit ausgeliehen, kann nicht gelöscht werden!")
           return False
       
       # Delete book
       c.execute("DELETE FROM buecher WHERE id = ?", (buch_id,))
       conn.commit()
       print("Das Buch wurde erfolgreich gelöscht!")
       return True
       
   except Exception as e:
       print(f"Deletion error: {e}")
       return False
    
   finally: 
       conn.close()

def hole_buch_status(buch_id):
    conn=sqlite3.connect('bibliothek.db')
    c=conn.cursor()
    
    try:
        c.execute("SELECT verfuegbar FROM buecher WHERE id = ?")
        result=c.fetchone()
        
        if not result:
            return "Nicht gefunden"
        
        if result[0]:
            return "Verfügbar"
        
        c.execute("SELECT faellig_am FROM ausleihen WHERE buch_id = ? AND ruecgabedatum IS NULL", (buch_id,))
        ausleihe=c.fetchone()
        
        if ausleihe:
            faellig_am= datetime.strptime(ausleihe[0],'%Y-%m-%d').date()
            heute=datetime.now().date()
            
            if heute> faellig_am:
                return "Rückgabe überfällig"
            else:
                return "Ausgeliehen"
        return "Verfügbar"
        
    finally:
        conn.close()
    
## SCHUELER
def loesche_alle_schueler():      
    conn=sqlite3.connect('bibliothek.db')
    c=conn.cursor()
    
    try:
        c.execute("SELECT COUNT(*) FROM ausleihen WHERE rueckgabedatum IS NULL")
        aktive_ausleihen=c.fetchone()[0]
        
        if aktive_ausleihen >0:
            print(f"Fehler: {aktive_ausleihen} aktive Ausleihen gefunden! Schüler können nicht gelöscht werden.") 
            return False
        
        c.execute("DELETE FROM schueler")
        conn.commit()
        print("Alle Schüler erfolgreich gelöscht!") 
        return True
    
    except Exception as e:
        print(f"Löschfehler: {e}")
        return False    
    finally:
        conn.close() 
    
def loesche_schueler(schueler_id):
    conn=sqlite3.connect('bibliothek.db')
    c=conn.cursor()
    try:
        c.execute("SELECT COUNT(*) FROM ausleihen WHERE schueler_id = ? AND rueckgabedatum IS NULL", (schueler_id,))
        aktive_ausleihen=c.fetchone()[0]
        
        if aktive_ausleihen > 0:
            print(f"Der Student hat {aktive_ausleihen} aktive Ausleihe.")
            return False
        c.execute("DELETE FROM schueler WHERe id = ?")
        conn.commit()
        print("Schüler gelöscht")
        return True
    
    except Exception as e:
        print(f"Löschungsfehler: {e}")
        return False
    
    finally:
        conn.close()  
        
if __name__ == "__main__":
    erstelle_datenbank()
    
    fuege_buch_hinzu("978-3-123-45678-9", "Python für Anfänger", "Max Mustermann", "B000001")
    
    dateipfad = "schueler.csv"
    lade_schueler_aus_csv(dateipfad)
    
    ergebnisse = suche_buch("Python")
    for buch in ergebnisse:
        print(buch)
    
    