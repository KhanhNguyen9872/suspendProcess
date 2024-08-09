import os
import subprocess
import time
import sys

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
	p = __import__('subprocess').Popen([executable, *args]) #  creationflags=subprocess.CREATE_NEW_CONSOLE
	print("> started: {} (PID: {})".format(getName(executable), p.pid))
	return p

def main() -> None:
	print()

	sec = sys.argv[1]
	executable = sys.argv[2]
	args = sys.argv[3:]
	fullPath = getPathExecutable(executable)

	p = run(fullPath, args)
	time.sleep(sec)

	suspend(p.pid)

	print("> waiting for user.... press enter to resume!")
	input()

	resume(p.pid)

	p.wait()
	return

main()