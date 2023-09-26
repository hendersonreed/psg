#!/bin/env python3

import sys
import os
import shutil
import subprocess
import http.server
import socketserver
import pathlib


help = """
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
"""  # noqa

valid_commands = ["build", "serve", "clean", "help"]

# Check if there is at least one argument,
# setting it to `command` for future reference.
if (len(sys.argv) < 2 or
   sys.argv[1] == "help" or
   sys.argv[1] not in valid_commands):
    print(help)
    sys.exit(1)

command = sys.argv[1]

# checking for required files/directories.
if not os.path.isfile("header.html"):
    print("header.html does not exist. Exiting now.")
    sys.exit(1)
else:
    with open("header.html", "r") as file:
        header_html = file.read()

if not os.path.isfile("footer.html"):
    print("footer.html does not exist. Exiting now.")
    sys.exit(1)
else:
    with open("footer.html", "r") as file:
        footer_html = file.read()

if not os.path.isdir("src"):
    print("src directory does not exist. Exiting now.")
    sys.exit(1)


def convert_to_markdown(src, dest):
    # print(f"would have converted {src}")
    # shutil.copy(src, dest)
    pandoc_execution = subprocess.run([
        "pandoc",
        "--from",
        "markdown",
        "--to",
        "html",
        src],
        capture_output=True,
        text=True)
    if pandoc_execution.stderr != "":
        sys.exit(1)
    out_html = (header_html + "\n" +
                pandoc_execution.stdout + "\n" +
                footer_html)
    dest = dest.replace('.md', '.html')

    with open(dest, "w") as file:
        file.write(out_html)


def build():
    """
    - find the `src` dir
    - iterate through every file in it.
    - run the case statement on the file extension:
        if md, pandoc and copy. Also add header and footer to it.
        if not md, just copy
    """
    source_directory = "src"
    destination_directory = "docs"
    os.makedirs(destination_directory, exist_ok=True)

    for root, dirs, files in os.walk(source_directory):
        for directory in dirs:
            source_dir = os.path.join(root, directory)
            dest_dir = os.path.join(
                    destination_directory,
                    os.path.relpath(source_dir, source_directory))
            os.makedirs(dest_dir, exist_ok=True)

        for file in files:
            source_path = os.path.join(root, file)
            dest_path = os.path.join(
                    destination_directory,
                    os.path.relpath(source_path, source_directory))

            if file.endswith(".md"):
                # Handle Markdown files differently
                convert_to_markdown(source_path, dest_path)
            else:
                # Copy non-Markdown files
                shutil.copy(source_path, dest_path)


def serve():
    """
    calls `build`,
    and calls the python http server to serve the `docs` dir.
    """
    build()

    os.chdir('./docs/')

    handler = http.server.SimpleHTTPRequestHandler
    port = 8080
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving directory at http://localhost:{port}")
        httpd.serve_forever()


def clean():
    """
    simply deletes the docs directory.
    """
    shutil.rmtree("./docs/")


eval(f"{command}()")