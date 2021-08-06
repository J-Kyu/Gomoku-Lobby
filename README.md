# Gomoku Lobby
Gomoku Lobby Server is lobby server which handles gomoku games. Gomoku Lobby is consist of two servers which are GSS(Gomoku Session Server) and GSMS (Gomoku Session Managing Server). GSS is responsible of game rule and communication between clients. On the other hand GSMS handles generating and killing GSS and delivering GSS information to client. 



<img src=".\images\topArchitecture.jpg" style="zoom:20%;" />

### Gomoku Session Detail Design

<img src=".\images\detail.jpg" alt="detail" style="zoom:20%;" />

GSS is separated into 3 states. In Ready state, GSS will wait until both clients are connected to  GSS. Once both client is connected to GSS, GSS will generate Gokumo game. Game Rule is as follows.

* Color of stone will be selected by reverse order of connection. (Early = black, Late = white)
* Rule is identical with ordinal Gokumo except the size of board can be varied in different session.
* (3x3 is allowed only for now, will be fixed)

GSS provides following methods.

