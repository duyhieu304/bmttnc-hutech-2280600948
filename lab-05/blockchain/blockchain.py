from block import Block
import hashlib
import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # Khởi tạo block đầu tiên (Genesis Block)
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        """Tạo một block mới và thêm vào chuỗi khối."""
        block = Block(len(self.chain) + 1, previous_hash, time.time(), self.current_transactions, proof)
        self.current_transactions = []  # Reset giao dịch hiện tại
        self.chain.append(block)
        return block

    def get_previous_block(self):
        """Trả về block trước đó."""
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        """Thuật toán POW để tìm proof hợp lệ."""
        new_proof = 1
        check_proof = False

        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':  # Điều kiện proof hợp lệ
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def add_transaction(self, sender, receiver, amount):
        """Thêm một giao dịch vào danh sách."""
        self.current_transactions.append({'sender': sender, 'receiver': receiver, 'amount': amount})
        return self.get_previous_block().index + 1  # Trả về index của block sẽ chứa giao dịch này

    def is_chain_valid(self, chain):
        """Xác minh xem blockchain có hợp lệ không."""
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]

            # Kiểm tra liên kết block
            if block.previous_hash != previous_block.hash:
                return False

            # Kiểm tra proof hợp lệ
            previous_proof = previous_block.proof
            proof = block.proof
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            
            if hash_operation[:4] != '0000':  # Proof không hợp lệ
                return False

            previous_block = block
            block_index += 1

        return True

# Kiểm tra hoạt động của blockchain
if __name__ == "__main__":
    blockchain = Blockchain()
    
    print("Genesis Block:")
    print("Hash:", blockchain.chain[0].hash)
    print("Proof:", blockchain.chain[0].proof)

    # Thêm một block mới
    proof = blockchain.proof_of_work(blockchain.get_previous_block().proof)
    new_block = blockchain.create_block(proof, blockchain.get_previous_block().hash)
    
    print("\nBlock mới được thêm:")
    print("Index:", new_block.index)
    print("Hash:", new_block.hash)
    print("Previous Hash:", new_block.previous_hash)
    print("Proof:", new_block.proof)
