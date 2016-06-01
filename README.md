# mreport: Memory Analysis Report

This minimal project is used to help on processing the statical analysis of the Memory Analysis Project

## Instalation
```
sudo pip install git+git@gitlab:ryukinix/mreport.git
```

## Params

```
usage: mar [-h] [--show-graph] [--save-graph] [-t TARGET] [-l LONG]
           [-i INTERVAL] [-v]
           csvs [csvs ...]

positional arguments:
  csvs                  The list of pair malloc_0x.csv free_0x separated by
                        spaces or a dir

optional arguments:
  -h, --help            show this help message and exit
  --show-graph          Show the graph after pre-processing
  --save-graph          Show the
  -t TARGET, --target TARGET
                        The path (can be a folder name or path) to save the
                        output
  -l LONG, --long-size LONG
                        The long size in seconds to labelize the allocation
                        time
  -i INTERVAL, --interval INTERVAL
                        The interval number to count longs on streaking rows
  -v, --verbose         Allow the user control printint or not control
                        operations
```



## Usage

The usage is based on the pairs of files of tool `mar` (Memory Analysis Report):

The more simple example:
```
mar lynx_malloc_01.csv lynx_free_01.csv
```

If you have a sequence malloc-free files, try a more simple approach:

```
mar lynx/
``` 

Where lynx has that content:


```
├── lynx
│   ├── lynx_free_1.csv
│   ├── lynx_malloc_1.csv

caso voc^tov ro
``` 

## License
MIT