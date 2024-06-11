from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)

router = DefaultRouter()


# from .views import StripeCheckoutView
# from .models import (
#     Survey,
#     Question,
#     Track,
#     # QuestionTrack,
#     Option,
#     Result
# )


router.register(r'survey', views.SurveyViewSet, basename='survey')
router.register(r'question', views.QuestionViewSet, basename='question')
router.register(r'track', views.TrackViewSet, basename='track')
router.register(r'option', views.OptionsViewSet, basename='option')
router.register(
    r'result/(?P<survey_name>[^/]+)/(?P<track_id>[0-9]+)', views.ResultViewSet, basename='result')
router.register(r'survey/(?P<survey_name>[^/]+)/questions',
                views.QuestionViewSet, basename='survey-questions')
router.register(r'question/(?P<question_id>[0-9]+)/options',
                views.OptionsViewSet, basename='question-option')


urlpatterns = [
    path('apioverview/', views.APIOverview),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('stripe/checkout/', views.StripeCheckoutView.as_view(),
         name='stripe_checkout'),
    path('stripe/products/', views.StripeProductView.as_view()),
    path('stripe/orders/', views.StripeOrdersView.as_view()),
    path('stripe/checkout/products/', views.get_list_on_chekout),
    path('stripe/treatments/products/', views.get_products_with_categories),
    path('partnerships-is-open/', views.button_status_api),
    path('partnerships-update/', views.update_button_status),
    path('contact-information/', views.get_info_contact),
    path('', include(router.urls)),

]
