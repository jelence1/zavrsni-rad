import threading
import example_ble_5
import output
import sys

def main():
	output_fun = threading.Thread(target=output.main)
	ble = threading.Thread(target=example_ble_5.main, args=(1,))

	output_fun.start()
	ble.start()
	ble.join()


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Shutting down...")
		sys.exit(0)
