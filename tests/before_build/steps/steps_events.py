import yaml
import datetime
import urllib2
import re
import glob
from behave import *

urlregex = re.compile(
    r'^(?:http)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
    r'localhost|' # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

@given('an event added')
def step_impl(context):
	pass

@then('event files must exist')
def step_impl(context):
    files = glob.glob('_events/*.md')
    all_events = []
    for f in files:
        stream = open(f, "r")
        events = yaml.load_all(stream)
        for event in events:
            assert isinstance(event, dict), "event data must exist"
            all_events.append((f,event))
            break
	context.events = all_events

@then('all mandatory event fields must exist and be valid')
def step_impl(context):

    mandatory_fields = ['layout', 'title', 'description', 'datelocation']
    for f,event in context.events:
        print ("Evaluating "+str(f))
        for field in mandatory_fields:
            assert event.get(field), "'"+field+"' value is missing"

        if event.get('archive'):
            assert event.get('archive').get('photos_url'), "'photos_url' value is missing"
            assert urlregex.match(event.get('archive').get('photos_url')), "'photos_url' value is not a valid URL"

            assert event.get('archive').get('videos_url'), "'videos_url' value is missing"
            assert urlregex.match(event.get('archive').get('videos_url')), "'videos_url' value is not a valid URL"

        if event.get('overview'):
            assert (
                (event.get('overview').get('left_content') and event.get('overview').get('right_content') and event.get('overview').get('center_content'))
                or
                (event.get('overview').get('left_content') and event.get('overview').get('right_content'))
                or
                (event.get('overview').get('center_content'))
                ), "'overview' value is wrong"
