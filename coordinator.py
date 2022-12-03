from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
from time import sleep


ok, abort = 'Ok', 'Abort'

'''
    Fucntions needed for the coordinator.
    These fucntions are not collabe by other instances via RPC
'''
def connectToOtherInstances():
    servers = {}
    for port, account in [(8001, 'A'), (8002, 'B')]:
        try:
            servers[account] = ServerProxy(f'http://localhost:{port}')
        except:
            print(f'Could not connect to localhost:{port}')

    return servers

def withdraw(transaction, servers):
    id, account, ammount = transaction
    if servers[account].prepare((id, ammount)) == ok:
        return True
    return False

def deposit(transaction, servers):
    id, account, ammount = transaction
    if servers[account].prepare((id, ammount)) == ok:
        return True
    return False

def checkConnection(servers):
    for server in servers.values():
        if not server:
            return False
    return True



def commit(id, servers):
    for server in servers.values():
        server.commit(id)

''' 
    All fuctions present in the coordinator class are collable via RPC by other Instances
'''
class Coordinator:
        def __init__(self) -> None:
            self.servers = connectToOtherInstances()
            self.accounts = None
            pass

        def transfer(self, transaction):

            # check connection to servers
            ct = 5
            while ct >= 0 and not checkConnection(self.servers):
                ct-=1
                sleep(2)
                

            from_, to_, ammount = transaction
            # Create an ID
            transaction_id = 3043
            w = (transaction_id,    from_,     - abs(ammount))
            d = (transaction_id,    to_,       abs(ammount))

            if withdraw(w, servers=self.servers) and deposit(d, servers=self.servers):
                commit(transaction_id, self.servers)
                return ok

            return abort



# CONSTs
ADDRESS = ('localhost', 8000)

WELCOME_MESSAGE = f'''COORDINATOR SERVER.
Running on {ADDRESS}.
Commands:
    - Quit server: control + c

Waiting for clients...'''

# Create server
with SimpleXMLRPCServer(ADDRESS, allow_none=True) as server:

    print(WELCOME_MESSAGE)
    
    server.register_introspection_functions()

    server.register_instance(Coordinator())

    # Run the server's main loop
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nQuitting server. Exiting...")