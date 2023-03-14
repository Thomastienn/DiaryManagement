import os
import rsa
import ast
from Feature import Feature

class Diary(Feature):
    FUNCS = ["Write", "Read", "Keys", "Find"]

    def __init__(self, dir: str) -> None:
        super().__init__(dir, self.FUNCS)
