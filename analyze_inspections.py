#!/usr/bin/env python3

import argparse
import dataclasses
import json
import os
import re
import xml.etree.ElementTree as ET

FILE_EXTENSIONS_TO_CONSIDER = ['.kt', '.java', '.kts']


@dataclasses.dataclass
class Diagnostic:
    file_name: str
    line_number: int
    error_level: str
    description: str


def analyze_file(path):
    diagnostics = []
    with open(path) as fin:
        text = fin.read()
    text = text.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
    text = text.replace('file://$PROJECT_DIR$/', '')
    text = text.replace('</problems>', '') + '</problems>'
    tree = ET.fromstring(text)
    for problem in tree.iter('problem'):
        file_name = problem.find('file').text
        _, file_ext = os.path.splitext(file_name)
        if file_ext.lower() not in FILE_EXTENSIONS_TO_CONSIDER:
            continue
        line_no = int(problem.find('line').text)
        error_level = problem.find('problem_class').get('severity')
        description = problem.find('description').text.replace('#loc', '').replace('<code>', '`').replace('</code>', '`').strip()
        diagnostics.append(Diagnostic(file_name, line_no, error_level, description))
    return diagnostics


def main():
    parser = argparse.ArgumentParser('Analyzes IntelliJ Inspections')
    parser.add_argument('-i', '--inspections', required=True, help='Path to inspections folder')
    args = parser.parse_args()

    ins = os.path.abspath(args.inspections)
    files = [os.path.join(ins, f) for f in os.listdir(ins) if f.endswith('.xml') and not f.startswith('.')]

    diagnostics = []

    for f in files:
        diagnostics.extend(analyze_file(f))

    output = {
        'diagnostics': diagnostics
    }
    print(json.dumps(output, indent=4, default=lambda x: x.__dict__))


if __name__ == "__main__":
    main()
