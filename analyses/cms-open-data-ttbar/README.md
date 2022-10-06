# How to get histograms with RDF and Coffea and compare results?
## Pre-requirements
### RDF $t\bar{t}$-analysis
1) Find the file *rdf_ttbar.py*
1) Ensure that code block that saves histograms is uncommented
1) Find the `disk` variable inside the file and set the path to the downloaded data depending on what disk you will use.

**Note**: There are two available disks in the perf machine:
* `/data/ssdext4_agc_data` - unmerged files
* `/data/ssdext4_agc_data_2` - larger merged files

**Note** two `.json` files inside the directory:
* `ntuples.json` - for accessing small unmerged files from the `/data/ssdext4_agc_data` disk
* `merged_nevts.json` - for accessing merged files from the `/data/ssdext4_agc_data_2` disk

The unmerged data files from the first disk must be accessed via `ntuples.json`. The merged files - via `merged_nevts.json`.
 
4) Find `ntuples` and `disk` variables to check coincidence

### Coffea $t\bar{t}$-analysis
1) Find the file *coffea_ttbar.py*
1) Ensure that location in the line `fileset = utils.construct_fileset(N_FILES_MAX_PER_SAMPLE, use_xcache=False, location=...)` is correclty spicified 
1) If you set the location to the first disk, change `merged_nevts.json` to `ntuples.json` inside the `utils.construct_fileset` 

## Running
1. Run scripts by using such syntax `<script.py> --nfiles <nfiles> --ncores <ncores>`

**Note**: histograms are saved in `histograms/` dir as `.root` files

## Verifying 
1. Find the file *sanity.py*
1. `get_mismatched` accepts the names of two root files and compares them
1. `get_mismatched` method gives histograms with significant deviations (deviations that pass some threshold)
1. To get those deviations you can either run `python ./sanity --nfiles <nfiles>` or import `get_mismatched` from `sanity` and use it in your own
