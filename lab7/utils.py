

ipport={"U":(0000), "V":(0000), "W":(0000), "X":(0000), "Y":(0000), "Z":(0000)}

ipStart = 8730

for i in ipport:
    ipStart += 1
    ipport[i] = ipStart

def getIpPorts():
    return ipport
