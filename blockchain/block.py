import hashlib
import json

class Block:
    def __init__(self):
        self.data = ""
        self.previous_hash = ""
        self.timestamp = None
        self.nonce = ""

    def generate_hash(self) -> str:
        sha256 = hashlib.sha256()
        this_block = self.data + self.previous_hash + str(self.timestamp) + str(self.nonce)
        sha256.update(this_block.encode())
        return sha256.hexdigest()
    
    def as_dict(self) -> dict:
        return {
            "data": self.data,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
