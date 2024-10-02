import pygame
from pygame.locals import *
from gl import RendererRT
from figures import *
from material import *
from lights import *
from texture import Texture

# Tamaño de la pantalla
width = 256
height = 256

screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rt = RendererRT(screen)
rt.glClearColor(0.5,0.0,0.0)
rt.glClear()

# Materiales
mirror = Material( spec = 128, Ks = 0.2, matType = REFLECTIVE)
jade = Material(texture = Texture("textures/jade.bmp"))
basketball = Material(texture = Texture("textures/basketball.bmp"))
glass = Material(spec = 128, Ks =0.2, ior = 1.5, matType=TRANSPARENT)
gold = Material([1,1,0],spec = 128, Ks =0.2, ior = 0.470, matType=TRANSPARENT)

snow = Material(diffuse=[1, 1, 1], spec=64, Ks=0.2)  # Blanco para el cuerpo del muñeco
black = Material(diffuse=[0, 0, 0], spec=128, Ks=0.5)  # Negro para los botones y pupilas
orange = Material(diffuse=[1, 0.5, 0], spec=64, Ks=0.3)  # Naranja para la nariz
gray = Material(diffuse=[0.7, 0.7, 0.7], spec=32, Ks=0.1)  # Gris para los ojos
mirror = Material(diffuse = [0.9,0.9,0.9], spec=128, Ks=0.2, matType= REFLECTIVE)

# Luces
# Luces
rt.lights.append(DirectionalLight(direction = [-1, -1, -1], intensity = 1.5))  # Aumentar intensidad
rt.lights.append(DirectionalLight(direction = [0.5, -0.5, -1], intensity = 1.5, color = [1, 1, 1]))
rt.lights.append(AmbientLight(intensity = 0.4))  # Aumentar la luz ambiental


rt.scene.append(Plane(position = [0, -1.5, -5], normal = [0, 1, 0], material = mirror))  # Suelo
rt.scene.append(Plane(position = [0, 1.5, -5], normal = [0, -1, 0], material = snow))  # Techo
rt.scene.append(Plane(position = [-2, 0, -5], normal = [1, 0, 0], material = snow))  # Pared izquierda
rt.scene.append(Plane(position = [2, 0, -5], normal = [-1, 0, 0], material = snow))  # Pared derecha
rt.scene.append(Plane(position = [0, 0, -7], normal = [0, 0, 1], material = snow))  # Pared del fondo


# Añadir dos cubos
rt.scene.append(AABB(position = [-1, -1, -5], sizes = [1, 1, 1], material = jade))  # Cubo 1
rt.scene.append(AABB(position = [1, -1, -5], sizes = [1, 1, 1], material = black))  # Cubo 2

# Añadir un disco
rt.scene.append(Disk(position = [0, -1.4, -4], normal = [0, 1, 0], radius = 0.7, material = orange))  # Disco


# Renderizar la escena
rt.glRender()

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
