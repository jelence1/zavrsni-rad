import threading
import example_ble_5
import proba_tk
#import proba as output
import sys

def main():
	output_thread = threading.Thread(target=proba_tk.main)
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
