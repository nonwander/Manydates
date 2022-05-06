from django.shortcuts import render

def index(request):
    context = {
        'index_title': 'WELCOME!',
        'index_text': 'my API-backend',
    }
    return render(request, 'index.html', context)

def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404,
    )

def server_error(request):
    return render(
        request,
        'misc/500.html',
        status=500
    )
