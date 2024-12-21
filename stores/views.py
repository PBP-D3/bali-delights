from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import Store
from .forms import StoreForm
from products.models import Product
from django.core import serializers
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def show_stores(request):
    stores = Store.objects.all()
    return render(request, 'stores.html', {'stores': stores})

def load_all_stores(request):
    stores = Store.objects.all()
    html = render_to_string('search_stores.html', {'stores': stores, 'is_user_store_view': False})
    return JsonResponse({'html': html})

@login_required(login_url="/login")
def show_user_store(request):
    user = request.user
    stores = Store.objects.filter(owner_id=user)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('search_stores.html', {'stores': stores, 'is_user_store_view': True})
        return JsonResponse({'html': html})
    
    return render(request, 'stores.html', {'stores': stores, 'is_user_store_view': True})


def search_stores(request):
    query = request.GET.get("q", "")
    if query:
        stores = Store.objects.filter(name__icontains=query)
    else:
        stores = Store.objects.all()
    
    is_user_store_view = request.path == '/stores/show_user_store/'
    
    html = render_to_string('search_stores.html', {'stores': stores, 'is_user_store_view': is_user_store_view})
    return JsonResponse({"html": html})

@login_required(login_url="/login")
def register_store(request):
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner_id = request.user
            store.save()
<<<<<<< HEAD
=======
            # user becomes owner
            request.user.role = "store_owner"
            request.user.save()
>>>>>>> 96142267eefa9f39795c370ba55897f89fbaa7c9
            data = {
                'html': render_to_string('search_stores.html', {'stores': Store.objects.filter(owner_id=request.user)}),
            }
            return JsonResponse(data) 

    else:
        form = StoreForm()

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required(login_url="/login")
def edit_store(request, id):
    store = get_object_or_404(Store, id=id)
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            form.save()
            return redirect('stores:owner_store_view', store.id)
    else:
        form = StoreForm(instance=store)

    return render(request, 'edit_store.html', {'form': form, 'store': store})

@login_required
def delete_store(request, id):
    store = get_object_or_404(Store, pk=id)

    store.delete()
    return redirect('stores:show_stores')
    

def show_store_details(request, id):
  store = get_object_or_404(Store, pk=id)
  search_query = strip_tags(request.GET.get('search', ''))

  products = Product.objects.filter(store_id=store)
  if search_query:
      products = products.filter(name__icontains=search_query)

  return render(request, 'show_store_details.html', {'store': store, 'products': products})

def owner_store_view(request, id):
  store = get_object_or_404(Store, pk=id)
  search_query = strip_tags(request.GET.get('search', ''))

  products = Product.objects.filter(store_id=store)
  if search_query:
      products = products.filter(name__icontains=search_query)

  return render(request, 'owner_store_view.html', {'store': store, 'products': products, 'search_query': request.GET.get('search', ''),})

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

@login_required(login_url="/login")
def api_user_stores(request):
    """API untuk mengirimkan semua store yang dimiliki oleh user yang login."""
    user = request.user
    stores = Store.objects.filter(owner_id=user).values('id', 'name', 'photo', 'location', 'owner_id')
    return JsonResponse(list(stores), safe=False)

def api_store_details(request, id):
    """API untuk mengirimkan detail store berdasarkan ID."""
    store = get_object_or_404(Store, pk=id)
    data = {
        'id': store.id,
        'name': store.name,
        'photo': store.photo,
        'location': store.location,
        'owner_id': store.owner_id_id,  # Foreign key, ambil id pemiliknya
    }
    return JsonResponse(data)
