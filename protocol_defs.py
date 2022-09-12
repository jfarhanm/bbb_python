class BBBDefs:
    # DENOTE THE START AND END OF A PACKET 
    START                   = 0XBB
    END                     = 0X10
    
    # RANDOM USEFUL DATA 
    REQ                     = 0x51
    RESP                    = 0X41
    ACK                     = 0X69
    ERR                     = 0X70
    CR                      = 0X10
    ETX                     = 0x03
class BBBMethods:
    # COMMON TO ALL METHODS
    ACK                     = 0X69
    ERR                     = 0X70
    OK                      = 0X71
    OK_CODE                 = 0X72

    # SERVICES
    CALLRESP                = 0X20
    REG_SERVICE             = 0X30
    REG_SERVICE_ACK         = 0X32
    STOP_SERVICE            = 0X33
    STOP_SERVICE_ACK        = 0X34

    # SERVICE CALLERS 
    CALL                    = 0X0A
    REG_CALLER              = 0X40
    REG_CALLER_ACK          = 0X41
    STOP_CALLER             = 0X42
    STOP_CALLER_ACK         = 0X43

    # FOR FUTURE ADDITION OF BROADCASTS 
    # BROADCASTER
    BROADCAST               = 0X50
    BROADCAST_REG           = 0X60
    BROADCAST_REG_ACK       = 0X61

    # BROADCAST RECEIVER
    BROADCAST_RECV_ACK      = 0X80
    BROADCAST_RECV_RDY      = 0X81
    BROADCAST_RECV_REG      = 0X82
    BROADCAST_RECV_REG_ACK  = 0X83

class BBBErrors:
    FRAME_PARSE_ERROR       = 0XA0
    INCOMPLETE_FRAME_ERROR  = 0XA1
    SERVICE_DOWN_ERROR      = 0XA2
    NAME_INVALID_ERROR      = 0XA3
    ALREADY_EXISTS_ERROR    = 0XA4
    DOES_NOT_EXIST_ERROR    = 0XA5





class BBBParser:
    def __init__(self) -> None:
        self.parse_array = []
        self.parse_cursor = 0
        pass
    
    def parse_step(self):
        pass
    

class StringReprs:
    def __init__(self) -> None:
        self.data_dict = {
            BBBDefs.ACK     :"Def - ACK",
            BBBDefs.CR      :"Def - CR",
            BBBDefs.START   :"Def - START",
            BBBDefs.END     :"Def - END",
            BBBDefs.REQ     :"Def - REQ",
            BBBDefs.RESP    :"Def - RESP",
            BBBDefs.ERR     :"Def - ERR",
            BBBErrors.FRAME_PARSE_ERROR : "FRAME_PARSE_ERROR",
            BBBErrors.INCOMPLETE_FRAME_ERROR : "INCOMPLETE_FRAME_ERROR",
            BBBErrors.SERVICE_DOWN_ERROR : "SERVICE_DOWN_ERROR ", 
            BBBErrors.NAME_INVALID_ERROR : "NAME_INVALID_ERROR",
            BBBErrors.ALREADY_EXISTS_ERROR  : "ALREADY_EXISTS_ERROR",
            BBBErrors.DOES_NOT_EXIST_ERROR  : "DOES_NOT_EXIST_ERROR",
            BBBMethods.ACK                     : "ACK",
            BBBMethods.ERR                     : "ERR",
            BBBMethods.OK                      : "OK",
            BBBMethods.OK_CODE                 : "OK_CODE",
            BBBMethods.CALLRESP                : "CALLRESP",
            BBBMethods.REG_SERVICE             : "REG_SERVICE",
            BBBMethods.REG_SERVICE_ACK         : "REG_SERVICE_ACK",
            BBBMethods.STOP_SERVICE            : "STOP_SERVICE",
            BBBMethods.STOP_SERVICE_ACK        : "STOP_SERVICE_ACK",
            BBBMethods.CALL                    : "CALL",
            BBBMethods.REG_CALLER              : "REG_CALLER",
            BBBMethods.REG_CALLER_ACK          :"REG_CALLER_ACK",
            BBBMethods.STOP_CALLER             :"STOP_CALLER",
            BBBMethods.STOP_CALLER_ACK         :"STOP_CALLER_ACK", 
            BBBMethods.BROADCAST               : "BROADCAST",
            BBBMethods.BROADCAST_REG           : "BROADCAST_REG",
            BBBMethods.BROADCAST_REG_ACK       : "BROADCAST_REG_ACK",
            BBBMethods.BROADCAST_RECV_ACK      : "BROADCAST_RECV_ACK",
            BBBMethods.BROADCAST_RECV_RDY      : "BROADCAST_RECV_RDY",
            BBBMethods.BROADCAST_RECV_REG      : "BROADCAST_RECV_REG",
            BBBMethods.BROADCAST_RECV_REG_ACK  : "BROADCAST_RECV_REG_ACK"
        }
        
class DefReprs:
    data_dict = {
        BBBDefs.ACK     :"Def - ACK",
        BBBDefs.CR      :"Def - CR",
        BBBDefs.START   :"Def - START",
        BBBDefs.END     :"Def - END",
        BBBDefs.REQ     :"Def - REQ",
        BBBDefs.RESP    :"Def - RESP",
        BBBDefs.ERR     :"Def - ERR",
        BBBErrors.FRAME_PARSE_ERROR : "FRAME_PARSE_ERROR",
        BBBErrors.INCOMPLETE_FRAME_ERROR : "INCOMPLETE_FRAME_ERROR",
        BBBErrors.SERVICE_DOWN_ERROR : "SERVICE_DOWN_ERROR ", 
        BBBErrors.NAME_INVALID_ERROR : "NAME_INVALID_ERROR",
        BBBErrors.ALREADY_EXISTS_ERROR  : "ALREADY_EXISTS_ERROR",
        BBBErrors.DOES_NOT_EXIST_ERROR  : "DOES_NOT_EXIST_ERROR",
        BBBMethods.ACK                     : "ACK",
        BBBMethods.ERR                     : "ERR",
        BBBMethods.OK                      : "OK",
        BBBMethods.OK_CODE                 : "OK_CODE",
        BBBMethods.CALLRESP                : "CALLRESP",
        BBBMethods.REG_SERVICE             : "REG_SERVICE",
        BBBMethods.REG_SERVICE_ACK         : "REG_SERVICE_ACK",
        BBBMethods.STOP_SERVICE            : "STOP_SERVICE",
        BBBMethods.STOP_SERVICE_ACK        : "STOP_SERVICE_ACK",
        BBBMethods.CALL                    : "CALL",
        BBBMethods.REG_CALLER              : "REG_CALLER",
        BBBMethods.REG_CALLER_ACK          :"REG_CALLER_ACK",
        BBBMethods.STOP_CALLER             :"STOP_CALLER",
        BBBMethods.STOP_CALLER_ACK         :"STOP_CALLER_ACK", 
        BBBMethods.BROADCAST               : "BROADCAST",
        BBBMethods.BROADCAST_REG           : "BROADCAST_REG",
        BBBMethods.BROADCAST_REG_ACK       : "BROADCAST_REG_ACK",
        BBBMethods.BROADCAST_RECV_ACK      : "BROADCAST_RECV_ACK",
        BBBMethods.BROADCAST_RECV_RDY      : "BROADCAST_RECV_RDY",
        BBBMethods.BROADCAST_RECV_REG      : "BROADCAST_RECV_REG",
        BBBMethods.BROADCAST_RECV_REG_ACK  : "BROADCAST_RECV_REG_ACK",
        None:"None"
    }
