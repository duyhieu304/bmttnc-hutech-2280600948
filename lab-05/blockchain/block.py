import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, proof):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = (str(self.index) + 
                str(self.previous_hash) + 
                str(self.timestamp) + 
                str(self.transactions) + 
                str(self.proof))
        return hashlib.sha256(data.encode()).hexdigest()

# Kiểm tra khởi tạo một block
if __name__ == "__main__":
    # Khởi tạo một block giả lập
    genesis_block = Block(0, "0", int(time.time()), ["Genesis Block"], 100)
    
    print("Block #0 (Genesis Block):")
    print("Hash:", genesis_block.hash)
    print("Previous Hash:", genesis_block.previous_hash)
    print("Timestamp:", genesis_block.timestamp)
    print("Transactions:", genesis_block.transactions)
    print("Proof:", genesis_block.proof)
