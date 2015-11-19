import os
import sys

def update(force=False):
    fetch_dry_run_results = os.popen('git fetch --dry-run').read()
    
    if not fetch_dry_run_results and not force:
        return
    os.popen('git fetch --all; git pull; git reset --hard origin/master').read()
    os.system('sudo pip install -r requirements.txt')
if 'force' in str(sys.argv):
    update(force=True)
else:
    update()
