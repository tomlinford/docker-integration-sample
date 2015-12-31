ps ax
netstat -tulpn
vault server -dev -config /vault/config.hcl &
sleep 0.5
VAULT_ADDR='http://127.0.0.1:8200' vault token-create -id token
while true; do sleep 10000; done
