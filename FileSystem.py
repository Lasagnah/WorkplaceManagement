import datetime
from typing import List, Optional

class FileNode:
    def __init__(self, name: str, size: int = 0, creation_date: Optional[datetime.datetime] = None):
        self.name = name
        self.size = size
        self.creation_date = creation_date or datetime.datetime.now()
        self.parent = None  # Will be set when added to a folder

    def __repr__(self):
        return f"FileNode(name={self.name}, size={self.size}, created={self.creation_date})"

class FolderNode:
    def __init__(self, name: str):
        self.name = name
        self.parent = None  # set when this folder is nested in another folder
        self.subfolders: List['FolderNode'] = []
        self.files: List[FileNode] = []

    def __repr__(self):
        return f"FolderNode(name={self.name})"

    def add_folder(self, folder: 'FolderNode'):
        folder.parent = self
        self.subfolders.append(folder)

    def add_file(self, file_node: FileNode):
        file_node.parent = self
        self.files.append(file_node)

    def remove_file(self, filename: str) -> bool:
        for f in self.files:
            if f.name == filename:
                self.files.remove(f)
                f.parent = None
                return True
        return False

    def remove_folder(self, foldername: str) -> bool:
        for fold in self.subfolders:
            if fold.name == foldername:
                self.subfolders.remove(fold)
                fold.parent = None
                return True
        return False

    def get_subfolder(self, foldername: str) -> Optional['FolderNode']:
        for fold in self.subfolders:
            if fold.name == foldername:
                return fold
        return None

    def get_file(self, filename: str) -> Optional[FileNode]:
        for f in self.files:
            if f.name == filename:
                return f
        return None

    def list_contents(self):
        folder_names = [f.name for f in self.subfolders]
        file_names = [f.name for f in self.files]
        return folder_names, file_names

    def search_file(self, filename: str) -> Optional[FileNode]:
        """Recursively search for a file in this folder and all subfolders."""
        # Check current folder
        for f in self.files:
            if f.name == filename:
                return f

        # Recursively search subfolders
        for fold in self.subfolders:
            result = fold.search_file(filename)
            if result is not None:
                return result

        return None

    def search_folder(self, foldername: str) -> Optional['FolderNode']:
        """Recursively search for a folder by name."""
        if self.name == foldername:
            return self

        for fold in self.subfolders:
            result = fold.search_folder(foldername)
            if result:
                return result
        return None


class FileManager:
    def __init__(self):
        self.root = FolderNode("root")

    def create_folder(self, folder_name: str, parent_folder_path: Optional[str] = None) -> bool:
        """Create a new folder inside the specified parent folder path or root if none given."""
        parent_folder = self._navigate_to_folder(parent_folder_path) if parent_folder_path else self.root
        if not parent_folder:
            print("Parent folder not found.")
            return False

        # Check if folder with same name exists at this level
        if parent_folder.get_subfolder(folder_name) is not None:
            print("Folder already exists.")
            return False

        new_folder = FolderNode(folder_name)
        parent_folder.add_folder(new_folder)
        return True

    def add_file(self, file_name: str, parent_folder_path: Optional[str] = None, size=0) -> bool:
        """Add a file to the specified folder."""
        parent_folder = self._navigate_to_folder(parent_folder_path) if parent_folder_path else self.root
        if not parent_folder:
            print("Parent folder not found.")
            return False

        # Check if file with same name exists
        if parent_folder.get_file(file_name):
            print("File already exists.")
            return False

        new_file = FileNode(name=file_name, size=size)
        parent_folder.add_file(new_file)
        return True

    def move_file(self, filename: str, source_folder_path: str, target_folder_path: str) -> bool:
        """Move file from one folder to another."""
        source_folder = self._navigate_to_folder(source_folder_path)
        target_folder = self._navigate_to_folder(target_folder_path)

        if not source_folder or not target_folder:
            print("Invalid source or target folder.")
            return False

        file_node = source_folder.get_file(filename)
        if not file_node:
            print("File not found in the source folder.")
            return False

        # Remove from source
        source_folder.remove_file(filename)
        # Add to target
        target_folder.add_file(file_node)
        return True

    def search_file(self, filename: str) -> Optional[FileNode]:
        return self.root.search_file(filename)

    def _navigate_to_folder(self, folder_path: Optional[str]) -> Optional[FolderNode]:
        """Navigate the folder structure using a path like 'root/folder/subfolder'."""
        if folder_path is None or folder_path == "" or folder_path == "root":
            return self.root

        parts = folder_path.strip("/").split("/")
        current = self.root
        for p in parts:
            next_folder = current.get_subfolder(p)
            if not next_folder:
                return None
            current = next_folder
        return current

    def list_folder_contents(self, folder_path: Optional[str] = None):
        folder = self._navigate_to_folder(folder_path) if folder_path else self.root
        if folder:
            folders, files = folder.list_contents()
            print("Folders:", folders)
            print("Files:", files)
        else:
            print("Folder not found.")

    def ensure_integrity(self):
        """Optional: Verify that all files have a parent and that the structure is consistent.
           This can be expanded to detect orphaned files or invalid references."""
        # In this simple example, the structure is inherently consistent if no external modifications
        # are made. More sophisticated checks can be implemented if needed.
        pass

    # Future Extensions:
    # - save_to_json(filepath)
    # - load_from_json(filepath)
    # - add_file_versioning
    # - sort files by size, date, etc.
    # - advanced search by metadata


if __name__ == "__main__":
    fm = FileManager()
    fm.create_folder("Documents")
    fm.create_folder("Projects", "root/Documents")
    fm.add_file("README.txt", "root")
    fm.add_file("Report.pdf", "root/Documents")
    fm.add_file("Code.py", "root/Documents/Projects")

    fm.list_folder_contents("root")           # Should list Documents folder and README.txt file
    fm.list_folder_contents("root/Documents") # Should list Projects folder and Report.pdf file

    # Search for a file recursively
    found_file = fm.search_file("Code.py")
    print("Found File:", found_file)

    # Move a file
    fm.move_file("Report.pdf", "root/Documents", "root")
    fm.list_folder_contents("root")
