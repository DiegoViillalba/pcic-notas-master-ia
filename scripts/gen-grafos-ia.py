#!/usr/bin/env python3
"""
Genera los grafos (SVG a color) de las notas de Inteligencia Artificial
sobre redes bayesianas y los escribe en Recursos/ de la materia en el vault.

    python3 scripts/gen-grafos-ia.py            # escribe en el vault
    python3 scripts/gen-grafos-ia.py --out DIR  # escribe en otra carpeta

Convencion de colores (se repite en la leyenda de cada figura):
  azul     raiz / causa (sin padres)
  morado   nodo intermedio
  naranja  efecto / hoja
  verde    evidencia observada
  rojo     variable de consulta
  gris     variable oculta (se suma)
  amarillo manta de Markov / elemento resaltado
Aristas: verde = camino activo, rojo discontinuo = camino bloqueado.
"""

import argparse
import html
from pathlib import Path

VAULT_RECURSOS = Path(
    "/Users/diegovillalba/Library/Mobile Documents/com~apple~CloudDocs/"
    "PCIC_Vault_reconstruido/01_Materias/Inteligencia_Artificial/Recursos"
)

W = 840
R = 30

# estado -> (relleno, borde, nombre en leyenda)
STATES = {
    "r": ("#dbe9fb", "#2f6fbd", "raíz / causa"),
    "m": ("#ece1fa", "#7b4fb8", "intermedio"),
    "e": ("#fde5cc", "#d8731a", "efecto"),
    "o": ("#c9efd6", "#1f8a4c", "evidencia observada"),
    "q": ("#fbd5d5", "#c93a3a", "consulta"),
    "h": ("#f1f1ef", "#8a8a85", "oculta (se suma)"),
    "y": ("#fff0b8", "#c49a00", "resaltado"),
}
EDGE = {"": "#55626e", "act": "#1f9d55", "blk": "#d64545", "new": "#7b4fb8"}


def esc(s):
    return html.escape(str(s), quote=False)


