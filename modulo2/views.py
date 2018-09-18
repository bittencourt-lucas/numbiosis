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
    template_name = 'modulo2/index.html'

class GaussJordanView(generic.TemplateView):
    template_name = 'modulo2/GaussJordan.html'


def calculaGaussJordan(request):
    
    print("Eliminação de Gauss Jordan:\n")
    print("Para:\n")
    print("[1 -1 2 2]")
    print("[2 1 -1 1]")
    print("[-2 -5 3 3]")
    
    matriz_A = [[1, -1, 2], [2, 1, -1], [-2, -5, 3]] # matriz
    vetor_b = [2, 1, 3] #vetor
    """
    
    Método de Eliminação de Gauss Jordan 

    matriz_A : matriz de coeficientes

    vetor_b : "matriz" de variaveis livres.

    retorno: solução do sistema


    """
    ###### Trecho para obtenção da matriz extendida
    
    if len(matriz_A) != len(vetor_b):
        return None
    matrizExtendida = matriz_A[:]
    for i in range(len(matrizExtendida)):
        matrizExtendida[i].append(vetor_b[i])
    ######

        
    for i in range(len(matrizExtendida)):
        #print(i)
        for j in range(len(matrizExtendida),i-1,-1):
            #print(matrizExtendida[i][j])
            matrizExtendida[i][j]/=matrizExtendida[i][i]
            #print(matrizExtendida[i][j])
        #print("pivo:", matrizExtendida[i][i])
        # print((len(matrizExtendida)-i))
        for j in range(len(matrizExtendida)):
            #  print(j)
            if j==i:
                continue
            if matrizExtendida[i][i] != 0:
                c = matrizExtendida[j][i]/matrizExtendida[i][i]
                ##print("matrizExtendida[",j,"][",i,"]",matrizExtendida[j][i])
                #print(c)
                if c != 0:
                    for k in range(len(matrizExtendida[i])):
                        #print(matrizExtendida[i][k])
                        #print(matrizExtendida[j][k])
                        matrizExtendida[j][k]-=c*matrizExtendida[i][k]
                        #print(matrizExtendida[j][k])
            else:
                return None
    print(matrizExtendida)
    #return matrizExtendida
    solucoes=[]
    solucoes.append(matrizExtendida[len(matrizExtendida)-1][len(matrizExtendida)]/matrizExtendida[len(matrizExtendida)-1][len(matrizExtendida)-1])
    #for i in matrizExtendida: # matriz triangular
    #        print(i)
    for i in range(len(matrizExtendida)-2,-1,-1):
        c=0
        for j in range(len(solucoes)):
            c+=solucoes[j]*matrizExtendida[i][len(matrizExtendida)-1-j]
        solucoes.append((matrizExtendida[i][len(matrizExtendida)]-c)/matrizExtendida[i][i])
    solucoes.reverse()
    print(solucoes)
    return HttpResponse(json.dumps({ 'solution': solucoes }), content_type="application/json")
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


def teste(request): # copiada do modulo1
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

