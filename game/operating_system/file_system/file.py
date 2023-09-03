from __future__ import annotations

from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from game.operating_system.file_system.directory import Directory

from game.world.user import User
from game.operating_system.file_system.storage_unit import StorageUnit, Permission
from game.operating_system.file_system.exceptions import FileSystemError


class File(StorageUnit):
    def __init__(self, name: str, contents: str, parent: Directory, created_by: User, permissions: dict[str, list[Permission]]={}) -> None:
        super().__init__(name, contents, parent, created_by, permissions)

    """
    MAIN
    """

    # Getters

    def get_filename(self, user: User) -> str:
        name: str = self.get_name(user)
        split: list[str] = name.split('.')
        if len(split) == 1:
            return name
        return '.'.join(split[:-1])
    
    def get_extension(self, user: User) -> str | None:
        name: str = self.get_name(user)
        split: list[str] = name.split('.')
        if len(split) == 1:
            return None
        return split[-1]

    """
    HELPERS
    """

    def _validate_contents(self, contents: str | Any, user: User) -> None:
        super()._validate_contents(contents, user)
        if not isinstance(contents, str):
            raise FileSystemError(self.error_messages.get("contents"))
