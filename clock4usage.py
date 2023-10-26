import sys

global clock_arm, list_of_pages, faults, hits
clock_arm=0
cache_size = 255 #how many pages we can fit
list_of_pages = [None] * 255
faults = 0
hits = 0

#disgusting python code but it works

def __init__(self):
    self.hits = 0

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
    cache[page] = max(cache[page]-1, 0) 

def add_or_increment(cache, page):
    global clock_arm, list_of_pages, faults, hits

    if page not in cache:
        #fault
        faults+=1
        list_of_pages[clock_arm] = page
        clock_arm+=1
        cache[page]=1
    else:
        #hit
        hits += 1
        cache[page] = min(cache[page]+1,4) 


def evict(cache):
    global clock_arm, list_of_pages, hits
    while True:
        #check counter, if it is leq than 1 evict
        if clock_arm >= cache_size:
            clock_arm = 0
    
        if list_of_pages[clock_arm] is None:
           return


        if cache[list_of_pages[clock_arm]] <= 1:
            cache.pop(list_of_pages[clock_arm])
            list_of_pages[clock_arm] = None
            return
        
        decrement(cache,list_of_pages[clock_arm])
        clock_arm+=1

            


def simulate(accesses):
    global clock_arm, list_of_pages
    cache = {}
    while len(cache) < cache_size:
        add_or_increment(cache,accesses.pop(0))

    #now the cache is full, for every insertion we need eviction
    clock_arm = 0 #reset clock arm
    while accesses: 
        page = accesses.pop(0) #get next page from trace
        if not page in cache:
            #we need to evict
            evict(cache)

        add_or_increment(cache,page)
    
    print("page faults: " + str(faults))
    print(f"hits: {hits}")




def main():
    if len(sys.argv) != 2:
        file_path = "trace_1737075246791"
    else:
        file_path = sys.argv[1]
    string_list = scan_file_into_list(file_path)
    simulate(string_list)

            
main()