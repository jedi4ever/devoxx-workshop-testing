from typing import List, Set, Optional
import os, sys
import fnmatch

def print_directory_structure(start_path: str, debug = False) -> str:
    def _generate_tree(dir_path: str, prefix: str = '') -> List[str]:
        entries = os.listdir(dir_path)
        entries = sorted(entries, key=lambda x: (not os.path.isdir(os.path.join(dir_path, x)), x.lower()))
        tree = []
        for i, entry in enumerate(entries):
            rel_path = os.path.relpath(os.path.join(dir_path, entry), start_path)
            if debug:
                print(f"Processing2: {rel_path}")

            # Skip if __pycache__ is in the path
            if any(part == '__pycache__' for part in rel_path.split(os.sep)):
                if debug:
                    print(f"Skipping __pycache__: {rel_path}")
                continue
            
            if i == len(entries) - 1:
                connector = '└── '
                new_prefix = prefix + '    '
            else:
                connector = '├── '
                new_prefix = prefix + '│   '
            
            full_path = os.path.join(dir_path, entry)
            if os.path.isdir(full_path):
                tree.append(f"{prefix}{connector}{entry}/")
                tree.extend(_generate_tree(full_path, new_prefix))
            else:
                tree.append(f"{prefix}{connector}{entry}")
        return tree

    tree = ['/ '] + _generate_tree(start_path)
    return '\n'.join(tree)

def scan_folder(start_path: str, debug = False) -> None:
    output = []
    # Write the directory structure
    output.append("Directory Structure:\n")
    output.append("-------------------\n")
    output.append(print_directory_structure(start_path))
    output.append("\n\n")
    output.append("File Contents:\n")
    output.append("--------------\n")

    for root, dirs, files in os.walk(start_path):
        rel_path = os.path.relpath(root, start_path)
        
        for file in files:
            file_rel_path = os.path.join(rel_path, file)

            file_path = os.path.join(root, file)
            
            if file.endswith('.pyc'):
                if debug:
                    print(f"Skipping compiled file: {file_rel_path}")
                continue
            if debug:
                print(f"Processing: {file_rel_path}")
            output.append(f"File: {file_rel_path}\n")
            output.append("-" * 50 + "\n")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as in_file:
                    content = in_file.read()
                    output.append(f"Content of {file_rel_path}:\n")
                    output.append(content)
            except Exception as e:
                print(f"Error reading file {file_rel_path}: {str(e)}. Skipping.")
                output.append(f"Error reading file: {str(e)}. Content skipped.\n")
            
            output.append("\n\n")
    return ''.join(output)