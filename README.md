# mreport: Memory Analysis Report

This minimal project is used to help on processing the statical analysis of the Memory Analysis Project

## Instalation
```
sudo pip install git+git@gitlab:ryukinix/mreport.git
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