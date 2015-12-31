from .base_test_case import AppTestCase


class TestVault(AppTestCase):
    compose_file = "vault"

    def test(self):
        secrets = self.make_request("get", "secrets").json()
        self.assertEqual(secrets, [])

        secret = self.make_request("post", "secrets", data={
            "secret": "foo",
        }).json()
        self.assertEqual(secret["secret"], "foo")

        secret = self.make_request("get", secret["url"]).json()
        self.assertEqual(secret["secret"], "foo")

        self.make_request("delete", secret["url"])
        response = self.make_request("get", secret["url"])
        self.assertEqual(response.status_code, 404)


class TestVaultDown(AppTestCase):
    compose_file = "vault_down"

    def test(self):
        # If vault is down, then a POST to /secrets/ should 500 and no secret
        # should be created.
        response = self.make_request("post", "secrets", data={"secret": "foo"})
        self.assertEqual(response.status_code, 500)

        secrets = self.make_request("get", "secrets").json()
        self.assertEqual(secrets, [])
