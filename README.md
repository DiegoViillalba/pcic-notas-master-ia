# PCIC — Notas de clase

Sitio de apuntes del Posgrado en Ciencias e Ingeniería de la Computación (UNAM), generado con [Quartz](https://quartz.jzhao.xyz/) v5 a partir de mis notas en Obsidian.

Publicado en <https://diego-villalba.com/pcic-notas-master-ia/>.

## Alcance del contenido

Se publican las carpetas `Clases/` y `Recursos/` de cada materia, más `03_Conceptos/` (conceptos atómicos que las clases enlazan constantemente — sin ellos, buena parte de los wikilinks quedarían rotos). Quedan fuera intencionalmente:

- `Tareas/` — entregas y trabajo en progreso, de carácter privado.
- Literatura, plantillas y administración del vault — material interno de estudio, no pensado para publicarse.

## Desarrollo local

```bash
npm install
npx quartz build --serve
```

## Actualizar el contenido

Este repo es independiente del vault de Obsidian. La forma normal de actualizarlo es correr `python3 scripts/sync-vault.py`, que copia el contenido vigente desde el vault, corrige incrustaciones/enlaces y publica. Ver el docstring de ese script para el detalle de cada paso, o `scripts/sync-vault.py --help`.
