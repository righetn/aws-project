from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import CarModel, CarBrand, Car

# Create your tests here.
class APITestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        self.c = Client()
        logged_in = self.c.login(username='testuser', password='12345')
        self.assertTrue(logged_in)

        self.car_brand = CarBrand.objects.create(name='peugeot')
        self.car_model = CarModel.objects.create(brand=self.car_brand, name='206', production_year=1998, price=5000)

    def test_add_model(self):
        response = self.c.post('/add_model', {
            'brand_name': 'reunault',
            'model_name': 'Megane',
            'production_year': 2005,
            'price': 5000
        })
        self.assertTrue(response.status_code == 200 or response.status_code == 302)
        try:
            CarBrand.objects.get(name='reunault')
        except CarBrand.DoesNotExist:
            self.fail("Brand has not been created")
        try:
            CarModel.objects.get(name='Megane')
        except CarModel.DoesNotExist:
            self.fail("Model has not been created")

    def test_delete_model(self):
        car_brand = CarBrand.objects.create(name='renault')
        car_model = CarModel.objects.create(brand=car_brand, name='laguna', production_year=2005, price=5000)
        car = Car.objects.create(model=car_model, price=5000, occasion=False)

        response = self.c.get('/remove_model/' + str(car_model.pk))
        self.assertTrue(len(Car.objects.filter(model=car_model)) == 0)
        try:
            CarModel.objects.get(pk=car_model.pk)
            self.fail("Model has not been removed")
        except CarModel.DoesNotExist:
            self.assertEqual(0, 0)

    def test_add_car(self):
        nb_car = len(Car.objects.filter(model=self.car_model))
        response = self.c.post('/add_car/' + str(self.car_model.pk), {
            'model': self.car_model,
            'price': 5000,
            'occasion': False,
            'number': 1
        })
        self.assertTrue(response.status_code == 200 or response.status_code == 302)
        self.assertTrue(len(Car.objects.filter(model=self.car_model)) == nb_car + 1)

    def test_remove_car(self):
        car = Car.objects.create(model=self.car_model, price=5000, occasion=False)
        response = self.c.get('/remove_car/' + str(self.car_model.pk) + '/' + str(car.pk))

        try:
            Car.objects.get(pk=car.pk)
            self.fail("Car has not been removed")
        except Car.DoesNotExist:
            self.assertEqual(0, 0)