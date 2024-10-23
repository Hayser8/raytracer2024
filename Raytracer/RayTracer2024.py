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
rt.envMap = Texture("textures/sky.bmp")  
rt.glClearColor(0.5, 0.0, 0.0)
rt.glClear()

# Materiales
stone = Material(texture=Texture("textures/stone.bmp"))
sand = Material(texture=Texture("textures/sand2.bmp"))
dark_green = Material(diffuse=[0.1, 0.3, 0.1], spec=32, Ks=0.1)  
gray = Material(diffuse=[0.7, 0.7, 0.7], spec=32, Ks=0.1)  
water = Material(diffuse=[0.1, 0.3, 0.6], spec=64, Ks=0.3, matType=REFLECTIVE)  
brown = Material(diffuse=[0.4, 0.2, 0.1], spec=32, Ks=0.1)  

# Luces
rt.lights.append(DirectionalLight(color=[1, 1, 1], intensity=1.5, direction=[-1, -1, -1]))  
rt.lights.append(AmbientLight(color=[1, 1, 1], intensity=0.2))  
rt.lights.append(PointLight(color=[1, 1, 1], intensity=1.2, position=[0, 1, -3]))  
rt.lights.append(Spotlight(color=[1, 1, 1], intensity=1.0, position=[2, 1, -5], direction=[0, -1, -1], innerAngle=30, outerAngle=45)) 


# Arena (plano)
rt.scene.append(Plane(position=[0, -1, -5], normal=[0, 1, 0], material=sand))

# Lago pequeño (disk)
rt.scene.append(Disk(position=[2, -0.99, -7], normal=[0, 1, 0], radius=2, material=water))

# Bambú alrededor del lago
rt.scene.append(Cylinder(position=[1, -1, -6], radius=0.1, height=1.8, material=dark_green))
rt.scene.append(Cylinder(position=[3, -1, -8], radius=0.1, height=1.6, material=dark_green))
rt.scene.append(Cylinder(position=[1.5, -1, -6], radius=0.1, height=1.8, material=dark_green))
rt.scene.append(Cylinder(position=[2.5, -1, -8], radius=0.1, height=1.5, material=dark_green))

# Crear un Bonsái (Cono con Cilindro)
rt.scene.append(Cone(position=[1.2, -1, -3.5], radius=0.25, height=0.4, material=gray))  # Base del bonsái ajustada
rt.scene.append(Cylinder(position=[1.2, -0.7, -3.5], radius=0.35, height=0.4, material=dark_green))  # Hojas del bonsái ajustadas

# Pirámide decorativa más pequeña y con color marrón sólido
rt.scene.append(Pyramid(position=[0.5, -1, -3], base=0.7, height=0.5, material=brown))

# Camino delimitado por piedras (patrón ondulado más natural)
left_positions = [
    [-2.2, -0.8, -2.3],
    [-2.0, -0.8, -3.2],
    [-2.3, -0.8, -4.1],
    [-2.1, -0.8, -5.0],
    [-2.4, -0.8, -6.1],
    [-2.2, -0.8, -7.0],
    [-2.3, -0.8, -8.2],
    [-2.1, -0.8, -9.3],
    [-2.3, -0.8, -10.1]
]
right_positions = [
    [-0.6, -0.8, -2.5],
    [-0.8, -0.8, -3.4],
    [-0.5, -0.8, -4.3],
    [-0.7, -0.8, -5.3],
    [-0.5, -0.8, -6.3],
    [-0.8, -0.8, -7.2],
    [-0.6, -0.8, -8.0],
    [-0.7, -0.8, -9.1],
    [-0.5, -0.8, -10.2]
]

# Tamaños de las piedras ajustados para que sean más pequeñas pero aún proporcionales
sizes = [0.3, 0.25, 0.2, 0.18, 0.15, 0.12, 0.1, 0.08, 0.06]

for i in range(len(left_positions)):
    rt.scene.append(Sphere(position=left_positions[i], radius=sizes[i], material=stone))
    rt.scene.append(Sphere(position=right_positions[i], radius=sizes[i], material=stone))

# Añadir más piedras para suplantar los huecos
extra_positions = [
    [-1.9, -0.8, -2.9], [-0.7, -0.8, -3.8], [-2.1, -0.8, -5.7], [-0.6, -0.8, -6.7]
]
extra_sizes = [0.2, 0.15, 0.1, 0.08]

for i in range(len(extra_positions)):
    rt.scene.append(Sphere(position=extra_positions[i], radius=extra_sizes[i], material=stone))

# Piedras grandes cerca del agua
rt.scene.append(Sphere(position=[0.5, -0.5, -7], radius=0.5, material=stone))
rt.scene.append(Sphere(position=[3.5, -0.5, -7], radius=0.5, material=stone))

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
