# Gomoku Lobby

[Example Video](https://youtu.be/SCW5VSFOUow)

Gomoku Lobby Server is lobby server which handles gomoku games. Gomoku Lobby is consist of two servers which are GSS(Gomoku Session Server) and GSMS (Gomoku Session Managing Server). GSS is responsible of game rule and communication between clients. On the other hand GSMS handles generating and killing GSS and delivering GSS information to client. 



<img src=".\images\topArchitecture.jpg" style="zoom:20%;" />

## Gomoku Session Detail Design

<img src=".\images\detail.jpg" alt="detail" style="zoom:20%;" />

GSS is separated into 3 states. In Ready state, GSS will wait until both clients are connected to  GSS. Once both client is connected to GSS, GSS will generate Gokumo game. Game Rule is as follows.

* Color of stone will be selected by reverse order of connection. (Early = black, Late = white)
* Rule is identical with ordinal Gokumo except the size of board can be varied in different session.
* (3x3 is allowed only for now, will be fixed)

## GSS provides following methods.

### RequestCode (Client -> GSS)

| Code | Explanation                    |
| ---- | ------------------------------ |
| 0001 | I am Reay                      |
| 0002 | Locating Stone on x,y position |
| 0003 | Is Game Ended                  |
| 0004 | Request gomoku board           |

### Response Code (GSS -> Client)

| Code | Explanation                                                  |
| ---- | ------------------------------------------------------------ |
| 1000 | The other client is not ready yet.....keep sending 001 packet |
| 1100 | Your Ready Has been Accepted....Sending your valid token     |
| 1200 | Number of player is full.....                                |
|      |                                                              |
| 1300 | Location is already occupied                                 |
| 1400 | Valid Location, your move has been accepted                  |
| 1500 | Invalid Location, your move has been denied                  |
| 1600 | This is not your turn                                        |
|      |                                                              |
| 1700 | Return Game Result                                           |
| 1800 | Return gomoku board                                          |
| 1900 | GSS is Not ready                                             |
| 9999 | Wrong Request                                                |

### Client
In this project, client will read given notation(기보) and request GSS to locate go stone. Client also has 3 state which are Ready,In-Game and End Game. In Ready state, client will keeep sending that the client is ready untill GSS answer with gomoku is ready. Once game has started, in the order of turns, each client will rquest to locate go stone by following the given notation(기보). In this process, GSS will check whether now is the player's turn and whether given location is valid location. If GSS successfully located go stone, client will ask whether the game is ended or not. If one of player made gomoku, then both client and GSS will change its state into Game End state. 


