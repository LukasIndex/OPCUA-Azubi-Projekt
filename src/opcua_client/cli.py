import getpass
import argparse


def parser_cli_arguments():  # defines parser cli arguments for the OPC UA client
    parser = argparse.ArgumentParser(
        prog="OPCUA Client",
        description="An OPCUA Client made for fast access to OPCUA Server Nodes via read/subscribe and access to events",
        epilog="Made by LukasIndex and NoahIndex"
    )
    parser.add_argument("-s","--server", help="OPC UA Endpoint eingabe")
    parser.add_argument("-u","--username", help="Username eingabe")
    parser.add_argument("-p","--password", help="Password eingabe")
    parser.add_argument("-v","--verbose", action="store_true", help="Großzügige ausgabe")
    parser.add_argument("-i","--interactive", action="store_true", help="Aktiviert interaktiven Modus mit Eingabeaufforderungen")
    parser.add_argument("-ID","--identify", action="store_true", help="Identifizierung der Maschiene")
    parser.add_argument("-e","--event", help='EVENT Node angeben: "ns=X;i=Y"')  # "" inside '' works somehow lol
    parser.add_argument("-n","--node", help='NODE angeben: "ns=X;i=Y"')
    parser.add_argument("-m","--mode", choices=["read", "subscribe"], help="Modus: read oder subscribe auswählen (read is fallback)")
    args = parser.parse_args()
    return args

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
    
def abfrage_password():  # waits for password input and returnes it
    while True:
        wert = getpass.getpass("Gib dein Passwort ein: ")  # getpass hides password while typing
        return wert
    
def abfrage_event():  # 3. waits for event node input and returnes it
    while True:
        event = input("Event Node eingeben: ").strip()
        if event:
            return event
        print("Eingabe darf nicht leer sein.")   
        
def abfrage_wert():  # 4. waits for node input from user and returnes it
    while True:
        wert = input("Abfrage Wert eingeben: ").strip()
        if wert:
            return wert
        print("Eingabe darf nicht leer sein.")
