import pprint

from loguru import logger

from game.operating_system.scripting.scanner.scanner import Scanner
from game.operating_system.scripting.parser.parser import Parser
from game.operating_system.scripting.parser.ast.visitor import AstPrinter
from game.operating_system.scripting.exceptions import ScriptError


class Love(object):
    def run_script_file(self, path: str) -> None:
        """
        This is here for purely debug purposes
        """
        with open(path, 'r') as f:
            script: str = f.read()
        self.run_script(script)

    def run_script(self, script: str) -> None:
        try:
            scanner = Scanner(script)
            tokens = scanner.scan_tokens()
            pprint.pprint(tokens)
            parser = Parser(tokens)
            AstPrinter().print(parser.parse())
        except ScriptError as e:
            logger.error(e)

    def shell(self) -> None:
        """
        This is only here for debug purposes (for now)
        """
        while True:
            line: str = input('> ')
            if line == 'quit': break
            self.run_script(line)
