python manage.py migrate
cat /mnt/init_data.py | python manage.py shell
export VAULT_URL="http://$VAULT_PORT_8201_TCP_ADDR:$VAULT_PORT_8201_TCP_PORT"
python manage.py runserver 0.0.0.0:8000
