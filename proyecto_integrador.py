import bpy
import math

def crear_material(nombre, color_rgb):
    # Implementación del modelo de color RGB [cite: 10]
    mat = bpy.data.materials.new(name=nombre)
    mat.diffuse_color = (*color_rgb, 1.0)
    return mat

def generar_escenario_animado():
    # 1. Limpieza del entorno [cite: 3, 6]
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # 2. Definición de Materiales [cite: 9, 19]
    mat_pared_a = crear_material("ParedOscura", (0.1, 0.1, 0.1))
    mat_pared_b = crear_material("ParedDetalle", (0.8, 0.2, 0.0))

    # 3. Parámetros del Semicírculo
    cantidad_bloques = 15
    radio_interno = 7
    radio_externo = 11
    radio_central = (radio_interno + radio_externo) / 2 # Carril por donde pasará la cámara
    angulo_total = math.pi # 180 grados

    # 4. Construcción Procedural (Transformaciones de Traslación y Escalamiento) [cite: 22, 34]
    for i in range(cantidad_bloques):
        angulo = (i / (cantidad_bloques - 1)) * angulo_total
        
        # Posiciones mediante trigonometría
        for r, material, es_detalle in [(radio_interno, mat_pared_a, False), (radio_externo, mat_pared_a, True)]:
            x = math.cos(angulo) * r
            y = math.sin(angulo) * r
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, 1))
            bloque = bpy.context.active_object
            bloque.rotation_euler.z = angulo + math.pi/2
            
            # Lógica de color alternada para la pared "izquierda" (interna) [cite: 23, 30]
            if r == radio_interno:
                if i % 2 == 0:
                    bloque.data.materials.append(mat_pared_a)
                else:
                    bloque.data.materials.append(mat_pared_b)
                    bloque.scale.z = 1.5 # Escalamiento visual [cite: 34]
            else:
                bloque.data.materials.append(mat_pared_a)

    # 5. Suelo (Cilindro escalado para cubrir el arco) [cite: 37, 46]
    bpy.ops.mesh.primitive_cylinder_add(radius=radio_externo + 1, depth=0.1, location=(0,0,0))

    # --- ANIMACIÓN DE RECORRIDO INTERIOR ---
    bpy.ops.object.camera_add()
    camara = bpy.context.active_object
    bpy.context.scene.camera = camara

    frames_totales = 120
    bpy.context.scene.frame_end = frames_totales

    for f in range(frames_totales + 1):
        t = f / frames_totales
        angulo_cam = t * angulo_total # Recorrido completo de 0 a PI
        
        # Posicionamiento en el carril central
        camara.location.x = math.cos(angulo_cam) * radio_central
        camara.location.y = math.sin(angulo_cam) * radio_central
        camara.location.z = 1.2 # Altura de los ojos
        
        # Rotación para que la cámara siempre mire "hacia adelante" en la curva
        camara.rotation_euler.x = math.radians(90) 
        camara.rotation_euler.z = angulo_cam + math.pi/2 + math.radians(90)
        
        # Insertar Keyframes de animación
        camara.keyframe_insert(data_path="location", frame=f)
        camara.keyframe_insert(data_path="rotation_euler", frame=f)

generar_escenario_animado()
