import math

def TrasnlationMatrix(x,y,z):
    return [[1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]]
    
def ScaleMatrix(x,y,z):
    return [[x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1]]

def rotacionX(angulo):
    cosA = math.cos(math.radians(angulo))
    sinA = math.sin(math.radians(angulo))
    return [[1, 0, 0, 0],
            [0, cosA, -sinA, 0],
            [0, sinA, cosA, 0],
            [0, 0, 0, 1]]

def rotacionY(angulo):
    cosA = math.cos(math.radians(angulo))
    sinA = math.sin(math.radians(angulo))
    return [[cosA, 0, sinA, 0],
            [0, 1, 0, 0],
            [-sinA, 0, cosA, 0],
            [0, 0, 0, 1]]

def rotacionZ(angulo):
    cosA = math.cos(math.radians(angulo))
    sinA = math.sin(math.radians(angulo))
    return [[cosA, -sinA, 0, 0],
            [sinA, cosA, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]]

def multiplicarMatrices(A, B):
    resultado = [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]

    for i in range(4):
        for j in range(4):
            resultado[i][j] = A[i][0] * B[0][j] + A[i][1] * B[1][j] + A[i][2] * B[2][j] + A[i][3] * B[3][j]
    return resultado

def transformarVertice(v, m):
    x = v[0] * m[0][0] + v[1] * m[0][1] + v[2] * m[0][2] + v[3] * m[0][3]
    y = v[0] * m[1][0] + v[1] * m[1][1] + v[2] * m[1][2] + v[3] * m[1][3]
    z = v[0] * m[2][0] + v[1] * m[2][1] + v[2] * m[2][2] + v[3] * m[2][3]
    w = v[0] * m[3][0] + v[1] * m[3][1] + v[2] * m[3][2] + v[3] * m[3][3]
    return [x, y, z, w]

def cofactor(matriz, row, col):
    submatriz = [[matriz[i][j] for j in range(len(matriz)) if j != col] for i in range(len(matriz)) if i != row]
    return ((-1) ** (row + col)) * determinante(submatriz)

def determinante(matriz):
    if len(matriz) == 2:
        return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]
    
    det = 0
    for col in range(len(matriz)):
        det += matriz[0][col] * cofactor(matriz, 0, col)
    return det

def inversaMatriz(m):
    if len(m) != 4 or len(m[0]) != 4:
        raise ValueError("La matriz debe ser de 4x4")

    det = determinante(m)
    if det == 0:
        raise ValueError("La matriz no tiene inversa")
    
    cofactores = [[cofactor(m, row, col) for col in range(4)] for row in range(4)]
    cofactores_transpuesta = [[cofactores[col][row] for col in range(4)] for row in range(4)]
    
    inversa = [[cofactores_transpuesta[row][col] / det for col in range(4)] for row in range(4)]
    return inversa

def magnitudVector(v):
    return math.sqrt(sum(vi**2 for vi in v))

def normalizarVector(v):
    mag = magnitudVector(v)
    if mag == 0:
        return [0] * len(v)
    return [vi / mag for vi in v]

def productoPunto(v1, v2):
    return sum(vi * vj for vi, vj in zip(v1, v2))

def productoCruz(v1, v2):
    if len(v1) == 3 and len(v2) == 3:
        return [v1[1] * v2[2] - v1[2] * v2[1],
                v1[2] * v2[0] - v1[0] * v2[2],
                v1[0] * v2[1] - v1[1] * v2[0]]
    else:
        raise ValueError("El producto cruz solo está definido para vectores de 3 dimensiones")
    
def multiplicarPorEscalar(escalar, vector):
    return [escalar * componente for componente in vector]


def barycentricCoords(A, B, C, P):
	
	# Se saca el �rea de los subtri�ngulos y del tri�ngulo
	# mayor usando el Shoelace Theorem, una f�rmula que permite
	# sacar el �rea de un pol�gono de cualquier cantidad de v�rtices.

	areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) - 
				  (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))

	areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) - 
				  (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

	areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) - 
				  (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))

	areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) - 
				  (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))

	# Si el �rea del tri�ngulo es 0, retornar nada para
	# prevenir divisi�n por 0.
	if areaABC == 0:
		return None

	# Determinar las coordenadas baric�ntricas dividiendo el 
	# �rea de cada subtri�ngulo por el �rea del tri�ngulo mayor.
	u = areaPCB / areaABC
	v = areaACP / areaABC
	w = areaABP / areaABC

	# Si cada coordenada est� entre 0 a 1 y la suma de las tres
	# es igual a 1, entonces son v�lidas.
	if 0<=u<=1 and 0<=v<=1 and 0<=w<=1:
		return (u, v, w)
	else:
		return None
    

def reflejarVector(vector, normal):
    dotProd = productoPunto(vector, normal)
    reflected = [
        2 * dotProd * normal[0] - vector[0],
        2 * dotProd * normal[1] - vector[1],
        2 * dotProd * normal[2] - vector[2]
    ]
    return normalizarVector(reflected)


def reflectVector(normal, direction):
     # R = 2 * (N . L) * N - L

     reflect = 2 * np.dot(normal, direction)
     reflect = np.multiply(reflect, normal)
     reflect = np.subtract(reflect, direction)
     reflect /= np.linalg.norm(reflect)

     return reflect