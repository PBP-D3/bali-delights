# main/context_processors.py

from django.templatetags.static import static

def navbar_links(request):
    links = {
        "products": {
            "url": "/products", 
            "filename": "home_icon.html",
            "user_only": False
        },
        "stores": {
            "url": "/stores/", 
            "filename": "store_icon.html",
            "user_only": False
        },
        "chats": {
            "url": "/chats/", 
            "filename": "chat_icon.html",
            "user_only": True
        },
        "history": {
            "url": "/carts/history/", 
            "filename": "history_icon.html",
            "user_only": True
        },
    }
    return {'links': links}