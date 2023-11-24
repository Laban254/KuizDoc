from django.urls import path, include
from .views import uploadDoc, summalizedoc, UserSignupView, UserLoginView, UserLogoutView, GenerateQuiz, AnswerQuiz, MyTokenObtainPairView, KuizDocUserView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('docupload', uploadDoc, basename='docupload')

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('upload/', include(router.urls) ),
    path('summarize/<int:id>/', summalizedoc.as_view(), name='summarize'),
    path('GenerateQuiz/<int:id>/', GenerateQuiz.as_view(), name='GenerateQuiz'),
    path('question/<int:id>/', AnswerQuiz.as_view(), name='AskQuestion'),
    path('login_kuizDoc/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', KuizDocUserView.as_view(), name='kuizDoc_register'),
]