import os


class FileManager:
    @staticmethod
    def get_all_json_in_dir(directory_path) -> list[str]:
        """Returns a list of all file paths ending in .json in the specified directory."""
        try:
            files = os.listdir(directory_path)
            return [
                os.path.join(directory_path, f) for f in files if f.endswith(".json")
            ]
        except FileNotFoundError:
            print(f"The directory {directory_path} does not exist.")
            return []
