from __future__ import annotations

from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from game.operating_system.file_system.directory import Directory
import re

from game.world.user import User
from game.operating_system.file_system.exceptions import FileSystemError
from enum import Enum


class Permission(Enum):
    READ = 0
    WRITE = 1
    EXECUTE = 2


class StorageUnit(object):
    def __init__(self, name: str, contents: str | list[StorageUnit], parent: Directory, created_by: User, permissions: dict[str, list[Permission]]={}) -> None:

        self.error_messages = {
            "permission": "Not enough permissions",
            "parent": "Invalid parent",
            "contents": "Invalid contents",
            "name": "Invalid name",
        }
              
        self.created_by: User = created_by
        self.permissions: dict[str, list[Permission]] = {
            self.created_by.name: [Permission.READ, Permission.WRITE, Permission.EXECUTE]
        }
        self.permissions.update(permissions)
        
        self.__parent: Directory
        self.__contents: str | list[StorageUnit]
        self.__name: str
        self.set_parent(parent, created_by)
        self.set_contents(contents, created_by)
        self.set_name(name, created_by)

    """
    MAIN
    """

    # Setters
    def set_parent(self, parent: Directory, user: User) -> None:
        self._validate_parent(parent, user)
        try: self.__parent.remove(self, user)
        except AttributeError: pass
        self.__parent = parent
        self.__parent.add(self, user)

    def set_contents(self, contents: str | list[StorageUnit], user: User) -> None:
        self._validate_contents(contents, user)
        self.__contents = contents

    def set_name(self, name: str, user: User) -> None:
        self._validate_name(name, user)
        self.__name = name

    # Getters

    def get_path(self, user: User) -> str:
        if not self.__parent.check_perms(user, Permission.READ):
            raise FileExistsError(self.error_messages.get("permission"))
        return f'{self.__parent.get_path(user)}/{self.__name}'
    
    def get_parent(self) -> StorageUnit:
        """This *might* need some additional permission checks"""
        return self.__parent
    
    def get_contents(self, user: User) -> str | list[StorageUnit]:
        if not self.check_perms(user, Permission.READ):
            raise FileExistsError(self.error_messages.get("permission"))
        return self.__contents
    
    def get_name(self, user: User) -> str:
        if not self.check_perms(user, Permission.READ):
            raise FileExistsError(self.error_messages.get("permission"))
        return self.__name
    
    def get_permissions(self) -> dict[str, list[Permission]]:
        return self.permissions
    
    # Others

    def check_perms(self, user: User, perm: Permission) -> bool:
        user_perms: list[Permission] | None = self.permissions.get(user.name)
        if user_perms is not None and perm in user_perms:
            return True
        return False

    """
    HELPERS
    """
    
    def _validate_parent(self, parent: Directory, user: User) -> None:
        if not parent.check_perms(user, Permission.WRITE):
            raise FileSystemError(self.error_messages.get("permission"))
        if not parent:
            raise FileSystemError(self.error_messages.get("parent"))
        
    def _validate_contents(self, contents: str | list[StorageUnit | Any] | Any, user: User) -> None:
        if not self.check_perms(user, Permission.WRITE):
            raise FileSystemError(self.error_messages.get("permission"))
        if not (isinstance(contents, list) or isinstance(contents, str)):
            raise FileSystemError(self.error_messages.get("contents"))
        if isinstance(contents, list):
            if not all([isinstance(content, StorageUnit) for content in contents]):
                raise FileSystemError(self.error_messages.get("contents"))
    
    def _validate_name(self, name: str, user: User) -> None:
        if not self.check_perms(user, Permission.WRITE):
            raise FileSystemError(self.error_messages.get("permission"))
        if not name or name.startswith('-') or name.startswith('.') or not re.match(r'^[a-zA-Z0-9_.-]+$', name):
            raise FileSystemError(self.error_messages.get("name"))
