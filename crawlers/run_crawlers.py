import os
dirname, filename = os.path.split(os.path.abspath(__file__))
for f in os.listdir(dirname):
    dirname, filename = os.path.split(f)
    if f.endswith('.py'):
        if filename not in ['__init__.py', 'run_crawlers.py', 'seattle_police_internal_affairs_closed_case_summaries.py']:
            os.system('python %s &' % (f))