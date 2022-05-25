# LIBRARY IMPORTS
import sys
import subprocess

# USER IMPORTS
import example_ble_5
import output
import globals


def main():
	p = subprocess.run(["python3", "intro_form.py"])

	if p.returncode == globals.EDIT_CODE:
		print("edit audio, run audacity. ",globals.RECORDING_CODE)
		sys.exit(0)
	else: 
		if p.returncode != globals.RECORDING_CODE:
			print("Exit code: ", p.returncode)
			sys.exit(p.returncode)

	p = subprocess.run(["python3", "params_form.py"])

	# if p.returncode != globals.RECORDING_CODE:
	# 	print("Exit code: ", p.returncode)
	# 	sys.exit(p.returncode)
	
	q = subprocess.run(["python3", "connect_popup.py"])

	if q.returncode != globals.RECORDING_CODE:
		pass

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Shutting down...")
		sys.exit(0)
