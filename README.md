# mar: Memory Analysis Report

## Abstract
Read malloc-free pairs CSVs from debugmalloc program,do a sequence of stats
processing to processing data.On the final of processing, get a summarization
and put on new CSV.Beyond that, the user can choice by CLI to save or show
graphs.

Developed by Manoel Vilela on Federal University of Pará.
— Student Researcher at 2016


## Instalation

## Subdeps
```
sudo apt-get install python3-pip libpng-dev libjpeg8-dev libfreetype6-dev
pip3 install setuptools 
``` 

## Easy Mode

```
sudo pip3 install git+https://gitlab.com/ryukinix/mar.git
```

## Make Mode
```
git clone git@gitlab.com:ryukinix/mar.git
cd mar && sudo make install
```

If you try modify and testing (develop), use `sudo make develop` rather `sudo make install`, this will create a dynamic instalation using symlinks to create the Python modules whose at each modification you do, you can test and receive it.

## Params

```
usage: mar [-h] [--show-graph] [--save-graph] [-t TARGET] [-l LONG]
           [-i INTERVAL] [-v] [--ignore IGNORE] [--ignore-first] [-c]
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
  -l LONG, --long-range LONG
                        The long range range like [x, y] (closed-range) or (a,
                        b) (open-range) to labelize the allocation time. Use
                        +inf or -inf to handle infinite intervals like (-inf,
                        +inf) will get all allocations
  -i INTERVAL, --interval INTERVAL
                        The interval number to count longs on streaking rows
  -v, --verbose         Allow the user control printint or not control
                        operations
  --ignore IGNORE       Pass a wildcard pattern to file experiments on reading
  --ignore-first        Ignore the first experiment (the same of --ignore
                        *1.csv)
  -c, --count-clusters  Count the short/mid/long allocations and save a csv.

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
``` 

## License
MIT