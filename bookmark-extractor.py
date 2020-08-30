#!/usr/bin/env python3

# Bookmark Extractor is licensed under the
# GNU General Public License Version 3.
# Dimitar D. Mitov 2020

import argparse
import json
import pathlib
import platform


def node_parser(node, level, name, target, writer):
    space = '  '

    if node['name'] == name:
        level = 0
        target = True

    if 'url' in node:
        if target is True:
            writer.write(
                (space * level) +
                '* ' +
                '[' + node['name'] + ']' +
                '(' + node['url'] + ')' +
                '  \n'
            )

    if 'url' not in node:
        if target is True:
            if node['name'] != name:
                writer.write(
                    (space * level) +
                    '* ' + node['name'] +
                    '  \n'
                )

    level = level + 1

    if node['type'] == 'folder':
        for child_node in node['children']:
            node_parser(child_node, level, name, target, writer)

    return True


def main():
    # Take desired bookmarks root directory from command line argument:
    commandline_parser = argparse.ArgumentParser()

    commandline_parser.add_argument(
        '-r',
        '--root',
        dest='root',
        type=str,
        metavar='name',
        required=True,
        help='desired bookmarks root folder'
    )

    arguments = commandline_parser.parse_args()

    root_name = None

    if arguments.root:
        root_name = arguments.root

    # Read the bookmarks file,
    # extract all wanted bookmarks and
    # write a Markdown output file:
    bookmarks_file_linux = '/.config/chromium/Default/Bookmarks'
    bookmarks_file_windows = '\\Google\\Chrome\\User Data\\Default\\Bookmarks'

    home_directory = str(pathlib.Path.home())
    bookmarks_file = None

    if platform.system() == 'Linux':
        bookmarks_file = home_directory + bookmarks_file_linux

    if platform.system() == 'Windows':
        bookmarks_file = home_directory + bookmarks_file_windows

    reader = open(bookmarks_file, 'r')
    bookmarks_file_contents = reader.read()
    reader.close()

    bookmarks_json = json.loads(bookmarks_file_contents)
    other_bookmarks = bookmarks_json['roots']['other']

    writer = open('bookmarks.md', 'w')
    writer.write('## ' + root_name + '\n')

    node_parser(other_bookmarks, 0, root_name, False, writer)

    writer.write(
        '\nCreated using ' +
        '[Bookmark Extractor]' +
        '(https://github.com/ddmitov/python-bookmark-extractor)\n'
    )

    writer.close()


if __name__ == '__main__':
    main()
