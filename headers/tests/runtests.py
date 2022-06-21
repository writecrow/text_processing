#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys
import filecmp
import pandas
import difflib
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import add_headers_full_name

if __name__ == '__main__':
    master = pandas.read_csv('test_metadata.csv')
    add_headers_full_name.add_headers_recursive('test_data', master)
    for dirpath, dirnames, files in os.walk('files_with_headers'):
        for name in files:
            # Skip non text files.
            if '.txt' not in name:
                continue
            expected = dirpath.replace('files_with_headers', 'expected_test_output')
            generated = os.path.join(dirpath, name)
            baseline = os.path.join(expected, name)
            report = filecmp.cmp(generated, baseline, shallow=False)
            if report is False:
                print('************************************************************')
                print('There are differences between the expected and actual output for ' + name)
                with open(baseline, 'r') as hosts0:
                    with open(generated, 'r') as hosts1:
                        diff = difflib.unified_diff(
                            hosts1.readlines(),
                            hosts0.readlines(),
                            fromfile='expected',
                            tofile='actual',
                        )
                        for line in diff:
                            sys.stdout.write(line)
                print('************************************************************')