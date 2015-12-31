import hvac
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Secret(models.Model):
    user = models.ForeignKey(User)

    @property
    def secret(self):
        client = hvac.Client(
            url=os.environ["VAULT_URL"], token=settings.VAULT_TOKEN)
        return client.read("secret/{}".format(self.pk))["data"]["value"]
