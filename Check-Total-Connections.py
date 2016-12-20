#! /usr/bin/env python

import socket
import sys
import base64

import time

import argparse

NUM_Sockets=20
IP="172.27.0.42"
#IP="127.0.0.1"
PORT=28006
WAIT=10
MIN_DATA=1023

server_address = (IP, PORT)
NTRIP=True
MOUNTPOINT="CMRx"
USER="IBS"
PASSWORD="IBS"
PROGRESS=False
DETAIL=True
VERBOSE=1

def open_connections(NUM_Sockets,sock,Total_Bytes,VERBOSE):
  Failed_To_Connect=0
  Connected=0
  # Create a TCP/IP socket

  for Current_Sock  in range(NUM_Sockets):

    sock [Current_Sock]= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock [Current_Sock].settimeout(1)
  #  sock [Current_Sock].setsockopt("SO_RCVBUF"
    if VERBOSE >=2:
      print >>sys.stderr, 'Connection %s connecting to %s port %i' % (Current_Sock+1,IP,PORT)
    try:
      sock[Current_Sock].connect(server_address)  
      if NTRIP:
        sock[Current_Sock].send(NTRIP_Get_String)
  #    print sock[Current_Sock].getsockname()[1]
      Connected+=1
    except :
      if VERBOSE >=1:
        print >>sys.stderr,"Failed to connect on connection %i (%i)" % (Current_Sock+1 , sock[Current_Sock].getsockname()[1])
      Failed_To_Connect+=1

  if VERBOSE >= 1:
    print >>sys.stderr,"Failed to connect: %s" % Failed_To_Connect
    print >>sys.stderr,"Connected %s" % Connected
  
  return(Connected,Failed_To_Connect)

def read_from_connections (NUM_Sockets,sock,Total_Bytes,VERBOSE,PROGRESS) :   
  current_Wait=0
  buffer_size=1024*50

  while current_Wait < WAIT:
    if PROGRESS:
      if current_Wait % 60 == 0:
        sys.stderr.write('{:<3}:'.format(int(current_Wait / 60)))

      sys.stderr.write('.')
    time.sleep(1)
  
    for Reverse_Sock  in range(NUM_Sockets):
      Current_Sock=NUM_Sockets-1-Reverse_Sock
    #  print "Reading %s" % Current_Sock
      data_received=0
      finished_data=False
      data=""
      while not finished_data:
        try:          
          data, server_address_info=sock[Current_Sock].recvfrom(buffer_size)
          data_received+=len(data)
          finished_data=len(data)!=buffer_size
        except socket.timeout:
          finished_data_data=False  
        except:
  #        print >>sys.stderr,"Got error reading on connection: %i"%Current_Sock
          finished_data=True
  #        print "len {} got {}".format(len(data),finished_data)
  #    print data
  #    print >>sys.stderr,"Read data of length %i from  socket %i" % (data_received,Current_Sock)
      Total_Bytes[Current_Sock]+=data_received 
    current_Wait+=1
    if PROGRESS:
      if current_Wait % 60 == 0:
        print >>sys.stderr


def check_results (NUM_Sockets,sock,Total_Bytes,DETAIL):
  Enough_Data=0

  for Current_Sock in range(NUM_Sockets):

    if Total_Bytes[Current_Sock]>= MIN_DATA:
      if DETAIL:
        print >>sys.stderr,"Connection %i, Got enough data %i, port (%i)" %  (Current_Sock+1,Total_Bytes[Current_Sock],sock[Current_Sock].getsockname()[1])
      Enough_Data+=1
    else:
      if DETAIL:
        print >>sys.stderr,"Connection %i, did not get enough data, %i, port (%i)" %  (Current_Sock+1 ,Total_Bytes[Current_Sock],sock[Current_Sock].getsockname()[1])
  return (Enough_Data)
  
#time.sleep(10)

def create_arg_parser():
    usage="Check_Total_Connections.py [options] [server] [port] "
    parser=argparse.ArgumentParser()
    parser.add_argument("server", type=str, help="IP of server to test")
    parser.add_argument("port", type=int, help="PORT of server to test")

#    parser.add_argument("-c", "--connections", type=int, dest="NumberConnections", default=60, help="Number of Connections to be opened")

