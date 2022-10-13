#!/usr/bin/env python
# coding: utf-8



import argparse


# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("--ncores", type=int)
parser.add_argument("--nfiles", type=int)
parser.add_argument("--startwith", type=int, help='number of first file')

# Read arguments from command line
args = parser.parse_args()


import ROOT
from ROOT import RDataFrame, TCanvas, THStack
ROOT.EnableImplicitMT(args.ncores or 128)
# get_ipython().run_line_magic('jsroot', 'on')
print(f'The num of threads = {ROOT.GetThreadPoolSize()}')
# verbosity = ROOT.Experimental.RLogScopedVerbosity(ROOT.Detail.RDF.RDFLogChannel(), ROOT.Experimental.ELogLevel.kInfo)
import os
print(os.environ['EXTRA_CLING_ARGS'])

# In[2]:


ROOT.gSystem.CompileMacro("helper/helper.cpp", "kO")


# In[3]:


N_FILES_MAX_PER_SAMPLE = args.nfiles or 1
FILE = f'rdf-{N_FILES_MAX_PER_SAMPLE}.root'
START = args.startwith or 0

disk = '/mnt/e/analysis-grand-challenge/datasets/cms-open-data-2015-download'




print(f'you are processing {N_FILES_MAX_PER_SAMPLE} files starting from {START}')



# In[16]:

from TtbarAnalysis import TtbarAnalysis          
                
                    



print(f'processing data located at {disk} disk')
analysisManager = TtbarAnalysis(disk=disk, n_files_max_per_sample=N_FILES_MAX_PER_SAMPLE, first=START)


import time
t0 = time.time()

analysisManager.Fill()
t1 = time.time()
print(f"\npreprocessing took {round(t1 - t0,2)} seconds")
analysisManager.Accumulate()
t2 = time.time()
print(f"processing took {round(t2 - t1,2)} seconds")
print(f"execution took {round(t2 - t0,2)} seconds")


analysisManager.TransfToDict()
analysisManager['ttbar'].keys()



output = ROOT.TFile.Open(f'histograms/{FILE}', 'RECREATE')
for process in analysisManager:
    for variation in analysisManager[process]:
        for region in analysisManager[process][variation]:
            hist_name = f"{region}_{process}_{variation}" if variation != 'nominal' else f"{region}_{process}"
            hist = analysisManager[process][variation][region]
            if not isinstance(hist, ROOT.TH1D): hist = hist.GetValue() #this this a bag
            if hist.IsZombie(): raise TypeError(hist_name)
            hist_sliced = ROOT.Slice(hist, 120, 550)
            hist_binned = hist_sliced.Rebin(2, hist.GetTitle())
            output.WriteObject(hist_binned, hist_name)
output.Close()


