import os
import sys
import json
import calendar
from datetime import datetime
import tarfile


class SimpleShell:
    def __init__(self, hostname, vfs_path, log_file, startup_script):
        self.hostname = hostname
        self.current_path = ""
        self.root_path = "/"
        self.vfs_path = vfs_path
        self.log_file = log_file
        self.load_vfs()
        self.history = []
        if startup_script:
            self.execute_startup_script(startup_script)

    def load_vfs(self):
        with tarfile.open(self.vfs_path) as tar:
            tar.extractall(path='vfs')
        self.current_path = 'vfs/vfs'
        self.root_path = 'vfs/vfs'

    def execute_startup_script(self, script_path):
        with open(script_path, 'r') as script:
            for line in script:
                self.execute_command(line.strip())

    def log_action(self, command):
        self.history.append({
            'command': command,
            'timestamp': datetime.now().isoformat()
        })

    def save_log(self):
        with open(self.log_file, 'w') as f:
            json.dump(self.history, f)

    def execute_command(self, command):
        self.log_action(command)

        command_line = list(command.split(" "));

        if command_line[0] == 'exit':
            self.save_log()
            sys.exit(0)

        elif command_line[0] == "cd":
            path = command_line[1]
            self.cd(path)

        elif command_line[0] == 'ls':
            self.ls()

        elif command_line[0] == 'tree':
            self.tree(self.current_path)

        elif command_line[0] == 'cal':
            self.cal(command_line)

        else:
            print(f"Unknown command: {command_line[0]}")

    def cd(self, path):
        if (path == "/"):
            self.current_path = self.root_path
        else:
            if path[0] == "/":
                self.current_path = self.root_path
                path = path[1:]
            new_path = os.path.join(self.current_path, path)
            if os.path.isdir(new_path):
                self.current_path = new_path

            else:
                print(f"Directory not found: {path}")

    def ls(self):
        print("\n".join(os.listdir(self.current_path)))

    def tree(self, path, level=0):
        for item in os.listdir(path):
            subpath = os.path.join(path, item)
            print('  ' * level + item)
            if os.path.isdir(subpath):
                self.tree(subpath, level + 1)

    def cal(self, command=[]):
        print(len(command), command)
        if len(command) == 1:
            print(1)
            now = datetime.now()
            print(calendar.month(now.year, now.month))
        elif len(command) == 2:
            print(2)
            print(calendar.calendar(int(command[1])))
        elif len(command) == 3:
            print(3)
            print(calendar.month(int(command[1]), int(command[2])))


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Usage: python main.py <hostname> <vfs_path> <log_file> <startup_script>")
        sys.exit(1)

    hostname = sys.argv[1]
    vfs_path = sys.argv[2]
    log_file = sys.argv[3]
    startup_script = sys.argv[4]

    shell = SimpleShell(hostname, vfs_path, log_file, startup_script)

    while True:
        command = input(f"{hostname}: {shell.current_path} $ ")
        shell.execute_command(command)
