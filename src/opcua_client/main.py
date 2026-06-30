import sys
import logging
import asyncio
import opcua_client.config as config
from rich import print
from opcua_client.cli import parser_cli_arguments, abfrage_wert, abfrage_uname, abfrage_password, abfrage_server
from opcua_client.opcua_client import OpcUaClient


async def async_main():  # define async main function

    args = parser_cli_arguments()  # calling the parser to use the cli arguments

    if not args.verbose:
        logging.getLogger("asyncua").setLevel(logging.CRITICAL)
    
    if args.verbose:
        print("Starte OPC UA Client")

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

    async def run_client():
        if args.event:
            if args.verbose:
                print("Events Werden Angezeigt, STRG C zum beenden")
            await client.subscribe_events()

        if args.node:
            config.NODE_TO_READ = args.node
        else:
            config.NODE_TO_READ = abfrage_wert()

        if args.verbose:
            print("Node:", config.NODE_TO_READ)

        if args.mode:
            modus = args.mode
        else:
            modus = input("Read oder Subscribe? (R/s): ").strip().lower()  # R in caps to visualize "pre select"

        if modus in ["s", "subscribe"]:
            if args.verbose:
                print(f"Modus: {modus}")
            await client.subscribe_node(config.NODE_TO_READ)
        else:
            if args.verbose:
                print(f"Modus: {modus}")
            value = await client.read_node(config.NODE_TO_READ)
            if args.verbose:
                print("Wert gelesen:")
            print(value)

    try:
        await client.connect()
        if args.verbose:
            if username != None:
                print("Angemeldet als:", username)
            else:
                print("Angemeldet als: Anonym")

        if args.identify:
            await client.machine_identifiers()  # calls a fuction for getting the machine identifiers

        if not args.interactive:
            await run_client()

        else:
            while True:
                await run_client()

                weiter = input("Nochmal abfragen? (y/N): ").strip().lower()  # N in caps to visualize "pre select"

                if weiter != "y":
                    break

    except (KeyboardInterrupt, asyncio.CancelledError):
        sys.exit(0)

    except Exception as e:
        print("Fehler:", e)

    finally:
        await client.disconnect()
        if args.verbose:
            print("Client beendet")


def main():  # main function calls async main function
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
