from blockchain.block import Block
import time

class Blockchain:
    def __init__(self, chain_data: dict):
        self.blocks = []
        for chain_item in chain_data:
            block = Block()
            block.data = chain_item["data"]
            block.previous_hash = chain_item["previous_hash"]
            block.timestamp = chain_item["timestamp"]
            self.blocks.append(block)
    
    def add_data(self, data: str) -> Block:
        timestamp = time.time()
        previous_hash = self.blocks[-1].generate_hash()
        block = Block()
        block.data = data
        block.timestamp = timestamp
        block.previous_hash = previous_hash
        self.blocks.append(block)
        if not self.validate():
            self.blocks.remove(block)
            return None
        return block
    
    def validate(self) -> bool:
        for i in range(len(self.blocks)-1, 0, -1):
            if i == 0:
                break
            block = self.blocks[i]
            previous_block = self.blocks[i-1]
            if block.previous_hash != previous_block.generate_hash():
                return False
        return True
