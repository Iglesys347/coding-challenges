"""Checker module contains function to check the user's solution."""

import os
import docker
from docker.errors import ImageNotFound

from codchal.settings import DEFAULT_DIR


def check_script(script_name, challenge):
    """Run script with the challenges inputs and compare the script outputs with the expected
    challenges outputs.

    Parameters
    ----------
    script_name : str
        The name of the script to check.
    challenge : Challenge
        The challenge that the script should solve.

    Returns
    -------
    int
        The score of the script for the challenge. 0 =< score =< challenge.max_score.
    """
    score = 0
    client = docker.APIClient()

    # checking that python:3 docker image exists
    try:
        client.inspect_image("python:3")
    except ImageNotFound:
        # pulling the image
        print("Image not found, pulling it...")
        client.pull("python:3")

    for inp, out in challenge.io:

        container = client.create_container(
            'python:3', f'python {script_name}', stop_timeout=10,
            stdin_open=True, volumes=['/tmp'], working_dir='/tmp/',
            host_config=client.create_host_config(binds={
                os.path.join(os.getcwd(), DEFAULT_DIR): {
                    'bind': '/tmp/',
                    'mode': 'rw',
                }
            })
        )

        sock = client.attach_socket(
            container, params={"stdin": 1, "stdout": 1, "stderr": 1, "stream": 1})
        client.start(container)
        sock._sock.send(inp.encode('utf8'))
        sock._sock.close()
        sock.close()
        try:
            status = client.wait(container, timeout=20)
            # status_code = status["StatusCode"]
        except:
            client.kill(container)
            # status_code = 137  # sigkill status code
        stdout = client.logs(container, stderr=False).decode()
        if stdout.endswith("\n"):
            stdout = stdout[:-1]
        # stderr = client.logs(container, stdout=False).decode()

        client.remove_container(container)

        # print('Exit: {}'.format(status_code))
        # print('log stdout: {}'.format(stdout))
        # print('log stderr: {}'.format(stderr))
        if out == stdout:
            score += 1

    return score
