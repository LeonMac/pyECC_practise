chain_act_dict={
    'mine':      ['/mine'  ,'GET'],
    'chk_chain': ['/chain' ,'GET'], 
    'node_reg':  ['/nodes/register' ,'POST'],
    'trx_new':   ['/transactions/new' , 'POST'],
    'node_reslv':['/nodes/resolve' , 'GET'],
    
}

IP = '127.0.0.1'
PORT = 5000

act_list = list(chain_act_dict.keys())

def get_path(act_name): 
    return chain_act_dict[act_name][0]

def get_method(act_name): 
    return chain_act_dict[act_name][1]

if __name__ == "__main__":
    for k in act_list:
        print(f"{get_path(k)}, {get_method(k)}")