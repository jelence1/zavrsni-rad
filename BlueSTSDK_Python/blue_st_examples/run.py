# LIBRARY IMPORTS
import sys
import subprocess
import threading

from multiprocessing.pool import ThreadPool



# USER IMPORTS
import example_ble_5
import params_form
import recording_logic
import globals
import pipe


def main():
	# globals.SOCKET_BLE.connect("tcp://localhost:5555")
	# globals.SOCKET_OUT.bind("tcp://*:5555")

	p = subprocess.run(["python3", "intro_form.py"])

	if p.returncode == globals.EDIT_CODE:
		print("edit audio, run audacity. ",globals.RECORDING_CODE)
		sys.exit(0)
	else: 
		if p.returncode != globals.RECORDING_CODE:
			print("Exit code: ", p.returncode)
			sys.exit(p.returncode)

	
	pool = ThreadPool(processes=1)
	async_result = pool.apply_async(pipe.main)

	p = subprocess.run(["python3", "params_form.py"])

	if p.returncode != globals.RECORDING_CODE:
		print("Exit code: ", p.returncode)
		sys.exit(p.returncode)

	return_val = async_result.get()
	data = list(return_val.values())
	print(data)

	#q = subprocess.run(["python3", "recording_logic.py", data])

	
	

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Shutting down...")
		sys.exit(0)
