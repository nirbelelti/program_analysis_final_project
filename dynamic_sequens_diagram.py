import json

def create_sequence_diagram(data_dict):
    methods = stuck_of_executed_methods(data_dict)
    for method in methods:

        print('Method:', method)

def stuck_of_executed_methods(
        data_dict):  # Since we are incrementing our interpretation over various methods, it creates a list of methods.
    methods = []
    for obj in data_dict['methods']:
        methods.append(obj['name'])
    return methods


if __name__ == '__main__':
    with open('java/json_bytcode/Simple.json', 'r') as f:
        data_dict = json.load(f)

    create_sequence_diagram(data_dict)