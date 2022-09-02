import json


class Challenge():
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
        with open(self.chal_file) as file:
            res = json.load(file)[key]
        return res

    @property
    def inputs(self):
        for inp in self._inputs:
            yield inp

    @property
    def outputs(self):
        for out in self._outputs:
            yield out

    @property
    def io(self):
        for inp, out in zip(self.inputs, self.outputs):
            yield inp, out
