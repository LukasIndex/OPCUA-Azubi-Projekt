import asyncio
import config
from cli import abfrage_wert, abfrage_uname, abfrage_server
from opcua_client import OpcUaClient
import getpass
import argparse


async def main():
    print("Starte OPC UA Client")

    
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", help="OPC UA Endpoint")
    parser.add_argument("--node", help="NodeId")
    parser.add_argument("--username", help="Username")
    parser.add_argument("--password", help="Password")
    parser.add_argument("--mode", choices=["read", "subscribe"], help="Modus: read oder subscribe")
    args = parser.parse_args()

    
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
        password = getpass.getpass("Gib dein Passwort ein: ")

    client = OpcUaClient(
        config.OPCUA_ENDPOINT,
        username=username,
        password=password
    )

    print("Angemeldet als:", username)

    try:
        await client.connect()
        print("Verbindung aufgebaut")

        while True:

           
            if args.node:
                config.NODE_TO_READ = args.node
            else:
                config.NODE_TO_READ = abfrage_wert()

            print("Node:", config.NODE_TO_READ)

          
            if args.mode:
                modus = args.mode
                print("Modus:", modus)
            else:
                modus = input("Read oder Subscribe? (r/s): ").strip().lower()

           
            if modus in ["s", "subscribe"]:
                await client.subscribe_node(config.NODE_TO_READ)
                break

            else:
                value = await client.read_node(config.NODE_TO_READ)
                print(f"Wert gelesen: {value}")

            weiter = input("Nochmal abfragen? (y/n): ").strip().lower()
            if weiter != "y":
                break

    except Exception as e:
        print("Fehler:", e)

    finally:
        await client.disconnect()
        print("Client beendet")


if __name__ == "__main__":
    asyncio.run(main())