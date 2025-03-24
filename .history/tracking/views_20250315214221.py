from django.http import HttpResponse

def tracking_view(request):
    """A simple view for the tracking app."""
    return HttpResponse("Tracking App is working!")
