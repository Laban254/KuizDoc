from django.urls import path, include
from .views import uploadDoc, summalizedoc

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('docupload', uploadDoc, basename='docupload')

urlpatterns = [
    
    path('upload/', include(router.urls) ),
    path('summarize/<int:id>/', summalizedoc.as_view(), name='summarize'),
]