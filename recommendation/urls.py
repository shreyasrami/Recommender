from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from .views import RegisterUserView, LoginUserView, RecommendView, UserDetailsView


schema_view = get_schema_view(
    openapi.Info(
        title="Recommendation System API",
        default_version="v3",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

    path('',schema_view.with_ui("swagger", cache_timeout=0),name="schema-swagger-ui",),
    path('user/register/', RegisterUserView.as_view(),name='register_user'),
    path('user/login/', LoginUserView.as_view(), name='token_obtain_pair'),
    path('user-details/<user_id>', UserDetailsView.as_view(), name='user_details'),
    path('recom/', RecommendView.as_view(), name='recommendation')
]
