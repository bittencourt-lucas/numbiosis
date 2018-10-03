import numpy as np
import sympy as sp

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
    f1     = request.POST.get('func1')		     # Função a ser utilizada nos calculos
    f2     = request.POST.get('func2')		     # Função a ser utilizada nos calculos

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

