from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

# Beispiel
ausleihen_liste = [
    {
        "ausleihe_id": 101,
        "schueler": "Max Mustermann",
        "adresse": "Musterstraße 12\n40667 Meerbusch",
        "buchtitel": "Die Physik der Zukunft",
        "autor": "Michio Kaku",
        "ausleihdatum": "15.11.2025",
        "faelligkeitsdatum": "29.11.2025",
        "tage_ueberzogen": 13
    },
    {
        "ausleihe_id": 102,
        "schueler": "Anna Müller",
        "adresse": "Bergstraße 8\n40670 Meerbusch",
        "buchtitel": "Tschick",
        "autor": "Wolfgang Herrndorf",
        "ausleihdatum": "18.11.2025",
        "faelligkeitsdatum": "02.12.2025",
        "tage_ueberzogen": 10
    },
    {
        "ausleihe_id": 103,
        "schueler": "Dmitri Petrov",
        "adresse": "Kaiserstraße 44\n40210 Düsseldorf",
        "buchtitel": "Grundkurs Informatik",
        "autor": "Jens Mönk",
        "ausleihdatum": "01.11.2025",
        "faelligkeitsdatum": "15.11.2025",
        "tage_ueberzogen": 27
    }
]



def erstelle_mahnschreiben(ausleihe_id, ausgabepfad):
    # Find matching entry
    eintrag = next((e for e in ausleihen_liste if e["ausleihe_id"] == ausleihe_id), None)
    if eintrag is None:
        raise ValueError(f"Ausleihe-ID {ausleihe_id} nicht gefunden!")

    schueler = eintrag["schueler"]
    adresse = eintrag["adresse"].split("\n")
    buchtitel = eintrag["buchtitel"]
    autor = eintrag["autor"]
    ausleihdatum = eintrag["ausleihdatum"]
    faelligkeitsdatum = eintrag["faelligkeitsdatum"]
    tage_ueberzogen = eintrag["tage_ueberzogen"]

    # Create PDF
    pdf_file = ausgabepfad + f"\\mahnschreiben_{ausleihe_id}.pdf"
    c = canvas.Canvas(pdf_file, pagesize=A4)
    c.setTitle("Mahnschreiben")

    y = 800

    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawString(40, y, "Mahnung zur Buchrückgabe")
    y -= 40

    c.setFont("Helvetica", 12)
    c.drawString(40, y, f"Datum: {faelligkeitsdatum}")
    y -= 40

    # Address block
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Schüleradresse:")
    y -= 20

    c.setFont("Helvetica", 12)
    c.drawString(40, y, schueler)
    y -= 18
    for line in adresse:
        c.drawString(40, y, line)
        y -= 18

    y -= 20


    text_lines = [
        "laut unseren Aufzeichnungen ist folgendes ausgeliehenes Medium",
        "über das Fälligkeitsdatum hinaus noch nicht zurückgegeben worden.",
        "",
        "Bitte bringen Sie das Buch zeitnah in die Schulbibliothek zurück.",
        ""
    ]

    for line in text_lines:
        c.drawString(40, y, line)
        y -= 18


    y -= 10
    c.setFont("Helvetica-Bold", 13)
    c.drawString(40, y, "Buchdetails")
    y -= 25

    c.setFont("Helvetica", 12)
    details = [
        f"Titel: {buchtitel}",
        f"Autor: {autor}",
        f"Ausgeliehen am: {ausleihdatum}",
        f"Fällig am: {faelligkeitsdatum}",
        f"Überzogen: {tage_ueberzogen} Tage"
    ]

    for d in details:
        c.drawString(40, y, d)
        y -= 18

    y -= 30


    c.drawString(40, y, "Falls das Buch bereits abgegeben wurde, betrachten Sie dieses Schreiben als gegenstandslos.")
    y -= 40

    c.drawString(40, y, "Mit freundlichen Grüßen")
    y -= 18
    c.drawString(40, y, "Ihre Schulbibliothek")
    y -= 40

    c.drawString(40, y, "Theodor-Fliedner-Gymnasium")
    y -= 18
    c.drawString(40, y, "E-Mail: bibliothek@schule.de")
    y -= 18
    c.drawString(40, y, "Telefon: 0211 / 1234567")

    c.save()




def erstelle_sammel_mahnung(ausleihen_liste, ausgabepfad):
    pdf_file = ausgabepfad + "\\sammelmahnung.pdf"
    c = canvas.Canvas(pdf_file, pagesize=A4)
    c.setTitle("Sammelmahnung")

    start_y = 800
    line_height = 18


    studenten = {}
    for e in ausleihen_liste:
        name = e["schueler"]
        if name not in studenten:
            studenten[name] = {
                "adresse": e["adresse"],
                "eintraege": []
            }
        studenten[name]["eintraege"].append(e)


    c.setFont("Helvetica-Bold", 20)
    c.drawString(40, start_y, "Sammelmahnung")
    start_y -= 40

    datum = datetime.today().strftime("%d.%m.%Y")
    c.setFont("Helvetica", 12)
    c.drawString(40, start_y, f"Datum: {datum}")
    start_y -= 30


    for schueler, daten in studenten.items():
        if start_y < 120:
            c.showPage()
            start_y = 800


        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, start_y, schueler)
        start_y -= 20

        c.setFont("Helvetica", 11)
        adresse = daten["adresse"].replace("\n", ", ")
        c.drawString(40, start_y, f"Adresse: {adresse}")
        start_y -= 20


        c.setFont("Helvetica-Bold", 11)
        c.drawString(40, start_y, "Titel")
        c.drawString(240, start_y, "Autor")
        c.drawString(380, start_y, "Fällig")
        c.drawString(450, start_y, "Überzogen")
        start_y -= 15
        c.line(40, start_y, 550, start_y)
        start_y -= 10


        c.setFont("Helvetica", 11)
        for b in daten["eintraege"]:
            if start_y < 80:
                c.showPage()
                start_y = 780

            c.drawString(40, start_y, b["buchtitel"])
            c.drawString(240, start_y, b["autor"])
            c.drawString(380, start_y, b["faelligkeitsdatum"])
            c.drawString(450, start_y, f'{b["tage_ueberzogen"]} Tage')
            start_y -= line_height

        start_y -= 10

    c.save()




#erstelle_mahnschreiben(101, "C:/Users/max/Nextcloud/Meine Daten/Informatik/Bib/Pfad")
#erstelle_sammel_mahnung(ausleihen_liste, "C:/Users/max/Nextcloud/Meine Daten/Informatik/Bib/Pfad")
erstelle_mahnschreiben(101, "I:\Informatik\Bib\Pfad")
erstelle_sammel_mahnung(ausleihen_liste, "I:\Informatik\Bib\Pfad")