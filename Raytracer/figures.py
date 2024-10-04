from MathLib import *
from intercept import Intercept
from math import atan2, acos, pi, isclose

class Shape(object):
    def __init__(self, position, material):
        self.position = position
        self.material = material
        self.type = "None"

    def ray_intersect(self, orig, dir):
        return None

class Sphere(Shape):
    def __init__(self, position, radius, material):
        super().__init__(position, material)
        self.radius = radius
        self.type = "Sphere"

    def ray_intersect(self, orig, dir):
        L = [self.position[i] - orig[i] for i in range(3)]
        tca = productoPunto(L, dir)
        d = (magnitudVector(L) ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return None
        
        thc = (self.radius ** 2 - d ** 2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None

        P = [orig[i] + dir[i] * t0 for i in range(3)]
        normal = [P[i] - self.position[i] for i in range(3)]
        normal = normalizarVector(normal)

        u = (atan2(normal[2], normal[0])) / (2*pi) + 0.5
        v = acos(-normal[1]) / pi

        return Intercept(point=P,
                         normal=normal,
                         distance=t0,
                         texCoords=[u, v],
                         rayDirection=dir,
                         obj=self)

class Plane(Shape):
    def __init__(self, position, normal, material):
        super().__init__(position, material)
        self.normal = normalizarVector(normal)
        self.type = "Plane"

    def ray_intersect(self, orig, dir):
        denom = productoPunto(dir, self.normal)
        
        if isclose(denom, 0):
            return None
        
        num = productoPunto([self.position[i] - orig[i] for i in range(3)], self.normal)
        t = num / denom

        if t < 0:
            return None

        P = [orig[i] + dir[i] * t for i in range(3)]

        return Intercept(point=P,
                         normal=self.normal,
                         distance=t,
                         texCoords=None,
                         rayDirection=dir,
                         obj=self)

class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        super().__init__(position, normal, material)
        self.radius = radius
        self.type = "Disk"

    def ray_intersect(self, orig, dir):
        planeIntercept = super().ray_intersect(orig, dir)

        if planeIntercept is None:
            return None
        
        contact = [planeIntercept.point[i] - self.position[i] for i in range(3)]
        contact = magnitudVector(contact)

        if contact > self.radius:
            return None
        
        return planeIntercept

class AABB(Shape):
    def __init__(self, position, sizes, material):
        super().__init__(position, material)
        self.sizes = sizes
        self.type = "AABB"

        self.planes = []

        rightPlane = Plane([position[0] + sizes[0]/2, position[1], position[2]], [1, 0, 0], material)
        leftPlane = Plane([position[0] - sizes[0]/2, position[1], position[2]], [-1, 0, 0], material)
        upPlane = Plane([position[0], position[1] + sizes[1]/2, position[2]], [0, 1, 0], material)
        downPlane = Plane([position[0], position[1] - sizes[1]/2, position[2]], [0, -1, 0], material)
        frontPlane = Plane([position[0], position[1], position[2] + sizes[2]/2], [0, 0, 1], material)
        backPlane = Plane([position[0], position[1], position[2] - sizes[2]/2], [0, 0, -1], material)

        self.planes.append(rightPlane)
        self.planes.append(leftPlane)
        self.planes.append(upPlane)
        self.planes.append(downPlane)
        self.planes.append(frontPlane)
        self.planes.append(backPlane)

        self.boundsMin = [0, 0, 0]
        self.boundsMax = [0, 0, 0]

        epsilon = 0.001

        for i in range(3):
            self.boundsMin[i] = position[i] - (epsilon + sizes[i]/2)
            self.boundsMax[i] = position[i] + (epsilon + sizes[i]/2)

    def ray_intersect(self, orig, dir):
        intercept = None
        t = float("inf")
        
        for plane in self.planes:
            planeIntercept = plane.ray_intersect(orig, dir)

            if planeIntercept is not None:
                planePoint = planeIntercept.point

                if (self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0] and
                    self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1] and
                    self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]):

                    if planeIntercept.distance < t:
                        t = planeIntercept.distance
                        intercept = planeIntercept
        
        if intercept is None:
            return None
        
        u, v = 0, 0

        if abs(intercept.normal[0]) > 0:
            u = (intercept.point[1] - self.boundsMin[1]) / self.sizes[1]
            v = (intercept.point[2] - self.boundsMin[2]) / self.sizes[2]

        elif abs(intercept.normal[1]) > 0:
            u = (intercept.point[0] - self.boundsMin[0]) / self.sizes[0]
            v = (intercept.point[2] - self.boundsMin[2]) / self.sizes[2]

        elif abs(intercept.normal[2]) > 0:
            u = (intercept.point[0] - self.boundsMin[0]) / self.sizes[0]
            v = (intercept.point[1] - self.boundsMin[1]) / self.sizes[1]

        u = min(0.999, max(0, u))
        v = min(0.999, max(0, v))

        return Intercept(point=intercept.point,
                         normal=intercept.normal,
                         distance=t,
                         texCoords=[u, v],
                         rayDirection=dir,
                         obj=self)

