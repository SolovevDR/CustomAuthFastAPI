from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_rsa_keypair(key_size=2048):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def save_keys(
    private_key: rsa.RSAPrivateKey,
    public_key: rsa.RSAPublicKey,
    private_filename: str,
    public_filename: str
):
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open(private_filename, "wb") as f:
        f.write(private_pem)

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(public_filename, "wb") as f:
        f.write(public_pem)


if __name__ == "__main__":
    private_key, public_key = generate_rsa_keypair()
    save_keys(
        private_key=private_key,
        public_key=public_key,
        private_filename="./src/private.pem",
        public_filename="./src/public.pem"
    )
