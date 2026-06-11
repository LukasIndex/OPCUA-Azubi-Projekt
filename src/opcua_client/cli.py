 
def abfrage_server():  # 1. waits for OPC UA server adress and returnes it 
    while True:
        wert = input("Server Adresse eingeben: ").strip()
        if wert:
            return wert
        print("Eingabe darf nicht leer sein.")


def abfrage_uname():  # 2. waits for username input and returnes it
    while True:
        wert = input("Benutzername eingeben: ").strip()
        return wert 
    
        
def abfrage_wert():  # 3. waits for node request from user
    while True:
        wert = input("Abfrage Wert eingeben: ").strip()
        if wert:
            return wert
        print("Eingabe darf nicht leer sein.")
