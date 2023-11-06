import json

def create_sequence_diagram(data_dict):

    my_file = open("Diagrams/MyDynamicSequenceDiagram.puml", "w+")
    my_file.write("@startuml\n")

    class_name = data_dict["name"].replace("/", "_")  # solv problem with / in name in plantuml
    for method in data_dict['methods']:

        method_name = method['name']
        my_file.write( class_name+" -> " + class_name + " : "+ str(method_name)+"()\n")

    my_file.write("@enduml")
    my_file.close()



if __name__ == '__main__':
    with open('java/json_bytcode/Simple.json', 'r') as f:
        data_dict = json.load(f)

    create_sequence_diagram(data_dict)