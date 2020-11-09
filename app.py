from blockchain.blockchain import Blockchain
from blockchain.block import Block
import time
import json
import sys

def write_default_blockchain():
    genesis_block = Block()
    genesis_block.data = "This is the sickest Blockchain implementation ever."
    genesis_block.timestamp = time.time()
    genesis_block.previous_hash = ""
    default = [genesis_block.as_dict()]
    default_raw = json.dumps(default, indent=4)
    with open("chain_data.json", "w") as chain_data_h:
        chain_data_h.write(default_raw)
    return default_raw

def main():
    try:
        with open("chain_data.json", "r") as chain_data_h:
            chain_data_raw = chain_data_h.read()
    except:
        print("Chain data missing or invalid, writing default chain.")
        chain_data_raw = write_default_blockchain()
    
    chain_data = []
    try:
        chain_data = json.loads(chain_data_raw)
    except:
        print("Invalid chain data detected.")
        sys.exit(-1)
    
    chain = Blockchain(chain_data)
    print(f"The blockchain has {len(chain.blocks)} blocks.")
    
    print("Adding crap block...")
    crap_block = Block()
    crap_block.data = "crap"
    crap_block.timestamp = 1337
    crap_block.previous_hash = "abc123"
    chain.blocks.append(crap_block)
    print("Valid?", chain.validate())
    chain.blocks.remove(crap_block)
    print("Removed crap block.")
    
    print("Adding good block...")
    chain.add_data("testing")
    print("Valid?", chain.validate())

    full_chain = []
    for block in chain.blocks:
        full_chain.append(block.as_dict())

    with open("chain_data.json", "w") as chain_data_h:
        chain_data_h.write(json.dumps(full_chain, indent=4))

if __name__ == "__main__":
    main()