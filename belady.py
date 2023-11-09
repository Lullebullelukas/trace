import sys

class Belady:
    def __init__(self,cache_size):
        self.trace = []
        self.cache_size = cache_size
        self.cache = [None] * self.cache_size
        self.refs = [0] * self.cache_size
        self.faults = 0 
        self.hits = 0
        self.free_index = 0
        self.page_distance = [-1] * self.cache_size


    def decrement_distance(self):
        for i in range(self.cache_size): 
            if self.page_distance[i] >= 0:
                self.page_distance[i] -= 1

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
        non_known = set()
        for i in range(self.cache_size):
            non_known.add(self.cache[i])

        for i in range(self.cache_size):
            dist = self.page_distance[i]
            if dist >= 0:
                non_known.remove(self.cache[i])

        #update our distance data structures
        for j in range(len(self.trace)):
            page = self.trace[j]
            if page in non_known:
                for i in range(self.cache_size):
                    if self.cache[i] == page:
                        self.page_distance[i] = j
                non_known.remove(page)
        
        if len(non_known) != 0:
            for i in range(self.cache_size):
                page = self.cache[i]
                if page in non_known:
                    self.free_index = i
                    self.page_distance[i] = -1
                    return
                
        max_index = 0
        for i in range(self.cache_size):
            if self.page_distance[i] > max_distance:
                max_distance = self.page_distance[i]
                max_index = i

        
        self.free_index = max_index






        

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
            if progress % 1000 == 0:
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
                self.decrement_distance()
                self.cache[self.free_index] = page   
                self.page_distance[self.free_index] = -1  
            progress += 1       
            if progress % 1000 == 0:
                print(f"progress: % {(progress/total_len)*100}", end='\r', flush=True)
               

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

    belady = Belady(cache_size)
    belady.scan_file_into_list(file_path)
    belady.simulate()
    print(f"\nHits: {belady.hits}")
    print(f"Faults: {belady.faults}")
