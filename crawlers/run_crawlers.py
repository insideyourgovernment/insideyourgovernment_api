import os
dirname, filename = os.path.split(os.path.abspath(__file__))
for f in os.listdir(dirname):
    #dirname, filename = os.path.split(f)
    if f.endswith('.py'):
        if f not in ['__init__.py', 'run_crawlers.py', 'socrata_dataset_catalog.py']:
            os.system('python %s &' % (os.path.join(dirname, f)))