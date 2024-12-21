import json
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
from django.views.decorators.csrf import csrf_exempt

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
            # user becomes owner
            request.user.role = "store_owner"
            request.user.save()
            data = {
                'html': render_to_string('search_stores.html', {'stores': Store.objects.filter(owner_id=request.user)}),
            }
            return JsonResponse(data) 

    else:
        form = StoreForm()

    return JsonResponse({'error': 'Invalid request'}, status=400)

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Store
import json
import base64
from django.core.files.base import ContentFile

@csrf_exempt
def register_store_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            photo_upload = data.get('photo_upload', "")
            if photo_upload:
                format, imgstr = photo_upload.split(';base64,') 
                ext = format.split('/')[-1] 
                photo_upload = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            else:
                photo_upload = None

            # Create a new store
            new_store = Store.objects.create(
                owner_id=request.user,
                name=data["name"],
                location=data["location"],
                description=data["description"],
                photo_upload=photo_upload,
                photo=data.get("photo", ""),
            )

            new_store.save()
            return JsonResponse({"status": "success"}, status=200)

        except KeyError as e:
            # Handle error if any field is missing
            return JsonResponse({"status": "error", "message": f"Missing field: {str(e)}"}, status=400)
        except Exception as e:
            # Handle other errors
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Invalid HTTP method"}, status=405)
    
@csrf_exempt
def edit_store_flutter(request, store_id):
    if request.method == 'POST':
        store = get_object_or_404(Store, id=store_id)
        data = json.loads(request.body)
        store.name = data.get('name', store.name)
        store.location = data.get('location', store.location)
        store.description = data.get('description', store.description)
        store.photo_upload = data.get('photo_upload', store.photo_upload)
        store.photo = data.get('photo', store.photo)
        store.save()
        return JsonResponse({'status': 'success', 'message': 'Store updated successfully'})
    else:
        return JsonResponse({"status": "error", "message": "Invalid HTTP method"}, status=405)

@csrf_exempt
def delete_store_flutter(request, store_id):
    print(2)
    store = get_object_or_404(Store, id=store_id)
    store.delete()
    return JsonResponse({'status': 'success', 'message': 'Store deleted successfully'})

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
    print(request.user)
    data = Store.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Store.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Store.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def show_json_by_owner(request):
    print(request.user)
    data = Store.objects.filter(owner_id=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
