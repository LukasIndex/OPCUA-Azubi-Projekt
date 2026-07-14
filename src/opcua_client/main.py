import sys
import logging
import getpass
import asyncio
import opcua_client.config as config
from rich import print
from opcua_client.cli import parser_cli_arguments, abfrage_server, abfrage_uname, abfrage_password, abfrage_event, abfrage_wert
from opcua_client.opcua_client import OpcUaClient


async def async_main():  # define async main function

    args = parser_cli_arguments()  # calling the parser to use the cli arguments

    if not args.verbose:
        logging.getLogger("asyncua").setLevel(logging.CRITICAL)  # if --verbose is not set only log the critical stuff
    
    if args.verbose:  # only prints if --verbose is set.
        print("Starte OPC UA Client")

    if args.server:
        config.OPCUA_ENDPOINT = args.server
    else:
        config.OPCUA_ENDPOINT = abfrage_server()

    if args.verbose:
        print("Endpoint:", config.OPCUA_ENDPOINT)  # prints the server adress of the opcua endpoint

   
    if args.username:
        username = args.username
    else:
        username = abfrage_uname()

  
    if args.password:
        password = args.password
    else:
        password = abfrage_password()
        
    client = OpcUaClient(  # gives the variable client the endpoint, username and password so it can be used later
        config.OPCUA_ENDPOINT,
        username=username,
        password=password
    )

    async def node_client():  # takes the node input and asks for read or subscribe
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
            await await_subscription("subscribe_node")
        else:
            if args.verbose:
                print(f"Modus: {modus}")
            value = await client.read_node(config.NODE_TO_READ)
            if args.verbose:
                print("Wert gelesen:")
            print(value)

    async def await_subscription(XtoSubscribe):  # uniform function for subscription delete logic
        SubscribeFunc = getattr(client, XtoSubscribe)
        await SubscribeFunc()

        async def wait_for_enter():
             print("Subscription aktiv, Enter drücken zum beenden")
             await asyncio.to_thread(getpass.getpass,prompt = "")

        try:
            await wait_for_enter()
        except (KeyboardInterrupt, asyncio.CancelledError):
            raise KeyboardInterrupt
        finally:
            if args.verbose:
                print("Subscription wird beendet")
            if client.active_subscription:
                try:
                    await client.active_subscription.delete()  # ends the subscription clean
                    client.active_subscription = None
                except Exception:
                    pass
        if not args.interactive:
            raise asyncio.CancelledError  # raises the error to the main function    


    async def run_client():  # start of the client
        if args.event:
            config.EVENT_NODE = args.event
            if args.verbose:
                print("Events Werden Angezeigt, STRG C zum beenden")
            await await_subscription("subscribe_events")
        elif not args.event and not args.node and not args.mode:
            action = input("Event oder Node abfragen? (e/N): ").strip().lower()
            if action == "e":
                if args.event:
                    config.EVENT_NODE = args.event
                else:
                    config.EVENT_NODE = abfrage_event()
                if args.verbose:
                    print("Events Werden Angezeigt, STRG C zum beenden")
                await await_subscription("subscribe_events")
            else:
                await node_client()
        else:
            await node_client()

    async def while_client():  # runs if --interactive is set
        while True:
            await run_client()  # loops the run_client for interactive mode 

            weiter = input("Nochmal abfragen? (y/N) oder neustarten (r): ").strip().lower()  # N in caps to visualize "pre select"
            if weiter == "r":
                args.event = None
                config.EVENT_NODE = None
                config.NODE_TO_READ = None
                args.node = None
                args.mode = None
                continue

            if weiter != "y":  # if anything else then "y" disconnect and break
                await client.disconnect()
                break

    try:
        await client.connect()  # waits for connection to the client with the defined endpoint etc.
        if args.verbose:
            if username != None:
                print("Angemeldet als:", username)
            else:
                print("Angemeldet als: Anonym")  # if no username is specified it counts as a anonymous login

        if args.browse:
            await client.show_nodes()

        if args.diagnostics:
            await client.server_diagnostics()

        if args.identify:
            await client.machine_identifiers()  # calls a fuction for getting the machine identifiers

        if not args.interactive:  # not interactive = run client once 
            await run_client()

        else:
            await while_client()  # interactive = loop the client

    except (KeyboardInterrupt, asyncio.CancelledError):  # if the programm gets interrupted via CTRL + C raise Keyboardinterrupt
        if args.verbose:
            print("Beendet durch Keyboard Interrupt")
            raise KeyboardInterrupt
    except Exception as e:
        print("Fehler:", e)

    finally:  # at last if a subscription is active try to end it and disconnect from server
        if client.active_subscription:
            try:
                await client.active_subscription.delete()
                client.active_subscription = None
            except Exception:
                pass
        try:
            await asyncio.wait_for(client.disconnect(), timeout=1.5)  # waits a bit for clean disconnect
        except Exception:
            pass

        if args.verbose:
            print("Client beendet")


def main():  # main function calls async main function
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:  # exit the programm when CTRL + C is pressed
        sys.exit(0)

if __name__ == "__main__":
    main()
