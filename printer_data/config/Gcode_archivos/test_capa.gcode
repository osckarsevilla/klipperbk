; Test de Primera Capa - 100x100mm
G21 ; Unidades en mm
G90 ; Coordenadas absolutas
M82 ; Extrusor en absoluto

; Inicio de calentamiento
M140 S60 ; Cama a 60°
M104 S200 ; Extrusor a 200°
M190 S60
M109 S200

START_PRINT BED=60 EXTRUDER=200 ; Llama a tu macro con Z-Tilt y Mesh

; Dibujo del cuadrado de prueba
G1 Z5 F3000 ; Levantar
G1 X60 Y60 F5000 ; Ir a posición inicial
G1 Z0.2 F300 ; Bajar a altura de capa
G1 X160 Y60 E3.5 F1500 ; Lado 1
G1 X160 Y160 E7 F1500 ; Lado 2
G1 X60 Y160 E10.5 F1500 ; Lado 3
G1 X60 Y60 E14 F1500 ; Lado 4

; Relleno rápido (opcional, para ver consistencia)
G1 X65 Y65 F5000
G1 X155 Y65 E17 F1200
G1 X155 Y70 F5000
G1 X65 Y70 E20 F1200

M117 Ajusta el Z-Offset ahora...
G4 S30 ; Pausa de 30 seg para que mires la capa