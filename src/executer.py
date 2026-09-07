import subprocess
from config import debug_ignore_parsers
from typing import Callable

def run_command(
    command: list[str],
    parser: Callable[[str], None] | None = None
    ) -> int:
    
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
    
        if process.stdout:
            active_parser = None if debug_ignore_parsers else parser
            for line in process.stdout:
                if active_parser is not None:
                    active_parser(line)
                else:
                    print(line, end="")
            
        process.stdout.close()
        return process.wait()