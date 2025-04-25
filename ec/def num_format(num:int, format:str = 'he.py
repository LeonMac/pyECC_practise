def num_format(num:int, format:str = 'hex'):
    if format == 'hex':
        return hex( num )
    else:
        return num 