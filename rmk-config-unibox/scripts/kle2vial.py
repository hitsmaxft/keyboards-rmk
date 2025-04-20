#!/usr/bin/env python3

import json
import argparse
import sys

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {file_path} is not a valid JSON file")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: {file_path} not found")
        sys.exit(1)

def validate_kle_layout(kle_data):
    if not isinstance(kle_data, list) or len(kle_data) < 2:
        print("Error: Invalid KLE format. Expected array with at least 2 elements")
        sys.exit(1)
    
    keyboard_info = kle_data[0]
    if not isinstance(keyboard_info, dict) or 'name' not in keyboard_info:
        print("Error: First element must be an object with 'name' property")
        sys.exit(1)

def convert_kle_to_vial(kle_data, vial_data):
    rows = len(kle_data) - 1  # Subtract 1 for the keyboard info
    cols = max(len(row) for row in kle_data[1:])
    
    # Validate matrix dimensions
    # if rows > vial_data['matrix']['rows'] or cols > vial_data['matrix']['cols']:
    #     print(f"Error: KLE layout ({rows}x{cols}) exceeds matrix dimensions ({vial_data['matrix']['rows']}x{vial_data['matrix']['cols']})")
    #     sys.exit(1)

    # Convert KLE layout to VIAL keymap format
    keymap = []
    for row in kle_data[1:]:
        keymap.append(row)

    vial_data['layouts']['keymap'] = keymap
    return vial_data

def main():
    parser = argparse.ArgumentParser(description='Convert KLE layout to VIAL layout')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('kle_file', nargs='?', help='KLE JSON file')
    group.add_argument('-i', '--input', help='KLE JSON file')
    parser.add_argument('vial_file', nargs='?', help='VIAL JSON file')
    parser.add_argument('-o', '--output', help='VIAL JSON file')
    parser.add_argument('-n', '--dry-run', action='store_true', help='Perform a dry run without updating the VIAL file')

    args = parser.parse_args()

    kle_file = args.input if args.input else args.kle_file
    vial_file = args.output if args.output else args.vial_file

    if not vial_file:
        parser.error("VIAL JSON file is required")

    kle_data = read_json_file(kle_file)
    vial_data = read_json_file(vial_file)

    # validate_kle_layout(kle_data)
    updated_vial = convert_kle_to_vial(kle_data, vial_data)

    if args.dry_run:
        print(f"Dry run - Changes that would be made to {vial_file}:")
        print(json.dumps(updated_vial, indent=2))
    else:
        # Write updated VIAL JSON
        try:
            with open(vial_file, 'w') as f:
                json.dump(updated_vial, f, indent=2)
            print(f"Successfully updated {vial_file}")
        except Exception as e:
            print(f"Error writing to {vial_file}: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()