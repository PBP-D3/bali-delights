# main/context_processors.py

from django.templatetags.static import static

def navbar_links(request):
    links = {
<<<<<<< HEAD
<<<<<<< HEAD
        "home": {
            "url": "/", 
=======
        "products": {
            "url": "/products", 
>>>>>>> 5a9e59f7027c96c63041055472554c90239d653d
=======
        "products": {
            "url": "/products", 
>>>>>>> f8b43257d2a50c14e7a6b1b8c4d61569b9cc8b77
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