"""Module to handle challenges."""

import json


class Challenge():
    """Class representing a challenge.

    Arguments
    ---------
    id : int
        The challenge ID.
    chal_file : str
        The challenge json file.
    name : str
        The challenge name.
    desc : str
        The description of the challenge.
    examples : list(tuple)
        A list of examples for the challenge. Each element of the list is a tuple. The first
        element of the tuple is an example input and the second element is the expected output.
    max_score : int
        The maximum that can be obtained by solving this challenge.
    difficulty : str ["easy", "medium", "hard"]
        The difficulty of the challenge. There is 3 levels of difficulty : easy, medium and hard.
    _inputs : list
        The list of inputs used to test the challenge solution.
    _outputs : list
        The list of outputs used to test the challenge solution.

    Methods
    -------
    _read_chal_json(id, chal_folder)
        Read the challenge informations from its json file.
    inputs()
        Yield the challenge inputs.
    outputs()
        Yield the challenge outputs.
    io()
        Yield the challenge inputs/outputs.
    """

    def __init__(self, id, chal_folder) -> None:
        self.id = id
        self.chal_file = chal_folder+str(self.id)+".json"
        self.name = self._read_chal_json("name")
        self.desc = self._read_chal_json("desc")
        self._inputs = self._read_chal_json("inputs")
        self._outputs = self._read_chal_json("outputs")
        self.examples = list(zip(self._read_chal_json("ex_inputs"),
                                 self._read_chal_json("ex_outputs")))
        self.max_score = len(self._inputs)
        self.difficulty = self._read_chal_json("difficulty")

    def _read_chal_json(self, key):
        """Return challenge inforomations from its json file.

        Parameters
        ----------
        key : str
            The key in the json file.

        Returns
        -------
        str
            The infomration in the json challenge file with the given key.
        """
        with open(self.chal_file, "r", encoding="utf8") as file:
            res = json.load(file)[key]
        return res

    @property
    def inputs(self):
        """Generator for challenge inputs.

        Yields
        ------
        str | int
            The challenges inputs.
        """
        for inp in self._inputs:
            yield inp

    @property
    def outputs(self):
        """Generator for challenge outputs.

        Yields
        ------
        str | int
            The challenges outputs.
        """
        for out in self._outputs:
            yield out

    @property
    def io(self):
        """Generator for challenge inputs/outputs.

        Yields
        ------
        str | int, str | int
            The challenges inputs and outputs.
        """
        for inp, out in zip(self.inputs, self.outputs):
            yield inp, out
