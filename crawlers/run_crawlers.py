import os
dirname, filename = os.path.split(os.path.abspath(__file__))
for f in os.listdir(dirname):
    dirname, filename = os.path.split(f)
    if f.endswith('.py'):
        if filename not in ['__init__.py', 'run_crawlers.py', 