import json
from urllib.request import urlretrieve
import os
from multiprocessing import Process
from time import time

def download_files(first, number, location, file_list):
        
    file_paths = [f["path"] for f in  file_list[first:number+first]]
    subdir = f'{process}_{variation}'
    dir_name = f"{location}/{subdir}"
    os.makedirs(dir_name, exist_ok=True)
    for i in range(number):
        if file_paths:
            path = file_paths[i]
        else: continue
        file = f"{dir_name}/{i+first}.root"
        if not os.path.exists(file):
            t = time()
            urlretrieve(path, file)
            t = time()-t
            print(f"{file} has been created ({t:.2f})")
            
        else:
            print(f"{file} already exists")
            
executors = []

with open ('ntuples_merged.json') as f:
    file_info = json.load(f)
for process in file_info:
    if process == 'data': continue
    for variation in file_info[process]:
        file_list = file_info[process][variation]['files']
        size = len(file_info[process][variation]['files'])
#         p1 = Process(target=download_files, args=(256, 257, '/data/ssdext4_agc_data/afalko', file_list,) )
        if size:
            p1 = Process(target=download_files, args=(0, 650, '/data/ssdext4_agc_data_2/afalko', file_list,))
            p1.start();
            executors.append(p1);
for ex in executors:
    ex.join()
    
#ttbar nominal 232
#wjets nominal 253
