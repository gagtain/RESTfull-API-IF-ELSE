from django.urls import path, register_converter
from .view import users, location, animals, animals_type, animals_locations, animals_type_in_animals

# расширение базового int на отрицательные числа
class NegativeIntConverter:

    regex = '-?\d+'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%d' % value

register_converter(NegativeIntConverter, 'negint')

urlpatterns = [
    path('accounts/<negint:pk>', users.UserAPI.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
    path('locations/<negint:pk>', location.LocationAPI.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
    path('locations', location.LocationAPI.as_view({'post':'create'})),
    path('animals/types/<negint:pk>', animals_type.AnimalTypeAPI.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
    path('animals/types', animals_type.AnimalTypeAPI.as_view({'post':'create'})),
    path('animals', animals.AnimalAPI.as_view({'post':'create'})),
    path('animals/<negint:pk>', animals.AnimalAPI.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
    path('animals/<negint:pk>/locations', animals_locations.AnimalLocationAPI.as_view({'get':'search_in_obj', 'put':'update'})),
    path('animals/<negint:pk>/locations/<negint:pointId>',
         animals_locations.AnimalLocationAPI.as_view({'post':'create','put':'update', 'delete':'destroy'})),
    path('animals/<negint:pk>/types/<negint:typeId>',
         animals_type_in_animals.AnimalTypeInAnimalsAPI.as_view({'post':'create','put':'update', 'delete':'destroy'})),
    path('animals/<negint:pk>/types',
         animals_type_in_animals.AnimalTypeInAnimalsAPI.as_view({'put':'update','post':'create'})),
    path('registration', users.RegistrationsAPI.as_view({'post':'create'})),
    path('accounts/search', users.UserAPI.as_view({'get':'search'})),
    path('animals/search', animals.AnimalAPI.as_view({'get':'search'})),
]