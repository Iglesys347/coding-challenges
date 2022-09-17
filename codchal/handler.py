"""Handler for user solution."""

import os
import re
import uuid

from codchal.errors import LanguageError, SolutionFormatError
from codchal.settings import FILE_EXT, DEFAULT_DIR, KNOWN_LANG


class SolHandler():
    """Class for handling of user solution.

    Attributes
    ----------
    raw_sol : str
        The raw user's solution.
    filename : str
        A randomly generated file name.
    script_filename : str
        The full path filename of the user's script.
    lang : str
        The language of the user's script (only python is supported for the moment).

    Methods
    -------
    _parse_sol()
        Parse the user raw solution and creates a file containing its script.
    __del__()
        When called, the destructor delete the file created by _parse_sol method.
    """

    def __init__(self, raw_sol) -> None:
        self.raw_sol = raw_sol
        self.filename = str(uuid.uuid4())
        self.script_filename, self.lang = self._parse_sol()

    def _parse_sol(self):
        """Parse the user raw solution and creates a file containing its script.

        Returns
        -------
        str, str
            Returns the full script filepath and the script language.
        """
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

        file_ext = [key for key, value in FILE_EXT.items() if value == lang][0]
        full_filename = self.filename+"."+file_ext
        with open(DEFAULT_DIR+full_filename, "w", encoding="utf8") as file:
            file.write(script)
        return full_filename, lang

    def __del__(self):
        """When called, the destructor delete the file created by _parse_sol method."""
        # deleting the created script when destructor called
        try:
            os.remove(DEFAULT_DIR+self.script_filename)
        except AttributeError:
            pass
