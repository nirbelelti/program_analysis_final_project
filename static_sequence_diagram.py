import re
import graphviz
# import plantuml


def extract_regular_methods_from_java_file(file_path):
    with open(file_path, 'r') as java_file:
        java_code = java_file.read()

    # Define a regular expression pattern to match entire Java methods
    method_pattern = r'((public|private|protected|static)\s+\w+\s+\w+\s*\(.*?\)\s*{.*?})'


    # Use regular expressions to find and extract entire methods
    methods = re.findall(method_pattern, java_code, re.DOTALL)  # Use re.DOTALL to match across multiple lines

    # Filter out the main method
    regular_methods = [method for method in methods if 'static void main' not in method[0]]


    # Return the list of extracted regular methods
    return regular_methods

def extract_class_name_from_java_file(file_path):
    with open(file_path, 'r') as java_file:
        java_code = java_file.read()

    class_pattern = r'class\s+(\w+)\s*{'
    # Extract the class name from the file
    class_match = re.search(class_pattern, java_code)
    class_name = class_match.group(1) if class_match else "UnknownClass"

    return class_name


def has_return_type(method_definition):
    # Define a regular expression pattern to match a return type
    return_type_pattern = r'\s+(\w+)\s+\w+\(.*\)\s*{'

    # Use regular expressions to find and extract the return type
    return_statement_match = re.search(return_type_pattern, method_definition)

    if return_statement_match:
        return_object = return_statement_match.group(1)
        return return_object is not None, return_object
    else:
        return False, None

def create_sequence_diagram(methods):
    # Create a new Graphviz Digraph
    sequence_diagram = graphviz.Digraph(format='png')
   # print(methods)

    class_name = extract_class_name_from_java_file('java/Main.java')
    my_file = open("Diagrams/MySequenceDiagram.puml", "w+")
    my_file.write("@startuml\n")

    #Define participants (actors) as nodes
    participants = set()
    print(methods)
    for method in methods:
        participant = method[0].split()[2]  # Extract method name
        participants.add(participant)
        if has_return_type(method[0])[1]!='void':
            my_file.write("System ->" + str(class_name) +":"+ str(participant)+"\n") # Add a node for the system call to participant
            my_file.write(str(class_name) + " --> System:" + has_return_type(method[0])[1] + "\n") # Add a node for the participant return value to the system
        else:
            my_file.write(str(class_name) + " -> " + str(class_name) +":"+ str(participant)+"\n") # Add a node for method call on participant without return value
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
java_file_path = 'java/Engine.java'
method_list = extract_regular_methods_from_java_file(java_file_path)
create_sequence_diagram(method_list)
