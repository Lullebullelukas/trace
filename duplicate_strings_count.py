import sys

def count_strings_appearing_more_than_once(filename):
    # Create a dictionary to store the counts of each string
    string_counts = {}
    duplicates_count = 0

    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()  # Remove leading/trailing whitespace
                if line in string_counts:
                    if string_counts[line] >= 1:
                        duplicates_count += 1
                    string_counts[line] += 1
                else:
                    string_counts[line] = 1

        print(f'Number of strings appearing more than once: {duplicates_count}')

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python count_duplicates.py <filename>")
    else:
        filename = sys.argv[1]
        count_strings_appearing_more_than_once(filename)
