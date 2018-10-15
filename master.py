from requests import get, exceptions,post
import os
from random import randint

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
    #One keeps track of total files, the other where are the files
    files, node_files = {} , {}
    for node in nodes:
        files_list = get(f'http://{node}/get_files').text.split('\n')
        for e in files_list:
            if e not in files:
                files[e] = 1
            else:
                files[e] += 1

            if e not in node_files:
                node_files[e] = [node]
            else:
                node_files[e].append(node)

    return files,node_files

def print_files(files):
    print('-------------------')
    print('File \ availability')
    print('-------------------')
    for k,v in files.items():
        print(k,v)

def print_opt_files(files):
    print('-------------------')
    print('Choose a file')
    print('-------------------')
    for k,i in zip(files.keys(),range(1,len(files)+1)):
        print(f'{i}) {k}')

def clr():
    if os.name=='posix':
        os.system('clear')
    else:
        os.system('cls')

if __name__ == '__main__': 
    slaves = [
    '127.0.0.1',
    '127.0.0.2',
    '127.0.0.3',
    ]
    ### Menu ###
    while True:
        clr()
        a = get_available(slaves)
        if len(a) == 0:
            clr()
            print("No nodes available\n[Press enter to retry]")
            input()
            continue
        f,node_files = get_files(a)
        print('-------')
        print("Menu")
        print('1) List files')
        print('2) Retrieve file')
        print('3) Send file')
        opt = input('')
        if opt not in ('123'):
            clr()
            print('Invalid opt [Press enter]');input()
        else:
            if opt == '1':
                clr()
                if len(f) == 0:
                    print("No nodes or files available")
                else:
                    print_files(f)
                input('[Press enter to continue]')
            if opt == '2':
                clr()
                print_opt_files(f)
                opt = input('Choose a file by number: ')
                
                try: 
                    opt = int(opt)
                    if (opt-1) not in range(len(f)):
                        raise Exception()
                    file_name = list(f.keys())[opt-1]    
                except:
                    clr()
                    input('Invalid file number\n[Press enter to continue]')
                    continue

                
                random_node = node_files[file_name][randint(0,len(a)-1)]
                #http://127.0.0.3/get_file?file_name=README.md
                file = get(f'http://{random_node}/get_file?file_name={file_name}').text
                clr()
                print("Head of file: ")
                print('\n'.join(file.split('\n')[:5]))
                print('\n\n')
                print(file_name)
                s_opt = input("Save?[Y/N] ").lower()
        
                if s_opt == 'y':
                    with open(file_name,'w+') as out:
                        out.write(file)
                

            if opt == '3':
                clr()
                print("------------------------------------")
                print("Select a file to send to other nodes")
                print("------------------------------------")
                files = '\n'.join(os.listdir())
                for f,i in zip(files.split('\n'), range(1,len(files)+1)):
                    print(f'{i}) {f}')
                opt = input("Select a file by number: ")
                try:
                    opt = int(opt)
                    if opt not in range(1,len(files)+1):
                        raise Exception()
                except:
                    print('Invalid file option\n[Press enter to continue]')
                    input()
                    continue

                with open(files.split('\n')[opt-1]) as file:
                    data = {'text': file.read(),
                            'file_name':files.split('\n')[opt-1]}
                    for node in a:
                        post(f'http://{node}/create_file',json=data)
                
                    
                input()