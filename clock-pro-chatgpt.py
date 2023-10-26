import sys

class ClockPro:
    def __init__(self, frame_count):
        self.frame_count = frame_count
        self.head = [None] * frame_count
        self.pro = [None] * frame_count
        self.tail = [None] * frame_count
        self.access_bits = [0] * frame_count
        self.ref_bits = [0] * frame_count
        self.page_counts = {}
        self.head_clock = 0
        self.pro_clock = 0
        self.tail_clock = 0
        self.faults = 0
        self.hits = 0

    def move_to_pro(self, index):
        if self.head[index] is not None:
            self.head[index] = None
            self.pro[self.pro_clock] = index
            self.pro_clock = (self.pro_clock + 1) % self.frame_count

    def move_to_tail(self, index):
        if self.pro[index] is not None:
            self.pro[index] = None
            self.tail[self.tail_clock] = index
            self.tail_clock = (self.tail_clock + 1) % self.frame_count

    def evict_page(self):
        if self.head[self.head_clock] is not None:
            index = self.head_clock
        elif self.pro[self.pro_clock] is not None:
            index = self.pro_clock
        else:
            index = self.tail_clock

        return index

    def access_page(self, page):
        self.hits+=1 #assume hit
        if page in self.head:
            index = self.head.index(page)
        elif page in self.pro:
            index = self.pro.index(page)
        elif page in self.tail:
            index = self.tail.index(page)
        else:
            self.hits-=1 #reverse hit, it was a fault
            self.faults+=1
            if None in self.head:
                index = self.head.index(None)
                self.head[index] = page
            else:
                index = self.evict_page()
                evicted_page = self.head[index]
                self.head[index] = page
                self.move_to_pro(index)
                if evicted_page in self.pro:
                    self.move_to_tail(self.pro.index(evicted_page))
                elif evicted_page in self.tail:
                    self.tail[self.tail.index(evicted_page)] = None

        self.access_bits[index] = 1

    def simulate(self, page_trace):
        page_trace = page_trace.split()
        page_faults = 0
        total_references = 0

        for page in page_trace:
            total_references += 1
            self.access_page(page)

        for page in self.head + self.pro + self.tail:
            self.page_counts[page] = self.page_counts.get(page, 0) + 1

        for page, count in self.page_counts.items():
            if page is not None:
                print(f"Page {page}: Accessed {count} times")

        page_faults = self.faults
        print(f"Total Page Faults: {page_faults}")
        print(f"Total number of hits: {self.hits}")
       

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clock_pro.py <frame_count> <input_file>")
        sys.exit(1)

    frame_count = int(sys.argv[1])
    input_file = sys.argv[2]

    try:
        with open(input_file, 'r') as file:
            page_trace = file.read()
    except FileNotFoundError:
        print("Input file not found.")
        sys.exit(1)

    clock_pro = ClockPro(frame_count)
    clock_pro.simulate(page_trace)
