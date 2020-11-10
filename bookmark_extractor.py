#!/usr/bin/env python3

# Python Bookmark Extractor is licensed under the
# GNU General Public License Version 3.
# Dimitar D. Mitov 2020
# https://github.com/ddmitov/python-bookmark-extractor

import argparse
import json
import pathlib
import platform
import requests


def node_parser(node, level, name, target, writer, url_check):
    space = '  '

    if node['name'] == name:
        level = 0
        target = True

    if 'url' in node:
        if target is True:
            print_url = True

            # Optionally check the URL of the bookmark:
            if url_check is True:
                response = None

                try:
                    response = requests.get(node['url'])
                except Exception:
                    pass

                if response is None:
                    print('PAGE NOT FOUND: ' + node['url'])
                    print_url = False

                if response is not None:
                    if response.status_code == 404:
                        print('PAGE NOT FOUND: ' + node['url'])
                        print_url = False

                    if response.status_code != 404:
                        print('OK: ' + node['url'])

            if print_url is True:
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

    # Recursively scan all subfolders:
    if node['type'] == 'folder':
        for child_node in node['children']:
            node_parser(child_node, level, name, target, writer, url_check)

    return True


def main():
    commandline_parser = argparse.ArgumentParser()

    # Take the desired bookmarks root folder from command line argument:
    commandline_parser.add_argument(
        '-r',
        '--root',
        dest='root',
        type=str,
        metavar='name',
        required=True,
        help='desired bookmarks root folder'
    )

    # Optional command line flag to check all bookmark URLs:
    commandline_parser.add_argument(
        '-c',
        '--check',
        action='store_true',
        help='check URL'
    )

    arguments = commandline_parser.parse_args()

    # Read the bookmarks file,
    # extract all wanted bookmarks and
    # write a Markdown output file:
    bookmarks_file_linux = '/.config/chromium/Default/Bookmarks'
    bookmarks_file_windows = (
        '\\AppData\\Local' +
        '\\Google\\Chrome\\User Data\\Default\\Bookmarks'
    )

    home_directory = str(pathlib.Path.home())
    bookmarks_file = None

    if platform.system() == 'Linux':
        bookmarks_file = home_directory + bookmarks_file_linux

    if platform.system() == 'Windows':
        bookmarks_file = home_directory + bookmarks_file_windows

    reader = open(bookmarks_file, 'r', encoding='utf8')
    bookmarks_file_contents = reader.read()
    reader.close()

    bookmarks_json = json.loads(bookmarks_file_contents)
    other_bookmarks = bookmarks_json['roots']['other']

    root_name = None

    if arguments.root:
        root_name = arguments.root

    writer = open('bookmarks.md', 'w', encoding='utf8')
    writer.write('## ' + root_name + '\n')

    url_check = False

    if arguments.check:
        url_check = True

    # Find the desired bookmarks root folder and scan it recursively:
    node_parser(other_bookmarks, 0, root_name, False, writer, url_check)

    writer.write(
        '\nCreated using ' +
        '[Python Bookmark Extractor]' +
        '(https://github.com/ddmitov/python-bookmark-extractor)  \n'
    )

    writer.close()


if __name__ == '__main__':
    main()
