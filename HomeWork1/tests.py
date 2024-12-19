import os
import tarfile
import unittest
from unittest.mock import patch
from HomeWork1 import ShallEmulator

class TestEmulator(unittest.TestCase):
    def setUp(self):
        self.emulator = ShallEmulator()
