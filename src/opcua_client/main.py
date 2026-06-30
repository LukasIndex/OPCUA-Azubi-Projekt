import sys
import asyncio
import opcua_client.config as config
from rich import print
from opcua_client.cli import parser_cli_arguments, abfrage_wert, abfrage_uname, abfrage_password, abfrage_server
from opcua_client.opcua_client import OpcUaClient


async def async_main():  # define async main function
    print("Starte OPC UA Client")

    args = parser_cli_arguments()  # calling the parser to use the cli arguments

    
    if args.server:
        config.OPCUA_ENDPOINT = args.server
    else:
        config.OPCUA_ENDPOINT = abfrage_server()

    # print("Endpoint:", config.OPCUA_ENDPOINT)  # prints the server adress of the opcua endpoint

   
    if args.username:
        username = args.username
    else:
        username = abfrage_uname()

  
    if args.password:
        password = args.password
    else:
        password = abfrage_password()
        
    client = OpcUaClient(
        config.OPCUA_ENDPOINT,
        username=username,
        password=password
    )

    try:
        await client.connect()
        print("Angemeldet als:", username)

        if args.identify:
            await client.machine_identifiers()  # calls a fuction for getting the machine name

        if not args.interactive and not args.node:
            raise ValueError("Bitte --node angeben oder --interactive verwenden.")

        if not args.interactive:
            if args.event:
                print("Events Werden Angezeigt:")
                await client.subscribe_events()

            config.NODE_TO_READ = args.node
            print("Node:", config.NODE_TO_READ)

            modus = args.mode
            if modus == None:
                print("Modus: Read")
            elif modus != None:
                print("Modus:", modus)

            if modus in ["s", "subscribe"]:
                await client.subscribe_node(config.NODE_TO_READ)
            else:
                value = await client.read_node(config.NODE_TO_READ)
                print(f"Wert gelesen: {value}")

        else:
            while True:
                if args.event:
                    print("Events Werden Angezeigt:")
                    await client.subscribe_events()
                    break

                if args.node:
                    config.NODE_TO_READ = args.node
                else:
                    config.NODE_TO_READ = abfrage_wert()

                print("Node:", config.NODE_TO_READ)

                if args.mode:
                    modus = args.mode
                else:
                    modus = input("Read oder Subscribe? (R/s): ").strip().lower()  # R in caps to visualize "pre select"

                if modus in ["s", "subscribe"]:
                    await client.subscribe_node(config.NODE_TO_READ)
                    break
                else:
                    value = await client.read_node(config.NODE_TO_READ)
                    print(f"Wert gelesen: {value}")

                weiter = input("Nochmal abfragen? (y/N): ").strip().lower()  # N in caps to visualize "pre select"

                if weiter != "y":
                    break

    except (KeyboardInterrupt, asyncio.CancelledError):
        sys.exit(0)

    except Exception as e:
        print("Fehler:", e)

    finally:
        await client.disconnect()
        print("Client beendet")


def main():  # main function calls async main function
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
