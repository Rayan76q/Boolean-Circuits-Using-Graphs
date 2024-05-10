from modules.open_digraph import *
import inspect

import inspect
import os

file_map = {
    "__init__.py": "modules/__init__.py",
    "adders.py": "modules/adders.py",
    "addition_checkEncode.py": "modules/addition_checkEncode.py",
    "bool_circ.py": "modules/bool_circ.py",
    "bool_circ_gates_mx.py": "modules/bool_circ_gates_mx.py",
    "matrix_operations.py": "modules/matrix_operations.py",
    "node.py": "modules/node.py",
    "open_digraph.py": "modules/open_digraph.py",
    "open_digraph_composition_mx.py": "modules/open_digraph_composition_mx.py",
    "open_digraph_paths_distance_mx.py": "modules/open_digraph_paths_distance_mx.py"
}

# Function to print the contents of a file or a specific method within the file
def print_content(file_name, method_name=None):
    file_path = file_map[file_name]
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return

    if method_name is None:
        # Print the whole file content
        with open(file_path, 'r') as file:
            content = file.read()
            print(content)
    else:
        # Import the module and find the method's source
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        module_globals = {}
        with open(file_path, 'r') as file:
            exec(file.read(), module_globals)

        if method_name in module_globals:
            # Print the specific method's content
            method_content = inspect.getsource(module_globals[method_name])
            print(method_content)
        else:
            print(f"Error: The method '{method_name}' does not exist in the file '{file_path}'.")

# Example usage:
# Specify the path to the desired Python file
file_name = 'bool_circ.py'
# If you want to print a specific method, replace 'method_name' with the desired method's name. Otherwise, set it to None.
method_name = None
# Call the functiom
print_content(file_name, method_name)
