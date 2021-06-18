
#Autor: Yahor Senichak
#login:xsenic00



import sys
from urllib.parse import urlparse
import binascii
import socket




if (len(sys.argv) != 5) :
    print("Incorect number arguments !")
    sys.exit(1)

if (not(sys.argv[1] == '-n' and sys.argv[3] == '-f') and not(sys.argv[1] == '-f' and sys.argv[3] == '-n')):
    print("Incorect arguments !")
    sys.exit(1)

if (sys.argv[1] == '-n'):
    IP = sys.argv[2]
    cesta = urlparse(sys.argv[4])
else:
    cesta = urlparse(sys.argv[2])
    IP = sys.argv[4]


if (cesta.scheme != 'fsp'):
    print("Incorrect protokol\n")
    sys.exit(1)     

socket.setdefaulttimeout(5.0)
message = bytes('WHEREIS ' + cesta.netloc, "utf-8")

soket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)




port = int(IP[IP.find(":") + 1 :])
test_address = IP[:IP.find(":") ]
address = (test_address,port)


soket.sendto(message, address)
data = soket.recv(2048).decode("utf-8")
soket.close()



if (data.split()[0] != 'OK'):
    print(data)
    sys.exit(1)


def get_file(address, name_of_file):
    
    soket = socket.socket()
    message = "GET " + name_of_file[1:] + " FSP/1.0\r\nHostname: "+ cesta.netloc +"\r\nAgent: xsenic00\r\n\r\n"
    
    message = bytes(message, "utf-8")

    
    port = int(address[address.find(":") + 1 :])
    test_address = address[:address.find(":") ]
    address = (test_address,port)
    soket.connect(address)
    soket.send(message)

    flag = True
    with open(name_of_file[(name_of_file.rfind("/")+1):], 'wb') as soubor:
        while True:
            data = soket.recv(2048)
            if (flag):
                if ('FSP/1.0 Success' in data.decode('ISO-8859-1')):
                    flag = False
                    continue
                else:
                    print('ERROR')
                    soubor.close()
                    soket.close()
                    sys.exit(1)

            if not data:
                break
            soubor.write(data)
    
    soubor.close()
    soket.close()
    return True




if (cesta.path == '/*'):
    get_file(data.split()[1], '/index')
    soubory = open('index')
    for line in soubory:
        get_file(data.split()[1], '/'+line[:(len(line)-1)])


    
else: 
    get_file(data.split()[1], cesta.path)
