from blockchain.blockchain import Blockchain
from blockchain.block import Block
import time
import json
import sys

def save_chain(chain: Blockchain, location: str = "chain_data.json") -> bool:
    """
    Returns a bool indicating whether or not the data was saved.
    
    Parameters:
    chain       -- the Blockchain to write to the file.
    location    -- the path to the file in which the data will be written.
    """

    try:
        with open(location, "w") as chain_data_h:
            chain_data_h.write(chain.to_json())
            return True
    except:
        return False

def write_default_blockchain() -> str:
    """Returns the string representation of the default Blockchain data."""

    genesis_block = Block()
    genesis_block.data = "This is the sickest Blockchain implementation ever."
    genesis_block.timestamp = time.time()
    genesis_block.previous_hash = ""

    # Create a temporary chain which we can convert to JSON.
    default_chain = Blockchain([])
    default_chain.blocks.append(genesis_block)
    save_chain(default_chain)
    
    return default_chain.to_json()

def main():
    """Example use of the Blockchain, with the ability to read and write to a file."""

    try:
        with open("chain_data.json", "r") as chain_data_h:
            chain_data_raw = chain_data_h.read()
    except:
        print("Chain data missing or invalid, writing default chain.")
        chain_data_raw = write_default_blockchain()
    
    chain_data = []
    try:
        # Convert the file contents (JSON) to a list of Blocks represented as dicts.
        chain_data = json.loads(chain_data_raw)
    except:
        print("Invalid chain data detected.")
        sys.exit(-1)
    
    # Initialise the Blockchain with the imported data.
    chain = Blockchain(chain_data)
    print(f"The blockchain has {len(chain.blocks)} blocks.")
    print(f"Hash of genesis block is {chain.blocks[0].generate_hash()}")
    print("Valid?", chain.validate())

    # If you're tinkering... here you could try adding or removing Blocks.
    # You may wish to use chain.add_data(data: str), or even add a
    # malicious block using the chain.blocks list directly.

    # In case of any modifications, write the chain to a file again.
    save_chain(chain)

if __name__ == "__main__":
    main()