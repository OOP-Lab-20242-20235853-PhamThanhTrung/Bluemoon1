
from django.contrib import admin
from django.urls import include, path
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('tamtrutamvang.urls')),
    path('nhankhau/', include('nhankhau.urls')),
    path('khoanthu/', include('khoanthu.urls')),
    path('noptien/', include('noptien.urls')),
    path('hokhau/', include('hokhau.urls')),
    path('register/', users_views.register, name='register'),
    path('login/', users_views.login_view, name='login'),
    path('logout/', users_views.logout_view, name='logout'),
]
