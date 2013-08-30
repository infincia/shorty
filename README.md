###Shorty

Very simple url shortener written in about 15 minutes, designed to generate a new unique short URL every time a long URL is added. So if google.com is entered twice, you will get 2 different short URLs that both work correctly. This may be desirable for privacy or other reasons, but a configuration option could be added to change that behavior or make it selectable by the user (checkbox on the page + additional option in the submission API).

The short url generation is currently using a truncated 8 character uuid, which may lead to collisions in some (rare?) cases, and that could lead to overwriting any existing URL stored under that key. A better system can probably be found that still avoids having to keep a counter/state somewhere. Short uuids serve the purpose for now, and upgrading to something else in the future shouldn't cause backward compatibility problems as all stored urls would still be there and map correctly.

 The Python module 'short_url' was considered for the short url generation, but it is intended to be used alongside an auto-incrementing database id number rather than directly with an incoming URL (it takes a number as input and never actually touches the long URL).

####Setup

Shorty is intended for use on Linux or BSD, and the package names given in the instructions are from Ubuntu but it should work on others once the equivalent packages are installed. OSX running on a colocated Mini should work as a host too if you install the right packages via homebrew.

Python packages are pinned at the latest versions available during testing, update them when needed.

Make sure to install the right system packages as some python modules used here depend on native system libraries.

#####Install system packages

    sudo aptitude install -y libev-dev libevent-dev
    sudo aptitude install -y python-dev python-setuptools python-software-properties python-virtualenv python-pip
    sudo aptitude install -y memcached

#####Clone repo

    cd /opt/
    git clone https://github.com/infincia/shorty.git


#####Setup virtualenv, activate it and install python packages

    virtualenv /opt/shorty/env
    source /opt/shorty/env/bin/activate
    pip install -r /opt/shorty/requirements.txt
    
#####Run the development server, port 8080 by default
    
    source /opt/shorty/env/bin/activate
    cd /opt/shorty
    python server.py
    
#####Visit the local machines IP in a browser

    http://localhost:8080/
    
####Deploying this in public

The code is not setup by default for deployment to a public server that large numbers of people would be accessing. 

To do that, disable Bottles development server in setup.py (near end of file), use gunicorn or another application server and stick nginx in front of the whole thing so it can handle static files for you and take responsibility for dealing with communication with clients


####API
The backend is organized as an html+js interface, and a separate set of json API endpoints. The API could be called from somewhere other than the html+js included with the project if someone found that to be useful.

Note: where multiple elements or values of a request or response are possible, a single pipe '|' character implies 'or'

    Endpoint: /api/url/submit
    Request:  JSON { 'url': 'http://google.com' }
    Response: JSON { 'success': true|false, 'short_url_id': 'LhKWdeNp' }
    

    Endpoint: /api/url/resolve
    Request:  JSON { 'short_url': 'http://mysite.com/u/LhKWdeNp' | 'short_url_id': 'LhKWdeNp' }
    Response: JSON { 'success': true|false, 'url': 'http://google.com' }

