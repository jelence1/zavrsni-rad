import threading
import example_ble_5
import output
#import proba as output
import sys

def main():
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
