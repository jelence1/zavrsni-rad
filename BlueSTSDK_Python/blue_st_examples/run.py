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

	
	# pool = ThreadPool(processes=1)
	# async_result = pool.apply_async(pipe.main)

	p = subprocess.run(["python3", "params_form.py"], text=True)

	if p.returncode != globals.RECORDING_CODE:
		print("Exit code: ", p.returncode)
		sys.exit(p.returncode)

	data = p.stdout
	print("DATA*** ",data)

	#q = subprocess.run(["python3", "recording_logic.py", data])

	
def main2():
	import output
	output_thread = threading.Thread(target=output.main)
	ble_thread = threading.Thread(target=example_ble_5.main, args=(1,))

	output_thread.start()
	ble_thread.start()
	ble_thread.join()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Shutting down...")
		sys.exit(0)
