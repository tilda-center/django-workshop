import factory

from v1.models import VerifyToken

class VerifyTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VerifyToken
    used = False
    email = factory.Faker('email')
