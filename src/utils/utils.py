from itertools import islice


# --- Utility functions

def get_data_from_file(path: str, count: int = 0, start_pos: int = 0):
    try:
        with open(path, "r") as file:
            if count is None or count == 0:
                lines = list(islice(file, start_pos, None))
            else:
                lines = list(islice(file, start_pos, start_pos + count))

            print(f"Read {len(lines)} lines from {path}")
            return lines

    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
    except PermissionError:
        print(f"Error: No permission to read file '{path}'.")
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return []