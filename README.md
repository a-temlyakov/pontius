pontius
=======

CLI for managing and deleting duplicate files.

#####Finding initial list of duplicates:

```bash
$ find -not -empty -type f -printf "%s\n" | sort -rn | uniq -d | xargs -I{} -n1 find -type f -size {}c -print0 | xargs -0 md5sum | sort | uniq -w32 --all-repeated=separate
```

This prints to stdout in the format of 'md5hash path_to_file', where path_to_file is relative to where the command was run. I have created a `find-duplicates` alias from above and just redirect the output to a file. It can take a while to finish, so I recommend running it in a `screen`. 

#####Running unit tests:

```bash
$ python -m unittest discover -v
```
