from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from scipy.misc import derivative
import numpy as np
import sympy as sp
import json
import math

from scipy.optimize import fsolve
# from __future__ import division
from numpy import linalg
from django.http import HttpResponse
# Create your views here.

class IndexView(generic.TemplateView):
    template_name = 'modulo2/index.html'

class GaussJordanView(generic.TemplateView):
    template_name = 'modulo2/gaussJordan.html'

class NewtonView(generic.TemplateView):
    template_name = 'modulo2/newton.html'

class SplinesView(generic.TemplateView):
    template_name = 'modulo2/splines.html'


def calculaGaussJordan(request):

    print("Eliminação de Gauss Jordan:\n")
    print("Para:\n")
    # print("[1 -1 2 2]")
    # print("[2 1 -1 1]")
    # print("[-2 -5 3 3]")
    print (">>>>>>>>>>>>>>>>>>>")
    matriz_A = json.loads(request.POST.get('matrizA'))
    matriz_A[:] = [list(map(int, elements)) for elements in matriz_A]

    vetor_b = json.loads(request.POST.get('vectorB'))
    vetor_b[:] = [list(map(int, elements)) for elements in vetor_b]
    vetor_b[:] = [elements[0] for elements in vetor_b]

    # print (request.POST.get('matriz_A'))
    # matriz_A = [[1, -1, 2], [2, 1, -1], [-2, -5, 3]] # matriz
    # vetor_b = [2, 1, 3] #vetor
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
    print('Matriz extendida')
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
    print('solucoes')
    print(solucoes)
    return HttpResponse(json.dumps({ 'solution': solucoes, 'extended': matrizExtendida }), content_type="application/json")

def cubic_spline(x, y):
    """
    Parametros são lista de floats
    ----------
    Retorna uma lista de uma lista de floats
    """
    n = len(x) - 1
    h = [x[i + 1] - x[i] for i in range(n)]
    al = [3 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1]) for i in range(1, n)]
    al.insert(0, 0)

    l = [1] * (n + 1)
    u = [0] * (n + 1)
    z = [0] * (n + 1)
    for i in range(1, n):
        l[i] = 2 * (x[i + 1] - x[i - 1]) - h[i - 1] * u[i - 1]
        u[i] = h[i] / l[i]
        z[i] = (al[i] - h[i - 1] * z[i - 1]) / l[i]

    b = [0] * (n + 1)
    c = [0] * (n + 1)
    d = [0] * (n + 1)
    for i in range(n - 1, -1, -1):  # for i in reversed(range(n)):
        c[i] = z[i] - u[i] * c[i + 1]
        b[i] = (y[i + 1] - y[i]) / h[i] - h[i] * (c[i + 1] + 2 * c[i]) / 3
        d[i] = (c[i + 1] - c[i]) / (3 * h[i])
    return [y, b, c, d]


def processingSpline(request):
    f = lambda x: eval(request.POST.get('f'))

    # entradas
    # def f(x): #função
    #     return math.e ** x

    # interval = 3
    interval = int(request.POST.get('interval'))
    x = [i for i in range(interval + 1)] #lista de floats
    y = [f(i) for i in range(interval + 1)] #lista de floats

    # processamento de x e y
    a = cubic_spline(x, y)

    # Preparando os dados para plotagem da spline
    points_per_interval = 5
    xs = []
    ys = []
    for i in range(3):
        xs.append(np.linspace(i, i + 1, points_per_interval))
        ys.append([a[0][i] +
                   a[1][i] * (xs[i][k] - i) +
                   a[2][i] * (xs[i][k] - i) ** 2 +
                   a[3][i] * (xs[i][k] - i) ** 3
                   for k in range(points_per_interval)])

    results = []
    for idx, val in enumerate(xs):
        for idx2, element in enumerate(val):
            # secants = {'x0': element, 'x1': ys[idx][idx2]}
            results.append([element, ys[idx][idx2]])

    # Preparando os dados para plotagem da função dada
    x = np.linspace(0, 3, interval * points_per_interval - (interval - 1))
    y = [f(x[i]) for i in range(len(x))]

    graphic = []
    for idx, element in enumerate(x):
        graphic.append([element, y[idx]])

    return HttpResponse(json.dumps({ 'graphic': graphic, 'aproximations': results }), content_type="application/json")

def jacobianMatrix(func1, func2, points):
    res = np.zeros((2,2))
    x = sp.Symbol('x')
    y = sp.Symbol('y')

    dx11 = sp.diff(func1,x)
    dx12 = sp.diff(func1,y)
    dx21 = sp.diff(func1,x)
    dx22 = sp.diff(func2,y)

    jx11 = lambda x, y : eval(str(dx11))
    jx12 = lambda x, y : eval(str(dx12))
    jx21 = lambda x, y : eval(str(dx21))
    jx22 = lambda x, y : eval(str(dx22))

    res[0,0] = jx11(points[0], points[1])
    res[0,1] = jx12(points[0], points[1])
    res[1,0] = jx21(points[0], points[1])
    res[1,1] = jx22(points[0], points[1])

    return res;

def fxMatrix(func1, func2, points):
    res = np.zeros((2,1))

    fx1 = lambda x, y : eval(str(func1))
    fx2 = lambda x, y : eval(str(func2))

    res[0,0] = fx1(points[0], points[1])
    res[1,0] = fx2(points[0], points[1])

    return res

def calculaNewton(request):
    graph  = []
    xl     = float(request.POST.get('xl'))       # Limite inferior
    xu     = float(request.POST.get('xu'))       # Limite superior
    TOL    = float(request.POST.get('tol'))      # Tolerância do cáculo
    N      = float(request.POST.get('maxi'))     # Maximo de iterações
    f1     = request.POST.get('func1')           # Função a ser utilizada nos calculos
    f2     = request.POST.get('func2')           # Função a ser utilizada nos calculos

    x = np.array([xl,xu])

    k=0  
    # iteracoes  
    while (k < N):  
       k += 1  
       #iteracao Newton  
       resultJacobian = jacobianMatrix(f1, f2, x)
       resultFx = fxMatrix(f1, f2, x)

       delta = -np.linalg.inv(resultJacobian).dot(resultFx)  

       x[0] = x[0] + delta[0];
       x[1] = x[1] + delta[1];
       graph.append([x[0], x[1]])

       # #criterio de parada  
       if (np.linalg.norm(delta,np.inf) < TOL):  
           break

    return HttpResponse(json.dumps({ 'points': graph }), content_type="application/json")

