#!/usr/bin/env python3
"""
Sincroniza las notas de clase del vault de Obsidian con este repo Quartz
y publica el sitio (commit + push a main, lo que dispara el deploy).

Uso:
    python3 scripts/sync-vault.py            # sincroniza, compila y publica
    python3 scripts/sync-vault.py --no-push  # sincroniza y compila, sin publicar
    python3 scripts/sync-vault.py --dry-run  # solo muestra qué haría

Qué hace, en orden:
  1. Copia Clases/ y Recursos/ de cada materia desde el vault a content/.
     Clases/ se aplana directo a la raíz de la materia (content/<Materia>/,
     sin subcarpeta) para que en el explorador y la tabla de contenidos las
     clases aparezcan de inmediato al abrir la materia. Recursos/ se
     mantiene como subcarpeta aparte. También copia 03_Conceptos/ del vault
     a content/Conceptos/, porque muchas notas de clase enlazan a esos
     conceptos atómicos y sin ellos publicados esos wikilinks quedan rotos.
  2. Limpia basura (.DS_Store, *.log, *.aux, *.out) en el contenido copiado.
  3. Normaliza nombres de archivo y texto de notas a NFC (evita que archivos
     con acentos en forma NFD, comunes en iCloud Drive, dejen de resolverse).
  4. Renombra los laboratorios HTML interactivos de Recursos/ a .htm y
     reescribe sus incrustaciones ![[...]] como <iframe> reales, porque
     Quartz no soporta transcluir HTML standalone vía wikilinks.
  5. Reescribe cualquier wikilink con ruta completa (p. ej.
     "01_Materias/Algoritmos/Recursos/x.pdf") a solo el nombre de archivo,
     para que la resolución "shortest" de Quartz los encuentre sin importar
     la carpeta real dentro de content/.
  6. Elimina copias duplicadas (mismo nombre, mismo contenido) dentro de
     content/ — dos archivos con igual nombre en carpetas distintas rompen
     esa misma resolución "shortest". El vault original nunca se toca.
  7. Reconstruye el sitio (npx quartz build) para validar que no haya errores.
  8. Hace commit y push a main (salvo --no-push), lo que dispara el deploy
     automático de GitHub Pages.

content/index.md (la portada) NO se toca: es tuyo, edítalo directamente.
"""

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = REPO_ROOT / "content"

VAULT_ROOT = Path(
    "/Users/diegovillalba/Library/Mobile Documents/com~apple~CloudDocs/PCIC_Vault_reconstruido"
)
VAULT_MATERIAS_DIR = VAULT_ROOT / "01_Materias"
VAULT_CONCEPTOS_DIR = VAULT_ROOT / "03_Conceptos"

# Nombre de carpeta en el vault -> nombre de carpeta en content/ (idénticos hoy,
# pero se deja explícito por si un día divergen).
MATERIAS = [
    "Algoritmos",
    "Inteligencia_Artificial",
    "Modelacion_Matematica",
    "Prog_Avanzada",
    "Seminario_Orientacion",
]

JUNK_PATTERNS = [".DS_Store", "*.log", "*.aux", "*.out"]

WIKILINK_RE = re.compile(r"(!?)\[\[([^\]|#]+)((?:#[^\]|]*)?)(\|[^\]]*)?\]\]")
HTML_EMBED_RE = re.compile(r"(?<!`)!\[\[([^\]|]+\.html)\]\](?!`)")


def log(msg: str) -> None:
    print(f"-> {msg}")


def run(cmd, cwd=REPO_ROOT, check=True, capture=False):
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=capture)
    if check and result.returncode != 0:
        if capture:
            print(result.stdout)
            print(result.stderr, file=sys.stderr)
        raise SystemExit(f"Comando falló: {' '.join(cmd)}")
    return result


