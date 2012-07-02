from django.utils import timezone

class TimezoneMiddleware(object):
    def process_request(self, request):
        if request.method == 'POST':
            tz = request.POST.get('user_tz', False)
            if tz:
                timezone.activate(tz)