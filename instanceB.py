from xmlrpc.server import SimpleXMLRPCServer
from threading import Lock

ok, abort = 'Ok', 'Abort'

# This instance holds account A
# instance class for regular servers (Not a coordinator)
class Instance:
        def __init__(self) -> None:
            self.account = {
                'balance': 300,
                'id': 'B',
            }
            self.lock = Lock()
            self.currentTransaction = None
            pass

        def prepare(self, transaction):


            if self.lock.locked(): 
                return abort
            
            try:
                self.lock.acquire()

                t_id, operation = transaction
                self.currentTransaction = transaction

                if operation + self.account['balance'] >= 0:
                    return ok
                return abort

            
            except:
                print('Something whent worng while cquaring lock')
                return abort

        def commit(self, t_id):

            if(t_id == self.currentTransaction[0]):
                self.account['balance'] += self.currentTransaction[1]
                
            self.lock.release()
            pass



ADDRESS = ('localhost', 8002)
WELCOME_MESSAGE = f'''COORDINATOR SERVER.
Running on {ADDRESS}.
Commands:
    - Quit server: control + c

Waiting for clients...'''


# Create server
with SimpleXMLRPCServer(ADDRESS, allow_none=True) as server:
    print(WELCOME_MESSAGE)
    
    
    server.register_introspection_functions()

    server.register_instance(Instance())

    # Run the server's main loop
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nQuitting server. Exiting...")
    


