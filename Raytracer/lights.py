from MathLib import reflejarVector, normalizarVector, productoPunto

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
