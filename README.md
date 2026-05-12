# psg: python site generator

This is my bare minumum site generator.

Features:

- uses pandoc to infer input format and produce HTML output.
- no templating, just smashes the generated html fragment between user-provided header and footer fragments.
- tiny and simple codebase, straightforward to extend as needed.


```
reed@mercury => cloc psg.py
       1 text file.
       1 unique file.
       0 files ignored.

github.com/AlDanial/cloc v 1.90  T=0.01 s (67.9 files/s, 9234.1 lines/s)
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Python                           1             26             33             80
-------------------------------------------------------------------------------
```

80 lines of Python (using just the included batteries), with one dependency (Pandoc).

```
reed@mercury => psg.py help

usage: psg [command]

commands:
    build - converts the site source stored in the `src` directory, and places it in the `docs` directory.
    serve - builds the the docs directory and launches Python's builtin server to serve the docs directory.
    clean - deletes the docs directory.
    help - display this message.

psg depends on the existence of the following:
    - `pandoc` in your $PATH
    - header.html, which is prepended to all generated html fragments
    - footer.html, which is appended to all generated html fragments.
    - a "src" directory containing the website to be generated.
```

psg will convert any markdown files in the `src` directory into HTML, using pandoc. All other files will be copied over verbatim, preserving the directory tree structure.

## installation

### installing dependencies

1. `psg` has only been tested with Python 3.11.4 at this time.
2. Ensure you have pandoc installed. You can do so with the following:

#### debian-based distros:

```shell
sudo apt-get install pandoc
```

#### rpm-based distros:

```shell
sudo dnf install pandoc
```

#### MacOS:
```shell
brew install pandoc
```

### downloading psg

It's as simple as can be.

```shell
curl https://raw.githubusercontent.com/hendersonreed/psg/main/psg.py > ./psg
```

Audit the code by reading through it to make sure it isn't doing anything malicious (always a good idea when curling random scripts). Then flip the executable bit.

```
chmod +x psg
```

Move psg anywhere in your path, or just keep it with your site source.
