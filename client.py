import socket
import time
import json
import secrets
import argparse
import os

class MockClient:

    def __init__(self):
        # client info
        self.port = None
        self.clientTokenID = secrets.token_urlsafe(16)
        
        # game info
        self.gameTokenID = None
        self.dolColor = None
        self.state = None
        self.winner = None
        self.gibo = []

    def SendToGS(self,ip,port,data):

        try:
            # connect to Gomoku Session
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip,port))
        except ConnectionRefusedError as err:
            print(err)
            return ''

        client_socket.sendall(data.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print('received: {0}'.format(response))
        return response


    def ReadGibo(self,file_Path):

        if not os.path.exists(file_path):
            print("No file exist")
            return

        print(file_path)
        with open(file_path) as json_file:
            gibo = json.load(json_file)
            for i in gibo.values():
                self.gibo.append(i)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description = 'Game Client')
    parser.add_argument('--f',type=str, help='File location')

    args = parser.parse_args()
    file_path =  args.f
    # MockClient Init
    a = MockClient()
    a.port = 9998
    a.ReadGibo(file_path)


    # ready state
    while True:
        time.sleep(1)

        if a.state == 'IN_GAME' or a.state == 'END_GAME' :
            break

        else:
            packet = a.SendToGS('0.0.0.0',9999,'0001^{{"tokenID": "{0}"}}'.format(a.clientTokenID))
            packet_chunk = packet.split('^')
            # check packet
            if len(packet_chunk) < 2:
                print('Not Enought Chunk')
                quit()

            inCommand = packet_chunk[0]
            inData = packet_chunk[1]

            jsonData = json.loads(inData)

            # verify response code
            # 1000-game session is not ready-yet, keep sending
            if inCommand == '1000':
                continue
            # 1100-game session is now ready, take your token code
            elif inCommand == '1100':
                if 'tokenID' in jsonData and 'dolColor' in jsonData:
                    a.gameTokenID = jsonData['tokenID']
                    a.dolColor = jsonData['dolColor']
                    a.state = 'IN_GAME'
                    break
            # 1200-game session is full
            elif inCommand == '1200':
                print('Gomoku Session is full')
                quit()


    # check
    if a.state == None or a.state == 'READY':
        print('Wrong State')
        quit()
            
    print(a.gameTokenID,a.dolColor)





    # IN_GAME state
    while True:
        if len(a.gibo[0]) <= 0:
            print("No more gibo.....Exiting from testing")
            quit()
        
        # 0002 - Locating  
        pos = a.gibo[0]
        packet = a.SendToGS('0.0.0.0',9999,'0002^{{"tokenID": "{0}", "x": "{1}", "y": "{2}" }}'.format(a.gameTokenID,pos[0],pos[1]))

        packet_chunk = packet.split('^')
        # check packet
        if len(packet_chunk) < 2:
            print('Not Enought Chunk')
            quit()

        inCommand = packet_chunk[0]
        inData = packet_chunk[1]

        jsonData = json.loads(inData)
        
        # 1900-game session is not ready
        if inCommand == '1900':
            time.sleep(1)
            continue

        # 1600-not my turn
        elif inCommand == '1600':
            time.sleep(1)
            continue
        # 1500-invalid Location and  1300-wrong location
        elif inCommand == '1500': 
            print("Debug----------------2")
            a.gibo.pop(0)
        elif inCommand == '1300':
            print("Debug----------------")
            a.gibo.pop(0)
        # 1400-dol has been accepted  (success)
        elif inCommand == '1400':
            a.gibo.pop(0)


        #pause for 1 sec
        time.sleep(1)

        # 0004-request grid
        packet = a.SendToGS('0.0.0.0',9999,'0004^{{"tokenID": "{0}" }}'.format(a.gameTokenID))

        packet_chunk = packet.split('^')
        # check packet
        if len(packet_chunk) < 2:
            print('Not Enought Chunk')
            quit()

        inCommand = packet_chunk[0]
        inData = packet_chunk[1]

        jsonData = json.loads(inData)
 
        # 0004 only takes 1800
        if inCommand != '1800':
            print("wrong packet")
            quit()

        grid = jsonData['grid']
        print(grid)


        #pause for 1 sec
        time.sleep(1)





        # 0003-ask is game over
        packet = a.SendToGS('0.0.0.0',9999,'0003^{{"tokenID": "{0}" }}'.format(a.gameTokenID))

        packet_chunk = packet.split('^')
        # check packet
        if len(packet_chunk) < 2:
            print('Not Enought Chunk')
            quit()

        inCommand = packet_chunk[0]
        inData = packet_chunk[1]

        jsonData = json.loads(inData)
 
        # 0003 only takes 1700
        if inCommand != '1700':
            print("wrong packet")
            quit()

        # game end
        if jsonData['gameState'] == 'GAME_END':
            a.state = 'GAME_END'
            a.winner = jsonData['winner']
            break


        #pause for 1 sec
        time.sleep(1)


    # game end