class Fig:
    def __init__(self, title, desc):
        self.title, self.desc = title, desc
        self.parts, self.y, self.used = [], 62, []

    # ---- primitivas -------------------------------------------------
    def _node(self, x, y, sym, label, st, badge=None, ring=False):
        fill, stroke, _ = STATES[st]
        if st not in self.used:
            self.used.append(st)
        dash = ' stroke-dasharray="6 4"' if st == "h" else ""
        sw = 3 if st in ("o", "q", "y") else 2.2
        out = []
        if ring:
            out.append(f'<circle cx="{x}" cy="{y}" r="{R + 6}" fill="none" stroke="{stroke}" stroke-width="1.6" stroke-dasharray="3 3"/>')
        out.append(f'<circle cx="{x}" cy="{y}" r="{R}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>')
        out.append(f'<text class="sym" x="{x}" y="{y + 8}">{esc(sym)}</text>')
        if label:
            out.append(f'<text class="lab" x="{x}" y="{y + R + 20}">{esc(label)}</text>')
        if badge:
            by = y + R + (40 if label else 22)
            out.append(f'<text class="badge" x="{x}" y="{by}" fill="{stroke}">{esc(badge)}</text>')
        return "\n".join(out)

    def _edge(self, a, b, kind, nodes):
        import math

        (x1, y1), (x2, y2) = nodes[a][:2], nodes[b][:2]
        d = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / d, (y2 - y1) / d
        sx, sy = x1 + ux * (R + 3), y1 + uy * (R + 3)
        ex, ey = x2 - ux * (R + 7), y2 - uy * (R + 7)
        col = EDGE[kind]
        dash = ' stroke-dasharray="7 5"' if kind in ("blk", "new") else ""
        sw = 3.2 if kind == "act" else 2.4
        mk = {"": "a0", "act": "a1", "blk": "a2", "new": "a3"}[kind]
        return f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{col}" stroke-width="{sw}"{dash} marker-end="url(#{mk})"/>'

    def _und(self, a, b, nodes, kind="new"):
        (x1, y1), (x2, y2) = nodes[a][:2], nodes[b][:2]
        col = EDGE[kind]
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="2.6" stroke-dasharray="7 5"/>'

    # ---- panel ------------------------------------------------------
    def panel(self, nodes, edges, h, subtitle=None, verdict=None, vcolor="neutral",
              note=None, cx=None, width=W, undirected=(), chips=(), x0=0):
        """nodes: {id: (x, y, simbolo, etiqueta, estado[, insignia[, aro]])}
        edges: [(a, b, tipo)] ; coordenadas relativas al panel."""
        top = self.y
        g = []
        if subtitle:
            g.append(f'<text class="sub" x="{x0 + width / 2}" y="{top + 22}">{esc(subtitle)}</text>')
            top_nodes = top + 36
        else:
            top_nodes = top + 6
        abs_nodes = {}
        for k, v in nodes.items():
            x, y = v[0] + x0, v[1] + top_nodes
            abs_nodes[k] = (x, y)
        for a, b, kind in edges:
            g.append(self._edge(a, b, kind, abs_nodes))
        for a, b in undirected:
            g.append(self._und(a, b, abs_nodes))
        for k, v in nodes.items():
            x, y = abs_nodes[k]
            sym, lab, st = v[2], v[3], v[4]
            badge = v[5] if len(v) > 5 else None
            ring = v[6] if len(v) > 6 else False
            g.append(self._node(x, y, sym, lab, st, badge, ring))
        for (cxp, cyp, txt) in chips:
            tw = 10 + 8.2 * len(txt)
            g.append(f'<rect x="{cxp + x0 - tw / 2:.0f}" y="{cyp + top_nodes - 13}" width="{tw:.0f}" height="26" rx="13" fill="#fff" stroke="#b9b5a8"/>'
                     f'<text class="chip" x="{cxp + x0}" y="{cyp + top_nodes + 5}">{esc(txt)}</text>')
        maxy = max(v[1] for v in nodes.values())
        extra = 56 if any(len(v) > 5 and v[5] for v in nodes.values()) else 34
        yy = top_nodes + max(h, maxy + R + extra)
        if verdict:
            colr = {"ok": ("#d7f2e0", "#1f8a4c"), "bad": ("#fbdcdc", "#c93a3a"),
                    "neutral": ("#e6ebf2", "#41566e"), "warn": ("#fff0b8", "#8a6d00")}[vcolor]
            tw = 24 + 8.4 * len(verdict)
            g.append(f'<rect x="{x0 + width / 2 - tw / 2:.0f}" y="{yy - 4}" width="{tw:.0f}" height="30" rx="15" fill="{colr[0]}" stroke="{colr[1]}"/>'
                     f'<text class="verd" x="{x0 + width / 2}" y="{yy + 16}" fill="{colr[1]}">{esc(verdict)}</text>')
            yy += 40
        if note:
            for line in ([note] if isinstance(note, str) else note):
                g.append(f'<text class="note" x="{x0 + width / 2}" y="{yy + 14}">{esc(line)}</text>')
                yy += 22
        self.parts.append("\n".join(g))
        self.y = yy + 16 if x0 == 0 and width == W else self.y
        self._last_bottom = yy + 16
        return self

    def advance(self):
        self.y = self._last_bottom

    def rule(self):
        self.parts.append(f'<line x1="60" y1="{self.y - 8}" x2="{W - 60}" y2="{self.y - 8}" stroke="#d8d4c8" stroke-dasharray="2 5"/>')
        self.y += 8

    def footer(self, lines):
        for line in ([lines] if isinstance(lines, str) else lines):
            self.parts.append(f'<text class="foot" x="{W / 2}" y="{self.y + 14}">{esc(line)}</text>')
            self.y += 24

    def svg(self):
        # leyenda
        used = [s for s in self.used]
        items, x = [], 0
        widths = {s: 34 + 8.2 * len(STATES[s][2]) for s in used}
        total = sum(widths.values())
        x = (W - total) / 2
        leg = []
        ly = self.y + 18
        for s in used:
            fill, stroke, name = STATES[s]
            dash = ' stroke-dasharray="4 3"' if s == "h" else ""
            leg.append(f'<circle cx="{x + 10:.0f}" cy="{ly}" r="8" fill="{fill}" stroke="{stroke}" stroke-width="2"{dash}/>'
                       f'<text class="leg" x="{x + 24:.0f}" y="{ly + 5}">{esc(name)}</text>')
            x += widths[s]
        H = ly + 26
        defs = "".join(
            f'<marker id="{i}" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0 0 L9 4.5 L0 9 Z" fill="{c}"/></marker>'
            for i, c in (("a0", EDGE[""]), ("a1", EDGE["act"]), ("a2", EDGE["blk"]), ("a3", EDGE["new"])))
        style = ("text{font-family:system-ui,-apple-system,'Segoe UI',sans-serif;fill:#26333d;text-anchor:middle}"
                 ".ttl{font-size:23px;font-weight:700}.sub{font-size:18px;font-weight:600;fill:#41566e}"
                 ".sym{font-size:24px;font-weight:700}.lab{font-size:16px;fill:#4a5560;paint-order:stroke;stroke:#fbfaf6;stroke-width:6px;stroke-linejoin:round}.badge{font-size:13px;font-weight:700}"
                 ".chip{font-size:14px;fill:#41566e}.verd{font-size:15px;font-weight:700}.note{font-size:15px;fill:#4a5560}"
                 ".foot{font-size:17px;fill:#26333d}.leg{font-size:14px;fill:#4a5560;text-anchor:start}")
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H:.0f}" viewBox="0 0 {W} {H:.0f}" role="img" aria-labelledby="t d">\n'
                f'<title id="t">{esc(self.title)}</title>\n<desc id="d">{esc(self.desc)}</desc>\n<defs>{defs}</defs>\n<style>{style}</style>\n'
                f'<rect x="1" y="1" width="{W - 2}" height="{H - 2:.0f}" rx="14" fill="#fbfaf6" stroke="#d8d4c8" stroke-width="2"/>\n'
                f'<text class="ttl" x="{W / 2}" y="38">{esc(self.title)}</text>\n'
                + "\n".join(self.parts) + "\n" + "\n".join(leg) + "\n</svg>\n")


def figure(title, desc):
    return Fig(title, desc)


OUT = {}


def P(f, *a, **k):
    f.panel(*a, **k)
    f.advance()
    return f


# =====================================================================
# Helpers de redes recurrentes
# =====================================================================
def lluvia(title, desc):
    f = figure(title, desc)
    P(f, {"R": (420, 50, "R", "lluvia", "r"), "T": (250, 190, "T", "tráfico", "e"), "U": (590, 190, "U", "paraguas", "e")},
      [("R", "T", ""), ("R", "U", "")], 270,
      verdict="Dada R, T y U son independientes", vcolor="ok",
      note="Sin observar R, T y U pueden estar asociados a través de la lluvia.")
    f.footer("P(R,T,U) = P(R) P(T|R) P(U|R)")
    return f


