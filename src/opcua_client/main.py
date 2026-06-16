import asyncio
import getpass
import argparse
import opcua_client.config as config
#  from opcua_client.console import open_window (Out of Scope)
from opcua_client.cli import abfrage_wert, abfrage_uname, abfrage_server
from opcua_client.opcua_client import OpcUaClient



def parser_cli_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", help="OPC UA Endpoint")
    parser.add_argument("--username", help="Username")
    parser.add_argument("--password", help="Password")
    #  parser.add_argument("--window", action="store_true", help="Öffnet ein seperates Fenster") (Out of Scope)
    parser.add_argument("--event", action="store_true", help="Alarmmeldungen der Maschiene")
    parser.add_argument("--node", help="NodeId")
    parser.add_argument("--mode", choices=["read", "subscribe"], help="Modus: read oder subscribe")
    args = parser.parse_args()
    return args



async def async_main():
    print("Starte OPC UA Client")

    args = parser_cli_arguments()

    
    if args.server:
        config.OPCUA_ENDPOINT = args.server
    else:
        config.OPCUA_ENDPOINT = abfrage_server()

    print("Endpoint:", config.OPCUA_ENDPOINT)

   
    if args.username:
        username = args.username
    else:
        username = abfrage_uname()

  
    if args.password:
        password = args.password
    else:
        password = getpass.getpass("Gib dein Passwort ein: ")  # password stays hidden via getpass

    client = OpcUaClient(
        config.OPCUA_ENDPOINT,
        username=username,
        password=password
    )

    try:
        await client.connect()
        print("Verbindung aufgebaut")
        print("Angemeldet als:", username)

        if args.event:
            print("Events Werden Angezeigt:")
            while client.subscribe_events():
                await client.subscribe_events()
                break
            

        if args.node:
            config.NODE_TO_READ = args.node
        else:
            config.NODE_TO_READ = abfrage_wert()

        print("Node:", config.NODE_TO_READ)

          
        if args.mode:
            modus = args.mode
            print("Modus:", modus)
        else:
            modus = input("Read oder Subscribe? (R/s): ").strip().lower()  # R in caps to visualize "pre select"

        while True:

            if modus in ["s", "subscribe"]:
                await client.subscribe_node(config.NODE_TO_READ)
                break

            else:
                value = await client.read_node(config.NODE_TO_READ)
                print(f"Wert gelesen: {value}")

            weiter = input("Nochmal abfragen? (y/N): ").strip().lower()  # N in caps to visualize "pre select"

            if weiter !="y":
                break

    except Exception as e:
        print("Fehler:", e)

    finally:
        await client.disconnect()
        print("Client beendet")


def main():
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
