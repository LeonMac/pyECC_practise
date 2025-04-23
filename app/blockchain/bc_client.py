import requests
import sys
from bc_cfg import IP, PORT, act_list, get_path, get_method

def usage_msg(run_name:str):
    print(f"usage: python {run_name} {' | '.join(act_list)} value")

if __name__ == "__main__":

    if len(sys.argv) != 3:
        usage_msg(sys.argv[0])
        print(f"accept 3 arguments. you input {len(sys.argv)} args!")
        sys.exit(1)
    
    if sys.argv[1] not in act_list:
        usage_msg(sys.argv[0])
        print(f"your input argument {sys.argv[1] } is not recognized!")
        sys.exit(1)
    
    value = sys.argv[2]
      
    if sys.argv[1] == 'trx_new':            # Create a new transaction
        json_body = {
            'sender': 'Alice',
            'recipient': 'Bob',
            'amount': value,
        }

    elif sys.argv[1] == 'mine':             # mine a new block
        json_body = ''

    elif sys.argv[1] == 'chk_chain':        # return the full chain

        json_body = ''

    elif sys.argv[1] == 'node_reg':         # node register with the server
        json_body = {
            'nodes': str(value),
        }
    else:

        pass

    method  = get_method(sys.argv[1])
    arg_url = get_path(sys.argv[1])
            
    # url = 'http://localhost:5000' + arg_url
    url = 'http://'+ IP + ':' + str(PORT) + arg_url

# Send the transaction to the server
if method == 'POST':
    response = requests.post(url, json=json_body)
elif method == 'GET':
    response = requests.get(url, json=json_body)

print(response.json())