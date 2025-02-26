import timeit
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import hashlib
import nacl.encoding
import nacl.signing


class Doctor:
    def __init__(self, name):
        self.name = name
        self.address = self.get_address(name)
        self.authorization = None

    def get_address(self, name):
        key = hashlib.sha256()
        key.update(name.encode('utf-8'))
        return key.hexdigest()


class Patient:
    def __init__(self, name):
        self.name = name
        self.address = self.get_address(name)
        self.illnesses = []
        self.private_key, self.public_key = self.generate_keys()

    def get_address(self, name):
        key = hashlib.sha256()
        key.update(name.encode('utf-8'))
        return key.hexdigest()

    def generate_keys(self):
        """
        Generates a private and the related public key
        Returns
        -------
        The private and the public key
        """
        # Generate keys
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        return private_key, public_key

    def refresh_keys(self):
        """
        Refresh temporary keys of the patient.
        Parameters
        ----------
        patient : an object Patient
        """
        self.private_key, self.public_key = self.generate_keys()
        print("Temporary keys have been refreshed. Old keys have been destroyed and will not work.")


class Minister:
    def __init__(self, incompatibilities):
        self.name = 'Minister of Health'
        self.address = self.get_address(self.name)
        self.minister_key = nacl.signing.SigningKey.generate()
        public_key = self.minister_key.verify_key
        self.public_key = public_key.encode(encoder=nacl.encoding.HexEncoder)
        self.incompatibilities = incompatibilities

    def get_address(self, name):
        key = hashlib.sha256()
        key.update(name.encode('utf-8'))
        return key.hexdigest()

    def generate_authorization(self, doctor):
        """
        Generates an authorization for a specified Doctor signing the doctor's address
        with the private key of the Minister
        Parameters
        ----------
        doctor

        Returns
        -------
        The address signed
        """
        assert isinstance(doctor, Doctor)
        signed = self.minister_key.sign(bytes(doctor.address, 'utf-8'))
        return signed


class Miner:
    def __init__(self, Health_block):
        self.wallet = 0
        self.chain = Health_block.chain
        self.blockchain = Health_block

    def mine_block(self):
        """
        Performs the proof of work and computes the time to do that
        Returns
        -------
        The nounce and the related time to find it
        """
        start = timeit.timeit()
        last_block = self.blockchain.last_block
        last_proof = last_block['nounce']
        nounce = self.blockchain.proof_of_work(last_proof)
        end = timeit.timeit()
        total_time = end - start
        return nounce, total_time
