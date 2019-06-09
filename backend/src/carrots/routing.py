from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.conf.urls import url

from ws.echo_consumer import EchoConsumer

routes = [
    url(r'echo/$', EchoConsumer), 
]

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(URLRouter(routes)),
})
