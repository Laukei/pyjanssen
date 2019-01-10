from pyjanssen import MCM, FORWARD, BACKWARD

def main():
	m = MCM(server=True,verbose=True)
	m.get_position(2)
	m.move(2,BACKWARD,steps=1)


def multithreading_bug():
	import time
	import threading

	m = MCM()
	def thing():
		while True:
			m.get_position(1,1)
			print('asked position')
			time.sleep(1)

	t = threading.Thread(target=thing)
	t.setDaemon(True)
	t.start()

	for i in range(5):
		m.move(1,FORWARD)
		print('moved forward')
		time.sleep(0.2)


if __name__ == "__main__":
	multithreading_bug()
