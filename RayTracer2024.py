import pygame
from pygame.locals import *
from gl import RendererRT
from figures import *
from material import Material
from lights import *

# Tamaño de la pantalla
width = 300
height = 400

screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rt = RendererRT(screen)

# Materiales para cada parte del muñeco
snow = Material(diffuse=[1, 1, 1], spec=64, Ks=0.2)  # Blanco para el cuerpo del muñeco
black = Material(diffuse=[0, 0, 0], spec=128, Ks=0.5)  # Negro para los botones y pupilas
orange = Material(diffuse=[1, 0.5, 0], spec=64, Ks=0.3)  # Naranja para la nariz
gray = Material(diffuse=[0.7, 0.7, 0.7], spec=32, Ks=0.1)  # Gris para los ojos

# Luces
rt.lights.append(DirectionalLight(direction=[-1, -1, -1]))
rt.lights.append(AmbientLight(intensity=0.2))

# Esferas para representar el cuerpo del muñeco de nieve (más pequeñas)
rt.scene.append(Sphere([0, -3, -8], 1.5, snow))  # Cuerpo inferior
rt.scene.append(Sphere([0, -1.5, -8], 1.2, snow))  # Cuerpo medio
rt.scene.append(Sphere([0, 0, -8], 0.9, snow))  # Cabeza

# Esferas para representar los botones (negros)
rt.scene.append(Sphere([0, -1, -6.5], 0.2, black))  # Botón superior
rt.scene.append(Sphere([0, -2, -6.5], 0.2, black))  # Botón medio
rt.scene.append(Sphere([0, -3, -6.5], 0.2, black))  # Botón inferior

# Esferas para representar los ojos (grises con pupilas negras)
rt.scene.append(Sphere([-0.25, 0.2, -6], 0.12, gray))  # Ojo izquierdo (gris)
rt.scene.append(Sphere([0.25, 0.2, -6], 0.12, gray))  # Ojo derecho (gris)
rt.scene.append(Sphere([-0.25, 0.2, -5.9], 0.05, black))  # Pupila izquierda (negro)
rt.scene.append(Sphere([0.25, 0.2, -5.9], 0.05, black))  # Pupila derecha (negro)

# Esfera para representar la nariz (naranja)
rt.scene.append(Sphere([0, 0, -6], 0.15, orange))  # Nariz

# Esferas para representar la boca (carita feliz con 4 esferas negras)
rt.scene.append(Sphere([-0.3, -0.15, -6], 0.07, black))  # Extremo izquierdo superior
rt.scene.append(Sphere([0.3, -0.15, -6], 0.07, black))  # Extremo derecho superior
rt.scene.append(Sphere([-0.15, -0.3, -6], 0.07, black))  # Izquierda
rt.scene.append(Sphere([0.15, -0.3, -6], 0.07, black))  # Derecha

rt.glRender()

# Generar el framebuffer como una imagen .bmp
rt.glGenerateFrameBuffer("output.bmp")

# Ciclo de renderizado
isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
