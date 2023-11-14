import sys
from collections import OrderedDict

class ClockPro:
    def __init__(self, cache_size):
        self.trace = []
        self.clock_hand = 0
        self.cache_size = cache_size
        self.non_res_cache = [None] * self.cache_size
        self.cache = [None] * self.cache_size
        self.refs = [0] * self.cache_size
        self.faults = 0 
        self.hits = 0
        self.free_index = 0
        self.cold_pages = set()
        self.non_res_pages = OrderedDict()

    # Function to read a file and put its rows into a list
    def scan_file_into_list(self, file_path):
        # Initialize an empty list to store the strings
        string_list = []

        try:
            # Open the file for reading
            with open(file_path, 'r') as file:
                # Read each line from the file
                for line in file:
                    # Remove leading and trailing whitespace and add to the list
                    string_list.append(line.strip())
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

        return string_list
    
    def add_non_res(self, page):
        if len(self.non_res_pages) == self.cache_size:
            self.non_res_pages.popitem(last = False)
        self.non_res_pages[page] = 0

    def evict(self):
        evicted = False
        while not evicted:
            #loop through the list and do stuff
            index = self.clock_hand % self.cache_size
            self.clock_hand += 1
            ref = self.refs[index]
            self.refs[index] = max(0, ref - 1)
            page = self.cache[index]

            if ref <= 1:
                self.free_index = index
                self.add_non_res(page)
                evicted = True

    def simulate(self):
        #fill cache until its full
        initial_faults = 0
        while self.trace and (initial_faults < self.cache_size):
            page = self.trace.pop(0)
            if page in self.cache:
                #hit
                self.hits += 1
                self.refs[self.cache.index(page)] = min(4, self.refs[self.cache.index(page)] + 1)
            else: 
                #fault
                self.faults += 1
                self.cache[self.free_index] = page
                self.refs[self.free_index] = 1
                self.free_index += 1
                initial_faults += 1

        #cache is now filled
        #for every miss we now need to evict

        while self.trace:
            page = self.trace.pop(0)
            
            if page in self.cache:
                #hit
                self.hits += 1
                #increase ref
                self.refs[self.cache.index(page)] = min(4, self.refs[self.cache.index(page)] + 1)
                
            else:
                #fault
                self.faults += 1
                self.evict()
                self.cache[self.free_index] = page
                self.refs[self.free_index] = 1

                if page in self.non_res_pages:
                    del self.non_res_pages[page]
                    self.non_res_cache[self.free_index] = None
                    self.refs[self.free_index] = 7

if __name__ == "__main__":
    if not (len(sys.argv) == 3 or len(sys.argv) == 2):
            file_path = "trace-big"
            cache_size = 255
    elif len(sys.argv) == 3: 
        file_path = sys.argv[1]
        cache_size = int(sys.argv[2])
    else:
        file_path = sys.argv[1]
        cache_size = 255
        
    clock_pro = ClockPro(cache_size)
    clock_pro.trace = clock_pro.scan_file_into_list(file_path)
    uniques = set()
    for string in clock_pro.trace:
        uniques.add(string)

    print(f"Working set size: {len(uniques)}")
    print(f"list len {len(clock_pro.trace)}")
    clock_pro.simulate()
    print(f"Hits: {clock_pro.hits}")
    print(f"Faults: {clock_pro.faults}")
