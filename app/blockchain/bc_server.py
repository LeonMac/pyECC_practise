# https://bimoputro.medium.com/build-your-own-blockchain-in-python-a-practical-guide-f9620327ed03

import hashlib
import json
from time import time
from bc_cfg import IP, PORT, POW_MINING_FEE, get_path, get_method

import requests
from flask import Flask, request, jsonify
import uuid

class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)
    
    def register_node(self, node):
        # print(f'tbd node : {node}')
        # print(self.nodes)
        self.nodes.add(node)
        pass

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
        'index': len(self.chain) + 1,
        'timestamp': time(),
        'transactions': self.current_transactions,
        'proof': proof,
        'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block


    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block

        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
        'sender': sender,
        'recipient': recipient,
        'amount': amount,
        })

        return self.last_block['index'] + 1
    
    # @staticmethod 是一个内置的装饰器，用于将一个方法声明为静态方法,
    # hash 方法被声明为静态方法，这意味着它可以在没有创建类实例的情况下被调用，并且它不会访问或修改类的状态。
    # 因此可以直接通过类名来调用它。而不需要创建一个对象实例来使用hash.

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block: Block
        """
        # sort_keys=True 是传递给 dumps 函数的一个参数，意味着在转换过程中，字典的键将会被排序。
        # 这样做可以确保相同的对象每次被转换时，都会生成相同的JSON字符串，因而生成一致的哈希值。
        block_string = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

    # @property 是一个装饰器，用于将一个方法转换为属性。
    # 当您尝试访问 blockchain.last_block 时，实际上是在调用 last_block 方法，而不是直接访问一个属性。
    # 这种用法通常用于实现延迟计算的属性或者需要在获取值之前进行额外处理的属性。
    # last_block = blockchain.last_block  # 直接通过属性访问--这种方式更加自然，因为而不需要显式地调用一个方法。
    @property
    def last_block(self):
        """
        Returns the last Block in the chain
        """
        return self.chain[-1]
    
    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
        - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
        - p is the previous proof, and p' is the new proof

        :param last_proof: <int>
        :return: <int>
        """
        proof = 0
        # 持续增加proof,试图找到一个hash值为四个0开头的值
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof
    
    @staticmethod
    def valid_proof(last_proof, proof, difficulty:int =4):
        """
        Validates the Proof

        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param difficulty: <int> difficulty leading zero number
        :return: <bool> True if correct, False if not.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:difficulty] == "0" * difficulty

    def valid_chain(self, chain, difficulty=4):
        """
        Determine if a given blockchain is valid

        :param chain: <list> A blockchain
        :param difficulty: <int> difficulty leading zero number, adjust PoW diffcilty
        :return: <bool> True if valid, False if not
        """
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], difficulty):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.

        :return: <bool> True if our chain was replaced, False if not
        """
        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

# start a Flask server
app = Flask(__name__)

# Generate a globally unique address for this server node
node_identifier = str(uuid.uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route(get_path('mine'), methods=[get_method('mine')])
def mine(worker_id:str ='0'):
    '''A route to mine a new block.'''
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    print(f"miner {worker_id} find the proof after {proof} hashes")
    blockchain.new_transaction(
        sender = worker_id,
        recipient = node_identifier,
        amount = POW_MINING_FEE,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route(get_path('trx_new'), methods=[get_method('trx_new')])
def new_transaction():
    '''A route to create a new transaction.'''
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route(get_path('chk_chain'), methods=[get_method('chk_chain')])
def full_chain():
    '''A route to return the full blockchain.'''
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route(get_path('node_reg'), methods=[get_method('node_reg')])
def register_nodes():
    '''A route allows nodes to register with the server and add them 
    to the list of nodes in the network'''
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

@app.route(get_path('node_reslv'), methods=[get_method('node_reslv')])
def consensus():
    '''route implements the consensus algorithm and resolves any conflicts 
    by replacing the current chain with the longest valid chain in the network.'''
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200    


if __name__ == '__main__':
    app.run(host=IP, port=PORT)