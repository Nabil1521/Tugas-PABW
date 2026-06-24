from django.shortcuts import render, redirect, get_object_or_404
from .models import Car

def read(request):
    cars = Car.objects.all()
    return render(request, 'readcar.html', {'cars': cars})


def create(request):
    if request.method == 'POST':
        Car.objects.create(
            carname=request.POST.get('carname', ''),
            carbrand=request.POST.get('carbrand', ''),
            carmodel=request.POST.get('carmodel', ''),
            carprice=request.POST.get('carprice', 0)
        )
        return redirect('read')

    return render(request, 'createcar.html')


def update(request, id):
    car = get_object_or_404(Car, id=id)

    if request.method == 'POST':
        car.carname = request.POST.get('carname', car.carname)
        car.carbrand = request.POST.get('carbrand', car.carbrand)
        car.carmodel = request.POST.get('carmodel', car.carmodel)
        car.carprice = request.POST.get('carprice', car.carprice)
        car.save()
        return redirect('read')

    return render(request, 'updatecar.html', {'car': car})


def delete_confirm(request, id):
    car = get_object_or_404(Car, id=id)
    return render(request, 'deletecar.html', {'car': car})


def delete(request, id):
    car = get_object_or_404(Car, id=id)
    if request.method == 'POST':
        car.delete()
        return redirect('read')
    return redirect('delete_confirm', id=id)


def search(request):
    results = []

    if request.method == 'POST':
        keyword = request.POST['keyword']
        results = Car.objects.filter(carname__icontains=keyword)

    return render(request, 'searchcar.html', {'results': results})


def settings(request):
    return render(request, 'settings.html')
