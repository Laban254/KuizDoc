from django.urls import path, include
from . import views
from .views import uploadDoc

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('docupload', uploadDoc, basename='docupload')

urlpatterns = [
    
    path('upload/', include(router.urls) ),
    path('summarize/<int:id>/', views.summalizedoc.as_view(), name='summarize'),
]