from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import logout


class UpdateLastActiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)


        if request.user.is_authenticated:
            request.user.last_active_datetime = timezone.now()
            request.user.save(update_fields=['last_active_datetime'])

        return response

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = timezone.now()

            if request.user.last_active_datetime:
                inactive_duration = now - request.user.last_active_datetime
                if inactive_duration > timedelta(minutes=1):
                    logout(request)
                else:

                    request.user.last_active_datetime = now
                    request.user.save()
            else:

                request.user.last_active_datetime = now
                request.user.save()

        response = self.get_response(request)
        return response