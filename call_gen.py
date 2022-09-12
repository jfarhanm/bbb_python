from typing import List
import protocol_defs

P_START = bytes([protocol_defs.BBBDefs.START])
P_CR = bytes([protocol_defs.BBBDefs.CR])

# Deprecation warning : In the future one more parameter is to be added : Service name 
# Note : Data has to be in binary   #lsb #msb
def generate_call(data:bytes,index:tuple[int,int]):
    '''call_data = [protocol_defs.BBBDefs.P_START,
                protocol_defs.BBBMethods.CALL,
                ord('5'),protocol_defs.BBBDefs.P_CR,
                ord('o'),ord('k'),ord('i'),ord('e'),cnt,
                protocol_defs.BBBDefs.P_CR,protocol_defs.BBBDefs.P_CR]'''
    length = len(data)
    out = P_START +bytes([protocol_defs.BBBMethods.CALL]) + bytes(index)+ str(length).encode("ascii") + P_CR + data + P_CR + P_CR 
    return out 

# Note : Data has to be in binary 
def generate_call_resp(data:bytes,status:int,status_code:int):
    '''[protocol_defs.BBBDefs.P_START,
        protocol_defs.BBBMethods.CALLRESP,
        protocol_defs.BBBMethods.OK,protocol_defs.BBBMethods.OK_CODE,
        ord('6'),protocol_defs.BBBDefs.P_CR,
        ord('w'),ord('o'),ord('r'),ord('k'),ord('s'),
        cnt,protocol_defs.BBBDefs.P_CR,protocol_defs.BBBDefs.P_CR]
    '''
    length  = len(data)
    out = P_START + bytes([protocol_defs.BBBMethods.CALLRESP,status,status_code]) + str(length).encode("ascii")  + P_CR  + data + P_CR + P_CR  
    return out 


# Deprecation warning : I will add multiple service names in the future 
def generate_reg_caller(service_names:List[str]=[]):
    '''[protocol_defs.BBBDefs.P_START,
        protocol_defs.BBBMethods.REG_CALLER,
        ord('T'),ord('E'),ord('S'),ord('T'),
        protocol_defs.BBBDefs.P_CR,protocol_defs.BBBDefs.P_CR]
    '''
    P_ETX = bytes([protocol_defs.BBBDefs.ETX])
    name_ascii="".encode('ascii')
    len_names = len(service_names)
    
    for index in range(0,len_names-1):
        name_ascii = name_ascii + service_names[index].encode("ascii") + P_ETX
    name_ascii = name_ascii + service_names[len_names-1].encode("ascii")
    out = P_START + bytes([protocol_defs.BBBMethods.REG_CALLER]) + name_ascii + P_CR + P_CR     
    return out 
   


def generate_stop_caller():
    '''[protocol_defs.BBBDefs.P_START,protocol_defs.BBBMethods.STOP_CALLER,protocol_defs.BBBDefs.P_CR,protocol_defs.BBBDefs.P_CR]'''
    out = P_START + bytes([protocol_defs.BBBMethods.STOP_CALLER]) + P_CR + P_CR  
    return out 


def generate_reg_service(name:str):
    '''[protocol_defs.BBBDefs.P_START,
        protocol_defs.BBBMethods.REG_SERVICE,
        ord('T'),ord('E'),ord('S'),ord('T'),
        protocol_defs.BBBDefs.P_CR,protocol_defs.BBBDefs.P_CR]
    '''
    name_ascii = name.encode("ascii")
    out = P_START + bytes([protocol_defs.BBBMethods.REG_SERVICE]) + name_ascii + P_CR + P_CR     
    return out 

def generate_stop_service():
    '''
    [protocol_defs.BBBDefs.P_START,protocol_defs.BBBMethods.STOP_SERVICE,protocol_defs.BBBDefs.P_CR,protocol_defs.BBBDefs.P_CR]
    '''
    out = P_START + bytes([protocol_defs.BBBMethods.STOP_SERVICE]) + P_CR + P_CR 
    return out 

# PRIORITY : Possibiility of a problem here 
# NOTE : Debug 
def generate_reg_caller_ack(status:int,status_code:int,caller_id_lsb:int,caller_id_msb:int, service_lists:List[int]):
    out = P_START + bytes([protocol_defs.BBBMethods.REG_CALLER_ACK]) +bytes([status,status_code,caller_id_lsb,caller_id_msb]) + bytes(service_lists) + bytes([0xff,0xff]) + P_CR + P_CR    
    return out 

