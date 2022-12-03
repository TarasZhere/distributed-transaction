from xmlrpc.client import ServerProxy

try:
    serverConnection = ServerProxy('http://localhost:8000')
    print('Connected to coordinator server')

    # print(serverConnection.system.listMethods())

    print(serverConnection.transfer(('A', 'B', 50))) 

except EnvironmentError as e:
    print('Could not connect to server...\n', e)
    pass