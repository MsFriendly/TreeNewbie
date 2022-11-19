import json

with open('/Users/amyliu19/Downloads/PasadenaUrbanTrees_Detection/PasadenaUrbanTrees/detection_datasets.json') as f:
    data = json.load(f)
with open('/Users/amyliu19/Downloads/PasadenaUrbanTrees_Detection/PasadenaUrbanTrees/detection_datasets.json', 'w') as f:
    json.dump(data, f, indent=2)