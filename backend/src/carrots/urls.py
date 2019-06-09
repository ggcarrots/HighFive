"""carrots URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include
from django.urls import path
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import SimpleRouter

from golocals.api import CommentsAPI
from golocals.api import InitiativesAPI
# from webhooks.routers import webhook_router

v1_router = SimpleRouter(trailing_slash=False)
v1_router.register("initiatives", InitiativesAPI, "initiatives")
v1_router.register("comments", CommentsAPI, "comments")


def index(request):
    return HttpResponse('Ok')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    # path('webhooks/', include(webhook_router.urls)),
    path('v1/', include(v1_router.urls)),
    path('docs/', include_docs_urls(title='My API title')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
