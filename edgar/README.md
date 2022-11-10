# edgar

This is a simple downloader for Edgar data based on the code developed during
the workshop on 7 November 2022. This version provides a simple command line
interface to enable switching functions by the user.

## Usage

### Index downloads

Index files in Edgar are quarterly. Define a year-quarter as `yyyyQq`, where the
second quarter of 2015 is `2015Q2`. Downloading index files between a starting
year-quarter and an ending year-quarter using the command:

`python3 edgar index yyyyQq yyyyQq`

### Form downloads

Forms are downloading based on the index files saved. This program simply loops
through all the index files and downloads any files not previously downloaded.
It supports downloading forms by type, but other features may be added. To
download all proxy statements (form DEF 14A), use the command:

`python edgar form 'DEF 14A'`

The quotes around the form name are required when there is a space, such as 'DEF
14A'. They may be omitted for forms that are contiguous, non-space characters.


