







from rest_framework.routers import DefaultRouter

from apps.contacts.api.views import ContactView

router = DefaultRouter()

router.register("", ContactView,basename="contact")

urlpatterns = router.urls