class Triangle(Shape):
    def __init__(self, p0, p1, p2, material):
        super().__init__(p0, material)
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.edge1 = [p1[i] - p0[i] for i in range(3)]
        self.edge2 = [p2[i] - p0[i] for i in range(3)]
        self.normal = normalizarVector(productoCruz(self.edge1, self.edge2))
        self.type = "Triangle"

    def ray_intersect(self, orig, dir):
        epsilon = 1e-6
        h = productoCruz(dir, self.edge2)
        a = productoPunto(self.edge1, h)

        if abs(a) < epsilon:
            return None

        f = 1.0 / a
        s = [orig[i] - self.p0[i] for i in range(3)]
        u = f * productoPunto(s, h)

        if u < 0.0 or u > 1.0:
            return None

        q = productoCruz(s, self.edge1)
        v = f * productoPunto(dir, q)

        if v < 0.0 or u + v > 1.0:
            return None

        t = f * productoPunto(self.edge2, q)

        if t > epsilon:
            P = [orig[i] + dir[i] * t for i in range(3)]
            w = 1 - u - v
            u_coord = w * 0.0 + u * 1.0 + v * 0.5
            v_coord = w * 0.0 + u * 0.0 + v * 1.0

            normal = self.normal
            if productoPunto(dir, normal) > 0:
                normal = [-normal[i] for i in range(3)]

            return Intercept(
                point=P,
                normal=normal,
                distance=t,
                texCoords=[u_coord, v_coord],
                rayDirection=dir,
                obj=self
            )
        else:
            return None

class Cylinder(Shape):
    def __init__(self, position, radius, height, material):
        super().__init__(position, material)
        self.radius = radius
        self.height = height
        self.type = "Cylinder"
        # Definir los extremos del cilindro (p1 = base, p2 = tapa superior)
        self.p1 = position
        self.p2 = [position[0], position[1] + height, position[2]]

    def ray_intersect(self, orig, dir):
        # Diferencia entre el origen del rayo y la base del cilindro
        delta_p = [orig[i] - self.p1[i] for i in range(3)]

        # Vector del cilindro a lo largo de la altura (p2 - p1)
        va = [self.p2[i] - self.p1[i] for i in range(3)]
        va = normalizarVector(va)  # Normalizar vector

        # Coeficientes de la ecuación cuadrática para el cilindro infinito
        A = productoPunto(dir, dir) - productoPunto(dir, va) ** 2
        B = 2 * (productoPunto(delta_p, dir) - productoPunto(dir, va) * productoPunto(delta_p, va))
        C = productoPunto(delta_p, delta_p) - productoPunto(delta_p, va) ** 2 - self.radius ** 2

        # Resolver la ecuación cuadrática
        discriminante = B * B - 4 * A * C
        if discriminante < 0:
            return None  # No hay intersección

        sqrt_discriminante = math.sqrt(discriminante)
        t0 = (-B - sqrt_discriminante) / (2 * A)
        t1 = (-B + sqrt_discriminante) / (2 * A)

        if t0 > t1:
            t0, t1 = t1, t0

        # Verificar si las intersecciones están dentro de los límites del cilindro finito
        y0 = orig[1] + t0 * dir[1]
        y1 = orig[1] + t1 * dir[1]

        if not (self.p1[1] <= y0 <= self.p2[1]):
            if not (self.p1[1] <= y1 <= self.p2[1]):
                return None
            t0 = t1

        # Seleccionar el valor de t más cercano al origen del rayo
        if t0 < 0:
            t0 = t1
            if t0 < 0:
                return None  # Ambos valores de t son negativos, no hay intersección

        P = [orig[i] + dir[i] * t0 for i in range(3)]
        normal = [P[0] - self.p1[0], 0, P[2] - self.p1[2]]
        normal = normalizarVector(normal)

        # Verificar las tapas del cilindro
        t_cap_bottom = (self.p1[1] - orig[1]) / dir[1] if dir[1] != 0 else float('inf')
        t_cap_top = (self.p2[1] - orig[1]) / dir[1] if dir[1] != 0 else float('inf')

        P_cap_bottom = [orig[i] + t_cap_bottom * dir[i] for i in range(3)]
        P_cap_top = [orig[i] + t_cap_top * dir[i] for i in range(3)]

        # Revisar si las intersecciones con las tapas están dentro del radio del cilindro
        dist_bottom = math.sqrt((P_cap_bottom[0] - self.p1[0]) ** 2 + (P_cap_bottom[2] - self.p1[2]) ** 2)
        dist_top = math.sqrt((P_cap_top[0] - self.p2[0]) ** 2 + (P_cap_top[2] - self.p2[2]) ** 2)

        if dist_bottom <= self.radius and 0 < t_cap_bottom < t0:
            t0 = t_cap_bottom
            P = P_cap_bottom
            normal = [0, -1, 0]  # Normal de la tapa inferior

        if dist_top <= self.radius and 0 < t_cap_top < t0:
            t0 = t_cap_top
            P = P_cap_top
            normal = [0, 1, 0]  # Normal de la tapa superior

        # Calcular coordenadas UV (opcional, según cómo uses la textura)
        u = (math.atan2(normal[2], normal[0])) / (2 * math.pi) + 0.5
        v = (P[1] - self.p1[1]) / self.height

        return Intercept(point=P,
                         normal=normal,
                         distance=t0,
                         texCoords=[u, v],
                         rayDirection=dir,
                         obj=self)