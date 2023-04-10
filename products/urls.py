from django.urls import path

from products.views import CreateProductCBV, DateNowCBV, GoodbyeCBV, HelloCBV, MainCBV, ProductDetailCBV, ProductsCBV

urlpatterns = [
    path("products/", ProductsCBV.as_view()),
    path("", MainCBV.as_view()),
    path("hello/", HelloCBV.as_view()),
    path("goodbye/", GoodbyeCBV.as_view()),
    path("products/<int:id>/", ProductDetailCBV.as_view()),
    path("products/create/", CreateProductCBV.as_view()),
    path("now_date/", DateNowCBV.as_view()),
]
