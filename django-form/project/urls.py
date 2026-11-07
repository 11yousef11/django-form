from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from pages import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.add_student, name='add_student'),
    path('students/', views.student_list, name='student_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
