#Check-Total-Connections.py#

##Usage
 
>Check-Total-Connections.py [-h] [-v] [-T] [-s] [--progress] [-t TIME]
                                  [-d DATA] [-n] [-u USER] [-p PASSWORD]
                                  [-m MOUNTPOINT]
                                  server port

###Positional arguments:
`server`

* IP of server to test

`port`

* PORT of server to test

###optional arguments:

`-h, --help`

* show this help message and exit

`-v, --verbose`

* Verbose. use -vv for more information

`-T, --tell`

* Tell the settings for the run.

`-s, --summary`

* Summary information about each connection, otherwise just totals are displayed

`--progress`

* Show indication of progress while reading from connections

`-t TIME, --time TIME`

* Minimum length of the time for the connection for data to be received. 
  * Note that the connections will be open for longer than this, this is just the minimum time that the connection will be open.

`-d DATA, --data DATA`

* Minimum amount of data to be received for the connection to be called good.

`-n, --ntrip`

* Connection is NTRIP, send user name and password after connecting
  * If NTRIP is not set then a normal TCP Connection is made
  * If NTRIP is set then a NTRIP V1 header is sent after connection

`-u USER, --user USER`

*  The Ntripcaster username. Default: IBS
*  Only used if the connection is NTRIP

`-p PASSWORD, --password PASSWORD` 

* The Ntripcaster password. Default: IBS
*  Only used if the connection is NTRIP

`-m MOUNTPOINT, --mount MOUNTPOINT`

* The Ntripcaster mountpoint. Default: CMRx
*  Only used if the connection is NTRIP


