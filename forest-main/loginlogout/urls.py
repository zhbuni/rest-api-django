from django.urls import path
from .views import Record, Login, Logout, TokenRecord

urlpatterns = [
    path('addUser/', Record.as_view(), name="register"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('token/', TokenRecord.as_view(), name='token')
]
