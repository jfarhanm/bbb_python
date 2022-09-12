from ast import Num, Str
import enum
import itertools
from logging import exception
import re
from tokenize import Number
from tracemalloc import stop
from typing import List
from typing_extensions import Self
import protocol_defs
from collections.abc import Iterable 
from typing import Optional
import time

class ParsedErrors:
    def __init__(self,err_type=0,err_code=0):
        err_type = 0
        err_code = 0




class ParsedFrame:
    def __init__(self):    
        self.header:Optional[int] = None
        self.data_size:Optional[int] = None
        self.result_type:Optional[ParsedErrors] = None
        self.data:Optional[tuple[int,int]] = None #(start,end)
        self.text_list:Optional[List[str]] = None # str
    
    @staticmethod
    def with_all(header:Optional[int]=None,
            data_size:Optional[int]=None,
            result_type:Optional[ParsedErrors]=None,
            data:Optional[tuple[int,int]]=None,
            text:Optional[List[str]]=None):
        f = ParsedFrame()
        f.header = header
        f.data_size = data_size
        f.result_type = result_type
        f.data = data
        f.text_list = text
        return f 
    def __repr__(self) -> str:
        output = f"""
        Packet:
            header: {protocol_defs.DefReprs.data_dict[self.header]},
            data_size:{self.data_size},
            result_type:{self.result_type},
            data:{self.data},
            text:{self.text_list}
        """
        return output
        
class ParserResultTypes:
    FRAME = 0
    INCOMPLETE_FRAME = 1
    PARSE_ERROR = 2


class ParseResult:
    def __init__(self,result_type,frame):
        self.result_type = result_type
        self.result = frame
    def __repr__(self) -> str:
        if self.result_type == ParserResultTypes.INCOMPLETE_FRAME:
            return "INCOMPLETE FRAME"
        elif self.result_type == ParserResultTypes.PARSE_ERROR:
            return "Error"
        else:
            return  repr(self.result)
    def is_valid_frame(self):
        if self.result_type==ParserResultTypes.FRAME:
            return True
        return False


