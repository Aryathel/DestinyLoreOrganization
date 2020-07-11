import sys
import time

class ProgressBar:
    background = None
    load = None
    head = None
    size = None
    count = 0

    def __init__(self, background, load, size, head=''):
        self.background = background
        self.load = load
        self.head = head
        self.size = int(size)
        self.last_time = time.time()
        self.last = 0
        self.eta = 0.00

    def progress(self, toAdd, status='', flush=True):
        bar_len = 60
        self.count += toAdd
        filled_len = int(round(bar_len * self.count / self.size))

        if self.count == self.size:
            self.eta = 0.0

        percents = round(100 * self.count / self.size, 2)
        if(self.head is None):
            bar = self.load * filled_len
        else:
            bar = self.load * (filled_len - 1) + self.head
        bar = bar + self.background * (bar_len - filled_len)

        str2print = '[%s] (%s/%s) %s%s %s... ETA: %s seconds\r' % (bar, self.count, self.size, percents, '%', status, self.eta)
        sys.stdout.write('%s\r' % (' ' * len(str2print)))
        if(flush):
            sys.stdout.flush()
            sys.stdout.write(str2print)
        else:
            print(str2print)
        if self.count == self.size:
            print('\n')

    def ETA(self):
        self.curr_time = time.time()
        self.eta = round((self.size - self.count) / (self.count - self.last) * (self.curr_time - self.last_time), 2)
        self.last_time = self.curr_time
        self.last = self.count

#run tests
def main():
    from time import sleep

    pb = ProgressBar(' ', '█', 10)
    pb.progress(0, status = "Loading Ishtar Categories")
    for idx in range(10):
        pb.progress(1, status = "Loading Ishtar Categories")
        time.sleep(1)


if __name__ == '__main__':
    main()