def copy_from_vault(dry_run: bool) -> None:
    """Copia Clases/ y Recursos/ de cada materia. Clases/ se aplana directo a
    la raíz de la materia (sin subcarpeta) para que en el explorador/TOC las
    clases aparezcan de inmediato al abrir la materia, no un nivel más abajo.
    Recursos/ sigue siendo una subcarpeta aparte."""
    if not VAULT_MATERIAS_DIR.is_dir():
        raise SystemExit(f"No se encontró el vault en: {VAULT_MATERIAS_DIR}")

    for materia in MATERIAS:
        vault_materia = VAULT_MATERIAS_DIR / materia
        dest_materia = CONTENT_DIR / materia

        if not vault_materia.is_dir():
            log(f"[aviso] {materia}: no existe en el vault, se omite")
            continue

        log(f"Copiando {materia}")
        if dry_run:
            continue

        if dest_materia.exists():
            shutil.rmtree(dest_materia)
        dest_materia.mkdir(parents=True, exist_ok=True)

        vault_clases = vault_materia / "Clases"
        if vault_clases.is_dir():
            for md in vault_clases.glob("*.md"):
                shutil.copy2(md, dest_materia / md.name)

        # Notas sueltas en la raíz de la materia (guías de estudio, etc.), salvo
        # "Indice*" — esas mezclan temario/evaluación/contacto del profesor y
        # tracking de tareas, contenido privado que no se publica.
        for md in vault_materia.glob("*.md"):
            if md.name.lower().startswith("indice"):
                continue
            shutil.copy2(md, dest_materia / md.name)

        vault_recursos = vault_materia / "Recursos"
        if vault_recursos.is_dir():
            shutil.copytree(vault_recursos, dest_materia / "Recursos")


def copy_conceptos(dry_run: bool) -> None:
    """Copia 03_Conceptos/ del vault a content/Conceptos/. Muchas notas de
    clase enlazan a estos conceptos atómicos; sin ellos publicados esos
    wikilinks quedan rotos."""
    if not VAULT_CONCEPTOS_DIR.is_dir():
        log("[aviso] 03_Conceptos no existe en el vault, se omite")
        return

    log("Copiando Conceptos")
    if dry_run:
        return

    dest = CONTENT_DIR / "Conceptos"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(VAULT_CONCEPTOS_DIR, dest)


def clean_junk(dry_run: bool) -> None:
    log("Limpiando basura (.DS_Store, *.log, *.aux, *.out)")
    if dry_run:
        return
    for pattern in JUNK_PATTERNS:
        for path in CONTENT_DIR.rglob(pattern):
            path.unlink()


def normalize_unicode(dry_run: bool) -> None:
    log("Normalizando nombres de archivo y texto a NFC")
    if dry_run:
        return

    # 1) Nombres de archivo/carpeta: de abajo hacia arriba para no invalidar
    #    rutas ya recorridas al renombrar un directorio padre.
    all_paths = sorted(CONTENT_DIR.rglob("*"), key=lambda p: len(p.parts), reverse=True)
    for path in all_paths:
        name = path.name
        normalized = unicodedata.normalize("NFC", name)
        if name != normalized:
            path.rename(path.with_name(normalized))

    # 2) Contenido de las notas markdown.
    for md in CONTENT_DIR.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        normalized = unicodedata.normalize("NFC", text)
        if text != normalized:
            md.write_text(normalized, encoding="utf-8")


def fix_html_embeds(dry_run: bool) -> None:
    log("Convirtiendo laboratorios HTML (.html -> .htm + <iframe>)")
    if dry_run:
        return

    renamed = 0
    for path in CONTENT_DIR.rglob("*.html"):
        new_path = path.with_suffix(".htm")
        path.rename(new_path)
        renamed += 1
    if renamed:
        log(f"  {renamed} archivo(s) .html renombrados a .htm")

    replaced = 0
    for md in CONTENT_DIR.rglob("*.md"):
        text = md.read_text(encoding="utf-8")

        def repl(m: re.Match) -> str:
            nonlocal replaced
            target = m.group(1)
            basename = os.path.basename(target)[: -len(".html")] + ".htm"
            replaced += 1
            return (
                f'<iframe src="{basename}" style="width:100%;height:600px;'
                f'border:1px solid var(--lightgray);border-radius:4px;" loading="lazy"></iframe>'
            )

        new_text = HTML_EMBED_RE.sub(repl, text)
        if new_text != text:
            md.write_text(new_text, encoding="utf-8")
    if replaced:
        log(f"  {replaced} incrustación(es) HTML reescritas como <iframe>")


