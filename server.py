import json
import socket
import select
import secrets
from Gomoku import Gomoku

class GomokuSession:

    def __init__(self):

        # gomoku info
        self.gameState = 'READY'
        self.userPool = []
        self.client_one_tokenID = None
        self.client_two_tokenID = None

        self.gomoku = None
    
        # server info
        self.ip = None
        self.port = None

    def HandlingClient(self,client_socket,addr):
        
        resposne = '1000^{}'

        packet = client_socket.recv(1024).decode('utf-8')
        packet_chunk = packet.split('^')

        
        inCommand = packet_chunk[0]
        inData = packet_chunk[1]
        jsonData = json.loads(inData)

        # 0001-client is ready
        if inCommand == '0001':
            # error check
            if 'tokenID' not in jsonData:
                print("Error-0001-Wrong Packet Format")
                return 
            # set client is ready
            if jsonData['tokenID'] not in self.userPool:
                self.userPool.append(jsonData['tokenID'])
            
            # check if game is ready
            if len(self.userPool) == 2:

                tokenID = secrets.token_urlsafe(16)
                # allocate token
                if self.client_one_tokenID == None:
                    self.client_one_tokenID = tokenID
                    response = '1100^{{ "tokenID": "{0}", "dolColor": "{1}" }}'.format(tokenID,"white")
                else:
                    self.client_two_tokenID = tokenID
                    response = '1100^{{ "tokenID": "{0}", "dolColor": "{1}" }}'.format(tokenID,"black")


                # create gomoku
                if self.client_two_tokenID and self.gomoku == None:
                   self.gomoku = Gomoku(self.client_one_tokenID,self.client_two_tokenID)
                   print("Debug______{0}, {1}".format(self.client_one_tokenID,self.client_two_tokenID))


            # game session is now full
            elif len(self.userPool) > 2:
                response = '1200^{}'
            else:
                response = '1000^{}'
            
        # below this line,is all about communicating with actual game session
        # thus, we have to check game session is ready
        elif not self.gomoku:
            response = '1900^{}'


        # 0002-locating here
        elif inCommand == '0002':
                       # not your turn
            if not self.gomoku.CheckTurn(jsonData['tokenID']):
                response = '1600^{}'
            # Not an empty spot
            elif not self.gomoku.CheckEmptyLocation(jsonData['x'],jsonData['y']):
                response = '1500^{}'
            # failed locating dol at position
            elif not  self.gomoku.LocatePos(jsonData['tokenID'],jsonData['x'],jsonData['y']):
                response = '1300^{}'
            # successfully locating dol
            else:
                grid = self.gomoku.GetGrid()
                response = '1400^{{ "grid": {0} }}'.format(grid)

        # 0003-Check Game Over
        elif inCommand == '0003':
            isGameOver, winner = self.gomoku.CheckGameOver()
            if isGameOver:
                response = '1700^{{ "gameState": "{0}", "winner": "{1}"   }}'.format("GAME_END",winner)
            else:
                response = '1700^{{ "gameState": "{0}", "winner": "{1}"   }}'.format("IN_GAME","None")
        # 0004-Request grid 
        elif inCommand == '0004':
            grid = self.gomoku.GetGrid()
            response = '1800^{{"grid": {0} }}'.format(grid)

        else:
            response = '9999^{}'

        print(packet)
        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()
                
    
    def Run(self):
        # create server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        # bind socket
        server_socket.bind((self.ip,self.port))
        # listening socket
        server_socket.listen()


        while True:
            print('waiting.....')
            # for preventing blocking, use select method
            readableFD, writeableFD, cnd = select.select([server_socket],[],[],3)
            for fd in readableFD:
                # when file descriptor is reading server socket
                if fd == server_socket:
                    client_socket, addr = server_socket.accept()
                    self.HandlingClient(client_socket,addr)

if __name__ == '__main__':
    # parse require

    a =  GomokuSession() 
    a.ip = '0.0.0.0'
    a.port = 9999

    a.Run()
