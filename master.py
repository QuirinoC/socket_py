from requests import get, exceptions

def get_available(slaves):
    available = []
    for slave in slaves:
        try:
            get(f'http://{slave}',timeout=0.5)
            print(f'Connected to: {slave}')
            available.append(slave)
        except (exceptions.ConnectionError):
            
            print(f'Offline node: {slave}')

    return available

def get_files(nodes):
    files = {}
    for node in nodes:
        files_list = get(f'http://{node}/get_files').text.split('\n')
        for e in files_list:
            if e not in files:
                files[e] = 1
            else:
                files[e] += 1
    return files

def print_files(files):
    print('-------------------')
    print('File \ availability')
    print('-------------------')
    for k,v in files.items():
        print(k,v)


if __name__ == '__main__': 
    slaves = [
    '127.0.0.1',
    '127.0.0.2',
    '127.0.0.3',
    ]
    a = get_available(slaves)
    f = get_files(a)
    print_files(f)
