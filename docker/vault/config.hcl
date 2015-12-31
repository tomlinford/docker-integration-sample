backend "inmem" {}

listener "tcp" {
    address = "0.0.0.0:8201"
    tls_disable = 1
}
