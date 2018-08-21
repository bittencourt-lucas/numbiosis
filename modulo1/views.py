from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
import numpy as np
import scipy as sp
import json
from django.http import HttpResponse
# Create your views here.

class IndexView(generic.TemplateView):
    template_name = 'modulo1/index.html'

class FalsaPosicaoView(generic.TemplateView):
    template_name = 'modulo1/falsaposicao.html'

class SecanteView(generic.TemplateView):
    template_name = 'modulo1/secante.html'

class MullerView(generic.TemplateView):
    template_name = 'modulo1/muller.html'

def calculafp(request):
    pontos = []
    a = int(request.POST.get('xl'))
    b = int(request.POST.get('xu'))
    f = lambda x: eval(request.POST.get('f'))
    maxi = int(request.POST.get('maxi'))
    tol = float(request.POST.get('tol'))
    ka = f(a)
    kb = f(b)
    i = 0
    while i < maxi:
        xm = (b * ka - a * kb) / (ka - kb)
        kxm = f(xm)
        if abs(a - b) < tol:
            pontos.append([xm, kxm])
            break
        elif (ka * kxm) < 0:
            b = xm
            pontos.append([xm, kxm])
        elif (ka * kxm) > 0:
            a = xm
            pontos.append([xm, kxm])
        i += 1
    print (xm);
    return HttpResponse(json.dumps({ 'points': pontos }), content_type="application/json")

def calculasecante(request):
    inf  = int(request.POST.get('xl'))                # Limite inferior
    sup  = int(request.POST.get('xu'))                # Limite superior
    it   = int(request.POST.get('maxi'))               # Número de iterações
    tol  = float(request.POST.get('tol'))             # Tolerância do cáculo
    func = lambda x: eval(request.POST.get('f'))      # Função a ser utilizada nos calculos

    k = 0
    xm = 0

    while k <= it:
        if abs(func(inf)) > tol or abs(sup - inf) > tol:
            xm = sup - (sup - inf) * (func(sup) / (func(sup) - func(inf)))
            inf = sup
            sup = xm
        k += 1
    # print (xm);
    return HttpResponse(json.dumps({ 'points': xm }), content_type="application/json")

def calculamuller(request):
    inf  = int(request.POST.get('xl'))                # Limite inferior
    sup  = int(request.POST.get('xu'))                # Limite superior
    it   = int(request.POST.get('maxi'))               # Número de iterações
    tol  = float(request.POST.get('tol'))             # Tolerância do cáculo
    func = lambda x: eval(request.POST.get('f'))      # Função a ser utilizada nos calculos

    x = [inf,sup,tol]
    for loopCount in range(it):
        x = swap_points(x)
        y = func(x[0]), func(x[1]), func(x[2])
        h1 = x[1]-x[0]
        h2 = x[0]-x[2]
        lam = h2/h1
        c = y[0]
        inf = (lam*y[1] - y[0]*((1.0+lam))+y[2])/(lam*h1**2.0*(1+lam))
        sup = (y[1] - y[0] - inf*((h1)**2.0))/(h1)
        if sup > 0:
            root = x[0] - ((2.0*c)/(sup+ (sup**2 - 4.0*inf*c)**0.5))
        else:
            root = x[0] - ((2.0*c)/(sup- (sup**2 - 4.0*inf*c)**0.5))
        # print "inf = %.5f sup = %.5f c = %.5f root = %.5f " % (inf,sup,c,root)
        # print "Current approximation is %.9f" % root
        if abs(func(root)) > x[0]:
            x = [x[1],x[0],root]
        else:
            x = [x[2],x[0],root]
        x = swap_points(x)
    return HttpResponse(json.dumps({ 'points': x }), content_type="application/json")