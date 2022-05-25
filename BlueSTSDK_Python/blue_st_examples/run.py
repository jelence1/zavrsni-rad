# LIBRARY IMPORTS
import sys
import subprocess

# USER IMPORTS
import example_ble_5
import output
import globals


def main():
	globals.SOCKET_BLE.connect("tcp://localhost:5555")
	globals.SOCKET_OUT.bind("tcp://*:5555")

	p = subprocess.run(["python3", "intro_form.py"])

	if p.returncode == globals.EDIT_CODE:
		print("edit audio, run audacity. ",globals.RECORDING_CODE)
		sys.exit(0)
	else: 
		if p.returncode != globals.RECORDING_CODE:
			print("Exit code: ", p.returncode)
			sys.exit(p.returncode)

	p = subprocess.run(["python3", "params_form.py"])
	q = subprocess.run(["python3", "recording_logic.py"])

	if p.returncode != globals.RECORDING_CODE:
		print("Exit code: ", p.returncode)
		sys.exit(p.returncode)

	
	

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Shutting down...")
		sys.exit(0)
