class Parser:
    def __init__(self, file_name):
        with open(file_name, "r") as file:
            self.lines = []
            for line in file.readlines():
                line_stripped = line.strip()
                if line_stripped != "" and line_stripped[0:2] != "//":
                    self.lines.append(line_stripped)
        self.read = -1
        self.current = ""

    def has_more_commands(self):
        return (len(self.lines) - self.read) > 0

    def advance(self):
        self.read += 1
        self.current = self.lines[self.read]

    def command_type(self):
        command = self.current.split()[0]
        if command[0] == "@":
            return "A_COMMAND"
        elif command[0][0] == "(":
            return "L_COMMAND"
        else:
            return "C_COMMAND"

    def symbol(self):
        command = self.current.split()[0]
        return command.strip("()@")

    def dest(self):
        command = self.current.split()[0]
        if "=" in command:
            return command.split("=")[0]
        return "null"

    def comp(self):
        command = self.current.split()[0]
        if "=" in command:
            command = command.split("=")[1]
        if ";" in command:
            command = command.split(";")[0]
        return command

    def jump(self):
        command = self.current.split()[0]
        if ";" in command:
            return command.split(";")[1]
        return "null"
