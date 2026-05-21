# Organización de macros (Mainsail / Fluidd)

## Grupos configurados

| Grupo | Macros |
|-------|--------|
| **Impresión** | START_PRINT, END_PRINT, PURGA_MANUAL, LINE_PURGE, PAUSE, RESUME, CANCEL_PRINT |
| **Calibración** | CALIBRAR_TODO, CALIBRAR_Z, CALIBRAR_CAMA, BLTOUCH_TEST |
| **Cama y tornillos** | TORNILLOS, IR_TORNILLO |
| **Malla** | MESH_SAVED, MESH_GUARDAR, MESH_BORRAR |
| **Filamento** | LOAD_FILAMENT, UNLOAD_FILAMENT, ATASCADO |
| **Mantenimiento** | MOTORS_OFF, CAMA_FRIO, VENTILADOR_OFF |

Las descripciones en Klipper usan el prefijo `[Grupo]` para buscarlas en modo Simple.

## Aplicar en la impresora

Con Moonraker en marcha:

```bash
python3 ~/printer_data/config/scripts/apply_macros_ui.py
# O desde otro PC:
python3 ~/printer_data/config/scripts/apply_macros_ui.py http://192.168.3.174:7125
```

Luego **F5** en Mainsail o Fluidd.

### Mainsail (manual)

1. Ajustes (engranaje) → **Macros** → modo **Expert**
2. Crear los mismos grupos que en `macros_ui.json` o ejecutar el script

### Fluidd (manual)

1. Ajustes → **Macros** → **Categories**
2. Crear categorías y asignar cada macro con su color

## Editar grupos

Modifica `printer_data/config/macros_ui.json` y vuelve a ejecutar el script.

## Dashboard Mainsail

En **Ajustes → Dashboard** puedes añadir un panel por cada grupo de macros (modo Expert).
