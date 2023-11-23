import sys
import heapq

# Function to read a file and put its rows into a list
def scan_file_into_list(file_path):
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

class LFU:
    def __init__(self, cache_size):
        self.cache_size = cache_size
        self.hits = 0
        self.clock_arm = 0
        self.faults = 0
        self.hits = 0
        self.heap = []

    def decrement(self, cache, page):
        cache[page] = max(cache[page] - 1, 0) 

    def add_or_increment(self, cache, page):
        if page not in cache:
            #fault
            self.faults += 1
            cache[page] = 0
            heapq.heappush(self.heap, (0, page))
        else:
            #hit
            self.hits += 1
            cache[page] = cache[page] + 1
            for i in range(len(self.heap)):
                freq, pg = self.heap[i]
                if pg == page:
                    self.heap[i] = (freq+1, pg)
                    break
            heapq.heapify(self.heap)

    def evict(self, cache):
        freq, page = heapq.heappop(self.heap)
        cache.pop(page)

    def simulate(self, accesses):
        cache = {}
        while accesses and (len(cache) < self.cache_size):
            self.add_or_increment(cache, accesses.pop(0))

        #now the cache is full, for every insertion we need eviction
        self.clock_arm = 0 #reset clock arm
        while accesses: 
            page = accesses.pop(0) #get next page from trace
            if not page in cache:
                #we need to evict
                self.evict(cache)

            self.add_or_increment(cache, page)

if __name__ == "__main__":
    if not (len(sys.argv) == 3 or len(sys.argv) == 2):
            file_path = "smol_trace"
            cache_size = 3
    elif len(sys.argv) == 3: 
        file_path = sys.argv[1]
        cache_size = int(sys.argv[2])
    else:
        file_path = sys.argv[1]
        cache_size = 255
    
    string_list = scan_file_into_list(file_path)
    uniques = set()
    for string in string_list:
        uniques.add(string)

    print(f"Working set size: {len(uniques)}")
    print(f"list len {len(string_list)}")
    lfu = LFU(cache_size)
    lfu.simulate(string_list)
    print(f"Hits: {lfu.hits}")
    print(f"Faults: {lfu.faults}")