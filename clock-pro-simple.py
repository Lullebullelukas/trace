import sys
from collections import OrderedDict

#TODO: implement eviction and hand movement
# data structures should now be in place but not all operations

class ClockPro:
    def __init__(self):
        self.trace = []
        self.clock_hand = 0
        self.cache_size = 255
        self.non_res_cache = [None] * self.cache_size
        self.cache = [None] * self.cache_size
        self.refs = [0] * self.cache_size
        self.faults = 0 
        self.hits = 0
        self.free_index = 0
        self.cold_pages = set()
        self.non_res_pages = OrderedDict()
        self.pages_in_cache = 0

# Function to read a file and put its rows into a list
    def scan_file_into_list(self,file_path):
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
            self.non_res_pages.popitem(last=False)
        self.non_res_pages[page] = 0

    def evict(self):
        evicted = False
        while not evicted:
            #loop through the list and do stuff
            index = self.clock_hand % self.cache_size
            self.clock_hand+=1
            ref = self.refs[index]
            self.refs[index] = max(0, ref-1)
            page = self.cache[index]

            if ref <= 1:
                self.cache[index] = None
                self.free_index = index
                self.add_non_res(page)
                evicted = True

    def simulate(self):
        #fill cache until its full
        trace = self.trace
        while self.pages_in_cache < self.cache_size:
            page = trace.pop(0)
            if page in self.cache:
                #hit
                self.hits+=1
                self.refs[self.cache.index(page)] = min(4, self.refs[self.cache.index(page)] + 1)
            else: 
                #fault
                self.faults+=1
                self.cache[self.free_index] = page
                self.refs[self.free_index] = 1
                self.free_index+=1
                self.pages_in_cache+=1

        #cache is now filled
        #for every miss we now need to evict

        while trace:
            page = trace.pop(0)
            
            if page in self.cache:
                #hit
                self.hits+=1
                #increase ref
                self.refs[self.cache.index(page)] = min(4, self.refs[self.cache.index(page)] + 1)
                
            else:
                #fault
                self.faults+=1
                self.evict()
                self.cache[self.free_index] = page
                self.refs[self.free_index] = 1

                if page in self.non_res_pages:
                    del self.non_res_pages[page]
                    self.non_res_cache[self.free_index] = None
                    self.refs[self.free_index] = 4

if __name__ == "__main__":
    if len(sys.argv) != 2:
        file_path = "trace_1737075246791"
    else:
        file_path = sys.argv[1]
    clock_pro = ClockPro()
    clock_pro.trace = clock_pro.scan_file_into_list(file_path)
    # Print the list of strings
    clock_pro.simulate()
    print(f"Hits: {clock_pro.hits}")
    print(f"Faults: {clock_pro.faults}")
    print(f"N Cold pages: {len(clock_pro.cold_pages)}")
    print(f"N NonRes pages: {len(clock_pro.non_res_pages)}")
