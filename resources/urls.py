from rest_framework import routers
from resources.views.color import Color
from resources.views.static_design import StaticDesign


router = routers.DefaultRouter()
router.register(r'^color', Color)
router.register(r'^static_design', StaticDesign)
