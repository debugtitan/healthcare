from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model

class BanUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_model = get_user_model()
        if request.user.is_authenticated and user_model.objects.filter(pk=request.user.pk, is_banned=True).exists():
            return HttpResponseForbidden("Your account has been banned.")
        return self.get_response(request)
