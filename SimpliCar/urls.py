from django.contrib import admin
from django.urls import path, re_path
from django.urls import include

from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_jwt_token, name='create-token'),
    re_path('api/', include('book.urls')),
]
