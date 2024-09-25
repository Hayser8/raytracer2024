from MathLib import *
from math import acos, asin, pi

def refractVector(normal, incident, n1, n2):
    # Convertir los parámetros a listas
    normal = list(normal)
    incident = list(incident)
    
    # Ley de Snell
    c1 = productoPunto(normal, incident)
    
    if c1 < 0:
        c1 = -c1
    else:
        normal = multiplicarPorEscalar(-1, normal)
        n1, n2 = n2, n1

    n = n1 / n2
    
    # Fórmula de refracción
    T1 = multiplicarPorEscalar(n, [incident[i] + c1 * normal[i] for i in range(3)])
    T2 = multiplicarPorEscalar(-1, normal)
    T = [T1[i] + T2[i] * (1 - n**2 * (1 - c1**2))**0.5 for i in range(3)]
    
    # Normalizar el vector resultante
    return normalizarVector(T)



def totalInternalReflection(normal, incident, n1, n2):
    # Usar productoPunto de la librería
    c1 = productoPunto(normal, incident)
    
    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1

    if n1 < n2:
        return False
    
    # Calcular theta1 usando acos
    theta1 = math.acos(c1)
    # Calcular thetaC usando asin
    thetaC = math.asin(n2 / n1)
    
    return theta1 >= thetaC



def fresnel(normal, incident, n1, n2):
    # Usar productoPunto de la librería
    c1 = productoPunto(normal, incident)
    
    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1

    # Calcular s2 como se indica
    s2 = (n1 * (1 - c1**2)**0.5) / n2
    c2 = (1 - s2**2) ** 0.5
    
    # Calcular F1 y F2 según las fórmulas de Fresnel
    F1 = (((n2 * c1) - (n1 * c2)) / ((n2 * c1) + (n1 * c2))) ** 2
    F2 = (((n1 * c2) - (n2 * c1)) / ((n1 * c2) + (n2 * c1))) ** 2

    # Calcular coeficientes de reflexión (Kr) y transmisión (Kt)
    Kr = (F1 + F2) / 2
    Kt = 1 - Kr
    return Kr, Kt