def alarma(title, desc, estados=None, badges=None, verdict=None, vcolor="neutral", note=None, chips=True, formula=True):
    est = {"B": "r", "E": "r", "A": "m", "J": "e", "M": "e"}
    est.update(estados or {})
    bd = badges or {}
    nodes = {
        "B": (260, 50, "B", "robo", est["B"], bd.get("B")),
        "E": (580, 50, "E", "terremoto", est["E"], bd.get("E")),
        "A": (420, 170, "A", "alarma", est["A"], bd.get("A")),
        "J": (260, 295, "J", "John llama", est["J"], bd.get("J")),
        "M": (580, 295, "M", "Mary llama", est["M"], bd.get("M")),
    }
    ed = [("B", "A", ""), ("E", "A", ""), ("A", "J", ""), ("A", "M", "")]
    ch = [(330, 50 - 0, "P(B)")][:0]
    chips_l = []
    if chips:
        chips_l = [(165, 50, "P(B)"), (675, 50, "P(E)"), (525, 170, "P(A | B,E)"), (150, 295, "P(J | A)"), (690, 295, "P(M | A)")]
    f = figure(title, desc)
    P(f, nodes, ed, 360, chips=chips_l, verdict=verdict, vcolor=vcolor, note=note)
    if formula:
        f.footer("P(B,E,A,J,M) = P(B) P(E) P(A|B,E) P(J|A) P(M|A)")
    return f


def aspersor(title, desc, estados=None, badges=None, verdict=None, vcolor="neutral", note=None, chips=True, formula=True, ring=None):
    est = {"C": "r", "S": "m", "R": "m", "W": "e"}
    est.update(estados or {})
    bd = badges or {}
    nodes = {
        "C": (420, 50, "C", "nublado", est["C"], bd.get("C")),
        "S": (250, 175, "S", "aspersor", est["S"], bd.get("S")),
        "R": (590, 175, "R", "lluvia", est["R"], bd.get("R")),
        "W": (420, 300, "W", "pasto mojado", est["W"], bd.get("W")),
    }
    ed = [("C", "S", ""), ("C", "R", ""), ("S", "W", ""), ("R", "W", "")]
    chips_l = []
    if chips:
        chips_l = [(545, 50, "P(C)"), (115, 175, "P(S | C)"), (725, 175, "P(R | C)"), (590, 300, "P(W | S,R)")]
    f = figure(title, desc)
    P(f, nodes, ed, 365, chips=chips_l, verdict=verdict, vcolor=vcolor, note=note)
    if formula:
        f.footer("P(c,s,r,w) = P(c) P(s|c) P(r|c) P(w|s,r)")
    return f


def cadena_rtl(title, desc, estados, badges=None, verdict=None, vcolor="neutral", note=None):
    est = {"R": "r", "T": "m", "L": "e"}
    est.update(estados)
    bd = badges or {}
    nodes = {
        "R": (160, 50, "R", "lluvia", est["R"], bd.get("R")),
        "T": (420, 50, "T", "tráfico", est["T"], bd.get("T")),
        "L": (680, 50, "L", "llegar tarde", est["L"], bd.get("L")),
    }
    f = figure(title, desc)
    P(f, nodes, [("R", "T", ""), ("T", "L", "")], 125,
      chips=[(290, 50 - 0, "")][:0] + [(160, 6, "P(r) = 0.1"), (420, 6, "P(t | R)"), (680, 6, "P(l | T)")],
      verdict=verdict, vcolor=vcolor, note=note)
    f.footer("P(r,t,l) = P(r) P(t|r) P(l|t)")
    return f


