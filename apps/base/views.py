from django.shortcuts import render


def view_404(request, exception=None):
    return render(request, 'errors/404.html', {})

def csrf_failure(request, reason=""):
    return render(request, 'errors/403.html', {})
