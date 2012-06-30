from django.utils import simplejson
from dajaxice.core import dajaxice_functions

def myexample(request, pid):
    return simplejson.dumps({'message':'You said %s!' % pid})

dajaxice_functions.register(myexample)