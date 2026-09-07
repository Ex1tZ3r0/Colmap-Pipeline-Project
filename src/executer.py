import subprocess
import sys

def run_command(command: list[str]):
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    
    if process.stdout:
        for line in process.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()

    return_code = process.wait()

    if return_code != 0:
        raise RuntimeError(f"Command failed with exit code {return_code}")

    return return_code