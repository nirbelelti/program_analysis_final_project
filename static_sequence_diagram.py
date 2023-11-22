import re

import graphviz
from tree_sitter import Language, Parser
# Set execution method
EXECUTION_CLASS_NAME = "Main"
EXECUTION_METHOD_NAME = "main"
JAVA_FILE_PATH = "java/CarWithLoopAndIf.java"
def is_basic_type(type):
    basic_types = ["byte", "short", "int", "long", "float", "double", "char", "boolean", "String", "Boolean", "Character", "Number", "Date"]
    for basic_type in basic_types:
        if basic_type == type:
            return True
    return False
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


def extract_class_method_call_data_from_java_file(file_path, execution_class_name="Main", execution_method_name="main"):
    diagram_data = []
    with open(file_path, 'r') as java_file:
        java_code = java_file.read()
    FILE = "./languages.so"
    Language.build_library(FILE, ["tree-sitter-java"])
    JAVA_LANGUAGE = Language(FILE, "java")
    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)
    tree = parser.parse(bytes(java_code, 'utf8'))

    method_result_type_map = extract_class_method_return_type(file_path)
    instance_class_map = {}

    # Get root node
    root_node = tree.root_node
    # Get execution class node
    class_nodes = [child for child in root_node.children if child.type == "class_declaration"]
    for class_node in class_nodes:
        class_identifiers = [child for child in class_node.children if child.type == 'identifier']
        for class_identifier in class_identifiers:
            if java_code[class_identifier.start_byte:class_identifier.end_byte] == execution_class_name:
                main_class_body_node = next(child for child in class_identifier.parent.children if child.type == 'class_body')
                field_declaration_nodes = [child for child in main_class_body_node.children if child.type == "field_declaration"]
                # Add field variable to instance class map
                for field_declaration_node in field_declaration_nodes:
                    field_type = ""
                    field_name = ""
                    # If the class of the instance is generic
                    generic_type_nodes = [child for child in field_declaration_node.children if child.type == "generic_type"]
                    if len(generic_type_nodes) > 0:
                        field_type = java_code[generic_type_nodes[0].start_byte:generic_type_nodes[0].end_byte]
                        # Get the inside type of generic type
                        pattern = r'<(.+?)>'
                        match = re.search(pattern, field_type)
                        if match:
                            field_type = match.group(1)
                        else:
                            field_type = ""

                        # If the field is in basic type, don't push it into map
                        if is_basic_type(field_type):
                            field_type = ""

                    # If the class of the instance is not generic
                    type_identifier_nodes = [child for child in field_declaration_node.children if child.type == "type_identifier"]
                    if len(type_identifier_nodes) > 0:
                        field_type = java_code[type_identifier_nodes[0].start_byte:type_identifier_nodes[0].end_byte]
                        # If the field is in basic type, don't push it into map
                        if is_basic_type(field_type):
                            field_type = ""
                    variable_declarator_node = next(child for child in field_declaration_node.children if child.type == "variable_declarator")
                    variable_name_node = next(child for child in variable_declarator_node.children if child.type == "identifier")
                    field_name = java_code[variable_name_node.start_byte:variable_name_node.end_byte]
                    if field_type:
                        instance_class_map[field_name] = field_type
                main_method_nodes = [child for child in main_class_body_node.children if child.type == "method_declaration"]
                # Get execution method node
                for main_method_node in main_method_nodes:
                    main_method_name = next(child for child in main_method_node.children if child.type == "identifier")
                    main_method_block = next(child for child in main_method_node.children if child.type == "block")
                    # Add method parameters to instance class map
                    formal_parameters_node = next(child for child in main_method_node.children if child.type == "formal_parameters")
                    parameters = []
                    formal_parameters = java_code[formal_parameters_node.start_byte:formal_parameters_node.end_byte]
                    pattern = r'\b([\w.]+)\s+([\w.]+)(?=[,)])'
                    matches = re.findall(pattern, formal_parameters)
                    for match in matches:
                        parameter_type = match[0]
                        parameter_instance = match[1]
                        parameters.append([parameter_type, parameter_instance])
                    for parameter in parameters:
                        if len(parameter) > 0:
                            instance_class_map[parameter[1]] = parameter[0]
                    if java_code[main_method_name.start_byte:main_method_name.end_byte] == execution_method_name:
                        # Execution code. Get rid of curly brackets, trim space in front and back of java code
                        java_code = java_code[main_method_block.start_byte:main_method_block.end_byte][1:-1].strip()
                        # Reset the tree node of new code
                        tree = parser.parse(bytes(java_code, 'utf8'))
                        root_node = tree.root_node
    # loop_info = None  # Loop-related information

    def get_method_name(node, java_code):
        method_name_node = [
            child for child in node.children if child.type == 'identifier'][-1]
        # print(method_name_node, java_code[method_name_node.start_byte:method_name_node.end_byte])
        return java_code[method_name_node.start_byte:method_name_node.end_byte]

    def get_class_name(node, java_code):
        class_name_node = next(
            child for child in node.parent.children if child.type == 'type_identifier')
        return java_code[class_name_node.start_byte:class_name_node.end_byte]

    def get_instance_name(node, java_code):
        if node.type == "new":
            class_name_node = next(
                child for child in node.parent.parent.children if child.type == 'identifier')
        else:
            class_name_node = next(
                child for child in node.children if child.type == 'identifier')
        return java_code[class_name_node.start_byte:class_name_node.end_byte]

    def get_argument_list(node, java_code):
        if node.type == 'new':
            argument_list_node = next(
                child for child in node.parent.children if child.type == 'argument_list')
        else:
            argument_list_node = next(
                child for child in node.children if child.type == 'argument_list')
        return java_code[argument_list_node.start_byte:argument_list_node.end_byte]

    def traverse(node):
        def get_method_invocation_and_new_method_diagram_data(child_node, java_code):

            if child_node.type == 'method_invocation':
                method_name = get_method_name(child_node, java_code)
                argument_list = get_argument_list(child_node, java_code)
                instance_name = get_instance_name(child_node, java_code)
                # print(child_node, child_node.children,java_code[child_node.start_byte:child_node.end_byte])

                if instance_name != "println":
                    class_name = instance_class_map.get(
                        instance_name, "UnknownClass")
                    return_type = method_result_type_map.get(
                        class_name + "." + method_name, "void")

                    diagram_data.append(
                        f"{execution_class_name} -> {class_name} : {method_name}{argument_list}\n")
                    diagram_data.append(f"activate {class_name}\n")
                    diagram_data.append(
                        f"{class_name} --> {execution_class_name} : {return_type}\n")
                    diagram_data.append(f"deactivate {class_name}\n")
                else:
                    println_node = next(child for child in child_node.children if child.type == "argument_list")
                    for method_invocation_and_new_method_node in println_node.children:
                        get_method_invocation_and_new_method_diagram_data(method_invocation_and_new_method_node,
                                                                          java_code)
            elif child_node.type == 'variable_declarator':
                # Get new method node in nested layers
                try:
                    class_name_node = next(child for child in child_node.parent.children if child.type == 'type_identifier')
                    class_name = java_code[class_name_node.start_byte:class_name_node.end_byte]
                    instance_name_node = next(child for child in child_node.children if child.type == 'identifier')
                    instance_name = java_code[instance_name_node.start_byte:instance_name_node.end_byte]
                    instance_class_map[instance_name] = class_name
                    object_creation_expression_node = next(child for child in child_node.children if child.type == "object_creation_expression")
                except Exception as e:
                    return

                new_function_node = next(child for child in object_creation_expression_node.children if child.type == "new")
                class_name = get_class_name(new_function_node, java_code)
                instance_name = get_instance_name(new_function_node, java_code)
                argument_list = get_argument_list(new_function_node, java_code)
                instance_class_map[instance_name] = class_name
                diagram_data.append(
                    f"{execution_class_name} -> {class_name} : new{class_name}{argument_list}\n")
                diagram_data.append(f"activate {class_name}\n")
                diagram_data.append(
                    f"{class_name} --> {execution_class_name} : {class_name}\n")
                diagram_data.append(f"deactivate {class_name}\n")

        def get_method_invocation_and_new_method_diagram_data_in_if_statement(child, java_code, is_root):
            for if_child in child.children:
                if if_child.type == "condition":
                    if is_root: prefix = "alt"
                    else: prefix = "else"
                    condition_code = java_code[if_child.start_byte:if_child.end_byte]
                    if len(condition_code) > 0:
                        diagram_data.append(
                            prefix + " " + java_code[if_child.start_byte:if_child.end_byte][1:-1].strip() + "\n")
                    else:
                        diagram_data.append(prefix + " " + "other condition" + "\n")
                if if_child.type == "block":
                    # When it is block of else
                    if child.parent.children[if_child.parent.children.index(if_child) - 1].type == "else":
                        diagram_data.append("else other condition" + "\n")
                    if_code = java_code[if_child.start_byte:if_child.end_byte][1:-1].strip()
                    if_node = parser.parse(bytes(if_code, 'utf8')).root_node
                    for expression_node in if_node.children:
                        for method_invocation_and_new_method_node in expression_node.children:
                            get_method_invocation_and_new_method_diagram_data(method_invocation_and_new_method_node,if_code)
                elif if_child.type == "if_statement":
                    get_method_invocation_and_new_method_diagram_data_in_if_statement(if_child, java_code, False)
        for child in node.children:
            if child.type == "if_statement":
                get_method_invocation_and_new_method_diagram_data_in_if_statement(child, java_code, True)
                diagram_data.append("end" + "\n")
            elif child.type == "for_statement" or child.type == "while_statement":
                loop_block = next(child for child in child.children if child.type == "block")
                diagram_data.append("loop" + "\n")
                loop_code = java_code[loop_block.start_byte:loop_block.end_byte][1:-1].strip()
                loop_node = parser.parse(bytes(loop_code, 'utf8')).root_node
                for expression_node in loop_node.children:
                    for method_invocation_and_new_method_node in expression_node.children:
                        get_method_invocation_and_new_method_diagram_data(method_invocation_and_new_method_node,
                                                                          loop_code)
                diagram_data.append("end" + "\n")
            else:
                for method_invocation_and_new_method_node in child.children:
                    get_method_invocation_and_new_method_diagram_data(method_invocation_and_new_method_node, java_code)

    diagram_data.append(f"activate {execution_class_name}\n")
    # Traverse the tree
    traverse(root_node)
    diagram_data.append(f"deactivate {execution_class_name}\n")
    return diagram_data


def create_sequence_diagram(diagram_data):
    sequence_diagram = graphviz.Digraph(format='png')
    java_file_path = JAVA_FILE_PATH
    extract_class_method_return_type(java_file_path)

    my_file = open("Diagrams/MySequenceDiagram.puml", "w+")
    my_file.write("@startuml\n")

    for string_data in diagram_data:
        my_file.write(string_data)

    my_file.write("@enduml")
    my_file.close()


java_file_path = JAVA_FILE_PATH
diagram_data = extract_class_method_call_data_from_java_file(java_file_path, EXECUTION_CLASS_NAME, EXECUTION_METHOD_NAME)
create_sequence_diagram(diagram_data)
