import os
dirname, filename = os.path.split(os.path.abspath(__file__))
for filename in os.listdir(dirname):
    if filename.endswith('.py'):
        if filename not in ['__init__.py', 'run_crawlers.py', 