# wget -q -O - https://raw.githubusercontent.com/peoplesnsallc/peoples_nsa_api/master/install.py | sudo python
import os

os.system('sudo apt-get install git')
os.system('sudo apt-get install rethinkdb')
os.system('git clone https://github.com/peoplesnsallc/peoples_nsa_api.git')
os.system('cd peoples_nsa_api; python update.py')
