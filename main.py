import os
import subprocess
import time
import sys
import threading
import psutil

def pidExist(pid: int) -> bool:
    return psutil.pid_exists(pid)

def checkFound(pid: int) -> None:
    while True:
        if not pidExist(pid):
            print("> program crashed!")
            os.kill(main_pid, sig)
        time.sleep(1)
    return

def getName(executable: str) -> str:
    return "/".join(executable.split("\\")).split("/")[-1]

def getPathExecutable(executable: str) -> str:
    return subprocess.getoutput("where " + executable)

def suspend(pid: int) -> None:
    os.system("tools\\pssuspend64.exe " + str(pid) + " >nul 2>&1")
    print("> suspended: PID: {}".format(pid))
    return

def resume(pid: int) -> None:
    os.system("tools\\pssuspend64.exe -r " + str(pid) + " >nul 2>&1")
    print("> resume: PID: {}".format(pid))
    return

def run(executable: str, args: list) -> None:
    p = subprocess.Popen([executable, *args], close_fds=False, creationflags=subprocess.CREATE_NEW_CONSOLE)
    print("> started: {} (PID: {})".format(getName(executable), p.pid))
    return p

def main() -> None:
    if (len(sys.argv) < 3):
        print("main.py [second] [executable] [args]")
        return

    sec = int(sys.argv[1])
    executable = sys.argv[2]
    args = sys.argv[3:]
    fullPath = getPathExecutable(executable)
    if not fullPath:
        fullPath = executable

    p = run(fullPath, args)
    threading.Thread(target=checkFound, args=(p.pid,)).start()

    print("> waiting for {} second....".format(sec))
    time.sleep(sec)

    suspend(p.pid)

    print("> waiting for user.... press enter to resume!")
    input()

    resume(p.pid)

    p.wait()
    return

if os.name == 'nt':
    sig = __import__('signal').SIGTERM
    main_pid = os.getpid()
    main()
    os.kill(main_pid, sig)
