

Tags:[python, py_lib]

### to be a dict

```
with open('coors.csv', mode='r') as infile:
    reader = csv.reader(infile)
    with open('coors_new.csv', mode='w') as outfile:
        writer = csv.writer(outfile)
        mydict = {rows[0]:rows[1] for rows in reader}
```

Alternately, for python <= 2.7.1, you want:

```
mydict = dict((rows[0],rows[1]) for rows in reader)
```



### read a single line

```
csv_reader = csv.reader(f)
csv_headings = next(csv_reader)
first_line = next(csv_reader)
```

