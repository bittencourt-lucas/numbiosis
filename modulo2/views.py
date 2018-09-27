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

class GaussJordanView(generic.TemplateView):
    template_name = 'modulo2/gausJordan.html'


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