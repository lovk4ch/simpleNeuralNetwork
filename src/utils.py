from itertools import islice

MSG_EMPTY_IMAGE_ARRAY = "Image array is empty or not loaded."
MSG_DATASET_IS_NOT_LOADED = "Failed to load dataset. Check the selected file exists and is not empty."
MSG_TRAINING_COMPLETED = "The neural network has been trained on {} records.\nNow please select test dataset."
MSG_UNKNOWN_NET_MODE = "Unknown net mode. Please select TRAIN or QUERY mode."
MSG_QUERY_COMPLETED = "{} records from dataset have been processed.\nAccuracy - {:.2f}%\nNow you can select a record to view its image and processed data."

class FileUtils:
    @staticmethod
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
