def abfrage_wert():
    while True:
        wert = input("Abfrage Wert eingeben: ").strip()
        if wert:
            return wert
        print("Eingabe darf nicht leer sein.")


def abfrage_pw():
    while True:
        wert = input("Passwort eingeben: ").strip()
        if wert:
            return wert
        print("Eingabe darf nicht leer sein.")