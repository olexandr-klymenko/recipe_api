"""recipe_api URL Configuration"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

info = openapi.Info(
    title="Recipe API",
    default_version="v1",
    description="Test description",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="olexandr.klymenko@gmail.com"),
    license=openapi.License(name="BSD License"),
)
schema_view = get_schema_view(
    info, public=True, permission_classes=(permissions.AllowAny,), validators=["ssv"]
)


api_patterns = [path("v1/", include("restservice.urls"))]

urlpatterns = (
    api_patterns
    + [
        path("", RedirectView.as_view(pattern_name="schema-swagger-ui")),
        path(
            r"swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"
        ),
        path(
            r"swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            r"redoc", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
        ),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
