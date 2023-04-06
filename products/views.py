from datetime import datetime

from django.shortcuts import HttpResponse, redirect, render

from products.costans import PAGINATION_LIMIT
from products.forms import ProductCreateForm
from products.models import Product


def hello(request):
    if request.method == "GET":
        return HttpResponse("hello, its my first project! Enjoy! :)")


def now_date(request):
    now_time = datetime.now()
    if request.method == "GET":
        return HttpResponse(now_time)


def goodbye(request):
    if request.method == "GET":
        return HttpResponse("Goodbye user!")


def main_view(request):
    if request.method == "GET":
        return render(request, "layouts/index.html")


def products_view(request):
    if request.method == "GET":
        products = Product.objects.all()
        search = request.GET.get("search")
        page = int(request.GET.get("page", 1))

        """starts_with, ends_with, icontains"""

        if search:
            products = products.filter(title__icontains=search) | products.filter(description__icontains=search)

        max_page = products.__len__() / PAGINATION_LIMIT
        max_page = round(max_page) + 1 if round(max_page) < max_page else round(max_page)

        """products splice"""
        products = products[PAGINATION_LIMIT * (page - 1) : PAGINATION_LIMIT * page]

        context = {"products": products, "user": request.user, "pages": range(1, max_page + 1)}
        return render(request, "products/products.html", context=context)


def products_detail_view(request, id):
    if request.method == "GET":
        product = Product.objects.get(id=id)
        context = {"product": product, "review": product.review_set.all(), "user": request.user}
        return render(request, "products/detail.html", context=context)


def product_create_view(request):
    if request.method == "GET":
        context = {"form": ProductCreateForm}
        return render(request, "products/create.html", context=context)

    if request.method == "POST":
        form = ProductCreateForm(request.POST, request.FILES)

        if form.is_valid():
            Product.objects.create(
                name=form.cleaned_data.get("name"),
                description=form.cleaned_data.get("description"),
                price=form.cleaned_data.get("price"),
                image=form.cleaned_data.get("image"),
            )
            return redirect("/products/")
        return render(request, "products/create.html", context={"form": form})
