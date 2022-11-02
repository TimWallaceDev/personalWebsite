"""
WSGI config for timwallace project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os, sys
sys.path.append('/home/pi/websites/timwallace/timwallace')

sys.path.append('/home/pi/websites/timwallace/timwallace/entries')

sys.path.append('/home/pi/websites/timwallace/venv/lib/python3.9/site-packages')

sys.path.append('/usr/lib/python3/dist-packages')


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timwallace.settings')

application = get_wsgi_application()
