from MathLib import reflejarVector, normalizarVector, productoPunto
import numpy as np
import math

class Light(object):
    def __init__(self, color=[1, 1, 1], intensity=1, lightType="None"):
        self.color = color
        self.intensity = intensity
        self.lightType = lightType

    def GetLightColor(self, intercept=None):
        return [(i * self.intensity) for i in self.color]

    def GetSpecularColor(self, intercept, viewPos):
        return [0, 0, 0]


class AmbientLight(Light):
    def __init__(self, color=[1, 1, 1], intensity=1):
        super().__init__(color, intensity, "Ambient")


class DirectionalLight(Light):
    def __init__(self, color=[1, 1, 1], intensity=1, direction=[0, -1, 0]):
        super().__init__(color, intensity, "Directional")
        # Reemplazo de np.linalg.norm con normalizarVector
        self.direction = normalizarVector(direction)

    def GetLightColor(self, intercept=None):
        lightColor = super().GetLightColor()

        if intercept:
            dir = [(i * -1) for i in self.direction]
            # Reemplazo de np.dot con productoPunto
            intensity = productoPunto(intercept.normal, dir)
            intensity = max(0, min(1, intensity))
            intensity *= (1 - intercept.obj.material.Ks)
            lightColor = [(i * intensity) for i in lightColor]

        return lightColor

    def GetSpecularColor(self, intercept, viewPos):
        specColor = self.color

        if intercept:
            dir = [(i * -1) for i in self.direction]
            reflect = reflejarVector(intercept.normal, dir)

            # Reemplazo de np.subtract y np.linalg.norm
            viewDir = [viewPos[i] - intercept.point[i] for i in range(3)]
            viewDir = normalizarVector(viewDir)

            # Reemplazo de np.dot con productoPunto
            specularity = max(0, productoPunto(viewDir, reflect)) ** intercept.obj.material.spec
            specularity *= intercept.obj.material.Ks
            specularity *= self.intensity
            specColor = [(i * specularity) for i in specColor]

        return specColor
    
class PointLight(Light):
    def __init__(self, color=[1,1,1], intensity=1, position=[0,0,0]):
        super().__init__(color, intensity,"Point")
        self.position = position

    def GetLightColor(self, intercept=None):
        lightColor = super().GetLightColor(intercept)

        if intercept:
            dir = [self.position[i] - intercept.point[i] for i in range(3)]
            R = math.sqrt(sum([d**2 for d in dir]))
            dir = [d / R for d in dir]

            intensity = sum([intercept.normal[i] * dir[i] for i in range(3)])
            intensity = max(0, min(1, intensity))
            intensity *= (1 - intercept.obj.material.Ks)

            # Ley de cuadrados inversos
            # attenuation = intensity / R^2
            # R es la distancia del punto intercepto a la luz punto
            if R != 0:
                intensity /= R**2

            lightColor = [i * intensity for i in lightColor]

        return lightColor


    def GetSpecularColor(self, intercept, viewPos):
        specColor = self.color

        if intercept:
            dir = [self.position[i] - intercept.point[i] for i in range(3)]
            R = math.sqrt(sum([d**2 for d in dir]))
            dir = [d / R for d in dir]

            reflect = reflejarVector(intercept.normal, dir)

            viewDir = [viewPos[i] - intercept.point[i] for i in range(3)]
            viewDir_magnitude = math.sqrt(sum([v**2 for v in viewDir]))
            viewDir = [v / viewDir_magnitude for v in viewDir]

            # Specular = (CV . R) ^ n * Ks
            specularity = max(0, sum([viewDir[i] * reflect[i] for i in range(3)])) ** intercept.obj.material.spec
            specularity *= intercept.obj.material.Ks
            specularity *= self.intensity

            if R != 0:
                specularity /= R**2

            specColor = [i * specularity for i in specColor]

        return specColor

class Spotlight(PointLight):
    def __init__(self, color=[1,1,1], intensity=1, position=[0,0,0], direction=[0,-1,0], innerAngle=50, outerAngle=60):
        super().__init__(color, intensity, position)
        self.direction = [d / math.sqrt(sum([x**2 for x in direction])) for d in direction] 
        self.innerAngle = innerAngle
        self.outerAngle = outerAngle
        self.LightType = "Spot"


    def GetLightColor(self, intercept=None):
        lightColor = super().GetLightColor(intercept)

        if intercept:
            lightColor = [i * self.SpotlightAttenuation(intercept) for i in lightColor]

        return lightColor


    def GetSpecularColor(self, intercept, viewPos):
        specularColor = super().GetSpecularColor(intercept, viewPos)

        if intercept:
            specularColor = [i * self.SpotlightAttenuation(intercept) for i in specularColor]

        return specularColor


    def SpotlightAttenuation(self, intercept=None):
        if intercept == None:
            return 0

        wi = [self.position[i] - intercept.point[i] for i in range(3)]
        wi_magnitude = math.sqrt(sum([wi[i]**2 for i in range(3)]))
        wi = [wi[i] / wi_magnitude for i in range(3)]  
        innerAngleRads = self.innerAngle * math.pi / 180
        outerAngleRads = self.outerAngle * math.pi / 180
        attenuation = (-sum([self.direction[i] * wi[i] for i in range(3)]) - math.cos(outerAngleRads)) / \
                    (math.cos(innerAngleRads) - math.cos(outerAngleRads))
        attenuation = min(1, max(0, attenuation))
        return attenuation

        