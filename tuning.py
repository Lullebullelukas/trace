import sys

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

class Clock4Usage:
    def __init__(self, cache_size):
        self.cache_size = cache_size
        self.hits = 0
        self.clock_arm = 0
        self.list_of_pages = [None] * self.cache_size
        self.faults = 0
        self.hits = 0

    def decrement(self, cache, page):
        cache[page] = max(cache[page] - 1, 0) 

    def add_or_increment(self, cache, page):
        if page not in cache:
            #fault
            self.faults += 1
            self.list_of_pages[self.clock_arm] = page
            self.clock_arm += 1
            cache[page] = 1
        else:
            #hit
            self.hits += 1
            cache[page] = min(cache[page] + 1, 3) 

    def evict(self, cache):
        while True:
            #check counter, if it is leq than 1 evict
            if self.clock_arm == self.cache_size:
                self.clock_arm = 0
            
            page = self.list_of_pages[self.clock_arm]
            self.decrement(cache, page)
            if cache[page] == 0:
                cache.pop(page)
                return
            
            self.clock_arm += 1

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
            file_path = "trace-big"
            cache_size = 255
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
    clock_4_usage = Clock4Usage(cache_size)
    clock_4_usage.simulate(string_list)
    print(f"Hits: {clock_4_usage.hits}")
    print(f"Faults: {clock_4_usage.faults}")