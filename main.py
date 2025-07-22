import hashlib
import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.ctime(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), time.ctime(), data, previous_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def display_chain(self):
        for block in self.chain:
            print(f"\nBlock {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Data: {block.data}")
            print(f"Hash: {block.hash}")
            print(f"Previous Hash: {block.previous_hash}")


#User Interaction CLI
if __name__ == "__main__":
    bc = Blockchain()

    while True:
        print("\n===== Simple Blockchain Menu =====")
        print("1. Add a new block")
        print("2. Display blockchain")
        print("3. Validate blockchain")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            data = input("Enter transaction data: ")
            bc.add_block(data)
            print("Block added successfully.")
        elif choice == '2':
            bc.display_chain()
        elif choice == '3':
            print("Blockchain is valid." if bc.is_chain_valid() else "Blockchain is invalid!")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")
