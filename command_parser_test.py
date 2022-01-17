import unittest
from command_parser import Command_Parser

class CommandParserTest(unittest.TestCase):

    def setUp(self) -> None:
        self._parser = Command_Parser()