import json

def has_returned_object_type(bytecode):
    for instruction in bytecode:
        if instruction["opr"] == "return" and instruction["type"] is not None:
            return True, instruction["type"]
    return False, None

def create_sequence_diagram(data_dict):

    my_file = open("Diagrams/MyDynamicSequenceDiagram.puml", "w+")
    my_file.write("@startuml\n")

    class_name = data_dict["name"].replace("/", "_")  # solv problem with / in name in plantuml
    for method in data_dict['methods']:

        method_name = method['name']
        bytecode = method["code"]["bytecode"]
        returns_object, return_type = has_returned_object_type(bytecode)
        calling_method = "actor" if returns_object else class_name
        my_file.write( calling_method+" -> " + class_name + " : "+ str(method_name)+"()\n")

        if returns_object:
            my_file.write( calling_method + " <-- " + class_name + " : " + str(return_type) + "\n")

    my_file.write("@enduml")
    my_file.close()



if __name__ == '__main__':
    with open('java/json_bytcode/Simple.json', 'r') as f:
        data_dict = json.load(f)

    create_sequence_diagram(data_dict)