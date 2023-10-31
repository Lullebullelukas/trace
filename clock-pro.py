import sys

#TODO: implement eviction and hand movement
# data structures should now be in place but not all operations

class ClockPro:
    def __init__(self):
        self.trace = []
        self.cold_hand = 0
        self.hot_hand = 0
        self.test_hand = 0
        self.cache_size = 255
        self.non_res_cache = [None] * self.cache_size
        self.cache = [None] * self.cache_size
        self.refs = [0] * self.cache_size
        self.faults = 0 
        self.hits = 0
        self.free_index = 0
        self.hot_pages = set()
        self.test_pages = set()
        self.non_res_pages = set()
        self.capacity_hot = self.cache_size / 2


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
    

    def evict(self):
        evicted = False
        while not evicted:
            #loop through the list and do stuff
            index = self.cold_hand % self.cache_size
            self.cold_hand+=1
            ref = self.refs[index]
            page = self.cache[index]

            if page in self.test_pages and ref > 0:
                    self.test_pages.discard(page)
                    #it was in test period when got it, promote to hot
                    if len(self.hot_pages)+1 >= self.capacity_hot:
                        self.move_hot_hand()
                    self.hot_pages.add(page)
                    continue
            
            if page in self.hot_pages:
                continue
            
            #if not reffed we can evict
            if ref < 1: 
                page = self.cache[index]
                self.cache[index] = None
                self.free_index = index
                evicted = True
                if page in self.test_pages:
                    #if in test period we put in non-res    
                    #appending this will make it over cap, so reduce by moving hands
                    
                    self.non_res_pages.add(page)
                    self.non_res_cache[index] = page

                    if len(self.non_res_pages) > self.cache_size:
                        self.move_test_hand()

                    self.hot_pages.discard(page)
                    self.test_pages.discard(page)


            else:
                self.refs[index] = 0
            

        
    def move_hot_hand(self):
        #TODO This: and test hand
        removed = False
        while not removed:
            index = self.hot_hand % self.cache_size
            self.hot_hand +=1
            page = self.cache[index]
           

            if page in self.hot_pages:
            
                if self.refs[index] < 1:
                    #not a hit so we can remove from hot
                    self.hot_pages.discard(page)
                    removed = True
              
                self.refs[index] = 0
            if page in self.test_pages:
                #when hot hand passes over a page in test period we terminate that test period
                self.test_pages.discard(page)
            




    def move_test_hand(self):
        removed = False
        while not removed:
            index = self.test_hand % self.cache_size
            self.test_hand +=1
            page = self.cache[index]
            non_res_page = self.non_res_cache[index]
            if non_res_page in self.non_res_pages:
                self.non_res_pages.discard(non_res_page)
                self.non_res_cache[index] = None
                removed = True
            if page in self.test_pages:
                self.test_pages.discard(page)

            


    def simulate(self):
        #fill cache until its full
        trace = self.trace
        initial_faults = 0
        while initial_faults < self.cache_size:
            page = trace.pop(0)
            if page in self.cache:
                #hit
                self.hits+=1
                self.ref[self.cache.index(page)] = 1
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
                #set ref to 1
                self.refs[self.cache.index(page)] = 1
                
            else:
                #fault
                self.faults+=1
                self.evict()
                self.cache[self.free_index] = page

                if page in self.non_res_pages:
                    self.non_res_pages.discard(page)
                    self.non_res_cache[self.free_index] = None
                    #it was in test period when got it, promote to hot
                    if len(self.hot_pages)+1 >= self.capacity_hot:
                        self.move_hot_hand()
                    self.hot_pages.add(page)

                

                if len(self.non_res_pages) > self.cache_size:
                    self.move_test_hand()

                self.test_pages.add(page) 
                

    



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
    print(f"N Hot pages: {len(clock_pro.hot_pages)}")
    print(f"N Test pages: {len(clock_pro.test_pages)}")
    print(f"N NonRes pages: {len(clock_pro.non_res_pages)}")