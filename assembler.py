import sys
from modules.parser import Parser
from modules.symbol_table import SymbolTable
import modules.code as code

# check usage
if len(sys.argv) != 2:
    raise Exception("Usage: python assembler.py [FILENAME]")

symbol_table = SymbolTable()
parser = Parser(sys.argv[1])

# first pass
i = -1
while parser.has_more_commands():
    parser.advance()
    match parser.command_type():
        case "L_COMMAND":
            symbol_table.add_entry(parser.symbol(), i + 1)
        case other:
            i += 1

# second pass
parser.reset()
lines = []
n = 16
while parser.has_more_commands():
    parser.advance()
    match parser.command_type():
        case "A_COMMAND":
            symbol = parser.symbol()
            if symbol.isdigit():
                index = int(symbol)
            else:
                if not symbol_table.contains(symbol):
                    symbol_table.add_entry(symbol, n)
                    n += 1
                index = symbol_table.get_address(symbol)
            lines.append(f"{index:016b}")
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
