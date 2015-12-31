import os
import requests
import subprocess
import sys
import time
import unittest


class DockerComposeTestCase(unittest.TestCase):
    compose_file = None
    show_docker_compose_output = False

    def setUp(self):
        compose_file = os.path.join(
            os.path.dirname(__file__), "compose",
            "{}.yml".format(self.compose_file))
        popen_kwargs = {}
        if not self.show_docker_compose_output:
            popen_kwargs = {
                "stdout": subprocess.PIPE,
                "stderr": subprocess.PIPE,
            }
        proc = subprocess.Popen(
            ["docker-compose", "-f", compose_file, "up"], **popen_kwargs)

        def cleanup():
            proc.kill()
            subprocess.call(
                ["docker-compose", "-f", compose_file, "kill"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.call(
                ["docker-compose", "-f", compose_file, "rm", "-f"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.addCleanup(cleanup)

    def get_docker_host(self):
        if not hasattr(self, "_docker_host"):
            if "linux" in sys.platform:
                docker_host = "localhost"
            else:
                docker_host = subprocess.check_output(
                    ["docker-machine", "ip", "dev"]).strip().decode(
                    "unicode_escape")
            self._docker_host = docker_host
        return self._docker_host

    def curl_until_success(self, port, endpoint="/", params={}):
        for i in range(10):
            try:
                response = requests.get("http://{}:{}{}".format(
                    self.get_docker_host(), port, endpoint), params=params)
            except requests.exceptions.ConnectionError:
                pass
            else:
                return response
            time.sleep(1)
        else:
            raise Exception("service didn't start in time")


class AppTestCase(DockerComposeTestCase):
    def setUp(self):
        super(AppTestCase, self).setUp()

        self._tokens = {}
        self.curl_until_success(8000)

    def make_request(self, command, path, data={}, params={}, user="test1"):
        auth = requests.auth.HTTPBasicAuth(user, "password12")

        if path.startswith("http://"):
            url = path
        else:
            url = "http://{}:8000/".format(self.get_docker_host())
            if path:
                url += path + "/"

        return getattr(requests, command)(
            url, auth=auth, data=data, params=params)