class BBBParser:
    def __init__(self):
        self.parse_cursor:int = 0
        self.header_type:Optional[int] = None
        self.data_bytes:Optional[int] = None 
        self.error_bytes:Optional[tuple[int,int]] = None 
        self.text_list:Optional[List[str]] = None 
    
   # #@staticmethod
   # def _debug_new(self)->BBBParser:
   #     a = BBBParser()
   #     a.header_type = protocol_defs.BBBMethods.REG_CALLER
   #     return a 
    

    def parse_textual(self,data=[]):
        index = 0
        try:
            index = data.index(protocol_defs.BBBDefs.CR)
        except:
            return None
        self.parse_cursor+=index
        #print(type(index))
        return "".join(map(chr,iter(data[:index])))
   
    
    # TODO : Test if parse_cursor+=index or parse_cursor+=index+1 
    def parse_textual_etx_delim_step(self, data:bytes)->Optional[tuple[str,bool,int]]:
        index = -1
        index = data.find(bytes([protocol_defs.BBBDefs.ETX]))
        if (index==-1):
            print(index)
            index_end = data.find(protocol_defs.BBBDefs.CR.to_bytes(1,'big'))
            if index_end==-1:
                return None
            return (data[:index_end].decode("utf-8"),False,index)
        self.parse_cursor+=index+1 
        return (data[:index].decode("utf-8"),True,index) 

    # TODO : What does data_size do?
    def parse_step(self , data)->ParseResult:
       # for m in data[self.parse_cursor:]:
       #     print("{0:02x}".format(m),end= " ")
       # print()  
    
        if len(data)>2:
            if data[0]!=protocol_defs.BBBDefs.START:
                return ParseResult(ParserResultTypes.PARSE_ERROR,None)
        else:
            return ParseResult(ParserResultTypes.INCOMPLETE_FRAME,None)

        if self.header_type is None:
            self.header_type = data[1]
            self.parse_cursor = 2
        

        if self.data_bytes is None:
            h = self.header_type
            print("{0:02x}".format(h))
            methods = protocol_defs.BBBMethods
            # NOTE : is there not a data size check about here ?
            # NOTE : Deprecation warning
            # In the future we shall add multiple names to REG_CALLER 
            # TEST : IMPORTANT 
            if h == methods.REG_CALLER:
                if self.text_list is None:
                    self.text_list = []
                while (m := self.parse_textual_etx_delim_step(data[self.parse_cursor:])) is not None:
                    self.text_list.append(m[0])
                    if m[1] ==  False: 
                        return ParseResult(ParserResultTypes.FRAME, ParsedFrame.with_all(self.header_type,None,None,data[:],self.text_list[:]) ) 

                return ParseResult(ParserResultTypes.INCOMPLETE_FRAME,None)
                print("REG_CALLER")

            elif h ==methods.REG_SERVICE:
                m = self.parse_textual(data[self.parse_cursor:])
                if m is None:
                    return ParseResult(ParserResultTypes.INCOMPLETE_FRAME,None)
                return ParseResult(ParserResultTypes.FRAME, ParsedFrame.with_all(self.header_type,None,None,data.copy(),[m[0]]) )
                print("REG_SERVICE")

            elif h == methods.STOP_CALLER:
                return ParseResult(ParserResultTypes.FRAME,ParsedFrame.with_all(self.header_type,None,None,None,None))
                print("STOP_CALLER")

            elif h == methods.STOP_SERVICE:
                return ParseResult(ParserResultTypes.FRAME,ParsedFrame.with_all(self.header_type,None,None,None,None))
                print("STOP_SERVICE") 
            
            # PRIORITY : self.data_bytes is not int 
            # TODO : Final Test
            elif h == methods.CALL:
                try:
                    index_lsb = data[self.parse_cursor]
                    index_msb = data[self.parse_cursor+1]
                    self.parse_cursor+=2
                    self.error_bytes = (index_lsb,index_msb)    # NOTE: STORES THE INDEX OF CALLER 
                except:
                    return ParseResult(ParserResultTypes.INCOMPLETE_FRAME,None)
                m = self.parse_textual(data[self.parse_cursor:])
                if m is None:
                    return ParseResult(ParserResultTypes.INCOMPLETE_FRAME,None)
                self.data_bytes = int(m)    #scope for error 
                print(m)
                print("CALL") 


            elif h == methods.CALLRESP:
                self.parse_cursor+=2
                if len(data[self.parse_cursor:])>0:
                    resp_code = data[self.parse_cursor-1]
                    resp_type = data[self.parse_cursor-2]
                    m = self.parse_textual(data[self.parse_cursor:])

                    if m is None:
                        return ParseResult(ParserResultTypes.INCOMPLETE_FRAME,None)
                    self.data_bytes = int(m)
                else:
                    return ParseResult(ParserResultTypes.INCOMPLETE_FRAME,None)
                print("CALLRESP") 



            elif h == methods.REG_SERVICE_ACK:
                print("REG_SERVICE_ACK") 
                if len(data[self.parse_cursor:])>=4:
                    if data[self.parse_cursor:][4] == protocol_defs.BBBDefs.CR:
                        temp_window= data[self.parse_cursor:]
                        resp_code = temp_window[0]
                        resp_type = temp_window[1]
                        e_code = ParsedErrors(resp_code,resp_type)
                        start = self.parse_cursor+2
                        end = start+1
                        return ParseResult(ParserResultTypes.FRAME,ParsedFrame.with_all(self.header_type,end-start,e_code,(start,end),None))
                    return ParseResult(ParserResultTypes.PARSE_ERROR,None)
                return ParseResult(ParserResultTypes.INCOMPLETE_FRAME,None)

            # TODO : Retest ; MSB,LSB confusion 
            # returns data [id,servid1,servid2,servid3]
            elif h == methods.REG_CALLER_ACK:
                print("REG_CALLER_ACK") 
                if len(data[self.parse_cursor:])>=7:
                    temp_window= data[self.parse_cursor:]
                    resp_code = temp_window[0]
                    resp_type = temp_window[1]
                    e_code = ParsedErrors(resp_code,resp_type)  
                    temp_window_iter = enumerate(iter(temp_window[2:]))
                    while True:
                        try:
                            index_lsb = next(temp_window_iter)
                            index_msb = next(temp_window_iter)
                            print("Indices are",index_lsb[1],index_msb[1])
                        except StopIteration:
                            return ParseResult(ParserResultTypes.INCOMPLETE_FRAME,None)
                        
                        if(index_lsb[1] == 0xFF) and (index_msb[1]== 0xFF):
                            s_start  = self.parse_cursor+2
                            s_end = s_start + index_lsb[0]
                            return ParseResult(ParserResultTypes.FRAME,ParsedFrame.with_all(self.header_type,s_end-s_start,e_code,(s_start,s_end),None))                    
                return ParseResult(ParserResultTypes.INCOMPLETE_FRAME,None)


            elif h == methods.STOP_SERVICE_ACK:
                if len(data[self.parse_cursor:])>=3:
                    if data[self.parse_cursor:][2] == protocol_defs.BBBDefs.CR:
                        temp_window= data[self.parse_cursor:]
                        resp_code = temp_window[0]
                        resp_type = temp_window[1]
                        e_code = ParsedErrors(resp_code,resp_type)
                        return ParseResult(ParserResultTypes.FRAME,ParsedFrame.with_all(self.header_type,None,e_code,None,None))
                    return ParseResult(ParserResultTypes.PARSE_ERROR,None)
                return ParseResult(ParserResultTypes.INCOMPLETE_FRAME,None)
                print("STOP_SERVICE_ACK")

            elif h == methods.STOP_CALLER_ACK:
                if len(data[self.parse_cursor:])>=3:
                    if data[self.parse_cursor:][2] == protocol_defs.BBBDefs.CR:
                        temp_window= data[self.parse_cursor:]
                        resp_code = temp_window[0]
                        resp_type = temp_window[1]
                        e_code = ParsedErrors(resp_code,resp_type)
                        return ParseResult(ParserResultTypes.FRAME,ParsedFrame.with_all(self.header_type,None,e_code,None,None))
                    return ParseResult(ParserResultTypes.PARSE_ERROR,None)
                return ParseResult(ParserResultTypes.INCOMPLETE_FRAME,None)
                print("STOP_CALLER_ACK") 

            else:
                return ParseResult(ParserResultTypes.INCOMPLETE_FRAME,None)

        # Working on the rest
        rest = data[self.parse_cursor+1:]
        if len(rest)>self.data_bytes:
            if rest[self.data_bytes] == protocol_defs.BBBDefs.CR:
                start = self.parse_cursor + 1
                end = start + self.data_bytes
                if self.error_bytes is not None:
                    return ParseResult(ParserResultTypes.FRAME,ParsedFrame.with_all(self.header_type,self.data_bytes,ParsedErrors(self.error_bytes[0],self.error_bytes[1]),(start,end),None))
                else:
                    return ParseResult(ParserResultTypes.FRAME,ParsedFrame.with_all(self.header_type,self.data_bytes,None,(start,end),None))
            else:
                return ParseResult(ParserResultTypes.PARSE_ERROR,None)
        return ParseResult(ParserResultTypes.INCOMPLETE_FRAME,None)

