from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
from booking.models import Booking
from django.template.context_processors import csrf
from booking.models import cars
from django.core.mail import send_mail
from django.conf import settings


def booking(request):
    c = {}
    c.update(csrf(request))
    if "name" not in request.session:
        request.session['checker']="yes"
        return render(request, 'login.html',c)
    else:
        return render(request,'booking.html', c)

def carlist(request):
    try:
        pickupdate = request.POST.get('pickup_date')
        dropoffdate = request.POST.get('dropoff_date')
        date1 = pickupdate.split("-")
        pickupdate1 = date(int(date1[0]), int(date1[1]), int(date1[2]))
        date2 = dropoffdate.split("-")
        dropoffdate1 = date(int(date2[0]), int(date2[1]), int(date2[2]))
        diff = dropoffdate1 - pickupdate1
        days = diff.days
        hours = days * 24
        hour = int(request.POST.get('dropoff_time')) - int(request.POST.get('pickup_time'))
        hours = hours + hour
        request.session['hours'] = hours
        request.session['pickup_location']=request.POST.get('pickup')
        request.session['dropoff_location'] = request.POST.get('dropoff')
        request.session['pickup_date'] = request.POST.get('pickup_date')
        request.session['dropoff_date'] = request.POST.get('dropoff_date')
        request.session['pickup_time'] = request.POST.get('pickup_time')
        request.session['dropoff_time'] = request.POST.get('dropoff_time')
        request.session['driver'] = request.POST.get('driver')
        pickup_location = request.POST.get('pickup')
        if pickup_location == 'all':
            car = cars.objects.all()
        else:
            car = cars.objects.filter(position=pickup_location)
        return render(request, 'carlist.html', {'cars': car})
    except AttributeError:
        return render(request,'home.html',context=None)

def bill(request):
    car = cars.objects.get(car_id=request.POST.get('book'))
    request.session['car_id']=request.POST.get('book')
    c = {
        'hours':request.session['hours'],
        'pickup_location': request.session['pickup_location'],
        'dropoff_location': request.session['dropoff_location'],
        'pickup_date': request.session['pickup_date'],
        'dropoff_date': request.session['dropoff_date'],
        'pickup_time': request.session['pickup_time'],
        'dropoff_time': request.session['dropoff_time'],
        'driver': request.session['driver'],
        'cars':car
    }
    return render(request,'bill.html',c)

def book(request):
    pickup_location= request.session['pickup_location']
    dropoff_location= request.session['dropoff_location']
    pickup_date=request.session['pickup_date']
    dropoff_date= request.session['dropoff_date']
    pickup_time =request.session['pickup_time']
    dropoff_time= request.session['dropoff_time']
    driver= request.session['driver']
    username=request.session['name1']
    car_id=request.session['car_id']
    s=Booking(car_id=car_id,pickup_location=pickup_location,dropoff_location=dropoff_location,
              pickup_date=pickup_date,dropoff_date=dropoff_date,pickup_time=pickup_time,
              dropoff_time=dropoff_time,driver=driver,username=username)
    s.save()
    subject='Confirmation Mail For Booking'
    message='Your booking details are below.'+'\n'+'\nCar_id:'+car_id+'\nPickuplocation:'+pickup_location+'\nPickupDate:'+pickup_date+'\nPickupTime:'+pickup_time+':00'+'\nDropoffLocation:'+dropoff_location+'\nDropoffDate:'+dropoff_date+'\nDropoffTime:'+dropoff_time+':00'+'\nDriver:'+driver
    from_email=settings.EMAIL_HOST_USER
    to_list=[request.session['email']]
    send_mail(subject,message,from_email,to_list,fail_silently=True)
    booking=Booking.objects.filter(username=username)
    del request.session['pickup_location']
    del request.session['dropoff_location']
    del request.session['pickup_date']
    del request.session['dropoff_date']
    del request.session['pickup_time']
    del request.session['dropoff_time']
    del request.session['driver']
    del request.session['car_id']
    return HttpResponseRedirect('/booking/bookingHistory/')

def bookingHistory(request):
    username = request.session['name1']
    booking1 = Booking.objects.filter(username=username)
    booking = reversed(booking1)
    return render(request, 'bookinghistory.html', {'booking': booking,})

def delete(request):
    Booking.objects.filter(id=request.POST.get('delete')).delete()
    return HttpResponseRedirect('/booking/bookingHistory/')



