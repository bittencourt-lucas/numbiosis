from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
import numpy as np
import scipy as sp
import json
import math
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
    return HttpResponse(json.dumps({ 'points': pontos }), content_type="application/json")

def calculasecante(request):
    pontos = []
    inf  = int(request.POST.get('xl'))                # Limite inferior
    sup  = int(request.POST.get('xu'))                # Limite superior
    it   = int(request.POST.get('maxi'))              # Número de iterações
    tol  = float(request.POST.get('tol'))             # Tolerância do cáculo
    func = lambda x: eval(request.POST.get('f'))      # Função a ser utilizada nos calculos

    k = 0
    xm = 0
    pontos.append([inf, sup])
    
    while k <= it:
        if abs(func(inf)) > tol or abs(sup - inf) > tol:
            xm = sup - (sup - inf) * (func(sup) / (func(sup) - func(inf)))
            inf = sup
            sup = xm
        pontos.append([sup, func(sup)])
        k += 1
    return HttpResponse(json.dumps({ 'points': pontos }), content_type="application/json")

def swap_points(x):
    s = []
    s = x
    s.sort()
    f = s[1]
    sn = s[2]
    t = s[0]
    s[0] = f
    s[1] = sn
    s[2] = t
    return s

def calculamuller(request):
    pontos = []
    a    = int(request.POST.get('xl'))                # Limite inferior
    b    = int(request.POST.get('xu'))                # Limite superior
    it   = int(request.POST.get('maxi'))              # Número de iterações
    r    = float(request.POST.get('tol'))             # Tolerância do cáculo
    func = lambda x: eval(request.POST.get('f'))      # Função a ser utilizada nos calculos

    x = [a,b,r]

    for loopCount in range(it):
        x = swap_points(x)
        y = func(x[0]), func(x[1]), func(x[2])
        h1 = x[1]-x[0]
        h2 = x[0]-x[2]
        lam = h2/h1
        c = y[0]
        a = (lam*y[1] - y[0]*((1.0+lam))+y[2])/(lam*h1**2.0*(1+lam))
        b = (y[1] - y[0] - a*((h1)**2.0))/(h1)
        if b > 0:
            root = x[0] - ((2.0*c)/(b+ (b**2 - 4.0*a*c)**0.5))
        else:
            root = x[0] - ((2.0*c)/(b- (b**2 - 4.0*a*c)**0.5))
        # print "a = %.5f b = %.5f c = %.5f root = %.5f " % (a,b,c,root)
        # print "Current approximation is %.9f" % root
        if abs(func(root)) > x[0]:
            x = [x[1],x[0],root]
        else:
            x = [x[2],x[0],root]
        x = swap_points(x)
        pontos.append([c, func(c)])
    return HttpResponse(json.dumps({ 'points': pontos }), content_type="application/json")

def teste(request):
    pontos = []
    x0     = int(request.POST.get('xl'))                # Limite inferior
    x1     = int(request.POST.get('xu'))                # Limite superior
    it     = int(request.POST.get('maxi'))              # Número de iterações

    x2 = (x0 + x1)/2
    k = 0

    while k <= it:
        h0 = x1 - x0
        h1 = x2 - x1

        delta0 = (func(x1) - func(x0) ) / (x1 - x0)
        delta1 = (func(x2) - func(x1) ) / (x2 - x1)
        
        a = (delta1 - delta1) / (h1 - h0)
        b = a * h1 + delta1
        c = func(x2)

        x3 = x2 + ((-2 * c) / b + (math.sqrt(b**2 - 4 * a * c)))

        x0 = x1
        x1 = x2 
        x2 = x3

        pontos.append([x0, func(x0)])
        pontos.append([x1, func(x1)])
        pontos.append([x2, func(x2)])
        k += 1

    return HttpResponse(json.dumps({ 'points': pontos }), content_type="application/json")

