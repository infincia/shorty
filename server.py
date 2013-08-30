from gevent import monkey; monkey.patch_all()

import platform
import json
import time
import logging
from operator import itemgetter

# pip packages
import gevent
import bottle; bottle.debug(mode=False)
from bottle import static_file
import shortuuid
from jinja2 import Undefined
from jinja2 import Environment
from jinja2 import FileSystemLoader


# used for quick storage of shortened urls in memory
import ultramemcache
memcache_client = ultramemcache.Client(['127.0.0.1:11211'], debug=False)

# could also use redis if you want to run this long term, memcache doesnt save anything to disk
# save_long_url() and get_long_url() would have to be rewritten to use redis in that case
#import redis
#redis_client = redis.StrictRedis()

# load templates
JINJA2_ENVIRONMENT_OPTIONS = { 'undefined' : Undefined }
# Hardcoded path here should probably be in a ConfigParser file.
jinja_environment = Environment(loader=FileSystemLoader('/opt/shorty/templates') )
INDEX_TEMPLATE = jinja_environment.get_template('index.html')


# separate functions for dealing with where and how short and long urls are handled, keeps it away from http routes
def save_long_url(long_url):
    try:
        short_url_id = shortuuid.uuid()[:8]
        memcache_client.set(short_url_id, long_url)
        return short_url_id
    except Exception as local_exception:
        logging.exception('Exception saving short url: %s', local_exception)
        return None

def get_long_url(short_url_id):
    try:
        long_url = memcache_client.get(short_url_id)
        return long_url
    except Exception as local_exception:
        logging.exception('Exception getting long url: %s', local_exception)
        return None
            

# create wsgi bottle app #
# ---------------------- #
shorty = bottle.Bottle()



# main site routes #
# ---------------- #

# serve static files directly so no webserver is needed during testing. This should never be reachable once Nginx is involved in serving the /static path, so it can remain enabled all the time.
@shorty.get('/static/<filepath:path>')
def server_static(filepath):
    # Hardcoded path here should probably be in a ConfigParser file.
    return static_file(filepath, root='/opt/shorty/static')


@shorty.get('/')
def index():
    return INDEX_TEMPLATE.render()


@shorty.get('/u/<short_url_id>')
@shorty.get('/u/<short_url_id>/')
def redirect_long_url(short_url_id):
    long_url = get_long_url(short_url_id)
    if long_url is not None:
        bottle.redirect(long_url)
    else:
        return bottle.abort(404,'URL not found')


# submission API, shorty.js submits here
@shorty.post('/api/url/submit')
def submit_long_url():
    submission_data = json.loads(bottle.request.body.readline())
    long_url = submission_data.get('url', None)
    if long_url is not None:
        short_url_id = save_long_url(long_url)
        return { 'success': True, 'short_url_id': short_url_id }
    else:
        # return a json dict with key 'success' set to false so javascript can show an error
        return { 'success': False }


# comment this line out if running under gunicorn
bottle.run(shorty, host='0.0.0.0', port=8080, server='gevent')

application = shorty
