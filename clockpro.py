import sys

global cold_arm, hot_arm, test_arm, available_index, list_of_pages,hot_pages 

available_index = 0
cold_arm = 0
hot_arm = 0
test_arm = 0

clock_arm=0
cache_size = 255 #how many pages we can fit
list_of_pages = [None] * 255
hot_pages = []
non_res_pages = []

#data structue for 

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


def decrement(cache, page):
    cache[page] = 0

# False is fault, True is hit
def add_or_increment(cache, page):
    global list_of_pages, available_index
    
    if page not in cache:
        #fault
        if list_of_pages[available_index] is not None:
            print("Panic! spot occupied\n")
            exit()
        list_of_pages[available_index] = page
        cache[page]=1
        return False
    else:
        #hit
        cache[page] = 1
        return True


def evict(cache):
    global cold_arm, list_of_pages, available_index
    while True:
        #check counter, if it is leq than 1 evict
        if cold_arm >= cache_size:
            cold_arm = 0
    
        if list_of_pages[cold_arm] is None:
           print("should not happen?")
           exit()
           


        if cache[list_of_pages[cold_arm]] < 1:
            #we evicted!
            cache.pop(list_of_pages[cold_arm])
            list_of_pages[cold_arm] = None
            available_index = cold_arm
            return
        
        decrement(cache,list_of_pages[cold_arm])
        
        cold_arm+=1

            


def simulate(accesses):
    global cold_arm, list_of_pages, available_index
    cache = {}
    while len(cache) < cache_size:
        if not add_or_increment(cache,accesses.pop(0)):
            #if we faulted
            available_index+=1

    #now the cache is full, for every insertion we need eviction
    available_index = None 
    while accesses: 
        page = accesses.pop(0) #get next page from trace
        if not page in cache:
            #we need to evict
            evict(cache)

        add_or_increment(cache,page)
    
    print(cache)
    print(len(cache))
    print(len([x for x in cache if cache[x] == 4]))
    print(len([x for x in cache if cache[x] == 3]))
    print(len([x for x in cache if cache[x] == 2]))
    print(len([x for x in cache if cache[x] == 1]))
    print(len([x for x in cache if cache[x] == 0]))




def main():
    if len(sys.argv) != 2:
        file_path = "trace_1737075246791"
    else:
        file_path = sys.argv[1]
    string_list = scan_file_into_list(file_path)
    simulate(string_list)

            
main()