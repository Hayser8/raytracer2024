from MathLib import *

class Camera(object):
    def __init__(self):
        self.translate = [0,0,0]
        self.rotate = [0,0,0]

    def GetViewMatrix(self):

        translateMat = TrasnlationMatrix(self.translate[0], self.translate[1], self.translate[2])

        rotatexMat = rotacionX(self.rotate[0])
        rotateyMat = rotacionY(self.rotate[1])
        rotatezMat = rotacionZ(self.rotate[2])

        rotatesemifinal = multiplicarMatrices(rotatexMat, rotateyMat)
        rotatefinal = multiplicarMatrices(rotatesemifinal, rotatezMat)

        camMatrix = multiplicarMatrices(translateMat,rotatefinal)

        return inversaMatriz(camMatrix)