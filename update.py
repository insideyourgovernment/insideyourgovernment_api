import os

def update():
    fetch_dry_run_results = os.popen('git fetch --dry-run').read()
    os.popen('git fetch --all; git reset --hard origin/master').read()
    if not fetch_dy_run_results:
        return
    os.system('sudo pip install -r requirements.txt')

update()
