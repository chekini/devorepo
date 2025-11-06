from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
from main import Hotspot
h = Hotspot()
def Inicio(request):
    dst = request.GET.get('dst')
    link= request.GET.get('link')
    username= request.GET.get('username')
    h.con(link,dst,username)
    return render(request,"App.html")

def Mikrotik(request):
    print(h.Link)
    print(h.Dst)
    print(h.Username)
    print(request.GET.get('Nombre'))
    print(request.GET.get('Apellido'))
    print(request.GET.get('Telefono'))
    print(request.GET.get('colonias'))
    return redirect(h.Link+"?dst="+h.Dst+"&username="+h.Username)
