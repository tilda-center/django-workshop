import factory
from django.contrib.auth.models import User
from factory import Faker

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = Faker('first_name', locale='en_US')
    last_name = Faker('last_name', locale='en_US')
    username = factory.Sequence(lambda n: f'user_{n}')
    email = Faker('email')

    @classmethod
    def create_with_password(cls, password='test123123!'):
        user = cls.create()
        user.set_password(password)
        user.save()
        return user