# TODO  : Test stateful code 
# TODO  : bloody damn test this shite 
# TODO  : incomplete frame should send result of whatever has been parsed 
if __name__ == '__main__':
    # Tests
    cnt = 0
    register_service  =   [protocol_defs.BBBDefs.START,protocol_defs.BBBMethods.REG_SERVICE,ord('T'),ord('E'),ord('S'),ord('T'),protocol_defs.BBBDefs.CR,protocol_defs.BBBDefs.CR]
    stop_service      =   [protocol_defs.BBBDefs.START,protocol_defs.BBBMethods.STOP_SERVICE,protocol_defs.BBBDefs.CR,protocol_defs.BBBDefs.CR] 
    for m in range(0,len(register_service)):
        d = BBBParser()
        p = d.parse_step(register_service[:m])
        print(repr(p))
    
    for m in range(0,len(stop_service)):
        d = BBBParser()
        p = d.parse_step(stop_service[:m])
        print(repr(p))

    # CHECK_FOR_RESULT :
    register_caller   =   [protocol_defs.BBBDefs.START,protocol_defs.BBBMethods.REG_CALLER,ord('T'),ord('E'),ord('S'),ord('T'),protocol_defs.BBBDefs.CR,protocol_defs.BBBDefs.CR]
    stop_caller       =   [protocol_defs.BBBDefs.START,protocol_defs.BBBMethods.STOP_CALLER,protocol_defs.BBBDefs.CR,protocol_defs.BBBDefs.CR] 

    for m in range(0,len(register_caller)):
        d = BBBParser()
        p = d.parse_step(register_caller[:m])
        print(repr(p))

    for m in range(0,len(stop_caller)):
        d = BBBParser()
        p = d.parse_step(stop_caller[:m])
        print(repr(p))


    # register caller 
    # CHECK_FOR_RESULT : CALL 
    call_service      =   [protocol_defs.BBBDefs.START,protocol_defs.BBBMethods.CALL,0x23,0x23,ord('5'),protocol_defs.BBBDefs.CR,ord('o'),ord('k'),ord('i'),ord('e'),cnt,protocol_defs.BBBDefs.CR,protocol_defs.BBBDefs.CR]
    call_response  =   [protocol_defs.BBBDefs.START,protocol_defs.BBBMethods.CALLRESP,protocol_defs.BBBMethods.OK,protocol_defs.BBBMethods.OK_CODE,ord('6'),protocol_defs.BBBDefs.CR,ord('w'),ord('o'),ord('r'),ord('k'),ord('s'),cnt,protocol_defs.BBBDefs.CR,protocol_defs.BBBDefs.CR]
    
    # Ok never mind a new instance is created each time 
    # TODO this is not efficient at all 
    # TODO change so that instance saves its state 
    for m in range(0,len(call_service)):
        d = BBBParser()
        p = d.parse_step(call_service[:m])
        print(repr(p))

    for m in range(0,len(call_response)):
        d = BBBParser()
        p = d.parse_step(call_response[:m])
        print(repr(p))
    
    Defs = protocol_defs.BBBDefs
    Methods = protocol_defs.BBBMethods                      
    
    # NOTE : Deprecation  warning  - caller can support multiple services starting v0.1.1                                
    #                                                               RESULT     ID         SERV_ID
    reg_caller_ack =    [Defs.START,Methods.REG_CALLER_ACK,         20,20,   30,30,       30,30,      Defs.CR,Defs.CR]
    reg_service_ack =   [Defs.START,Methods.REG_SERVICE_ACK,        20,20,   30,30,      Defs.CR,Defs.CR]
    stop_service_ack =  [Defs.START,Methods.STOP_SERVICE_ACK,       20,20,   Defs.CR,Defs.CR]
    stop_caller_ack =   [Defs.START,Methods.STOP_CALLER_ACK,        20,20,   Defs.CR,Defs.CR]
    

    d = BBBParser()
    p = d.parse_step(reg_caller_ack)
    print(repr(p))


    d = BBBParser()
    p = d.parse_step(reg_service_ack)
    print(repr(p))


    d = BBBParser()
    p = d.parse_step(stop_caller_ack)
    print(repr(p))


    d = BBBParser()
    p = d.parse_step(stop_service_ack)
    print(repr(p))


    
