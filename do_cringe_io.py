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


def simulate(accesses):
    cache_size = 255 #how many pages we can fit
    cache = []
    while len(cache) < cache_size:
        #do something
        page=accesses.pop(0)
        if page not in cache:
            cache.append(page)
            
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
    else:
        file_path = sys.argv[1]
        string_list = scan_file_into_list(file_path)
        simulate(string_list)
