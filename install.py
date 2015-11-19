# wget -q -O - https://raw.githubusercontent.com/peoplesnsallc/peoples_nsa_api/master/install.py | sudo python
import os

os.system('sudo apt-get -y install git')
os.system('source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list')
os.system('wget -qO- https://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -')
os.system('sudo apt-get -y update')
os.system('sudo apt-get -y install rethinkdb')
os.system('git clone https://github.com/peoplesnsallc/peoples_nsa_api.git')
os.system('cd peoples_nsa_api; python update.py')
