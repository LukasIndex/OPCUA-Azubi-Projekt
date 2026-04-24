def abfrage_wert():
    while True:
        wert = input("Abfrage Wert eingeben: ").strip()
        if wert:
            return wert
        print("Eingabe darf nicht leer sein.")