# =====================================================================
# Definicion de cada figura
# =====================================================================
def build():
    # --- 1. lluvia, trafico, paraguas ---------------------------------
    OUT["ia14-lluvia-trafico-paraguas.svg"] = lluvia("Una independencia reduce la tabla",
        "R apunta a T y a U. Dado R, T y U son independientes.").svg()
    OUT["ia29-lluvia-trafico-paraguas.svg"] = lluvia("Lluvia, tráfico y paraguas",
        "R lluvia es padre de T tráfico y U paraguas. Dado R, T y U son independientes.").svg()

    # --- 2. alarma ------------------------------------------------------
    OUT["ia14-red-alarma.svg"] = alarma("Alarma: cinco variables, cinco factores",
        "B y E apuntan a A; A apunta a J y M.").svg()
    OUT["ia29-red-alarma.svg"] = alarma("Red bayesiana de alarma",
        "B y E apuntan a A; A apunta a J y M. Las raíces son independientes antes de observar efectos.").svg()

    # --- 3. cadena de cuatro nodos ------------------------------------
    def c4(title, desc, with_ev):
        f = figure(title, desc)
        base = {"X": (130, 40, "X", "raíz", "r"), "Y": (330, 40, "Y", "padre de Z", "m"),
                "Z": (530, 40, "Z", "padre de W", "m"), "W": (730, 40, "W", "último nodo", "e")}
        ed = [("X", "Y", "act"), ("Y", "Z", "act"), ("Z", "W", "act")]
        P(f, dict(base), ed, 105, subtitle="Sin evidencia",
          verdict="Camino activo: no se garantiza X ⊥ W", vcolor="bad")
        f.rule()
        ob = dict(base)
        ob["Z"] = (530, 40, "Z", "padre de W", "o", "observado")
        ed2 = [("X", "Y", "blk"), ("Y", "Z", "blk"), ("Z", "W", "blk")]
        P(f, ob, ed2, 105, subtitle="Con Z observado", verdict="Camino bloqueado: X ⊥ W | Z", vcolor="ok")
        f.footer("P(X,Y,Z,W) = P(X) P(Y|X) P(Z|Y) P(W|Z)")
        return f
    OUT["ia14-cadena-cuatro.svg"] = c4("Padres y conexiones indirectas", "Cadena X→Y→Z→W.", True).svg()
    OUT["ia29-cadena-cuatro-nodos.svg"] = c4("Cadena de cuatro nodos: observar bloquea el camino",
        "Observar Z bloquea el único camino entre X y W.", True).svg()

    # --- 4. cadena presion -> lluvia -> trafico -----------------------
    def c3(title, desc):
        f = figure(title, desc)
        base = {"X": (160, 40, "X", "presión baja", "r"), "Y": (420, 40, "Y", "lluvia", "m"), "Z": (680, 40, "Z", "tráfico", "e")}
        P(f, base, [("X", "Y", "act"), ("Y", "Z", "act")], 105, subtitle="Sin conocer la lluvia",
          verdict="Camino activo: la presión informa sobre el tráfico", vcolor="bad")
        f.rule()
        ob = dict(base)
        ob["Y"] = (420, 40, "Y", "lluvia", "o", "observado")
        P(f, ob, [("X", "Y", "blk"), ("Y", "Z", "blk")], 105, subtitle="Con la lluvia observada",
          verdict="Camino bloqueado: X ⊥ Z | Y", vcolor="ok")
        return f
    OUT["ia14-cadena-presion.svg"] = c3("Cadena: observar el medio bloquea", "X→Y→Z").svg()
    OUT["ia29-cadena-presion-lluvia-trafico.svg"] = c3("Presión → lluvia → tráfico", "X→Y→Z").svg()

    # --- 5. causa comun --------------------------------------------------
    f = figure("Causa común: observar el origen bloquea", "Y apunta a X y a Z.")
    base = {"Y": (420, 40, "Y", "entrega próxima", "r"), "X": (230, 175, "X", "foro activo", "e"), "Z": (610, 175, "Z", "laboratorio lleno", "e")}
    P(f, base, [("Y", "X", "act"), ("Y", "Z", "act")], 235, subtitle="Sin evidencia",
      verdict="Camino X ← Y → Z activo", vcolor="bad")
    f.rule()
    ob = dict(base)
    ob["Y"] = (420, 40, "Y", "entrega próxima", "o", "observado")
    P(f, ob, [("Y", "X", "blk"), ("Y", "Z", "blk")], 235, subtitle="Con Y observado",
      verdict="Camino bloqueado: X ⊥ Z | Y", vcolor="ok")
    OUT["ia14-causa-comun.svg"] = f.svg()

    # --- 6. efecto comun -------------------------------------------------
    f = figure("Efecto común y evidencia descendiente", "R→T←B y T→T′.")
    base = {"R": (230, 40, "R", "lluvia", "r"), "B": (610, 40, "B", "partido", "r"),
            "T": (420, 165, "T", "tráfico", "m"), "T2": (420, 290, "T′", "reporte de tráfico", "e")}
    ed0 = [("R", "T", "blk"), ("B", "T", "blk"), ("T", "T2", "")]
    P(f, base, ed0, 335, subtitle="Sin evidencia", verdict="R → T ← B bloqueado: R ⊥ B", vcolor="ok")
    f.rule()
    ob = dict(base); ob["T"] = (420, 165, "T", "tráfico", "o", "observado")
    P(f, ob, [("R", "T", "act"), ("B", "T", "act"), ("T", "T2", "")], 335, subtitle="Se observa T",
      verdict="El colisionador se abre: R y B dependen", vcolor="bad")
    f.rule()
    ob = dict(base); ob["T2"] = (420, 290, "T′", "reporte de tráfico", "o", "observado")
    P(f, ob, [("R", "T", "act"), ("B", "T", "act"), ("T", "T2", "")], 335, subtitle="Se observa solo el descendiente T′",
      verdict="También se abre: R y B dependen", vcolor="bad")
    OUT["ia14-efecto-comun.svg"] = f.svg()

    # --- 7. ejemplo 2 ---------------------------------------------------
    f = figure("Ejemplo 2: abrir y volver a bloquear", "L→R, R→D, R→T, B→T, T→T′.")
    def ej2(rst, tst, t2st, ed_kinds, **kw):
        return {"L": (110, 40, "L", "baja presión", "r"), "R": (290, 40, "R", "lluvia", rst),
                "T": (480, 40, "T", "tráfico", tst), "B": (680, 40, "B", "partido", "r"),
                "D": (290, 170, "D", "goteo", "e"), "T2": (480, 170, "T′", "reporte", t2st)}
    eds = lambda a, b, c: [("L", "R", a), ("R", "T", b), ("B", "T", c), ("R", "D", ""), ("T", "T2", "")]
    P(f, ej2("m", "m", "e", None), eds("blk", "blk", "blk"), 235, subtitle="Sin evidencia",
      verdict="Camino L → R → T ← B bloqueado en T", vcolor="ok")
    f.rule()
    n = ej2("m", "o", "e", None); n["T"] = (480, 40, "T", "tráfico", "o", "observado")
    P(f, n, eds("act", "act", "act"), 235, subtitle="Se observa T",
      verdict="T se abre: el camino queda activo", vcolor="bad")
    f.rule()
    n = ej2("o", "o", "e", None)
    n["T"] = (480, 40, "T", "tráfico", "o", "observado"); n["R"] = (290, 40, "R", "lluvia", "o", "observado")
    P(f, n, eds("blk", "blk", "act"), 235, subtitle="Se observan T y R",
      verdict="R observado bloquea L → R → T: L ⊥ B | R,T", vcolor="ok")
    OUT["ia14-ejemplo2.svg"] = f.svg()

    # --- 8. ejemplo 3 ---------------------------------------------------
    f = figure("Ejemplo 3: deben bloquearse todos los caminos", "R→T, R→D, T→S, D→S.")
    def ej3(rst, sst, k_sup, k_inf):
        n = {"R": (420, 40, "R", "lluvia", rst, "observado" if rst == "o" else None),
             "T": (270, 160, "T", "tráfico", "m"), "D": (570, 160, "D", "goteo", "m"),
             "S": (420, 280, "S", "tristeza", sst, "observado" if sst == "o" else None)}
        e = [("R", "T", k_sup), ("R", "D", k_sup), ("T", "S", k_inf), ("D", "S", k_inf)]
        return n, e
    n, e = ej3("r", "e", "act", "blk")
    P(f, n, e, 330, subtitle="Sin evidencia", verdict="Superior T ← R → D activo", vcolor="bad")
    f.rule()
    n, e = ej3("o", "e", "blk", "blk")
    P(f, n, e, 330, subtitle="Se observa R", verdict="Superior bloqueado, inferior bloqueado: T ⊥ D | R", vcolor="ok")
    f.rule()
    n, e = ej3("o", "o", "blk", "act")
    P(f, n, e, 330, subtitle="Se observan R y S", verdict="Observar S abre T → S ← D: T y D dependen", vcolor="bad")
    OUT["ia14-ejemplo3-dos-caminos.svg"] = f.svg()

    # --- 9. MIT perro ---------------------------------------------------
    f = figure("MIT: causas alternativas de un ladrido", "B→D←R.")
    base = {"B": (260, 40, "B", "ladrón", "r"), "R": (580, 40, "R", "mapache", "r"), "D": (420, 165, "D", "perro ladra", "m")}
    chips = [(120, 40, "P(B) = 0.1"), (720, 40, "P(R) = 0.5")]
    P(f, base, [("B", "D", "blk"), ("R", "D", "blk")], 235, subtitle="A priori", chips=chips,
      verdict="B y R independientes", vcolor="ok")
    f.rule()
    ob = dict(base); ob["D"] = (420, 165, "D", "perro ladra", "o", "observado")
    P(f, ob, [("B", "D", "act"), ("R", "D", "act")], 235, subtitle="Se escucha el ladrido", chips=chips,
      verdict="Causas alternativas: B y R pasan a depender", vcolor="bad")
    OUT["ia14-mit-perro-mapache.svg"] = f.svg()

    # --- 10. colisionador con descendiente ------------------------------
    f = figure("Observar un descendiente activa el colisionador", "X→Y←Z y Y→D.")
    base = {"X": (260, 40, "X", "", "r"), "Z": (580, 40, "Z", "", "r"), "Y": (420, 160, "Y", "", "m"), "D": (420, 275, "D", "descendiente", "e")}
    P(f, base, [("X", "Y", "blk"), ("Z", "Y", "blk"), ("Y", "D", "")], 320, subtitle="Sin evidencia",
      verdict="X ⊥ Z", vcolor="ok")
    f.rule()
    ob = dict(base); ob["D"] = (420, 275, "D", "descendiente", "o", "observado")
    P(f, ob, [("X", "Y", "act"), ("Z", "Y", "act"), ("Y", "D", "")], 320, subtitle="Solo D observado",
      verdict="Independencia no garantizada", vcolor="bad")
    OUT["ia29-colisionador-descendiente.svg"] = f.svg()

    # --- 11. fuego, humo, alarma ---------------------------------------
    f = figure("Fuego, humo y alarma: dos modelos posibles", "Cadena F→H→A o causa común F→H, F→A.")
    P(f, {"F": (160, 40, "F", "fuego", "r"), "H": (420, 40, "H", "humo", "m"), "A": (680, 40, "A", "alarma", "e")},
      [("F", "H", ""), ("H", "A", "")], 110, subtitle="Detector que responde al humo (cadena)",
      verdict="Supuesto: A ⊥ F | H", vcolor="ok")
    f.rule()
    P(f, {"F": (420, 40, "F", "fuego", "r"), "H": (250, 170, "H", "humo", "e"), "A": (590, 170, "A", "alarma", "e")},
      [("F", "H", ""), ("F", "A", "")], 235, subtitle="Dos efectos de una causa común",
      verdict="Supuesto: H ⊥ A | F", vcolor="ok")
    OUT["ia29-fuego-humo-alarma.svg"] = f.svg()

    # --- 12. caries ------------------------------------------------------
    f = figure("Caries: una causa común, dos observaciones", "C→T y C→K.")
    P(f, {"C": (420, 45, "C", "caries", "r"), "T": (250, 175, "T", "dolor dental", "e"), "K": (590, 175, "K", "detección", "e")},
      [("C", "T", ""), ("C", "K", "")], 245, verdict="Supuesto: T ⊥ K | C", vcolor="ok",
      note="Sin observar C, el dolor y la detección pueden estar relacionados.")
    f.footer("P(C,T,K) = P(C) P(T|C) P(K|C)")
    OUT["ia29-red-caries.svg"] = f.svg()

    # --- 13. tripletas ---------------------------------------------------
    f = figure("Las tres tripletas y el efecto de observar Y", "Cadena, causa común y colisionador.")
    def tri(kind, obs):
        n = {"X": (80, 30, "X", "", "r"), "Y": (190, 30, "Y", "", "m"), "Z": (300, 30, "Z", "", "e")}
        if kind == "cadena":
            e = [("X", "Y", ""), ("Y", "Z", "")]
            n["X"] = (80, 30, "X", "", "r"); n["Z"] = (300, 30, "Z", "", "e")
            open_ = not obs
        elif kind == "comun":
            e = [("Y", "X", ""), ("Y", "Z", "")]
            n["Y"] = (190, 30, "Y", "", "r"); n["X"] = (80, 30, "X", "", "e")
            open_ = not obs
        else:
            e = [("X", "Y", ""), ("Z", "Y", "")]
            n["X"] = (80, 30, "X", "", "r"); n["Z"] = (300, 30, "Z", "", "r")
            open_ = obs
        if obs:
            n["Y"] = (190, 30, "Y", "", "o", "observado")
        e = [(a, b, "act" if open_ else "blk") for a, b, _ in e]
        return n, e, open_
    f.parts.append(f'<text class="sub" x="230" y="{f.y + 18}">Sin evidencia</text><text class="sub" x="610" y="{f.y + 18}">Y observado</text>')
    f.y += 30
    for kind, name in (("cadena", "Cadena  X → Y → Z"), ("comun", "Causa común  X ← Y → Z"), ("colis", "Colisionador  X → Y ← Z")):
        f.parts.append(f'<text class="sub" x="{W / 2}" y="{f.y + 14}" fill="#7b4fb8" style="fill:#7b4fb8">{esc(name)}</text>')
        top = f.y + 22
        base_y = f.y
        f.y = top
        for col, obs in ((230, False), (610, True)):
            n, e, op = tri(kind, obs)
            f.panel(n, e, 40, verdict=("Camino activo: dependencia posible" if op else "Camino bloqueado: X ⊥ Z" + (" | Y" if obs else "")),
                    vcolor="bad" if op else "ok", x0=col - 190, width=380)
            end = f._last_bottom
            f.y = top
        f.y = end + 6
        f.rule()
    f.footer("Colisionador: también se activa al observar un descendiente de Y.")
    OUT["ia29-tripletas-d-separacion.svg"] = f.svg()

    # ================== NUEVAS ==========================================
    # --- regla de la cadena (Agentes probabilisticos, sec. 10) ----------
    f = figure("Regla de la cadena: del grafo completo al supuesto del modelo", "R→T, R→U, T→U contra R→T, R→U.")
    base = {"R": (420, 40, "R", "lluvia", "r"), "T": (250, 175, "T", "tráfico", "e"), "U": (590, 175, "U", "paraguas", "e")}
    P(f, base, [("R", "T", ""), ("R", "U", ""), ("T", "U", "new")], 235, subtitle="Sin suponer independencia: todos los padres previos",
      verdict="P(r,t,u) = P(r) P(t|r) P(u|r,t)", vcolor="neutral")
    f.rule()
    P(f, base, [("R", "T", ""), ("R", "U", "")], 235, subtitle="Con el supuesto U ⊥ T | R: desaparece la flecha T → U",
      verdict="P(r,t,u) = P(r) P(t|r) P(u|r)", vcolor="ok")
    OUT["ia29-regla-cadena-grafo.svg"] = f.svg()

    # --- contraejemplo cadena XYZ (Redes bayesianas sec. 10) ------------
    f = figure("La topología no obliga a la dependencia", "X→Y→Z con dos conjuntos de CPT.")
    base = {"X": (160, 40, "X", "moneda justa", "r"), "Y": (420, 40, "Y", "", "m"), "Z": (680, 40, "Z", "", "e")}
    P(f, base, [("X", "Y", "act"), ("Y", "Z", "act")], 125, subtitle="CPT deterministas: Y = X y Z = Y",
      verdict="Dependientes: P(X=1, Z=1) = 0.5 ≠ 0.25", vcolor="bad")
    f.rule()
    P(f, base, [("X", "Y", "blk"), ("Y", "Z", "blk")], 125, subtitle="Todas las CPT dan 0.5, sin usar a sus padres",
      verdict="Independientes: las flechas existen pero no transmiten", vcolor="ok")
    f.footer("Ambos modelos respetan la factorización P(X) P(Y|X) P(Z|Y).")
    OUT["ia14-contraejemplo-cadena.svg"] = f.svg()

    # --- manto de Markov (Redes bayesianas sec. 11.1) --------------------
    f = figure("Manto de Markov en la red de alarma", "Manto de B y de J.")
    def mb(sel, blanket, text):
        est = {k: "h" for k in "BEAJM"}
        est[sel] = "q"
        for b in blanket:
            est[b] = "y"
        n = {"B": (260, 40, "B", "robo", est["B"]), "E": (580, 40, "E", "terremoto", est["E"]),
             "A": (420, 150, "A", "alarma", est["A"]), "J": (260, 260, "J", "John llama", est["J"]),
             "M": (580, 260, "M", "Mary llama", est["M"])}
        return n
    ed = [("B", "A", ""), ("E", "A", ""), ("A", "J", ""), ("A", "M", "")]
    P(f, mb("B", "AE", ""), ed, 310, subtitle="MB(B) = {A, E}: su hijo y el otro padre de ese hijo",
      verdict="Dado {A, E}: B ⊥ {J, M}", vcolor="ok")
    f.rule()
    P(f, mb("J", "A", ""), ed, 310, subtitle="MB(J) = {A}", verdict="Conocida la alarma, J es independiente de B, E y M", vcolor="ok")
    OUT["ia14-manto-markov.svg"] = f.svg()

    # --- moralizacion (Redes bayesianas sec. 11.2) -----------------------
    f = figure("Moralización: verificar d-separación con el subgrafo ancestral", "R→T←B, T→T′.")
    base = {"R": (230, 40, "R", "lluvia", "r"), "B": (610, 40, "B", "partido", "r"),
            "T": (420, 160, "T", "tráfico", "m"), "T2": (420, 280, "T′", "reporte (evidencia)", "o", "observado")}
    P(f, base, [("R", "T", ""), ("B", "T", ""), ("T", "T2", "")], 330, subtitle="1. Subgrafo ancestral de {R, B, T′}",
      verdict="Se conservan R, B, T, T′", vcolor="neutral")
    f.rule()
    P(f, base, [("R", "T", ""), ("B", "T", "")], 330, subtitle="2–3. Se casan los padres de T (R — B) y se quitan las flechas",
      undirected=[("R", "B")], verdict="Tras quitar la evidencia T′, R — B sigue conectado: no hay d-separación", vcolor="bad")
    OUT["ia14-moralizacion.svg"] = f.svg()

    # --- cadena R->T->L para inferencia (sec. 6-9, 14) --------------------
    OUT["ia15-cadena-consulta-l.svg"] = cadena_rtl("Cadena R → T → L: consulta P(L)",
        "Consulta L; ocultas R y T.", {"L": "q", "R": "h", "T": "h"}, {"L": "consulta"},
        verdict="Se suman R y T: ocho mundos", vcolor="neutral").svg()
    OUT["ia15-cadena-evidencia-r.svg"] = cadena_rtl("Cadena R → T → L: consulta P(L | r)",
        "Evidencia R=r; oculta T; consulta L.", {"R": "o", "T": "h", "L": "q"}, {"R": "R = r", "L": "consulta"},
        verdict="Se restringe R y solo se suma T", vcolor="neutral").svg()
    OUT["ia15-cadena-evidencia-t.svg"] = cadena_rtl("Cadena R → T → L: consulta P(L | t)",
        "Evidencia T=t; oculta R; consulta L.", {"R": "h", "T": "o", "L": "q"}, {"T": "T = t", "L": "consulta"},
        verdict="Observar T bloquea R: P(L | t) viene de su CPT", vcolor="ok").svg()
    OUT["ia15-cadena-evidencia-no-r.svg"] = cadena_rtl("Cadena R → T → L: consulta P(L | ¬r)",
        "Evidencia R=¬r; oculta T; consulta L.", {"R": "o", "T": "h", "L": "q"}, {"R": "R = ¬r", "L": "consulta"},
        verdict="Se restringe R = ¬r y se suma T", vcolor="neutral").svg()

    # --- alarma: consulta P(B | j, m) ------------------------------------
    OUT["ia15-alarma-consulta.svg"] = alarma("Alarma: consulta P(B | j, m)", "Consulta B; evidencia J y M; ocultas A y E.",
        {"B": "q", "J": "o", "M": "o", "A": "h", "E": "h"}, {"B": "consulta", "J": "J = j", "M": "M = m"},
        verdict="Se conserva B, se fijan J y M y se suman A y E", vcolor="neutral").svg()

    # --- poliarbol Z -> X_i -> Y_i ----------------------------------------
    f = figure("Causa común con ramas: Z → Xᵢ → Yᵢ", "Poliárbol con n = 3 ramas; consulta X3.")
    n = {"Z": (420, 45, "Z", "causa común", "h"),
         "X1": (160, 170, "X₁", "", "h"), "X2": (420, 170, "X₂", "", "h"), "X3": (680, 170, "X₃", "consulta", "q"),
         "Y1": (160, 295, "Y₁", "", "o", "observado"), "Y2": (420, 295, "Y₂", "", "o", "observado"), "Y3": (680, 295, "Y₃", "", "o", "observado")}
    ed = [("Z", "X1", ""), ("Z", "X2", ""), ("Z", "X3", ""), ("X1", "Y1", ""), ("X2", "Y2", ""), ("X3", "Y3", "")]
    P(f, n, ed, 350, verdict="Consulta P(X₃ | y₁, y₂, y₃); ocultas Z, X₁, X₂", vcolor="neutral",
      note="Cada rama entrega un resumen mᵢ(Z): eliminar ramas primero mantiene las tablas pequeñas.")
    OUT["ia15-poliarbol-ramas.svg"] = f.svg()

    # --- no poliarbol -------------------------------------------------------
    f = figure("Un DAG que no es poliárbol", "R→T, R→D, T→S, D→S.")
    n = {"R": (420, 40, "R", "", "r"), "T": (270, 160, "T", "", "m"), "D": (570, 160, "D", "", "m"), "S": (420, 280, "S", "", "e")}
    P(f, n, [("R", "T", ""), ("R", "D", ""), ("T", "S", ""), ("D", "S", "")], 335,
      verdict="Ciclo no dirigido R – T – S – D: no es poliárbol", vcolor="bad")
    OUT["ia15-no-poliarbol.svg"] = f.svg()

    # --- red de muestreo: nublado, aspersor, lluvia, pasto --------------------
    OUT["ia16-red-aspersor.svg"] = aspersor("Red del muestreo: nublado, aspersor, lluvia y pasto",
        "C→S, C→R, S→W, R→W.").svg()
    OUT["ia16-muestreo-previo.svg"] = aspersor("Muestreo previo: sortear en orden topológico",
        "Orden C, S, R, W.", badges={"C": "1.º", "S": "2.º", "R": "3.º", "W": "4.º"},
        verdict="Cada nodo se sortea después de sus padres", vcolor="neutral",
        note="S y R pueden intercambiarse: ninguno es padre del otro.").svg()
    OUT["ia16-rechazo-pesos.svg"] = aspersor("Evidencia +w: consulta P(C | +w)",
        "W observado; C consulta.", {"C": "q", "S": "h", "R": "h", "W": "o"}, {"W": "+w", "C": "consulta"},
        verdict="Rechazo: se descartan los mundos con −w · Pesos: W se fija y pesa P(+w | S,R)", vcolor="neutral").svg()
    OUT["ia16-gibbs-manta.svg"] = aspersor("Gibbs: actualizar S con su manta de Markov",
        "Se vuelve a sortear S dado C, R y W.", {"C": "y", "S": "q", "R": "y", "W": "y"}, {"S": "se actualiza"},
        verdict="Manta de S = {C, R, W}: P(s | c) P(−w | s, +r)", vcolor="neutral",
        note="C es su padre, W su hijo y R el otro padre de W.").svg()

    # --- aprendizaje de parametros ---------------------------------------------
    f = figure("Aprender CPT contando: género y calificación", "G→R y G→R←A.")
    P(f, {"G": (260, 40, "G", "género", "r"), "R": (580, 40, "R", "calificación", "e")}, [("G", "R", "")], 110,
      subtitle="Un padre: una fila P(R | g) por género", verdict="P(g) = N(g)/N · P(r | g) = N(r,g)/N(g)", vcolor="neutral")
    f.rule()
    P(f, {"G": (190, 40, "G", "género", "r"), "A": (650, 40, "A", "ganó premio", "r"), "R": (420, 40 + 120, "R", "calificación", "e")},
      [("G", "R", ""), ("A", "R", "")], 215, subtitle="Dos padres: una fila por cada par (g, a), con menos ejemplos por fila",
      verdict="Más filas ⇒ más parámetros y conteos más pequeños", vcolor="warn")
    OUT["ia17-genero-calificacion.svg"] = f.svg()

    f = figure("Compartir parámetros", "G→R1 y G→R2 con la misma CPT.")
    P(f, {"G": (420, 40, "G", "género", "r"), "R1": (250, 175, "R₁", "calificación 1", "e"), "R2": (590, 175, "R₂", "calificación 2", "e")},
      [("G", "R1", ""), ("G", "R2", "")], 245, chips=[(420, 175, "P(R₁|G) = P(R₂|G)")],
      verdict="Los conteos de R₁ y R₂ se combinan para estimar una sola CPT", vcolor="ok",
      note="Restricción del modelo: obliga a que las dos CPT sean iguales.")
    OUT["ia17-parametros-compartidos.svg"] = f.svg()

    f = figure("Datos incompletos: el género no se observa", "G oculto; R1 y R2 observados.")
    P(f, {"G": (420, 40, "G", "género (oculto)", "h"), "R1": (250, 175, "R₁", "observada", "o"), "R2": (590, 175, "R₂", "observada", "o")},
      [("G", "R1", ""), ("G", "R2", "")], 245, verdict="Cada registro es (?, r₁, r₂): ya no se puede contar", vcolor="bad",
      note="EM: E calcula P(g | r₁, r₂) como conteos fraccionarios; M reestima las CPT.")
    f.footer("P(r₁,r₂) = Σ_g P(g) P(r₁|g) P(r₂|g)")
    OUT["ia17-genero-oculto.svg"] = f.svg()

    f = figure("Aprender la estructura: candidatos sobre G, A y R", "Tres DAG candidatos.")
    cand = [("Sin aristas", []), ("G → R", [("G", "R", "")]), ("G → R ← A", [("G", "R", ""), ("A", "R", "")])]
    xs = [140, 420, 700]
    # tres paneles lado a lado
    top = f.y
    for (name, eds), x in zip(cand, xs):
        f.y = top
        n = {"G": (90, 40, "G", "", "r"), "A": (190, 40, "A", "", "r"), "R": (140, 150, "R", "", "e")}
        f.panel(n, eds, 190, subtitle=name, x0=x - 140, width=280)
    f.y = f._last_bottom
    f.footer(["Cada candidato se ajusta con sus parámetros y se puntúa:",
              "S(G) = max_θ log P(D | G, θ) − ρ C(G)   (verosimilitud menos complejidad)"])
    OUT["ia17-busqueda-estructura.svg"] = f.svg()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=VAULT_RECURSOS)
    args = ap.parse_args()
    build()
    args.out.mkdir(parents=True, exist_ok=True)
    for name, svg in OUT.items():
        (args.out / name).write_text(svg, encoding="utf-8")
    print(f"{len(OUT)} SVG escritos en {args.out}")


if __name__ == "__main__":
    main()
