from django.conf.urls import url
from commands.views.sections.edit import Edit as EditSection
from commands.views.sections.add import Add as AddSection
from commands.views.sections.remove import Remove as RemoveSections
from commands.views.sections.turn_on import TurnOn as TurnOnSection
from commands.views.sections.turn_off import TurnOff as TurnOffSection
from commands.views.system.turn_on import TurnOn
from commands.views.system.turn_off import TurnOff
from commands.views.system.reset import Reset
from commands.views.system.connect_device import ConnectDevice
from commands.views.system.status import Status

urlpatterns = [
    url(r'^commands/system/turn_off$', TurnOff.as_view()),
    url(r'^commands/system/turn_on$', TurnOn.as_view()),
    url(r'^commands/system/reset$', Reset.as_view()),
    url(r'^commands/system/connect_device$', ConnectDevice.as_view()),
    url(r'^commands/system/status$', Status.as_view()),
    url(r'^commands/sections/add$', AddSection.as_view()),
    url(r'^commands/sections/remove$', RemoveSections.as_view()),
    url(r'^commands/sections/(?P<index>\d+)/edit$', EditSection.as_view()),
    url(r'^commands/sections/(?P<index>\d+)/turn_on$', TurnOnSection.as_view()),
    url(r'^commands/sections/(?P<index>\d+)/turn_off$', TurnOffSection.as_view())
]
