import sys

def count_duplicate_strings(filename):
    # Create a dictionary to store the counts of each string
    string_counts = {}

    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()  # Remove leading/trailing whitespace
                if line in string_counts:
                    string_counts[line] += 1
                else:
                    string_counts[line] = 1

        # Print the duplicate strings and their counts
        for string, count in string_counts.items():
            if count > 1:
                print(f'{string}: {count} times')

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python count_duplicates.py <filename>")
    else:
        filename = sys.argv[1]
        count_duplicate_strings(filename)
