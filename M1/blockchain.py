import datetime
import json
import hashlib
from urllib import response
from flask import Flask, jsonify

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(nonce = 1, previous_hash = '0')
        
    def create_block(self, nonce, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'nonce': nonce,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_nonce):
        new_nonce = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_nonce += 1
        return new_nonce
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        current_block_index = 1
        while current_block_index < len(chain):
            current_block = chain[current_block_index]
            if current_block['previous_hash'] != self.hash(previous_block):
                return False
            
            previous_nonce = previous_block['nonce']
            current_nonce = current_block['nonce']
            hash_operation = hashlib.sha256(str(current_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = current_block
            current_block_index += 1
        return True
        
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

blockchain = Blockchain()

@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'length': len(blockchain.chain),
        'chain': blockchain.chain
    }
    return jsonify(response), 200

@app.route('/mine_block', methods=['POST'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_nonce = previous_block['nonce']
    previous_hash = blockchain.hash(previous_block)

    current_nonce = blockchain.proof_of_work(previous_nonce)
    current_block = blockchain.create_block(current_nonce, previous_hash)
    response = {
        'message': 'New block mined successfully',
        'block': current_block
    }
    return jsonify(response), 200

@app.route('/is_valid', methods=['GET'])
def is_chain_valid():
    response = {
        'is_chain_valid': 'true' if blockchain.is_chain_valid(blockchain.chain) else 'false'
    }
    return jsonify(response), 200

app.run(host = '0.0.0.0', port = 5000)



        