import json

# open the JSON file
with open('tree_structure.json', 'r') as infile:
   
    json_data = json.load(infile)


tree_nodes = json.loads(json_data)

# iterate over the tree nodes and print the data for each node
for node in tree_nodes:
    print(node)
