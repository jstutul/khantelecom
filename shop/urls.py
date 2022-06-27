from django.urls import path
from shop import views
app_name="App_Shop"
urlpatterns = [
    path('',views.Shop,name="shop"),
    path('details/<int:id>',views.ProductDetails,name="singleproduct"),
    path('category/<int:id>',views.CategoryProducts,name="category"),
    path('login',views.Loginview,name="login"),
    path('loginout',views.LogOutview,name="logout"),
]