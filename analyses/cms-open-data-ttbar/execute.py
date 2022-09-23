import os

for i_run in range(3):
    
    for app in ['coffea','rdf']:
        
        if app == 'rdf':
                options = ['O3']
        else: options = [app]
        for option in options:
            for nfiles in range(50, 650, 50):# + list(range(250, 3751, 700)):
#                 print(nfiles)
    #             for nfiles in [3750]:
                folder = f'benchmarks/{nfiles}/{option}'
                os.makedirs(folder, exist_ok=True)  
    #            for ncores in [16,32+16,64+16,96+16]:
                for ncores in [64]:#list(range(8,65,8)) + [96,128]:#[1]+list(range(32,129,32))+list(range(8, 32, 8)):
                    
                    file = f'{ncores}'
                    file = f'{folder}/{file}'
#                     com = f'mv {file}_mv {file}/0'
                    os.makedirs(file, exist_ok=True)
                    
                    i = i_run
                    while (os.path.exists(f'{file}/{i}')): i+=1
                    file = f'{file}/{i}'
                    com = f'touch {file}'    
                    os.system(com)
                    print(com)
                    
                    com = f'/usr/bin/time python {app}_ttbar.py --ncores {ncores} --nfiles {nfiles} > {file} 2>&1'
                    print(com, option)
                    com = f'env EXTRA_CLING_ARGS=-{option} {com}' if app == 'rdf' else 'f () { while true; do grep MemAvailable /proc/meminfo | awk \'{ print $2 }\'; sleep 0.05; done }\nf > log.txt &\nLOGGER_PID=$!\nsleep 0.1\n' + com + '\nsleep 0.1\nkill $LOGGER_PID\nawk \'BEGIN { min = 1e12; max = 0; } { if ($1 > max) max = $1; if ($1 < min) min = $1; } END {print((max - min),"kB") }\' log.txt ' + f'> {file}.rss'
                    
                        
                    os.system(com)

