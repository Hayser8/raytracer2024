from MathLib import reflejarVector
from refractionFunctions import *


OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2


class Material(object):
    def __init__(self, diffuse = [1,1,1], spec = 1, Ks = 0, ior = 1.0,texture = None, matType = OPAQUE):
        self.diffuse = diffuse
        self.spec = spec
        self.Ks = Ks
        self.ior = ior
        self.texture = texture
        self.matType = matType

    def GetSurfaceColor(self, intercept, renderer, recursion = 0):
        # Phong reflection model
        # LightCOlor = LightColor + Specular
        # FinalColor = DiffuseColor * LightColor
        lightColor = [0,0,0]
        reflectColor= [0,0,0]
        refractColor = [0,0,0]
        finalColor = self.diffuse

        if self.texture and intercept.texCoords:
            textureColor = self.texture.getColor(intercept.texCoords[0], intercept.texCoords[1])
            finalColor = [finalColor[i] * textureColor[i] for i in range(3)]

        for light in renderer.lights:
            shadowIntercept = None

            if light.lightType == "Directional":
                lightDir = [-i for i in light.direction]
                shadowIntercept = renderer.glCastRay(intercept.point, lightDir, intercept.obj)

            if shadowIntercept == None:
                lightColor = [(lightColor[i] + light.GetSpecularColor(intercept, renderer.camera.translate)[i]) for i in range(3)]

                if self.matType == OPAQUE:
                    lightColor = [(lightColor[i] + light.GetLightColor(intercept)[i]) for i in range(3)]


        if self.matType == REFLECTIVE:
            rayDir = [-i for i in intercept.rayDirection]
            reflect = reflejarVector(rayDir, intercept.normal)
            reflectIntercept = renderer.glCastRay(intercept.point, reflect, intercept.obj, recursion + 1)
            if reflectIntercept != None:
                reflectColor = reflectIntercept.obj.material.GetSurfaceColor(reflectIntercept, renderer, recursion + 1)
            else: 
                reflectColor = renderer.glEnvMapColor(intercept.point, reflect)
        
        elif self.matType == TRANSPARENT:
            # Revisamos si estamos afuera
            outside = productoPunto(intercept.normal, intercept.rayDirection) < 0

            # Agregar margen de error
            bias = multiplicarPorEscalar(0.001, intercept.normal)

            # Generamos los rayos de reflección
            rayDir = [-i for i in intercept.rayDirection]
            reflect = reflejarVector(rayDir, intercept.normal)

            if outside:
                reflectOrig = [intercept.point[i] + bias[i] for i in range(len(bias))]
            else:
                reflectOrig = [intercept.point[i] - bias[i] for i in range(len(bias))]

            reflectIntercept = renderer.glCastRay(reflectOrig, reflect, None, recursion + 1)
            if reflectIntercept is not None:
                reflectColor = reflectIntercept.obj.material.GetSurfaceColor(reflectIntercept, renderer, recursion + 1)
            else:
                reflectColor = renderer.glEnvMapColor(intercept.point, reflect)

            # Generamos los rayos de refracción
            if not totalInternalReflection(intercept.normal, intercept.rayDirection, 1.0, self.ior):
                refract = refractVector(intercept.normal, intercept.rayDirection, 1.0, self.ior)

                if outside:
                    refractOrig = [intercept.point[i] - bias[i] for i in range(len(bias))]
                else:
                    refractOrig = [intercept.point[i] + bias[i] for i in range(len(bias))]

                refractIntercept = renderer.glCastRay(refractOrig, refract, None, recursion + 1)
                if refractIntercept is not None:
                    refractColor = refractIntercept.obj.material.GetSurfaceColor(refractIntercept, renderer, recursion + 1)
                else:
                    refractColor = renderer.glEnvMapColor(intercept.point, reflect)

                # Usando las ecuaciones de Fresnel, determinamos cuánta reflección
                # y cuánta refracción agregar al color final
                Kr, Kt = fresnel(intercept.normal, intercept.rayDirection, 1.0, self.ior)
                reflectColor = multiplicarPorEscalar(Kr, reflectColor)
                refractColor = multiplicarPorEscalar(Kt, refractColor)




        finalColor = [(finalColor[i] * (lightColor[i] + reflectColor[i] + refractColor[i]) ) for i in range(3)]
        finalColor = [min(1,finalColor[i]) for i in range(3)]

        return finalColor
    