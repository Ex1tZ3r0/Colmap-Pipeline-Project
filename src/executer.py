import subprocess
from config import debug_ignore_parsers, debug_force_basic_parser, debug_broadcast_commands
from typing import Callable
from src.parsers import basic_parser, print_clean_line, broadcast_command
from rich.console import Console

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

        if debug_broadcast_commands:
            broadcast_command(str(command))
        
        if process.stdout:
            
            active_parser = None if debug_ignore_parsers else parser
            
            for line in process.stdout:
                if active_parser is not None:
                    active_parser(line)
                if debug_force_basic_parser:
                    basic_parser(line)
                else:
                    print(line, end="")
            
            process.stdout.close()
        return process.wait()