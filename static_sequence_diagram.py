import re

import graphviz
from tree_sitter import Language, Parser


def extract_class_method_return_type(file_path):
    with open(file_path, 'r') as java_file:
        java_code = java_file.read()

    FILE = "./languages.so"
    Language.build_library(FILE, ["tree-sitter-java"])
    JAVA_LANGUAGE = Language(FILE, "java")
    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)
    tree = parser.parse(bytes(java_code, 'utf8'))

    method_result_type_map = {}

    for class_node in tree.root_node.children:
        if class_node.type == 'class_declaration':
            class_name_node = next(
                child for child in class_node.children if child.type == 'identifier')
            class_name = java_code[class_name_node.start_byte:class_name_node.end_byte]

            for method_node in class_node.children[2].children:
                if method_node.type == 'method_declaration':
                    method_name_node = next(
                        child for child in method_node.children if child.type == 'identifier')
                    method_name = java_code[method_name_node.start_byte:method_name_node.end_byte]
                    return_type_node = method_node.child_by_field_name('type')
                    return_type = str(return_type_node.text)[
                        2:-1] if return_type_node else ''
                    method_result_type_map[class_name +
                                           "." + method_name] = return_type

    return method_result_type_map


def extract_class_method_call_data_from_java_file(file_path):
    diagram_data = []
    with open(file_path, 'r') as java_file:
        java_code = java_file.read()

    main_method_pattern = r'public\s+static\s+void\s+main\s*\([^)]*\)\s*{\s*([^}]*)\s*}'
    match = re.search(main_method_pattern, java_code)

    if match:
        java_code = match.group(1).strip()

    FILE = "./languages.so"
    Language.build_library(FILE, ["tree-sitter-java"])
    JAVA_LANGUAGE = Language(FILE, "java")
    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)
    tree = parser.parse(bytes(java_code, 'utf8'))

    method_result_type_map = extract_class_method_return_type(file_path)
    instance_class_map = {}
    loop_info = None  # Loop-related information

    def traverse(node, parent_class="Main"):
        nonlocal loop_info
        for child in node.children:
            if child.type == 'method_invocation':
                method_name = get_method_name(child)
                argument_list = get_argument_list(child)
                instance_name = get_instance_name(child)

                if instance_name != "println":
                    class_name = instance_class_map.get(
                        instance_name, "UnknownClass")
                    return_type = method_result_type_map.get(
                        class_name + "." + method_name, "void")

                    diagram_data.append(
                        f"{parent_class} -> {class_name} : {method_name}{argument_list}\n")
                    diagram_data.append(f"activate {class_name}\n")
                    diagram_data.append(
                        f"{class_name} --> {parent_class} : {return_type}\n")
                    diagram_data.append(f"deactivate {class_name}\n")
            elif child.type == 'new':
                class_name = get_class_name(child)
                instance_name = get_instance_name(child)
                argument_list = get_argument_list(child)

                instance_class_map[instance_name] = class_name

                diagram_data.append(
                    f"{parent_class} -> {class_name} : new{class_name}{argument_list}\n")
                diagram_data.append(f"activate {class_name}\n")
                diagram_data.append(
                    f"{class_name} --> {parent_class} : {class_name}\n")
                diagram_data.append(f"deactivate {class_name}\n")
            elif child.type == 'for_statement':
                loop_variable = get_loop_variable(child)
                loop_start = get_loop_start(child)
                loop_end = get_loop_end(child)

                loop_info = {
                    'loop_variable': loop_variable,
                    'loop_start': loop_start,
                    'loop_end': loop_end
                }

                diagram_data.append(
                    f"{parent_class} -> {parent_class} : Loop from {loop_start} to {loop_end}\n")

                # Recursively traverse the loop body
                traverse(child.child_by_field_name('statement'), parent_class)

                # Reset loop_info after processing the loop
                loop_info = None

            elif loop_info and child.type == 'block':
                # Inside a loop, traverse the block
                traverse(child, parent_class)

            else:
                traverse(child, parent_class)

    def get_method_name(node):
        method_name_node = [
            child for child in node.children if child.type == 'identifier'][-1]
        return java_code[method_name_node.start_byte:method_name_node.end_byte]

    def get_class_name(node):
        class_name_node = next(
            child for child in node.parent.children if child.type == 'type_identifier')
        return java_code[class_name_node.start_byte:class_name_node.end_byte]

    def get_instance_name(node):
        if node.type == "new":
            class_name_node = next(
                child for child in node.parent.parent.children if child.type == 'identifier')
        else:
            class_name_node = next(
                child for child in node.children if child.type == 'identifier')
        return java_code[class_name_node.start_byte:class_name_node.end_byte]

    def get_argument_list(node):
        if node.type == 'new':
            argument_list_node = next(
                child for child in node.parent.children if child.type == 'argument_list')
        else:
            argument_list_node = next(
                child for child in node.children if child.type == 'argument_list')
        return java_code[argument_list_node.start_byte:argument_list_node.end_byte]

    traverse(tree.root_node)
    return diagram_data


def create_sequence_diagram(diagram_data):
    sequence_diagram = graphviz.Digraph(format='png')
    java_file_path = 'java/Main.java'
    extract_class_method_return_type(java_file_path)

    my_file = open("Diagrams/MySequenceDiagram.puml", "w+")
    my_file.write("@startuml\n")
    my_file.write("activate Main\n")

    for string_data in diagram_data:
        my_file.write(string_data)

    my_file.write("deactivate Main\n")
    my_file.write("@enduml")
    my_file.close()


java_file_path = 'java/Main.java'
diagram_data = extract_class_method_call_data_from_java_file(java_file_path)
create_sequence_diagram(diagram_data)
