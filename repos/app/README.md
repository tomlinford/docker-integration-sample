# Sample app
This is just a basic django rest framework app used for storing secrets. One
can POST to `/secrets/` to create a new secret and access it later with GET
`/secrets/{id}/`. The text for the secret is encrypted and stored in vault (by
hashicorp).

90% of the written source code exists in `app/urls.py`, and the `Secret` model
is in `secret/models.py`.
