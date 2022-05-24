# LIBRARY IMPORTS
from glob import glob
from http.client import CONTINUE
import threading
import sys
import subprocess

# USER IMPORTS
import example_ble_5
import output
import globals
#import proba as output



def main():
	output_thread = threading.Thread(target=output.main)
	ble_thread = threading.Thread(target=example_ble_5.main, args=(1,))

	output_thread.start()
	ble_thread.start()
	ble_thread.join()

def new_main():
	p = subprocess.run(["python3", "intro_form.py"])

	if p.returncode == globals.EDIT_CODE:
		print("edit audio, run audacity. ",globals.RECORDING_CODE)
		sys.exit(0)
	else: 
		if p.returncode != globals.RECORDING_CODE:
			print("Exit code: ", p.returncode)
			sys.exit(0)

	q = subprocess.run(["python3", "params_form.py"])
	print("i am here")
	if q.returncode != globals.RECORDING_CODE:
		print("Exit code: ", p.returncode)
	
	print("i rly want to recordddd :))) ")

if __name__ == "__main__":
	try:
		new_main()
	except KeyboardInterrupt:
		print("Shutting down...")
		sys.exit(0)