def fix_wikilink_paths(dry_run: bool) -> None:
    log("Simplificando wikilinks con ruta completa a solo nombre de archivo")
    if dry_run:
        return

    # Nombres (sin extensión) de los recursos .htm ya renombrados, para poder
    # completar la extensión en links tipo [[expectimax-paso-a-paso]] que en
    # el vault original apuntaban al archivo sin extensión.
    htm_stems = {p.stem.lower() for p in CONTENT_DIR.rglob("*.htm")}

    total = 0
    for md in CONTENT_DIR.rglob("*.md"):
        text = md.read_text(encoding="utf-8")

        def repl(m: re.Match) -> str:
            nonlocal total
            bang, target, anchor, alias = m.groups()
            target = target.strip()
            basename = target.rsplit("/", 1)[-1] if "/" in target else target
            changed = "/" in target
            # Los .html de Recursos ya se renombraron a .htm (ver
            # fix_html_embeds); un [[link|alias]] normal (sin "!") que todavía
            # apunte a ".html" quedaría roto si no se actualiza aquí también.
            if basename.lower().endswith(".html"):
                basename = basename[: -len(".html")] + ".htm"
                changed = True
            elif "." not in basename and basename.lower() in htm_stems:
                basename = basename + ".htm"
                changed = True
            if not changed:
                return m.group(0)
            total += 1
            return f"{bang}[[{basename}{anchor}{alias or ''}]]"

        new_text = WIKILINK_RE.sub(repl, text)
        if new_text != text:
            md.write_text(new_text, encoding="utf-8")
    if total:
        log(f"  {total} wikilink(s) simplificados")


def fix_display_math(dry_run: bool) -> None:
    """Pone los delimitadores $$ de los bloques de matematica display en su
    propia linea (y vuelve bloque lo que va en una sola linea). Quartz/remark-math falla con "$$\\begin{aligned}" pegado en
    la misma linea (KaTeX recibe el bloque sin \\begin y la pagina se corta en
    ese punto). Obsidian si lo acepta, por eso en el vault no se nota."""
    log("Separando delimitadores $$ de bloques de matematica display")
    open_re = re.compile(r"^(\s*(?:>\s*)*)\$\$(.*)$")
    changed = 0
    for md in CONTENT_DIR.rglob("*.md"):
        if md == CONTENT_DIR / "index.md":
            continue
        out, in_math, in_code, dirty = [], False, False, False
        prefix = ""
        for line in md.read_text(encoding="utf-8").split("\n"):
            if not in_math and line.lstrip(" >").startswith("```"):
                in_code = not in_code
            if in_code:
                out.append(line)
                continue
            if not in_math:
                m = open_re.match(line)
                one = re.match(r"^(\s*(?:>\s*)*)\$\$(.+?)\$\$\s*$", line)
                if one and one.group(2).strip() and "$$" not in one.group(2):
                    # "$$ f $$" solo en su linea: remark-math lo toma como
                    # formula inline; se convierte a bloque para centrarla.
                    pre = one.group(1)
                    out += [f"{pre}$$", f"{pre}{one.group(2).strip()}", f"{pre}$$"]
                    dirty = True
                    continue
                if m and "$$" not in m.group(2):
                    prefix = m.group(1)
                    in_math = True
                    if m.group(2).strip():
                        out += [f"{prefix}$$", f"{prefix}{m.group(2).strip()}"]
                        dirty = True
                        continue
                out.append(line)
            else:
                idx = line.find("$$")
                if idx == -1:
                    out.append(line)
                    continue
                in_math = False
                before, after = line[:idx], line[idx + 2 :]
                if before.strip():
                    out.append(before.rstrip())
                    out.append(f"{prefix}$${after}")
                    dirty = True
                else:
                    out.append(line)
        if dirty:
            changed += 1
            if not dry_run:
                md.write_text("\n".join(out), encoding="utf-8")
    log(f"  {changed} nota(s) con bloques $$ corregidos")


def fix_math_dollars(dry_run: bool) -> None:
    """Dentro de matematica, cambia "\\$" por "\\mathdollar ". Quartz le quita
    la barra al escape de markdown antes de que KaTeX vea la formula, asi que
    "$U(\\$3k)$" llega como "U($3k)" y KaTeX falla con un "$" suelto. Fuera de
    matematica "\\$" se deja igual (es el escape normal de markdown)."""
    log("Reemplazando \\$ dentro de formulas por \\mathdollar")
    display_re = re.compile(r"\$\$(.+?)\$\$", re.S)
    inline_re = re.compile(r"(?<![\\$])\$(?!\$)((?:[^$\\\n]|\\.)+?)\$(?!\$)")

    def swap(m: re.Match) -> str:
        body = m.group(1).replace("\\$", "\\mathdollar ")
        return m.group(0)[: m.start(1) - m.start()] + body + m.group(0)[m.end(1) - m.start() :]

    changed = 0
    for md in CONTENT_DIR.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        if "\\$" not in text:
            continue
        new = display_re.sub(swap, text)
        new = inline_re.sub(swap, new)
        if new != text:
            changed += 1
            if not dry_run:
                md.write_text(new, encoding="utf-8")
    log(f"  {changed} nota(s) con \\$ en formulas corregidas")


