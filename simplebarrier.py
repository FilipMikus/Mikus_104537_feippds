from fei.ppds import Mutex, Event


class SimpleBarrier:

    def __init__(self, n):

        self.n = n
        self.c = 0
        self.mutex = Mutex()
        self.event = Event()


    def wait(self):

        self.mutex.lock()
        if self.c == 0:
            self.event.clear()
        self.c += 1
        if self.c == self.n:
            self.event.signal()
        self.mutex.unlock()
        self.event.wait()