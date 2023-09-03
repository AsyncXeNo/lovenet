from __future__ import annotations

from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from game.operating_system.file_system.directory import Directory
    from game.operating_system.file_system.file import File

from game.world.user import User
from game.operating_system.file_system.storage_unit import StorageUnit, Permission
from game.operating_system.file_system.exceptions import FileSystemError


class Directory(StorageUnit):
    def __init__(self, name: str, contents: list[StorageUnit], parent: Directory | Any, created_by: User, permissions: dict[str, list[Permission]]={}) -> None:
        super().__init__(name, contents, parent, created_by, permissions)

    """
    MAIN
    """

    def add(self, storage_unit: StorageUnit, user: User) -> None:
        """
        This might not be how it works in a real linux file system. Because technically you can add a file to a folder without having read permissions to it. However, that is dumb and this implementation is easy so I will go with this.
        """
        contents: list[StorageUnit] | Any = self.get_contents(user)
        contents.append(storage_unit)
        self.set_contents(contents, user)

    def remove(self, storage_unit: StorageUnit, user: User) -> None:
        contents: list[StorageUnit] | Any = self.get_contents(user)
        contents.remove(storage_unit)
        self.set_contents(contents, user)

    def get_files(self, user: User) -> list[StorageUnit]:
        contents: list[StorageUnit] | Any = self.get_contents(user)
        return list(filter(lambda su: isinstance(su, File), contents))
    
    def get_directories(self, user: User) -> list[StorageUnit]:
        contents: list[StorageUnit] | Any = self.get_contents(user)
        return list(filter(lambda su: isinstance(su, Directory), contents))

    """
    HELPERS
    """

    def _validate_contents(self, contents: list[StorageUnit | Any] | Any, user: User) -> None:
        super()._validate_contents(contents, user)
        if not isinstance(contents, list):
            raise FileSystemError(self.error_messages.get("contents"))
        

class Root(Directory):
    def __init__(self, contents: list[StorageUnit], created_by: User, permissions: dict[str, list[Permission]]={}) -> None:
        super().__init__('', contents, None, created_by, permissions)

    """
    MAIN
    """

    def set_parent(self, parent: StorageUnit, user: User) -> None:
        return

    """
    HELPERS
    """

    def _validate_parent(self, parent: StorageUnit | Any, user: User) -> None:
        if parent is not None:
            raise FileSystemError(self.error_messages.get("parent"))
        
    def _validate_name(self, name: str, user: User) -> None:
        if name != '':
            raise FileSystemError(self.error_messages.get("name"))
