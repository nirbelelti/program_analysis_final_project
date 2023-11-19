import re
import graphviz
from tree_sitter import Language, Parser


# def extract_regular_methods_from_java_file(file_path):
#     with open(file_path, 'r') as java_file:
#         java_code = java_file.read()
#
#     # Define a regular expression pattern to match entire Java methods
#     method_pattern = r'((public|private|protected|static)\s+\w+\s+\w+\s*\(.*?\)\s*{.*?})'
#
#     # Use regular expressions to find and extract entire methods
#     methods = re.findall(method_pattern, java_code, re.DOTALL)  # Use re.DOTALL to match across multiple lines
#
#     # Filter out the main method
#     regular_methods = [method for method in methods if 'static void main' not in method[0]]
#
#     # Return the list of extracted regular methods
#     return regular_methods


# def extract_class_name_from_java_file(file_path):
#     with open(file_path, 'r') as java_file:
#         java_code = java_file.read()
#
#     class_pattern = r'class\s+(\w+)\s*{'
#     # Extract the class name from the file
#     class_match = re.search(class_pattern, java_code)
#     class_name = class_match.group(1) if class_match else "UnknownClass"
#
#     return class_name


# def has_return_type(method_definition):
#     # Define a regular expression pattern to match a return type
#     return_type_pattern = r'\s+(\w+)\s+\w+\(.*\)\s*{'
#
#     # Use regular expressions to find and extract the return type
#     return_statement_match = re.search(return_type_pattern, method_definition)
#
#     if return_statement_match:
#         return_object = return_statement_match.group(1)
#         return return_object is not None, return_object
#     else:
#         return False, None

def extract_class_method_return_type(file_path):
    # Read the code
    with open(file_path, 'r') as java_file:
        java_code = java_file.read()
    FILE = "./languages.so"
    Language.build_library(FILE, ["tree-sitter-java"])
    JAVA_LANGUAGE = Language(FILE, "java")
    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)
    # Parse Java code
    tree = parser.parse(bytes(java_code, 'utf8'))

    # Get root node
    root_node = tree.root_node

    # Map for methods and result types
    method_result_type_map = {}

    # Iterate class node
    for class_node in root_node.children:
        # print(class_node)
        if class_node.type == 'class_declaration':
            # Get class name
            class_name_node = next(child for child in class_node.children if child.type == 'identifier')
            class_name = java_code[class_name_node.start_byte:class_name_node.end_byte]
            # print(class_name)
            # Iterate method node
            # class_node.children[2] is class body
            for method_node in class_node.children[2].children:
                # print(method_node)
                if method_node.type == 'method_declaration':

                    # Get class name
                    method_name_node = next(child for child in method_node.children if child.type == 'identifier')
                    method_name = java_code[method_name_node.start_byte:method_name_node.end_byte]
                    # print(method_name)
                    # Get return type
                    return_type_node = method_node.child_by_field_name('type')
                    return_type = str(return_type_node.text)[2:-1] if return_type_node else ''
                    method_result_type_map[class_name + "." + method_name] = return_type
    return method_result_type_map

