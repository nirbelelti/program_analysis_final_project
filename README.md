# Program Analysis Sequence Diagram
## use of the program
### Static Analysis
#### 1. Run the program
```bash
$ cd src
$ python3 static_sequence_diagram.py
```

### Dynamic Analysis
#### 1. Run the program
```bash
$ cd src  
$ python3 dynamic_sequens_diagram.py
```
#### 2. Run the test
```bash
$ cd tests
$ python3 test_call_method.py
$ python3 test_has_return_type.py

```
## Use of plantuml
when you run the program, the program will generate a file called "sequence_diagram.puml" in the Diagrams folder.
You can use the plantuml site to generate the sequence diagram by uploading the file content or install plantuml addon on your idea.
you can find the plantuml site here: http://www.plantuml.com/plantuml/uml/SyfFKj2rKt3CoKnELR1Io4ZDoSa70000

## Output files
### Static Analysis and Dynamic Analysis
the output files are located in the Diagrams folder,
the file name is MySequenceDiagram.puml for static analysis and MyDynamicSequenceDiagram.puml for dynamic analysis.

## Chenge the input file
you can change the input file by changing the path in the main function in the static_sequence_diagram.py file and the dynamic_sequens_diagram.py file.