import threading
import time


class Worker(threading.Thread):
    ns = threading.local()

    def __init__(self, val):
        threading.Thread.__init__(self)
        self.val = val

    def run(self):
        # self.ns.val = self.val
        for i in range(5):
            self.ns.val = self.val+1
            print("Thread:", self.name, "value:", self.ns.val)
            time.sleep(2)

    def set_val(self, new_val):
        self.val = new_val




if __name__ == "__main__":
    a = Worker(99)
    a.start()
    a.set_val(999)
    time.sleep(2)
    a.set_val(888)
