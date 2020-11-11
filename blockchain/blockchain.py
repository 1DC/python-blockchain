from blockchain.block import Block
import json
import time

class Blockchain:
    def __init__(self, chain_data: list):
        self.blocks = []
        self.add_chain_data(chain_data)
        
    def add_chain_data(self, chain_data: list):
        """
        Takes a list of blocks, usually ingested from a JSON file, and adds them to the chain.

        Parameters:
        chain_data -- a list of dicts with "data", "previous_hash", "timestamp".
        """

        for chain_item in chain_data:
            block = Block()
            block.data = chain_item["data"]
            block.previous_hash = chain_item["previous_hash"]
            block.timestamp = chain_item["timestamp"]
            self.blocks.append(block)
    
    def add_data(self, data: str) -> bool:
        """
        Adds a new Block to the Blockchain. Returns a bool indicating success or failure.

        Parameters:
        data -- the data (represented as a string) to be stored.
        """

        timestamp = time.time()

        # The previous hash is important since this is what helps us ensure
        # that our Blockchain has not lost its integrity. Each block will
        # keep track of the block before it, using its hash, thus we
        # will know that no block has been tamperered with.
        previous_hash = self.blocks[-1].generate_hash()

        block = Block()
        block.data = data
        block.timestamp = timestamp
        block.previous_hash = previous_hash
        self.blocks.append(block)

        # We validate the entire Blockchain to ensure that
        # the block we just inserted did not break our
        # Blockchain integrity.
        if not self.validate():
            self.blocks.remove(block)
            return False

        return True
    
    def validate(self) -> bool:
        """Returns a bool indicating whether the Blockchain's integrity has been upheld."""

        # Loop through each of the Blocks in the Blockchain,
        # starting at the last block, working our way
        # backwards until we reach the Genesis Block.
        for i in range(len(self.blocks)-1, 0, -1):
            # If we have reached the Genesis block, we do not
            # need to verify further.
            if i == 0: break

            block = self.blocks[i]
            previous_block = self.blocks[i-1]

            # We check integrity by ensuring that the Block's
            # known previous_hash value matches the Block
            # that came before it. If it doesn't, then
            # we know that the Block before it has
            # been tampered with, and that the
            # Blockchain is no longer safe.
            if block.previous_hash != previous_block.generate_hash():
                return False

        return True
    
    def to_json(self) -> str:
        """Returns a JSON string representation of the Blockchain's Blocks."""

        # Convert list of Blocks to list of dicts.
        full_chain = []
        for block in self.blocks:
            full_chain.append(block.__dict__)

        return json.dumps(full_chain, indent=4)