SVG_EMBED_RE = re.compile(r"(?<!`)!\[\[([^\]|]+\.svg)(?:\|[^\]]*)?\]\](?!`)")


def fix_svg_embeds(dry_run: bool) -> None:
    """Convierte ![[x.svg]] en una imagen markdown ![alt](x.svg).
    Quartz traduce el wikilink de un SVG a <object data="x.svg"> con la ruta
    sin resolver (relativa a la nota, no a Recursos/), asi que el navegador
    recibe un 404 y el diagrama nunca aparece. Como imagen markdown la ruta si
    se resuelve. El alt se toma del <title> del SVG."""
    log("Convirtiendo incrustaciones de SVG a imagenes")
    titles = {}
    for svg in CONTENT_DIR.rglob("*.svg"):
        m = re.search(r"<title[^>]*>(.*?)</title>", svg.read_text(encoding="utf-8", errors="ignore"), re.S)
        titles[svg.name] = re.sub(r"[\[\]\n]", " ", m.group(1)).strip() if m else ""
    changed = 0
    for md in CONTENT_DIR.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        new = SVG_EMBED_RE.sub(
            lambda m: f"![{titles.get(Path(m.group(1)).name, '')}]({Path(m.group(1)).name})", text
        )
        if new != text:
            changed += 1
            if not dry_run:
                md.write_text(new, encoding="utf-8")
    log(f"  {changed} nota(s) con SVG convertidos")


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def dedupe_identical_files(dry_run: bool) -> None:
    """Obsidian embeds resuelven por nombre de archivo (estrategia 'shortest'),
    así que dos archivos con el mismo nombre en distintas carpetas rompen la
    resolución de enlaces. Si su contenido es idéntico, basta con conservar
    uno solo dentro de content/ (el vault original no se toca)."""
    by_name = defaultdict(list)
    for path in CONTENT_DIR.rglob("*"):
        if path.is_file() and path.suffix.lower() != ".md":
            by_name[path.name.lower()].append(path)

    removed = 0
    unresolved = []
    for name, paths in by_name.items():
        if len(paths) < 2:
            continue
        hashes = {p: _sha256(p) for p in paths}
        if len(set(hashes.values())) == 1:
            # Idénticos: conserva el de ruta más corta (más "canónico"), borra el resto.
            paths.sort(key=lambda p: len(p.parts))
            keep, drop = paths[0], paths[1:]
            for p in drop:
                removed += 1
                if not dry_run:
                    p.unlink()
        else:
            unresolved.append((name, paths))

    if removed:
        log(f"Deduplicando: {removed} copia(s) idéntica(s) eliminada(s) dentro de content/")
    if unresolved:
        log("[aviso] mismo nombre pero contenido distinto (revisar a mano):")
        for name, paths in unresolved:
            for p in paths:
                print(f"     {p.relative_to(CONTENT_DIR)}")


def build_site(dry_run: bool) -> None:
    log("Compilando el sitio (npx quartz build)")
    if dry_run:
        return
    run(["npx", "quartz", "build"])


def git_publish(push: bool, dry_run: bool) -> None:
    run(["git", "add", "-A"])
    status = run(["git", "status", "--porcelain"], capture=True)
    if not status.stdout.strip():
        log("Sin cambios que publicar")
        return

    log("Cambios detectados:")
    print(status.stdout)

    if dry_run:
        log("[dry-run] no se hace commit ni push")
        return

    run(
        [
            "git",
            "commit",
            "-m",
            "Sincronizar notas desde el vault de Obsidian\n\n"
            "Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>",
        ]
    )

    if push:
        log("Haciendo push a origin/main")
        run(["git", "push", "origin", "main"])
        log("Listo. El deploy se dispara automáticamente en GitHub Actions.")
    else:
        log("Commit creado localmente (--no-push): pushea manualmente cuando quieras")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-push", action="store_true", help="No hacer push tras el commit")
    parser.add_argument(
        "--dry-run", action="store_true", help="Mostrar qué se haría, sin modificar nada"
    )
    args = parser.parse_args()

    copy_from_vault(args.dry_run)
    copy_conceptos(args.dry_run)
    clean_junk(args.dry_run)
    normalize_unicode(args.dry_run)
    fix_html_embeds(args.dry_run)
    fix_wikilink_paths(args.dry_run)
    fix_display_math(args.dry_run)
    fix_math_dollars(args.dry_run)
    fix_svg_embeds(args.dry_run)
    dedupe_identical_files(args.dry_run)
    build_site(args.dry_run)
    git_publish(push=not args.no_push, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
