import json



def has_returned_object_type(bytecode, class_name):
    for instruction in bytecode:
        if instruction["opr"] == "return" and instruction["type"] is not None:
            return True, instruction["type"]
    return False, None

def call_method(bytecode, method_name, caller_class):
    for instruction in bytecode:
        if instruction["opr"] == "invoke":
            invoked_class_name = instruction.get("method",{}).get("ref",{}).get("name")
            invoked_method_name = instruction.get("method",{}).get("name")

            if invoked_class_name:
                if 'java/' in invoked_class_name:
                    continue
                if caller_class:
                    my_file.write( caller_class.capitalize() + " -> " + invoked_class_name.capitalize() + " : " + invoked_method_name+"()" + "\n")
                    my_file.write(invoked_class_name.capitalize() + " --> " + invoked_class_name.capitalize() +" : " + invoked_method_name +"\n")

def create_sequence_diagram(data_dict, my_file):
    my_file.write("@startuml\n")
    class_name = data_dict["name"].replace("/", "_")  # solv problem with / in name in plantuml

    def process_method(method, caller_class):
        method_name = method['name']
        bytecode = method["code"]["bytecode"]
        returns_object, return_type = has_returned_object_type(bytecode, caller_class)
        calling_method = "Actor" if returns_object else caller_class

        my_file.write(calling_method.capitalize() + " -> " + caller_class.capitalize() + " : " + method_name + "()\n")
        call_method(bytecode, method_name, method_name)

        if returns_object:
            my_file.write(calling_method.capitalize() + " <-- " + caller_class.capitalize() + " : " + str(return_type) + "\n")

        for instruction in bytecode:
            if instruction["opr"] == "invoke":
                class_name = instruction.get("method",{}).get("ref",{}).get("name")
                if class_name:
                    if "java/" in class_name or "Java/" in class_name:
                       continue
                else:
                    continue


    for method in data_dict['methods']:
        class_name = data_dict["name"].replace("/", "_")
        process_method(method, class_name)

    my_file.write("@enduml")
    my_file.close()


if __name__ == '__main__':
    with open('java/json_bytcode/Car.json', 'r') as f:
        data_dict = json.load(f)

    with open("Diagrams/MyDynamicSequenceDiagram.puml", "w") as my_file:
        create_sequence_diagram(data_dict, my_file)
