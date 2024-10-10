import pygame
from pygame.locals import *
from gl import RendererRT
from figures import *
from material import *
from lights import *
from texture import Texture

# Tamaño de la pantalla
width = 512
height = 512

screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rt = RendererRT(screen)
rt.envMap = Texture("textures/night.bmp")
rt.glClearColor(0.5, 0.0, 0.0)
rt.glClear()

# Materiales
mirror = Material(spec = 128, Ks = 0.2, matType = REFLECTIVE)
jade = Material(texture=Texture("textures/jade.bmp"))
glass = Material(spec=128, Ks=0.2, ior=1.5, matType=TRANSPARENT)
gold = Material([1, 1, 0], spec=128, Ks=0.2, ior=0.470, matType=TRANSPARENT)

snow = Material(diffuse=[1, 1, 1], spec=64, Ks=0.2)  # Blanco para el cuerpo del muñeco
black = Material(diffuse=[0, 0, 0], spec=128, Ks=0.5)  # Negro para los botones y pupilas
orange = Material(diffuse=[1, 0.5, 0], spec=64, Ks=0.3)  # Naranja para la nariz
basketball = Material(texture = Texture("textures/basketball.bmp"))
mirrortwo = Material(spec = 128, Ks = 0.2, matType = REFLECTIVE)
gray = Material(diffuse=[0.7, 0.7, 0.7], spec=32, Ks=0.1)  # Gris para los ojos

# Luces
rt.lights.append(DirectionalLight(direction=[-1, -1, -1], intensity=1.5))  # Aumentar intensidad
rt.lights.append(DirectionalLight(direction=[0.5, -0.5, -1], intensity=1.5, color=[1, 1, 1]))
rt.lights.append(AmbientLight(intensity=0.1))  # Aumentar la luz ambiental

# Añadir tres triángulos en la parte superior de la escena
rt.scene.append(Triangle(
    p0=[-2, 1, -5], 
    p1=[-1, 2, -5], 
    p2=[-2, 2, -5], 
    material=jade))  # Triángulo opaco

rt.scene.append(Triangle(
    p0=[-0.5, 1, -5], 
    p1=[0.5, 2, -5], 
    p2=[-0.5, 2, -5], 
    material=mirror))  # Triángulo reflectivo

rt.scene.append(Triangle(
    p0=[1, 1, -5], 
    p1=[2, 2, -5], 
    p2=[1, 2, -5], 
    material=glass))  # Triángulo transparente

# Añadir tres cilindros en la parte inferior de la escena
rt.scene.append(Cylinder(
    position=[-2, -1, -6], 
    radius=0.5, 
    height=1.5, 
    material=jade))  # Cilindro opaco

rt.scene.append(Cylinder(
    position=[0, -1, -6], 
    radius=0.5, 
    height=1.5, 
    material=mirror))  # Cilindro reflectivo

rt.scene.append(Cylinder(
    position=[2, -1, -6], 
    radius=0.5, 
    height=1.5, 
    material=glass))  # Cilindro reflectivo

# rt.scene.append(Cylinder(
#     position=[2, -1, -6], 
#     radius=0.5, 
#     height=1.5, 
#     material=glass))  # Cilindro transparente

# rt.scene.append(Sphere(position = [-1.5, 0, -5], radius = 0.7, material = jade))
# rt.scene.append(Sphere(position = [-1.5, -1.5, -5], radius = 0.7, material = basketball))
# rt.scene.append(Sphere(position = [0, 0, -5], radius = 0.7, material = mirror))
# rt.scene.append(Sphere(position = [0, -1.5, -5], radius = 0.7, material = mirrortwo))
# rt.scene.append(Sphere(position = [1.5, 0, -5], radius = 0.7, material = glass))
# rt.scene.append(Sphere(position = [1.5, -1.5, -5], radius = 0.7, material = gold))

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
