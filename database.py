import sqlite3
import csv
from datetime import datetime, timedelta

class Error(Exception): ...
def erstelle_datenbank():
    conn = sqlite3.connect('bibliothek.db')
    c = conn.cursor() 
    
    c.execute(''' CREATE TABLE IF NOT EXISTS buecher
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  isbn TEXT,
                  titel TEXT,
                  autor TEXT,
                  barcode TEXT UNIQUE,
                  verfuegbar BOOLEAN)w
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
        raise Error("Fehler: Barcode bereits vergeben!")
       
    
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
       raise Error(f"Übersprungen – Barcode bereits vorhanden: {barcode}")
        
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
           raise Error(" Das Buch ist derzeit ausgeliehen, kann nicht gelöscht werden!")
          
       # Delete book
       c.execute("DELETE FROM buecher WHERE id = ?", (buch_id,))
       conn.commit()
       print("Das Buch wurde erfolgreich gelöscht!")
       return True
       
   except Exception as e:
       raise Error(f"Deletion error: {e}")
    
   finally: 
       conn.close()
       
def bearbeite_buch(buch_id, isbn=None, titel=None, autor=None, barcode=None, signatur=None):
      conn = sqlite3.connect('bibliothek.db')
      c = conn.cursor()  
   
    try: 
        uptades=[]
        values=[]
        
        if isbn:
            uptades.append("isbn= ?")
            values.append(isbn)
        if titel:
            uptades.append("titel= ?")
            values.append(titel)
        if autor:
            uptades.append("autor= ?")
            values.append(autor)
        if barcode:
            uptades.append("barcode= ?")
            values.append(barcode)
        if signatur:
            uptades.append("signatur= ?")
            values.append(signatur)
            
        if not updates:
            raise Error("Das Buch konnte nicht finden")   
        
    
    except:

def hole_buch_status(buch_id):
    conn=sqlite3.connect('bibliothek.db')
    c=conn.cursor()
    
    try:
        c.execute("SELECT verfuegbar FROM buecher WHERE id = ?", (buch_id,))
        result=c.fetchone()
        
        if not result:
            return "Nicht gefunden"
        
        if result[0]:
            return "Verfügbar"
        
        c.execute("SELECT faellig_am FROM ausleihen WHERE buch_id = ? AND ruecgabedatum IS NULL", (buch_id,))
        ausleihe=c.fetchone()
        
        if ausleihe:
            faellig_am= datetime.strptime(ausleihe[0],'%Y-%m-%d').date()
            gestern=datetime.today().date()- timedelta(days=1)
            if gestern > faellig_am:
                return "Rückgabe überfällig"
            else:
                return "Ausgeliehen"
        return "Verfügbar"
        
    finally:
        conn.close()

def leihe_buch_aus(buch_id, schueler_id):
   conn=sqlite3.connect('bibliothek.db')
   c=conn.cursor()
    
   try: 
        c.execute("SELECT verfuegbar FROM buecher WHERE id = ?", (buch_id,)) 
        buch=c.fetchone()
       
        if not buch or not buch[0]:
           raise Error("Buch ist nicht verfügbar")
        
        c.execute("SELECT id FROM buecher WHERE id = ?", (schueler_id,))
        
        if not c.fetchone():
            raise Error("Schüler nicht gefunden")#
        
        gestern=datetime.today().date()- timedelta(days=1)
        rueckgabedatum =gestern + timedelta(days=14)
        
        c.execute("INSERT INTO ausleihen (buch_id, schueler_id, ausleihdatum, faellig_am) VALUES(?,?,?,?)", (buch_id, schueler_id, gestern, rueckgabedatum))
        
        c.execute("UPDATE buecher SET verfuegbar = 0 WHERE id=?," (buch_id))
        conn.commit()
        
        print(f"Das Buch wurde erfolgreich zurückgegeben. Rückgabe:{rueckgabedatum}")
        return True
    
   except Exception as e:
     raise Error(f"Ausleihe Fehler: {e}")  
 
   finally:
       conn.close()
## SCHUELER

def suche_schueler(suchebegriff):
    conn = sqlite3.connect('bibliothek.db')
    c = conn.cursor()
    
    c.execute('''SELECT * FROM schueler WHERE name LIKE ? OR klasse LIKE ? OR email LIKE ?''',(f'%{suchebegriff}%',f'%{suchebegriff}%',f'%{suchebegriff}%'))
    
    schueler= c.fetchall()
    conn.commit()
    conn.close()
    return schueler

def loesche_alle_schueler():      
    conn=sqlite3.connect('bibliothek.db')
    c=conn.cursor()
    
    try:
        c.execute("SELECT COUNT(*) FROM ausleihen WHERE rueckgabedatum IS NULL")
        aktive_ausleihen=c.fetchone()[0]
        
        if aktive_ausleihen >0:
            raise Error(f"Fehler: {aktive_ausleihen} aktive Ausleihen gefunden! Schüler können nicht gelöscht werden.") 

        
        c.execute("DELETE FROM schueler")
        conn.commit()
        print("Alle Schüler erfolgreich gelöscht!") 
        return True
    
    except Exception as e:
        raise Error(f"Löschfehler: {e}")
    finally:
        conn.close() 
    
def loesche_schueler(schueler_id):
    conn=sqlite3.connect('bibliothek.db')
    c=conn.cursor()
    try:
        c.execute("SELECT COUNT(*) FROM ausleihen WHERE schueler_id = ? AND rueckgabedatum IS NULL", (schueler_id,))
        aktive_ausleihen=c.fetchone()[0]
        
        if aktive_ausleihen > 0:
            raise Error(f"Der Student hat {aktive_ausleihen} aktive Ausleihe.")

        c.execute("DELETE FROM schueler WHERe id = ?")
        conn.commit()
        print("Schüler gelöscht")
        return True
    
    except Exception as e:
        raise Error(f"Löschungsfehler: {e}")
      
    
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
        
    ergebnisse = suche_schueler("Ali")
    for schueler in ergebnisse:
        print(schueler)
    
    