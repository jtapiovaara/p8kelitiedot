import requests
import datetime
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import City
from .forms import CityForm


def city(request):
    """Haetaan OpenWeatherMap tietoja eri kaupunkeihin. Kaupunkeja voi lisätä ja poistaa. Lisäksi esitetään Uudenmaan
    alueen neljän viimeisen tunnin sadetilanne Ilmailulaitoksen sääkartalla. Kaupunkikoodi 200 tunnistaaj,jos
    paikka on ylipäätään olemassa."""
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=88b98c1b6cdea2bfed07ed9333ba3790'
    # url = 'http://api.openweathermap.org/data/2.5/forecast?id=658225&units=metric&APPID=88b98c1b6cdea2bfed07ed9333ba3790'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                print(r)

                if r['cod'] == 200:
                    form.save()
                    # message = 'Onnistui!'
                    # messages.add_message(message='Kaupunki lisättiin', level=3)
                else:
                    err_msg='Kaupunkia ei ole olemassa!'
                    # messages.add_message(message='Kaupunkia ei ole olemassa!', level=2)
            else:
                err_msg = 'Kaupunki on jo tietokannassa!'
                # messages.add_message(message='Kaupunki on jo tietokannassa!', level=1)

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'Kaupunki lisättiin'
            message_class = 'is-success'
    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city,
            'temperature': r['main']['temp'],
            'feels_like': r['main']['feels_like'],
            'pressure': r['main']['pressure'],
            'speed': r['wind']['speed'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    weather_map_moment_1 = datetime.datetime.now() - timedelta(hours=3)
    weather_map_moment_2 = datetime.datetime.now() - timedelta(hours=4)
    weather_map_moment_3 = datetime.datetime.now() - timedelta(hours=5)
    weather_map_moment_4 = datetime.datetime.now() - timedelta(hours=6)
    # print(str(weather_map_moment_1))
    context = {
        'moment1': weather_map_moment_1,
        'moment2': weather_map_moment_2,
        'moment3': weather_map_moment_3,
        'moment4': weather_map_moment_4,
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class
    }

    return render(request, 'keli/keli.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')
