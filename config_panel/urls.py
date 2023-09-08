from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import *

schema_view = get_schema_view(
   openapi.Info(
      title="Fantasy_game_api",
      default_version='v1',
      description="description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="gitech@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('bologin', bologinviewset.as_view()),
    path('getservertime', getservertimeviewset.as_view()),
    path('updatekyc', upd_kycdetailviewset.as_view()),
    path('kycdetail', kycdetailviewset.as_view()),
    path('contestsCreation', contestsCreationviewset.as_view()),
    path('contestwisesales', contestwisesalesviewset.as_view()),
    path('managementreport', managementreportviewset.as_view()),
    path('playerwiseledger', playerwiseledgerviewset.as_view()),
    path('gamewisesales', gamewisesalesdetailsviewset.as_view()),
    path('addmoneydetails', addmoneydetailsviewset.as_view()),
    path('withdrawdetails', withdrawdetailsviewset.as_view()),
    path('playertransactionsummary', playertransactionsummaryviewset.as_view()),
    path('playertransactiondetails', playertransactiondetailsviewset.as_view()),
    path('changepassword', changepasswordviewset.as_view()),
    path('UserBlockactive', UserBlockactiveviewset.as_view()),
    path('playerregistrationDetail', playerregistrationDetailviewset.as_view()),
    path('dashboard', dashboardviewset.as_view()),
    path('dashboardgamepayout',dashboard_gamepayout_viewset.as_view()),
    path('dashboardoverallpayout',dashboard_overallpayout_viewset.as_view()),
    path('dashboardswpt',getdashboardswptviewset.as_view()),
    path('dashboardmonthwisepayout',dashboard_monthwise_payout_viewset.as_view()),
    path('dashboardmonthwise',dashboard_monthwise_viewset.as_view()),
    path('swagger/', schema_view.with_ui('swagger')),
    path('swaggerdocs/', schema_view.with_ui('redoc')),

]
