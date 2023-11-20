import json

def has_returned_object_type(bytecode, class_name):
    for instruction in bytecode:
        if instruction["opr"] == "return" and instruction["type"] is not None:
            return True, instruction["type"]
    return False, None

def call_method(bytecode, output_file, caller_class):
    arg_values = []
    for instruction in bytecode:
        if instruction["opr"] == "push":
            arg_values.append(instruction["value"])

        if instruction["opr"] == "invoke":
            invoked_class_name = instruction.get(
                "method", {}).get("ref", {}).get("name")
            invoked_method_name = instruction.get("method", {}).get("name")
            for name in instruction.get(
                    "method", {}).get("args"):
                if isinstance(name,
                              dict):  # Take to consideration arguments that are instances of class into the constractor.
                    if name.get('kind', {}) == 'class':
                        if name.get('name') and 'java/' not in name.get('name') and name.get(
                                'name') != invoked_class_name:
                            arg_values.append({'type': name.get('kind'), 'value': name.get('name')})

            if invoked_class_name:
                if 'java/' in invoked_class_name:
                    continue
                if caller_class:
                    values = ""
                    for value in arg_values:
                        values += (str(value['type']) + ": " + str(value['value']) + ", ")
                    #   Delete remain comma of the last parameter
                    if values[-2:] == ", ":
                        values = values[:-2]
                    output_file.write(caller_class.capitalize(
                    ) + " -> " + invoked_class_name.capitalize() + " : " + invoked_method_name + "(" + values + ")" + "\n")
                    output_file.write("activate " + invoked_class_name.capitalize() + "\n")
                    if invoked_method_name == '<init>':
                        output_file.write(invoked_class_name.capitalize(
                        ) + " --> " + caller_class.capitalize() + " : " + invoked_class_name + "\n")
                    else:
                        output_file.write(invoked_class_name.capitalize(
                        ) + " --> " + caller_class.capitalize() + " : " + invoked_method_name + "()\n")
                    output_file.write("deactivate " + invoked_class_name.capitalize() + "\n")
            arg_values = []


def create_sequence_diagram(data_dict, output_file):
    output_file.write("@startuml\n")
    class_name = data_dict["name"].replace("/", "_")  # solv problem with / in name in plantuml

    def process_method(method, caller_class):
        method_name = method['name']
                #############
        # if method_name != '<init>':
        #     output_file.write("activate " + method_name.capitalize() + "\n")
            ############
        bytecode = method["code"]["bytecode"]
        returns_object, return_type = has_returned_object_type(bytecode, caller_class)
        calling_method = "Actor" if returns_object else caller_class

        output_file.write(calling_method.capitalize() + " -> " + caller_class.capitalize() + " : " + method_name + "()\n")
        call_method(bytecode, output_file, method_name)

        if returns_object:
            output_file.write(
                calling_method.capitalize() + " <-- " + caller_class.capitalize() + " : " + str(return_type) + "\n")

        for instruction in bytecode:
            if instruction["opr"] == "invoke":
                class_name = instruction.get("method", {}).get("ref", {}).get("name")
                if class_name:
                    if "java/" in class_name or "Java/" in class_name:
                        continue
                else:
                    continue
                #########
        # if method_name != '<init>':
        #     output_file.write("deactivate " + method_name.capitalize() + "\n")
        #########

    for method in data_dict['methods']:
        class_name = data_dict["name"].replace("/", "_")
        process_method(method, class_name)

    output_file.write("@enduml")
    output_file.close()


if __name__ == '__main__':
    with open('java/json_bytcode/Car.json', 'r') as f:
        data_dict = json.load(f)

    with open("Diagrams/MyDynamicSequenceDiagram.puml", "w") as output_file:
        create_sequence_diagram(data_dict, output_file)
