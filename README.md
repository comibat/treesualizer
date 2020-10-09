# treesualizer

## Description
Treesualizer parse output of 'tree' linux command and shows the content in tree-like and list-like view using GUI.

It is very usefull in cases when you have a shell on a remote location (or smb share) and you want to search for files or extensions.

Use something like
```bash
tree -a 2>/dev/null 1> tree.txt
```
... and then
```bash
python3 treesualizer.py tree.txt
```
to get all searchable.

## Requirements
python3, with no additional libraries requred.

## Disclaimer
It's not perfect, but it works.

## Credits
Special thanks to mjokic (https://github.com/mjokic) for the name contribution.