def extract_class_method_call_data_from_java_file(file_path):
    # Data to draw sequence diagram
    diagram_data = []
    # Read the code
    with open(file_path, 'r') as java_file:
        java_code = java_file.read()
    main_method_pattern = r'public\s+static\s+void\s+main\s*\([^)]*\)\s*{\s*([^}]*)\s*}'
    match = re.search(main_method_pattern, java_code)

    # Get the main method code
    if match:
        java_code = match.group(1).strip()
    FILE = "./languages.so"
    Language.build_library(FILE, ["tree-sitter-java"])
    JAVA_LANGUAGE = Language(FILE, "java")
    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)
    # Parse Java code
    tree = parser.parse(bytes(java_code, 'utf8'))

    # Map for methods to get their return types
    method_result_type_map = extract_class_method_return_type(file_path)
    # print(method_result_type_map)
    # Map for instances to get their classes
    instance_class_map = {}

    # Traverse the Syntax Tree
    def traverse(node):

        for child in node.children:
            # print(instance_class_map)
            # print(child)
            if child.type == 'method_invocation':
                # Method invocation data
                method_name = get_method_name(child)
                argument_list = get_argument_list(child)
                instance_name = get_instance_name(child)
                if instance_name != "println":
                    # Get class name by mapping
                    # print(instance_class_map)
                    class_name = instance_class_map[instance_name]
                    # Get return type name by mapping
                    return_type = method_result_type_map[class_name + "." + method_name]
                    # print("Method Invocation:")
                    diagram_data.append("Main -> " + instance_name + "_" + class_name + " : " + method_name + argument_list + "\n")
                    diagram_data.append("activate " + instance_name + "_" + class_name + "\n")
                    diagram_data.append(instance_name + "_" + class_name + " --> Main" + " : " + return_type + "\n")
                    diagram_data.append("deactivate " + instance_name + "_" + class_name + "\n")
                    # print("  Method Name:", method_name)
                    # print("  Instance_name:", instance_name)
                    # print("  Arguments:", argument_list)
            elif child.type == 'new':
                # New function data
                class_name = get_class_name(child)
                instance_name = get_instance_name(child)
                argument_list = get_argument_list(child)
                # print("New Object:")
                # Store the corresponding classes of instances
                instance_class_map[instance_name] = class_name
                # print(instance_class_map)
                diagram_data.append("Main -> " + instance_name + "_" + class_name + " : " + "new" + class_name + argument_list + "\n")
                diagram_data.append("activate " + instance_name + "_" + class_name + "\n")
                diagram_data.append(instance_name + "_" + class_name + " --> Main" + " : " + class_name + "\n")
                diagram_data.append("deactivate " + instance_name + "_" + class_name + "\n")
                # print("  Class Name:", class_name)
                # print("  Instance Name:", instance_name)
                # print("  Arguments:", argument_list)
            traverse(child)

    # Get the method name
    def get_method_name(node):
        method_name_node = [child for child in node.children if child.type == 'identifier'][-1]
        method_name = java_code[method_name_node.start_byte:method_name_node.end_byte]
        return method_name

    # Get the class name
    def get_class_name(node):
        class_name_node = next(child for child in node.parent.children if child.type == 'type_identifier')
        class_name = java_code[class_name_node.start_byte:class_name_node.end_byte]
        return class_name

    # Get the instance name
    def get_instance_name(node):
        # For class method invocation and new method, there are 2 different way to get their instance name
        if node.type == "new":
            class_name_node = next(child for child in node.parent.parent.children if child.type == 'identifier')
        else:
            class_name_node = next(child for child in node.children if child.type == 'identifier')
        class_name = java_code[class_name_node.start_byte:class_name_node.end_byte]
        return class_name

    # Get the argument_list
    def get_argument_list(node):
        # For class method invocation and new method, there are 2 different way to get their argument list
        if node.type == 'new':
            argument_list_node = next(child for child in node.parent.children if child.type == 'argument_list')
        else:
            argument_list_node = next(child for child in node.children if child.type == 'argument_list')
        argument_list = java_code[argument_list_node.start_byte:argument_list_node.end_byte]
        return argument_list

    # Traverse the Syntax Tree to get class method invocation and new method
    traverse(tree.root_node)
    # print(diagram_data)
    return diagram_data

def create_sequence_diagram(diagram_data):
    # Create a new Graphviz Digraph
    sequence_diagram = graphviz.Digraph(format='png')
    extract_class_method_call_data_from_java_file('java/Main.java')
    # class_name = extract_class_name_from_java_file('java/Main.java')
    my_file = open("Diagrams/MySequenceDiagram.puml", "w+")
    my_file.write("@startuml\n")
    my_file.write("activate Main\n")
    # print(diagram_data)
    for string_data in diagram_data:
        # print(string_data)
        my_file.write(string_data)
    my_file.write("deactivate Main\n")
    my_file.write("@enduml")
    my_file.close()

    # for participant in participants:
    #     sequence_diagram.node(participant, participant)

    # # Define interactions (messages) between methods
    # for i in range(len(methods) - 1):
    #     current_method = methods[i][0].split()[2]
    #     next_method = methods[i + 1][0].split()[2]
    #
    #     # Example: Assume methodA calls methodB
    #     sequence_diagram.edge(current_method, next_method)
    #
    # # Render the sequence diagram to a file (e.g., PNG)
    # output_file = 'Diagrams/sequence_diagram.png'
    # sequence_diagram.render(output_file)


# Example usage
java_file_path = 'java/Main.java'
extract_class_method_return_type(java_file_path)
diagram_data = extract_class_method_call_data_from_java_file(java_file_path)
create_sequence_diagram(diagram_data)
