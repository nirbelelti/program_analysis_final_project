import re
import sys

# Java code
JAVA_FILE_PATH = "java/CarWithLoopAndIf.java"

# Read Java code from file
with open(JAVA_FILE_PATH, "r") as file:
    java_code = file.read()

# Define regular expressions to match class and method declarations
class_pattern = re.compile(r"\s*class\s+(\w+)\s*{")
method_pattern = re.compile(r"\s*(\w+)\s+(\w+)\s*\(([^)]*)\)\s*{")
constructor_pattern = re.compile(r"\s*(\w+)\s*=\s*new\s+(\w+)\(([^)]*)\)\s*;")

# Extract class, method, and constructor information
classes = class_pattern.findall(java_code)
methods = method_pattern.findall(java_code)
constructors = constructor_pattern.findall(java_code)

# Open the file for writing
with open("Diagrams/Syntactic.puml", "w+") as my_file:
    # Redirect standard output to the file
    sys.stdout = my_file

    # Print PlantUML header
    print("@startuml")

    # Identify constructor calls and generate PlantUML code
    for obj, class_type, obj_params in constructors:
        params = ', '.join(param.strip() for param in obj_params.split(','))
        print(f"Main -> {class_type} : {class_type}({params})")
        print(f"{class_type} --> Main : {obj}")

    # Print PlantUML footer
    print("@enduml")

    # Reset standard output
    sys.stdout = sys.__stdout__
