from rest_framework.exceptions import NotFound, PermissionDenied
from .custom_valid import The_object_already_exists


def get_object_or_404(klass, *args, **kwargs):
    try:
        return  klass.objects.get(*args, **kwargs)
    except:
        raise NotFound("Нет объекта %s с id %d" % (klass.__name__, kwargs["id"]))

def get_object_or_403(klass, *args, **kwargs):
    try:
        return  klass.objects.get(*args, **kwargs)
    except:
        raise PermissionDenied("Нет объекта %s с id %d" % (klass.__name__, kwargs["id"]))

def get_object_or_409(klass, field, *args, **kwargs):
    try:
        klass.objects.get(*args, **kwargs)
        raise The_object_already_exists("Объект %s с параметрами %s уже сущетвует" % (klass.__name__, field))
    except klass.DoesNotExist:
        return True


def get_M2M_or_404(klass, name, **kwargs):
    try:
        return  klass.get(**kwargs)
    except:
        raise NotFound("Нет объекта c id %s в списке %s" % (kwargs["id"], name))
