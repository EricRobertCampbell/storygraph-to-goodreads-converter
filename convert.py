#!/usr/bin/env python3

import argparse
import csv

def main() -> None:
    """ Convert the input (storygraph) file to goodreads format and write to the output file """
    # find the input and output files
    parser = argparse.ArgumentParser(description="Convert a SoryGraph export file to a Goodreads import file")
    parser.add_argument('-i', '--input_filename', type=str, required=True, help="The input (StoryGraph) file")
    parser.add_argument('-o', '--output_filename', type=str, default="goodreads_import.csv", help="The output (Goodreads) file")
    parser.add_argument('-t', '--test', type=int, help="(Optional) a number of rows to convert. Useful for testing.")

    args = parser.parse_args()

    outputs = []
    with open(args.input_filename, 'r') as input_file:
        reader = csv.DictReader(input_file)
        for index, row in enumerate(reader):
            if not args.test or (args.test and index < args.test):
                converted_row = convert_storygraph_goodreads(row)
                outputs.append(converted_row)

    with open(args.output_filename, 'w') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=outputs[0].keys())
        writer.writeheader()
        writer.writerows(outputs)
        print(f"Wrote {len(outputs)} books to {args.output_filename}")

def convert_storygraph_goodreads(sg: dict) -> dict:
    """ Convert a dict representing a storgaph row to goodreads """
    # label in storygraph: label in goodreads. Anything not in here will be ignored.
    sg_gr_mapping = {
        "Title": "Title",
        "Authors": "Author",
        "ISBN/UID": "ISBN",
        "Star Rating": "My Rating",
        "Last Date Read": "Date Read",
        "Read Status": "Shelves",
    }
    gr = {sg_gr_mapping[key]: value for key, value in sg.items() if key in sg_gr_mapping}
    gr['My Rating'] = int(round(float(gr['My Rating']), 0)) if gr['My Rating'] != '' else ''
    return gr

if __name__ == "__main__":
    main()
