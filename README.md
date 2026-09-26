# PCIC — Notas de clase

Sitio de apuntes del Posgrado en Ciencias e Ingeniería de la Computación (UNAM), generado con [Quartz](https://quartz.jzhao.xyz/) v5 a partir de mis notas en Obsidian.

Publicado en <https://diego-villalba.com/pcic-notas/>.

## Alcance del contenido

Se publican únicamente las carpetas `Clases/` y `Recursos/` de cada materia. Quedan fuera intencionalmente:

- `Tareas/` — entregas y trabajo en progreso, de carácter privado.
- Notas de literatura, conceptos, plantillas y administración del vault — material interno de estudio, no pensado para publicarse.

## Desarrollo local

```bash
npm install
npx quartz build --serve
```

## Actualizar el contenido

Este repo es independiente del vault de Obsidian. Para publicar notas nuevas, copia las carpetas `Clases/` y `Recursos/` actualizadas de la materia correspondiente a `content/<Materia>/`, actualiza `content/index.md` si agregaste clases nuevas, haz commit y push a `main`; el deploy a GitHub Pages es automático (ver `.github/workflows/deploy.yml`).
