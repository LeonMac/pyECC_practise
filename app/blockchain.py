# https://bimoputro.medium.com/build-your-own-blockchain-in-python-a-practical-guide-f9620327ed03

import hashlib
import json
from time import time
import requests

class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Create the genesis block

        self.new_block(previous_hash=1, proof=100)

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
    def valid_proof(last_proof, proof, difficulty):
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