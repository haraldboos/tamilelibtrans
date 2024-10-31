from .models import Impresm

def getImpre(request):
    try:

        inmpress = Impresm.objects.latest('update')
    except Impresm.DoesNotExist:
        inmpress=None
    return {'latest_impress_file': inmpress}
