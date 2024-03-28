

ipPort={"U":(0000),"V":(0000), "W":(0000), "X":(0000), "Y":(0000), "Z":(0000)}

ipStart = 8730

for i in ipPort:
    ipStart += 1
    ipPort[i] = ipStart

def getIpPorts():
    return ipPort
