import sys
from modules.parser import Parser
import modules.code as code

# check usage
if len(sys.argv) != 2:
    raise Exception("Usage: python assembler.py [FILENAME]")

parser = Parser(sys.argv[1])

# parse and translate lines
lines = []
while parser.has_more_commands():
    parser.advance()
    match parser.command_type():
        case "A_COMMAND":
            num = int(parser.symbol())
            lines.append(f"{num:016b}")
        case "C_COMMAND":
            comp = code.comp(parser.comp())
            dest = code.dest(parser.dest())
            jump = code.jump(parser.jump())
            line = "111" + comp + dest + jump
            lines.append(line)

# write to file
filename = sys.argv[1].rstrip(".asm") + ".hack"
with open(filename, "w") as file:
    for line in lines:
        file.write(line)
        file.write("\n")
