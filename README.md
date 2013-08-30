####Shorty

Very simple url shortener written in about 15 minutes, not designed to ensure that multiple identical URLs are shortened to the same short url (perhaps a desirable property for privacy?).

Make sure to setup the virtualenv and install the right system packages 

#####Setup

Intended for use on Linux, and these package names are from Ubuntu but it should work on OSX too if you install the right packages via homebrew

Python packages are pinned at the latest versions available during testing, update them when needed

######Install system packages

    sudo aptitude install -y libev-dev libevent-dev
    sudo aptitude install -y python-dev python-setuptools python-software-properties python-virtualenv python-pip
    sudo aptitude install -y memcached

######Clone repo

    cd /opt/
    git clone https://github.com/infincia/shorty.git


######Setup virtualenv, activate it and install python packages

    virtualenv /opt/shorty/env
    source /opt/shorty/env/bin/activate
    pip install -r /opt/shorty/requirements.txt
    
######Run the development server, port 8080 by default
    
    source /opt/shorty/env/bin/activate
    cd /opt/shorty
    python server.py
    
######Visit the local machines IP in a browser

    http://localhost:8080/
