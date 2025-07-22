import hashlib
import time
import json
import os

# Represents a single block in the blockchain
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index                # Position in the chain
        self.timestamp = timestamp        # When the block was created
        self.data = data                  # Data (like transaction info)
        self.previous_hash = previous_hash  # Hash of the previous block
        self.hash = self.calculate_hash()   # Current block's hash

    # Hash is calculated based on block content
    def calculate_hash(self):
        content = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(content.encode()).hexdigest()

# Represents the entire blockchain and its operations
class Blockchain:
    def __init__(self, filename="blockchain.json"):
        self.chain = []       # Stores all blocks
        self.file = filename  # File for saving/loading chain
        if os.path.exists(self.file):
            self.load_chain()
        else:
            self.create_genesis_block()

    # Creates the first block in the chain manually
    def create_genesis_block(self):
        print("🪙 Creating genesis block...")
        genesis = Block(0, time.time(), "Genesis Block", "0")
        self.chain.append(genesis)
        self.save_chain()

    # Adds a new block with user-provided data
    def add_block(self, data):
        last_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=data,
            previous_hash=last_block.hash
        )
        self.chain.append(new_block)
        self.save_chain()
        print(f"✅ Block {new_block.index} added.")

    # Saves the blockchain to a JSON file
    def save_chain(self):
        with open(self.file, 'w') as f:
            json.dump([self.block_to_dict(b) for b in self.chain], f, indent=4)

    # Loads the blockchain from a JSON file
    def load_chain(self):
        with open(self.file, 'r') as f:
            chain_data = json.load(f)
            self.chain = []
            for b in chain_data:
                block = Block(
                    b['index'],
                    b['timestamp'],
                    b['data'],
                    b['previous_hash']
                )
                block.hash = b['hash']  # Use stored hash (don't recalculate)
                self.chain.append(block)

    # Converts a Block object to a dictionary (for saving)
    def block_to_dict(self, block):
        return {
            'index': block.index,
            'timestamp': block.timestamp,
            'data': block.data,
            'previous_hash': block.previous_hash,
            'hash': block.hash
        }

    # Prints each block's data in a readable format
    def view_chain(self):
        for block in self.chain:
            print(f"\n🔹 Block {block.index}")
            print(f"Data        : {block.data}")
            print(f"Timestamp   : {block.timestamp}")
            print(f"Hash        : {block.hash}")
            print(f"Prev Hash   : {block.previous_hash}")
            print("-" * 40)

    # Checks if the blockchain is valid and unmodified
    def validate_chain(self):
        print("\n🔍 Validating blockchain...")
        try:
            with open(self.file, 'r') as f:
                chain_data = json.load(f)
        except Exception as e:
            print(f"❌ Failed to load blockchain: {e}")
            return False

        for i, block in enumerate(chain_data):
            # Recalculate the hash from raw fields
            recalculated_hash = hashlib.sha256(
                f"{block['index']}{block['timestamp']}{block['data']}{block['previous_hash']}".encode()
            ).hexdigest()

            # Check if hash matches what's stored
            if block['hash'] != recalculated_hash:
                print(f"❌ Tampering detected at block {block['index']}: Hash mismatch")
                print(f"    Expected: {recalculated_hash}")
                print(f"    Found   : {block['hash']}")
                return False

            # Check if each block points correctly to the previous one
            if i > 0 and block['previous_hash'] != chain_data[i - 1]['hash']:
                print(f"❌ Broken chain at block {block['index']}: Previous hash mismatch")
                print(f"    Expected: {chain_data[i - 1]['hash']}")
                print(f"    Found   : {block['previous_hash']}")
                return False

        print("✅ Blockchain is valid.")
        return True
    
        # Clears the blockchain and recreates the genesis block
    def wipe_chain(self):
        confirm = input("⚠️ Are you sure you want to wipe the entire blockchain? (yes/no): ").strip().lower()
        if confirm == "yes":
            self.chain = []
            self.create_genesis_block()
            print("🧹 Blockchain wiped and reset to genesis block.")
        else:
            print("❎ Wipe cancelled.")


# Text-based menu for interacting with the blockchain
def main():
    bc = Blockchain()

    while True:
        print("\n📘 Simple Blockchain Menu")
        print("1. Add block with data")
        print("2. View entire blockchain")
        print("3. Validate blockchain")
        print("4. Wipe blockchain (reset to genesis block)")
        print("5. Exit")


        choice = input("Choose an option: ")

        if choice == "1":
            data = input("Enter data to store in the block: ")
            bc.add_block(data)
        elif choice == "2":
            bc.view_chain()
        elif choice == "3":
            bc.validate_chain()
        elif choice == "5":
            print("👋 Exiting. Goodbye!")
            break
        elif choice == "4":
            bc.wipe_chain()

        else:
            print("❌ Invalid option. Please choose 1-4.")

if __name__ == "__main__":
    main()
