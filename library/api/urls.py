from django.urls import path, include
from rest_framework import routers
from rest_framework.schemas import get_schema_view


from .views import BookApiView

router = routers.DefaultRouter()
router.register("book", BookApiView, "book_api")
urlpatterns = [
    path("", include(router.urls)),
    path(
        "openapi",
        get_schema_view(title="Library", description="API for all things …"),
        name="openapi-schema",
    ),
]
