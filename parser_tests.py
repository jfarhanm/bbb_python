import bbb_parser
import call_gen
data = ("HELLO_BBB_WORLD").encode("ascii")

name_a = "PROTEST"
name_b = "NOOBTEST"
name_c = "NOBITO"
name_d = "LALA"
name_list = [name_a,name_b,name_c,name_d]

rgclr = call_gen.generate_reg_caller(name_list)
print(rgclr)

rgclrack = call_gen.generate_reg_caller_ack(69,69,20,20,[2,4,5,3])
clrcall = call_gen.generate_call(data,(2,4))





rgclr_len = len(rgclr)
rgclrack_len = len(rgclrack)
clrcall_len = len(clrcall)

def try_print(d:bbb_parser.ParseResult):
    if d.result_type == bbb_parser.ParserResultTypes.INCOMPLETE_FRAME:
        return
    elif d.result_type == bbb_parser.ParserResultTypes.FRAME:
        print(repr(d))
    else:
        print("Error in packet")
    return    



# TEST 1
for m in range(0,rgclr_len):
    d_rgclr = bbb_parser.BBBParser()
    try_print(d_rgclr.parse_step(rgclr[:m]))


for m in range(0,rgclrack_len):
    d_rgclrack = bbb_parser.BBBParser()
    try_print(d_rgclrack.parse_step(rgclrack[:m]))


for m in range(0,clrcall_len):
    d_clrcall = bbb_parser.BBBParser()
    try_print(d_clrcall.parse_step(clrcall[:m]))

