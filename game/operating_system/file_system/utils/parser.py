import json

from typing import Any

from game.operating_system.file_system.directory import Directory, Root
from game.operating_system.file_system.file import File
from game.operating_system.file_system.storage_unit import StorageUnit
from game.operating_system.file_system.storage_unit import Permission
from game.world.user import User


class Parser(object):
    
    """
    TO JSON
    """

    @staticmethod
    def to_json_file(root: Root, user: User, path: str) -> None:
        json_data = Parser.to_json(root, user)
        with open(path, 'w') as f:
            f.write(json_data)

    @staticmethod
    def to_json(root: Root, user: User) -> str:
        return json.dumps(Parser.__d_to_json(root, user), indent=4)

    @staticmethod
    def __d_to_json(directory: Directory, user: User) -> dict[str, object]:
        contents: list[object] = []

        for storage_unit in directory.get_contents(user):
            if isinstance(storage_unit, Directory):
                contents.append(Parser.__d_to_json(storage_unit, user))
            elif isinstance(storage_unit, File):
                contents.append(Parser.__f_to_json(storage_unit, user))
        
        permissions: dict[str, list[Permission]] = directory.get_permissions()
        permissions_json: dict[str, list[int]] = { username: [perm.value for perm in perms] for (username, perms) in permissions.items() }

        return {
            "name": directory.get_name(user),
            "contents": contents,
            "permissions": permissions_json
        }

    @staticmethod
    def __f_to_json(file: File, user: User) -> dict[str, object]:
        permissions: dict[str, list[Permission]] = file.get_permissions()
        permissions_json: dict[str, list[int]] = { username: [perm.value for perm in perms] for (username, perms) in permissions.items() }
        
        return {
            "name": file.get_name(user),
            "contents": file.get_contents(user),
            "permissions": permissions_json
        }
    
    """
    FROM JSON
    """

    @staticmethod
    def from_json_file(path: str, user: User) -> Directory:
        with open(path, 'r') as f:
            json_string = f.read()
        return Parser.from_json(json_string, user)

    @staticmethod
    def from_json(json_data: str, user: User) -> Root:
        data: dict[str, object] = json.loads(json_data)

        permissions_json: dict[str, list[int]] | Any = data["permissions"]
        permissions: dict[str, list[Permission]] = { username: [Permission(perm) for perm in perms] for (username, perms) in permissions_json.items() }
        contents: list[StorageUnit] = []

        root: Root = Root(contents, user, permissions)

        contents_json: list[dict[str, object]] | Any = data["contents"]    
        for storage_unit in contents_json:
            if isinstance(storage_unit.get("contents"), str):
                root.add(Parser.__f_from_json(storage_unit, user, root), user)
            else:
                root.add(Parser.__d_from_json(storage_unit, user, root), user)
        
        return root
    
    @staticmethod
    def __d_from_json(json_data: dict[str, object], user: User, parent: Directory | None) -> Directory:
        name: str | Any = json_data["name"]
        permissions_json: dict[str, list[int]] | Any = json_data["permissions"]
        permissions: dict[str, list[Permission]] = { username: [Permission(perm) for perm in perms] for (username, perms) in permissions_json.items() }
        contents: list[StorageUnit] = []

        directory: Directory = Directory(name, contents, parent, user, permissions)

        contents_json: list[dict[str, object]] | Any = json_data["contents"]
        for storage_unit in contents_json:
            if isinstance(storage_unit.get("contents"), str):
                directory.add(Parser.__f_from_json(storage_unit, user, directory), user)
            else:
                directory.add(Parser.__d_from_json(storage_unit, user, directory), user)

        return directory

    @staticmethod
    def __f_from_json(json_data: dict[str, object], user: User, parent: Directory) -> File:
        name: str | Any = json_data["name"]
        permissions_json: dict[str, list[int]] | Any = json_data["permissions"]
        permissions: dict[str, list[Permission]] = { username: [Permission(perm) for perm in perms] for (username, perms) in permissions_json.items() }
        contents: str | Any = json_data["contents"]

        return File(name, contents, parent, user, permissions)
