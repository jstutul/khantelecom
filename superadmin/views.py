import datetime
from shop.models import Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from cart.models import SellingList

# Create your views here.
from shop.forms import BillForm
from shop.models import MyBill, ProductPurchase


def getGraphForPurchase(purchase):
    purchasemonth = {
        "Jan": 0,
        "Feb": 0,
        "Mar": 0,
        "Apr": 0,
        "May": 0,
        "Jun": 0,
        "July": 0,
        "Aug": 0,
        "Sept": 0,
        "Oct": 0,
        "Nov": 0,
        "Dec": 0,
    }
    for i in purchase:
        if i.timestamp.month == 1:
            purchasemonth["Jan"] = i.price
        elif i.timestamp.month == 2:
            purchasemonth["Feb"] = i.price
        elif i.timestamp.month == 3:
            purchasemonth["Mar"] = i.price
        elif i.timestamp.month == 4:
            purchasemonth["Apr"] = i.price
        elif i.timestamp.month == 5:
            purchasemonth["May"] = i.price
        elif i.timestamp.month == 6:
            purchasemonth["Jun"] = i.price
        elif i.timestamp.month == 7:
            purchasemonth["July"] = i.price
        elif i.timestamp.month == 8:
            purchasemonth["Aug"] = i.price
        elif i.timestamp.month == 9:
            purchasemonth["Sept"] = i.price
        elif i.timestamp.month == 10:
            purchasemonth["Oct"] = i.price
        elif i.timestamp.month == 11:
            purchasemonth["Nov"] = i.price
        elif i.timestamp.month == 12:
            purchasemonth["Dec"] = i.price
        return purchasemonth


def getGraphForSelling(selling):
    selling_month = {
        "Jan": 0,
        "Feb": 0,
        "Mar": 0,
        "Apr": 0,
        "May": 0,
        "Jun": 0,
        "July": 0,
        "Aug": 0,
        "Sept": 0,
        "Oct": 0,
        "Nov": 0,
        "Dec": 0,
    }
    for i in selling:
        if i.sellingDate.month == 1:
            selling_month["Jan"] = i.amount
        elif i.sellingDate.month == 2:
            selling_month["Feb"] = i.amount
        elif i.sellingDate.month == 3:
            selling_month["Mar"] = i.amount
        elif i.sellingDate.month == 4:
            selling_month["Apr"] = i.amount
        elif i.sellingDate.month == 5:
            selling_month["May"] = i.amount
        elif i.sellingDate.month == 6:
            selling_month["Jun"] = i.amount
        elif i.sellingDate.month == 7:
            selling_month["July"] = i.amount
        elif i.sellingDate.month == 8:
            selling_month["Aug"] = i.amount
        elif i.sellingDate.month == 9:
            selling_month["Sept"] = i.amount
        elif i.sellingDate.month == 10:
            selling_month["Oct"] = i.amount
        elif i.sellingDate.month == 11:
            selling_month["Nov"] = i.amount
        elif i.sellingDate.month == 12:
            selling_month["Dec"] = i.amount

        return selling_month


def Dashboard(request):
    year=2022
    buy=0
    sell=0
    if request.method=="POST":
        print("POST")
        year=request.POST['yearname']
    print(year)
    purchase = ProductPurchase.objects.filter(timestamp__year=year)
    selling = SellingList.objects.filter(sellingDate__year=year)
    if purchase.count()>0 and selling.count()>0:
        getSellG=getGraphForSelling(selling)
        getPursG=getGraphForPurchase(purchase)

        sell=[]
        for key,val in getPursG.items():
            sell.append(val)
        buy=[]
        for key,val in getSellG.items():
            buy.append(val)

    contex={
        'getSellG':buy,
        'getPursG':sell,
        'year':year,
    }
    return render(request, 'dashboard/dashboard-sales.html',contex)


@login_required(login_url="App_Shop:login")
def SalesList(request):
    all_sales = SellingList.objects.all().order_by("-id")
    sellers = User.objects.all()
    sName = 0
    pNo = 0
    sDate, eDate = "", ""
    if request.method == "POST":
        sName = request.POST["sellerName"]
        sDate = request.POST["startDate"]
        eDate = request.POST["endDate"]
        pNo = request.POST["pageNo"]

        print(sDate, eDate)
        if sName != "":
            sName = int(sName)
            all_sales = all_sales.filter(seller_id=sName)
        if sDate != "":
            all_sales = all_sales.filter(sellingDate__gte=sDate)
        if eDate != "":
            all_sales = all_sales.filter(sellingDate__lte=eDate)
        if pNo != "":
            all_sales = all_sales[:int(pNo)]

    context = {
        'all_sales': all_sales,
        'sellers': sellers,
        'sellerName': sName,
        'sDate': sDate,
        'eDate': eDate,
        'pNo': pNo,
    }
    return render(request, 'dashboard/sales.html', context)


@login_required(login_url="App_Shop:login")
def AddExpense(request):
    mybill = MyBill.objects.all().order_by("-id")
    form = BillForm(request.POST or None)
    sellers = User.objects.all()
    sName = 0
    pNo = 0
    startDate, endDate = "", ""
    if request.method == "POST":
        if "filterForm" in request.POST:
            dateRange = request.POST['daterange']
            pNo = request.POST["pageNo"]
            sName = request.POST["sellerName"]

            if dateRange != "":
                dateSplit = dateRange.split(" to ")
                startDate = dateSplit[0]
                endDate = dateSplit[1]
                mybill = mybill.filter(timestamp__range=[startDate, endDate])
            if sName != "":
                sName = int(sName)
                mybill = mybill.filter(user_id=sName)

            if pNo != "":
                mybill = mybill[:int(pNo)]
        else:
            if form.is_valid():
                formData = form.save(commit=False)
                formData.user = request.user
                formData.save()
                messages.success(request, "Bill added successfully", extra_tags="bill_add")
                return redirect('App_Admin:addexpense')
    else:
        form = BillForm()
    context = {
        'form': form,
        'mybill': mybill,
        'sellers': sellers,
        'sellerName': sName,
        'sDate': startDate,
        'eDate': endDate,
        'pNo': pNo,
    }
    return render(request, 'dashboard/expenselist.html', context)


def CategoryView(request):
    category = Category.objects.all().order_by("-id")
    context = {
        'category': category,
    }
    return render(request, 'dashboard/category.html', context)
