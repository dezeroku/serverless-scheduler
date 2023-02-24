#!/usr/bin/env python3

import json
import sys


def convert(filename_in, filename_out, var_name):
    with open(filename_in) as temp:
        content = json.loads(temp.read())

    with open(filename_out, "w") as temp:
        temp.write(f"{var_name} = ")
        temp.write(json.dumps(content, indent=4, sort_keys=True))
        temp.write("\n\n")


def main():
    if len(sys.argv) < 4:
        print("Provide the json filename, outfile name and variable name")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    var_name = sys.argv[3]

    convert(input_file, output_file, var_name)


if __name__ == "__main__":
    main()
