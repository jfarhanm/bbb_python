import socket
import bbb_parser
import protocol_defs
READ_SIZE = 96

class Message:
    def __init__(self,meta_data,data) -> None:
        self.meta_data = meta_data  # frame 
        self.data = data            # data




class Conn:
    def __init__(self,sock = None) -> None:
        if sock is None:
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.buffer = []

    def connect(self,host,port):
        self.sock.connect((host,port))
        # probably throws an exception here 

    def send(self,data):
        total_sent = 0;
        MSG_LEN = 20    # TODO add smth here 
        self.sock.sendall(data)

    def recv(self):
        read_size = 4096
        chunks=b''
        bytesread_total =0
        work = True
        parser = bbb_parser.BBBParser()
        
        while work:
            l_chunk = self.sock.recv(read_size) 
            bytes_read = len(l_chunk);
            bytesread_total +=bytes_read
            chunks+=l_chunk[:bytes_read]
            out = parser.parse_step(chunks)
            if out.result_type == bbb_parser.ParserResultTypes.PARSE_ERROR:
                print("Parse Error")
                return None
            elif out.result_type == bbb_parser.ParserResultTypes.INCOMPLETE_FRAME:
                # TODO send incomplete frame data here 
                # TODO handle this issue 
                # TODO question:  does the parser save state ?
                pass 
            elif out.result_type == bbb_parser.ParserResultTypes.FRAME:
                return Message(out.result,chunks)
            # Ok what do I do here lol 

if __name__=='__main__':
    conn = Conn()
    conn.connect('localhost',8008)
    conn.send(bytes([protocol_defs.BBBDefs.START,protocol_defs.BBBMethods.REG_CALLER,ord('T'),ord('E'),ord('S'),ord('T'),protocol_defs.BBBDefs.CR,protocol_defs.BBBDefs.CR]))
    reply = conn.recv() # should give me a REGCALLERACK 
    print(reply)
