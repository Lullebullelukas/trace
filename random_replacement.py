import sys
import random

class RandomReplacement:
    def __init__(self,cache_size):
        self.trace = []
        self.cache_size = cache_size
        self.cache = [None] * self.cache_size
        self.faults = 0 
        self.hits = 0
        self.free_index = 0

# Function to read a file and put its rows into a list
    def scan_file_into_list(self,file_path):
        try:
            # Open the file for reading
            with open(file_path, 'r') as file:
                # Read each line from the file
                for line in file:
                    # Remove leading and trailing whitespace and add to the list
                    self.trace.append(line.strip())
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def evict(self):
        self.free_index = random.randint(0, self.cache_size-1) 

    def simulate(self):
        #fill cache until its full
        trace = self.trace
        initial_faults = 0
        while initial_faults < self.cache_size:
            page = trace.pop(0)
            if page in self.cache:
                #hit
                self.hits+=1
            else: 
                #fault
                self.faults+=1
                self.cache[self.free_index] = page
                self.free_index+=1
                initial_faults+=1
             
        #cache is now filled
        #for every miss we now need to evict

        while trace:
            page = trace.pop(0)
            if page in self.cache:
                #hit
                self.hits+=1
            else:
                #fault
                self.faults+=1
                self.evict()
                self.cache[self.free_index] = page
               
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

    rand = RandomReplacement(cache_size)
    rand.scan_file_into_list(file_path)
    rand.simulate()
    print(f"\nHits: {rand.hits}")
    print(f"Faults: {rand.faults}")
