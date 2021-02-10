"""sc-master URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls import url
from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from app.views.commands.set_color import CmdSetColor
from app.views.commands.new_section import CmdNewSection
from app.views.commands.edit_section import CmdEditSection
from app.views.commands.turn_off import CmdTurnOff
from app.views.commands.reset import CmdReset
from app.views.commands.scrpi_connect import CmdScRpiConnect
from app.views.commands.scrpi_status import CmdScRpiStatus
from app.views.resources.color import ResrColor
from app.views.resources.color_comb import ResrColorCombination
from app.views.token import Token


schema_view = get_schema_view(
   openapi.Info(
      title="Strip Controller Master API",
      default_version='v1',
      contact=openapi.Contact(email="brunopiaggiok@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

resources = routers.DefaultRouter()

resources.register(r'color', ResrColor)
resources.register(r'color_combination', ResrColorCombination)

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^token', Token.as_view()),
    url(r'^commands/turn_off$', CmdTurnOff.as_view()),
    url(r'^commands/reset$', CmdReset.as_view()),
    url(r'^commands/set_color$', CmdSetColor.as_view()),
    url(r'^commands/new_section$', CmdNewSection.as_view()),
    url(r'^commands/edit_section$', CmdEditSection.as_view()),
    url(r'^commands/scrpi/connect$', CmdScRpiConnect.as_view()),
    url(r'^commands/scrpi/status$', CmdScRpiStatus.as_view()),
    url(r'^resources/', include(resources.urls)),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