#    parser.add_argument("-t", "--latitude", type="float", dest="lat", default=50.09, help="Your latitude.  Default: %default")
#    parser.add_argument("-g", "--longitude", type="float", dest="lon", default=8.66, help="Your longitude.  Default: %default")
#    parser.add_argument("-e", "--height", type="float", dest="height", default=1200, help="Your ellipsoid height.  Default: %default")

    parser.add_argument("-v", "--verbose", action="count", dest="verbose", default=False, help="Verbose")
    parser.add_argument("-T", "--tell",action="store_true", dest="tell", default=False, help="Tell the settings for the run")

    parser.add_argument("-s", "--summary", action="store_true", dest="detail", default=False, help="Summary information about each connection. Otherwise just totals are displayed")
    parser.add_argument("--progress", action="store_true", dest="progress", default=False, help="Show indication of progress while reading from connections")
#    parser.add_argument("-s", "--ssl", action="store_true", dest="ssl", default=False, help="Use SSL for the connection")

    parser.add_argument("-t", "--time", type=int, dest="Time", default=30, help="Minimum length of the time for the connection for data to be received")
    parser.add_argument("-d", "--data", type=int, dest="Data", default=200, help="Minimum amount of data to be received for the connection to be called good.")

    parser.add_argument("-n", "--ntrip", action="store_true", dest="ntrip", default=False, help="Connection is NTRIP, send user name and password after connecting")

    parser.add_argument("-u", "--user", type=str, dest="user", default="IBS", help="The Ntripcaster username.  Default: IBS")
    parser.add_argument("-p", "--password", type=str, dest="password", default="IBS", help="The Ntripcaster password. Default: IBS")
    parser.add_argument("-m", "--mount", type=str, dest="mountpoint", default="CMRx", help="The Ntripcaster mountpoint. Default: CMRx")
    
    return (parser)

def process_arguments ():
    parser=create_arg_parser()
    options = parser.parse_args()
#    print options
    NTRIP_Get_String = None
    NTRIP=options.ntrip
    if NTRIP:
      User_Details=base64.b64encode(options.user+":"+options.password)
      NTRIP_Get_String = "GET /%s HTTP/1.1\r\nUser-Agent: NTRIP\r\nAuthorization: Basic %s\r\n\r\n" % (options.mountpoint,User_Details)
      
    VERBOSE=options.verbose
    DETAIL=options.detail
    PROGRESS=options.progress
    MIN_DATA=options.Data
    
    NUM_Sockets=options.NumberConnections
    WAIT=options.Time
    PROGRESS=options.progress
    IP=options.server
    PORT=options.port
    NUM_Sockets=options.NumberConnections

    if options.tell:
        print "Server: " + IP
        print "Port: %i" % PORT
        print "Connections: %i" % NUM_Sockets
        print "Test Length: %i" % WAIT
        print "Minimum Data: %i" % MIN_DATA
        print "NTRIP:%r" % NTRIP
        print "Verbose: %r" % VERBOSE
        print "Summary: %r" % DETAIL
        print "Progress: %r" % PROGRESS
        if NTRIP:
          print "User: " +  options.user
          print "Password: " +  options.password
          print "Mountpoint: " + options.mountpoint
        print
    
    return (IP,PORT,NUM_Sockets,WAIT,MIN_DATA,VERBOSE,DETAIL,PROGRESS,NTRIP,NTRIP_Get_String)



(IP,PORT,NUM_Sockets,WAIT,MIN_DATA,VERBOSE,DETAIL,PROGRESS,NTRIP,NTRIP_Get_String) = process_arguments()


sock=[None]*NUM_Sockets
Total_Bytes=[0]*NUM_Sockets

server_address = (IP, PORT)


if VERBOSE >= 1:
  print >>sys.stderr,"Opening Connections"

(Connected,Failed_To_Connect)=open_connections(NUM_Sockets,sock,Total_Bytes,VERBOSE)

if VERBOSE >= 1:
  print >>sys.stderr,"Opening Connections completed"


if VERBOSE>=1:
  print >>sys.stderr,"Reading data"
read_from_connections (NUM_Sockets,sock,Total_Bytes,VERBOSE,PROGRESS)  
if VERBOSE>=1:
  print >>sys.stderr,"Reading data completed"
Enough_Data=check_results(NUM_Sockets,sock,Total_Bytes,DETAIL)  

print "Connected %s" % Connected
print "Enough Data %s" % Enough_Data
print "Failed to connect: %s" % Failed_To_Connect
print ""
