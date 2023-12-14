import math
import pdb

def getNewWorkGroup(wg, WGM, MOverMT0, NOverMT1):
    numFullWG = NOverMT1//WGM
    wgSerial = (wg[1]%WGM)*MOverMT0 + wg[0]
    wgSet = wg[1]//WGM
    if wgSet < numFullWG: 
        X = wgSerial//WGM
        Y = wgSerial%WGM
    else:
        remainder = NOverMT1%WGM
        X = wgSerial//remainder
        Y = wgSerial%remainder
    wg_new = (X, Y + wgSet*WGM)
    #pdb.set_trace()
    return wg_new


MOverMT0 = 8
NOverMT1 = 16
WGM = 5
nCUs = 12


for wg0 in range(MOverMT0):
    line = ''
    for wg1 in range(NOverMT1):    
        wg_new = getNewWorkGroup((wg0, wg1), WGM, MOverMT0, NOverMT1)
        line += ' |(%d, %d) -> (%d, %d)|'%(wg0, wg1, wg_new[0], wg_new[1])
    line += '\n'
    print(line)


