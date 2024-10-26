# main/context_processors.py

from django.templatetags.static import static

def navbar_links(request):
    links = {
        "home": {
            "url": "/", 
            "filename": "home_icon.html"
        },
        "stores": {
            "url": "/stores/", 
            "filename": "store_icon.html"
        },
        "chats": {
            "url": "/chats/", 
            "filename": "chat_icon.html"
        },
        "history": {
            "url": "/history/", 
            "filename": "history_icon.html"
        },

    }
    return {'links': links}