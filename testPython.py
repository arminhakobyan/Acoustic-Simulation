import yaml

def index_2d(list, item):
    for i, x in enumerate(list):
        if item in x:
            return i, x.index(item)

with open('initial_configs.yaml') as f:
    d = yaml.safe_load(f)

a, _ = index_2d(d['Sources']['keys'], 'Source1')
print(a)
