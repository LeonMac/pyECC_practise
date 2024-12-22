import requests
import sys
from bc_cfg import act_list, get_path, get_method

def usage_msg(run_name:str):
    print(f"usage: python {run_name} {' | '.join(act_list)}")

if __name__ == "__main__":

    if len(sys.argv) != 2:
        usage_msg(sys.argv[0])
        print(f"accept 2 arguments. you input {len(sys.argv)} args!")
        sys.exit(1)
    
    if sys.argv[1] not in act_list:
        usage_msg(sys.argv[0])
        print(f"your input argument {sys.argv[1] } is not recognized!")
        sys.exit(1)
    
    method  = get_method(sys.argv[1])
    arg_url = get_path(sys.argv[1])
    
      
    if sys.argv[1] == 'trx_new':            # Create a new transaction
        json_body = {
            'sender': 'Alice',
            'recipient': 'Bob',
            'amount': 5,
        }

    elif sys.argv[1] == 'mine':

        pass
    elif sys.argv[1] == 'chk_chain':        # check chain status

        json_body = ''
    else:

        pass
            


    url = 'http://localhost:5000' + arg_url

# Send the transaction to the server
if method == 'POST':
    response = requests.post(url, json=json_body)
elif method == 'GET':
    response = requests.get(url, json=json_body)

print(response.json())