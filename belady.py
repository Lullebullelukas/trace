import sys

class Belady:
    def __init__(self):
        self.trace = []
        self.cache_size = 255
        self.cache = [None] * self.cache_size
        self.refs = [0] * self.cache_size
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
        max_distance = -1
        self.free_index = 0
        #loop through cache
        for i in range(self.cache_size):
            #loop through trace
            for j in range(len(self.trace)):
                if self.trace[j] == self.cache[i]:
                    if j > max_distance:
                        max_distance = j
                        self.free_index = i
                    break
            if max_distance == -1:
                self.free_index = i
                return

    def simulate(self):
        #fill cache until its full
        progress = 0
        trace = self.trace
        total_len = len(trace)
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
            progress += 1
            print(f"progress: % {(progress/total_len)*100}", end='\r',flush=True)

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
            progress += 1       
            print(f"progress: % {(progress/total_len)*100}", end='\r', flush=True)
               

if __name__ == "__main__":
    if len(sys.argv) != 2:
        file_path = "trace_1751869864240"
    else:
        file_path = sys.argv[1]
    belady = Belady()
    belady.scan_file_into_list(file_path)
    belady.simulate()
    print(f"Hits: {belady.hits}")
    print(f"Faults: {belady.faults}")
