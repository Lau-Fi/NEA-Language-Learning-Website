"""
ASGI config for djangotemplates project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os # imports the OS libarary so the users can run the environment. 

from channels.auth import AuthMiddlewareStack 
from channels.routing import ProtocolTypeRouter, URLRouter # used within the ASGI application (for chatroom) protocol type router finds the protocol and the URL gets the URL
from channels.security.websocket import AllowedHostsOriginValidator # security to only accept allowed hosts, imported to find their origin
from django.core.asgi import get_asgi_application #from the django core library imports the ASGI application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangotemplates.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

import example.routing

#This is the protocol router to use websocketing and connect it with my django ASGI app 
#imported above. The http connects to this through a dictionary. The websocket = through the valid 
#host origin the URL router which routes my app called example with routing and the websocket URL patterns
#as its membership accessors. The url patterns are groups of urls that match a given pattern such as in my urls.py


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(example.routing.websocket_urlpatterns))
        ),
    }
)

