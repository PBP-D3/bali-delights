from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import Store
from .forms import StoreForm
from products.models import Product
from django.core import serializers

def show_stores(request):
    stores = Store.objects.all()
    return render(request, 'stores.html', {'stores': stores})

@login_required(login_url="/login")
def show_user_store(request):
    # Get the current user
    user = request.user
    
    # Retrieve the store owned by the user
    stores = Store.objects.filter(owner_id=user.id)
    print(stores)
    
    return render(request, 'user_store.html', {'stores': stores})

@login_required(login_url="/login")
def register_store(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner_id = request.user
            store.save()
            return redirect('stores:show_user_store')  # Redirect to the store listing page after registration
    else:
        form = StoreForm()
    
    return render(request, 'register_store.html', {'form': form})

@login_required(login_url="/login")
def edit_store(request, id):
    store = get_object_or_404(Store, id=id)
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            return redirect('stores:show_user_store')
    else:
        form = StoreForm(instance=store)

    return render(request, 'edit_store.html', {'form': form, 'store': store})

@login_required
def delete_store(request, id):
    store = get_object_or_404(Store, pk=id)

    store.delete()
    return redirect('stores:show_user_store')
    

def show_store_details(request, id):
    store = get_object_or_404(Store, pk=id)
    products = Product.objects.filter(store_id=store)
    return render(request, 'show_store_details.html', {'store': store, 'products': products})

def owner_store_view(request, id):
    store = get_object_or_404(Store, pk=id)
    products = Product.objects.filter(store_id=store)
    return render(request, 'owner_store_view.html', {'store': store, 'products': products})

def show_xml(request):
    data = Store.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Store.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Store.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Store.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")



