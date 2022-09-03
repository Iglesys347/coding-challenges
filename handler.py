"""Handler for user solution."""

import os
import re
import uuid

from errors import LanguageError, SolutionFormatError
from settings import FILE_EXT, DEFAULT_DIR, KNOWN_LANG


class SolHandler():
    def __init__(self, raw_sol) -> None:
        self.raw_sol = raw_sol
        self.filename = str(uuid.uuid4())
        self.script_filename, self.lang = self._parse_sol()

    def _parse_sol(self):
        if not self.raw_sol.startswith("```") or not self.raw_sol.endswith("```"):
            raise SolutionFormatError(
                "The solution should begin with ```<language> and end with ```")
        result = re.search('```(.*)```', self.raw_sol, re.DOTALL).group(1)
        # the first line should be the language
        lang = result.split("\n")[0]
        if lang == "":
            raise SolutionFormatError(
                "The solution should begin with ```<language> and end with ```")
        if lang not in KNOWN_LANG:
            raise LanguageError("Unknown language.")
        script = "\n".join(result.split("\n")[1:])

        # generating random filename
        file_ext = [key for key, value in FILE_EXT.items() if value == lang][0]
        full_filename = self.filename+"."+file_ext
        with open(DEFAULT_DIR+full_filename, "w", encoding="utf8") as file:
            file.write(script)
        return full_filename, lang

    def __del__(self):
        # deleting the created script when destructor called
        try:
            os.remove(DEFAULT_DIR+self.script_filename)
        except AttributeError:
            pass


if __name__ == "__main__":
    res = SolHandler(
        """```python
for in in range(10):
    print(i)
``""")
    print(res.script_filename)
    input()
