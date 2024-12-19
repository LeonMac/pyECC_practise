import requests

# Create a new transaction
new_transaction = {
    'sender': 'Alice',
    'recipient': 'Bob',
    'amount': 5,
}

# Send the transaction to the server
response = requests.post('http://localhost:5000/transactions/new', json=new_transaction)
print(response.json())