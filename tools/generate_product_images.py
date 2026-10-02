#!/usr/bin/env python3
"""
商品画像ジェネレータ。
data.sql の各商品 (id 1..24) に対応するイラストを SVG で生成し、
frontend/public/images/products/{id}.svg に出力する。

    python3 tools/generate_product_images.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "frontend/public/images/products"
W, H = 400, 300


def frame(bg1, bg2, body):
    """共通の背景 (グラデーション + 床の影) で包む"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{bg1}"/>
      <stop offset="1" stop-color="{bg2}"/>
    </linearGradient>
    <radialGradient id="shadow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#000" stop-opacity="0.22"/>
      <stop offset="1" stop-color="#000" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <ellipse cx="200" cy="262" rx="140" ry="16" fill="url(#shadow)"/>
{body}
</svg>
"""


IMAGES = {}


def image(pid, bg1, bg2):
    def deco(fn):
        IMAGES[pid] = (bg1, bg2, fn)
        return fn
    return deco


@image(1, "#fff4e6", "#ffd8a8")
def coffee_mug():  # 陶器のコーヒーマグ
    return """
  <path d="M248 120 q52 0 52 46 t-52 46" fill="none" stroke="#f1f3f5" stroke-width="18"/>
  <path d="M248 120 q52 0 52 46 t-52 46" fill="none" stroke="#ced4da" stroke-width="4"/>
  <path d="M120 92 h140 v140 q0 28 -28 28 h-84 q-28 0 -28 -28 z" fill="#f8f9fa" stroke="#adb5bd" stroke-width="3"/>
  <ellipse cx="190" cy="94" rx="70" ry="12" fill="#5c3d2e"/>
  <ellipse cx="190" cy="92" rx="70" ry="10" fill="none" stroke="#adb5bd" stroke-width="3"/>
  <rect x="120" y="150" width="140" height="22" fill="#e8590c" opacity="0.85"/>
  <path d="M165 70 q-12 -18 0 -36 M190 66 q-12 -18 0 -36 M215 70 q-12 -18 0 -36" fill="none" stroke="#adb5bd" stroke-width="4" stroke-linecap="round" opacity="0.7"/>
"""


@image(2, "#e7f5ff", "#a5d8ff")
def headphones():  # ワイヤレスヘッドホン
    return """
  <path d="M110 190 v-40 a90 90 0 0 1 180 0 v40" fill="none" stroke="#343a40" stroke-width="18" stroke-linecap="round"/>
  <path d="M120 150 a80 80 0 0 1 160 0" fill="none" stroke="#868e96" stroke-width="5"/>
  <rect x="82" y="160" width="58" height="92" rx="24" fill="#212529"/>
  <rect x="92" y="172" width="38" height="68" rx="16" fill="#495057"/>
  <rect x="260" y="160" width="58" height="92" rx="24" fill="#212529"/>
  <rect x="270" y="172" width="38" height="68" rx="16" fill="#495057"/>
  <circle cx="289" cy="196" r="4" fill="#4dabf7"/>
"""


@image(3, "#ebfbee", "#b2f2bb")
def running_shoe():  # ランニングシューズ
    return """
  <path d="M70 236 h268 q16 0 14 -14 l-2 -10 h-280 z" fill="#f8f9fa" stroke="#ced4da" stroke-width="3"/>
  <path d="M72 212 q-6 -40 26 -62 l60 -50 q14 -10 26 2 l40 44 q30 22 80 30 q48 8 46 36 z" fill="#1c7ed6"/>
  <path d="M158 100 l40 46" stroke="#fff" stroke-width="4"/>
  <path d="M150 130 l22 -8 M160 144 l22 -8 M170 158 l22 -8" stroke="#fff" stroke-width="5" stroke-linecap="round"/>
  <path d="M110 200 q60 -40 130 -10 q50 18 98 10" fill="none" stroke="#fab005" stroke-width="8" stroke-linecap="round"/>
  <path d="M74 224 h272" stroke="#ced4da" stroke-width="3" stroke-dasharray="10 8"/>
"""


@image(4, "#fff9db", "#ffe8a3")
def backpack():  # レザーバックパック
    return """
  <path d="M170 64 q30 -30 60 0" fill="none" stroke="#5c3d2e" stroke-width="10"/>
  <rect x="120" y="70" width="160" height="186" rx="40" fill="#8b5a2b"/>
  <path d="M120 120 q80 -40 160 0 v-10 q0 -40 -40 -40 h-80 q-40 0 -40 40 z" fill="#6f4520"/>
  <rect x="150" y="170" width="100" height="70" rx="14" fill="#7a4b22" stroke="#5c3d2e" stroke-width="3"/>
  <path d="M160 186 h80" stroke="#c9a46b" stroke-width="3" stroke-dasharray="6 4"/>
  <rect x="160" y="112" width="12" height="44" rx="3" fill="#5c3d2e"/>
  <rect x="228" y="112" width="12" height="44" rx="3" fill="#5c3d2e"/>
  <rect x="158" y="148" width="16" height="12" rx="2" fill="#d4af37"/>
  <rect x="226" y="148" width="16" height="12" rx="2" fill="#d4af37"/>
"""


@image(5, "#f1f3f5", "#dee2e6")
def wrist_watch():  # アナログ腕時計
    return """
  <rect x="170" y="20" width="60" height="100" rx="10" fill="#7c4a1e"/>
  <rect x="170" y="180" width="60" height="90" rx="10" fill="#7c4a1e"/>
  <circle cx="200" cy="150" r="72" fill="#adb5bd"/>
  <circle cx="200" cy="150" r="62" fill="#fff" stroke="#495057" stroke-width="3"/>
  <rect x="270" y="142" width="12" height="16" rx="3" fill="#868e96"/>
  <g stroke="#212529" stroke-width="4" stroke-linecap="round">
    <path d="M200 96 v10 M200 194 v10 M146 150 h10 M244 150 h10"/>
  </g>
  <path d="M200 150 L200 110" stroke="#212529" stroke-width="5" stroke-linecap="round"/>
  <path d="M200 150 L232 168" stroke="#212529" stroke-width="4" stroke-linecap="round"/>
  <path d="M200 150 L176 118" stroke="#e03131" stroke-width="2" stroke-linecap="round"/>
  <circle cx="200" cy="150" r="5" fill="#212529"/>
"""


@image(6, "#e3fafc", "#99e9f2")
def water_bottle():  # ステンレス水筒
    return """
  <defs>
    <linearGradient id="steel" x1="0" x2="1">
      <stop offset="0" stop-color="#868e96"/><stop offset="0.35" stop-color="#f1f3f5"/><stop offset="1" stop-color="#495057"/>
    </linearGradient>
  </defs>
  <rect x="172" y="30" width="56" height="40" rx="8" fill="#343a40"/>
  <rect x="176" y="66" width="48" height="12" fill="#495057"/>
  <path d="M168 78 h64 q18 10 18 40 v124 q0 18 -18 18 h-64 q-18 0 -18 -18 v-124 q0 -30 18 -40 z" fill="url(#steel)"/>
  <rect x="150" y="150" width="100" height="56" fill="#0c8599" opacity="0.85"/>
  <path d="M180 162 q20 18 40 0 M180 178 q20 18 40 0" fill="none" stroke="#fff" stroke-width="3" opacity="0.8"/>
"""


@image(7, "#f3f0ff", "#d0bfff")
def keyboard():  # メカニカルキーボード
    keys = []
    for row in range(4):
        for col in range(12):
            x = 58 + col * 24 + (row % 2) * 6
            y = 118 + row * 26
            keys.append(f'<rect x="{x}" y="{y}" width="20" height="20" rx="3" fill="#f8f9fa" stroke="#adb5bd"/>')
    return f"""
  <rect x="44" y="100" width="312" height="150" rx="12" fill="#343a40"/>
  {''.join(keys)}
  <rect x="110" y="224" width="180" height="18" rx="3" fill="#f8f9fa" stroke="#adb5bd"/>
  <rect x="58" y="224" width="44" height="18" rx="3" fill="#4c6ef5"/>
  <rect x="298" y="224" width="44" height="18" rx="3" fill="#4c6ef5"/>
"""


@image(8, "#f8f9fa", "#ced4da")
def mouse():  # ワイヤレスマウス
    return """
  <path d="M200 50 q80 0 80 100 v40 q0 72 -80 72 q-80 0 -80 -72 v-40 q0 -100 80 -100 z" fill="#495057"/>
  <path d="M200 50 q80 0 80 100 h-80 z" fill="#5c636a"/>
  <path d="M200 50 q-80 0 -80 100 h80 z" fill="#5c636a"/>
  <path d="M200 50 v100 M120 150 h160" stroke="#212529" stroke-width="3"/>
  <rect x="192" y="80" width="16" height="36" rx="8" fill="#212529"/>
  <rect x="196" y="88" width="8" height="10" rx="3" fill="#74c0fc"/>
"""


@image(9, "#212529", "#495057")
def desk_lamp():  # LEDデスクランプ
    return """
  <path d="M90 250 L330 50 L330 250 Z" fill="#fff3bf" opacity="0.15"/>
  <ellipse cx="140" cy="252" rx="60" ry="12" fill="#adb5bd"/>
  <rect x="96" y="240" width="88" height="14" rx="6" fill="#ced4da"/>
  <path d="M140 240 L190 140 L270 90" fill="none" stroke="#dee2e6" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="190" cy="140" r="10" fill="#868e96"/>
  <path d="M250 70 L320 110 L296 150 L226 110 Z" fill="#f1f3f5"/>
  <path d="M296 150 L226 110" stroke="#ffe066" stroke-width="8" stroke-linecap="round"/>
"""


@image(10, "#f4fce3", "#d8f5a2")
def monstera():  # 観葉植物 モンステラ
    leaf = '<path d="M0 0 q40 -50 0 -110 q-40 60 0 110 z" fill="#2b8a3e"/><path d="M0 0 v-100" stroke="#8ce99a" stroke-width="3"/><path d="M-14 -40 l10 4 M-18 -70 l12 4 M14 -50 l-10 4 M12 -80 l-10 4" stroke="#d8f5a2" stroke-width="5" stroke-linecap="round"/>'
    leaves = "".join(
        f'<g transform="translate(200 170) rotate({a}) scale({s})">{leaf}</g>'
        for a, s in [(-55, 1.0), (-25, 1.15), (0, 1.25), (28, 1.1), (58, 0.95)]
    )
    return f"""
  {leaves}
  <path d="M140 170 h120 l-14 90 h-92 z" fill="#f8f9fa" stroke="#ced4da" stroke-width="3"/>
  <rect x="134" y="162" width="132" height="16" rx="4" fill="#e9ecef" stroke="#ced4da" stroke-width="3"/>
"""


@image(11, "#fff0f6", "#fcc2d7")
def sunglasses():  # UVカット サングラス
    return """
  <path d="M60 120 q-20 -10 -26 30" fill="none" stroke="#212529" stroke-width="8" stroke-linecap="round"/>
  <path d="M340 120 q20 -10 26 30" fill="none" stroke="#212529" stroke-width="8" stroke-linecap="round"/>
  <path d="M60 118 h110 q4 70 -52 70 q-60 0 -58 -70 z" fill="#212529"/>
  <path d="M230 118 h110 q2 70 -58 70 q-56 0 -52 -70 z" fill="#212529"/>
  <path d="M70 126 h92 q0 54 -44 54 q-50 0 -48 -54 z" fill="#364fc7"/>
  <path d="M238 126 h92 q2 54 -48 54 q-44 0 -44 -54 z" fill="#364fc7"/>
  <path d="M80 134 l30 0 l-26 30 z M248 134 l30 0 l-26 30 z" fill="#fff" opacity="0.35"/>
  <path d="M170 124 q30 -16 60 0" fill="none" stroke="#212529" stroke-width="8"/>
"""


@image(12, "#e7f5ff", "#74c0fc")
def umbrella():  # ジャンプ式 長傘
    drops = "".join(f'<path d="M{x} {y} l-4 12" stroke="#1971c2" stroke-width="3" stroke-linecap="round" opacity="0.5"/>'
                    for x, y in [(60, 40), (100, 90), (330, 60), (350, 140), (50, 170), (300, 20)])
    return f"""
  {drops}
  <path d="M60 140 q140 -160 280 0 q-23 -20 -47 0 q-23 -20 -47 0 q-23 -20 -46 0 q-23 -20 -46 0 q-23 -20 -47 0 q-24 -20 -47 0 z" fill="#e03131"/>
  <path d="M200 30 q-40 50 -46 110 M200 30 q40 50 46 110 M200 30 v110" fill="none" stroke="#a61e4d" stroke-width="2"/>
  <path d="M200 30 v-12" stroke="#495057" stroke-width="5"/>
  <path d="M200 140 v100 q0 22 -22 22 q-20 0 -20 -18" fill="none" stroke="#5c3d2e" stroke-width="8" stroke-linecap="round"/>
"""


@image(13, "#e9ecef", "#adb5bd")
def smartphone():  # スマートフォン
    return """
  <defs>
    <linearGradient id="screen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#4c6ef5"/><stop offset="1" stop-color="#be4bdb"/>
    </linearGradient>
  </defs>
  <rect x="140" y="24" width="120" height="238" rx="22" fill="#212529"/>
  <rect x="148" y="32" width="104" height="222" rx="16" fill="url(#screen)"/>
  <rect x="182" y="38" width="36" height="10" rx="5" fill="#212529"/>
  <g fill="#fff" opacity="0.85">
    <rect x="160" y="80" width="22" height="22" rx="6"/><rect x="189" y="80" width="22" height="22" rx="6"/><rect x="218" y="80" width="22" height="22" rx="6"/>
    <rect x="160" y="112" width="22" height="22" rx="6"/><rect x="189" y="112" width="22" height="22" rx="6"/><rect x="218" y="112" width="22" height="22" rx="6"/>
  </g>
  <text x="200" y="196" font-family="sans-serif" font-size="30" fill="#fff" text-anchor="middle">12:34</text>
  <rect x="178" y="240" width="44" height="4" rx="2" fill="#fff" opacity="0.8"/>
"""


@image(14, "#f8f9fa", "#dee2e6")
def dslr_camera():  # 一眼レフカメラ
    return """
  <path d="M160 70 h80 l14 30 h-108 z" fill="#343a40"/>
  <rect x="70" y="96" width="260" height="150" rx="16" fill="#212529"/>
  <rect x="70" y="120" width="54" height="126" rx="12" fill="#343a40"/>
  <rect x="270" y="80" width="40" height="18" rx="4" fill="#495057"/>
  <circle cx="210" cy="172" r="64" fill="#495057"/>
  <circle cx="210" cy="172" r="52" fill="#212529" stroke="#868e96" stroke-width="4"/>
  <circle cx="210" cy="172" r="34" fill="#1864ab"/>
  <circle cx="210" cy="172" r="18" fill="#0b2545"/>
  <circle cx="198" cy="160" r="8" fill="#fff" opacity="0.6"/>
  <circle cx="300" cy="118" r="6" fill="#e03131"/>
"""


@image(15, "#fff9db", "#ffec99")
def notebook():  # A5 方眼ノート
    grid = "".join(f'<path d="M{x} 50 v200" stroke="#a5d8ff" stroke-width="1"/>' for x in range(150, 300, 12))
    grid += "".join(f'<path d="M140 {y} h160" stroke="#a5d8ff" stroke-width="1"/>' for y in range(60, 250, 12))
    rings = "".join(f'<circle cx="128" cy="{y}" r="7" fill="none" stroke="#868e96" stroke-width="4"/>' for y in range(64, 250, 22))
    return f"""
  <rect x="124" y="44" width="186" height="216" rx="6" fill="#1c7ed6"/>
  <rect x="120" y="40" width="180" height="216" rx="6" fill="#fff" stroke="#ced4da" stroke-width="2"/>
  <g transform="translate(-10 0)">{grid}</g>
  {rings}
  <path d="M170 120 q20 -30 40 0 t40 0" fill="none" stroke="#495057" stroke-width="3"/>
"""


@image(16, "#f3f0ff", "#e5dbff")
def fountain_pen():  # 万年筆
    return """
  <g transform="rotate(-35 200 150)">
    <rect x="60" y="134" width="150" height="34" rx="16" fill="#1b1f3b"/>
    <rect x="200" y="136" width="100" height="30" rx="8" fill="#212529"/>
    <rect x="196" y="134" width="10" height="34" fill="#d4af37"/>
    <rect x="90" y="128" width="90" height="6" rx="3" fill="#d4af37"/>
    <path d="M300 138 h24 l40 13 l-40 13 h-24 z" fill="#d4af37"/>
    <path d="M326 151 h34" stroke="#7c5a00" stroke-width="2"/>
    <circle cx="330" cy="151" r="3" fill="#7c5a00"/>
  </g>
  <path d="M90 250 q40 -20 80 0 t80 0" fill="none" stroke="#1b1f3b" stroke-width="3"/>
"""


@image(17, "#ebfbee", "#c3fae8")
def kyusu():  # 常滑焼の急須
    return """
  <path d="M150 170 q-60 -20 -80 -60" fill="none" stroke="#a0522d" stroke-width="14" stroke-linecap="round"/>
  <ellipse cx="200" cy="180" rx="78" ry="70" fill="#b5502a"/>
  <ellipse cx="200" cy="130" rx="54" ry="12" fill="#8b3a1c"/>
  <ellipse cx="200" cy="124" rx="44" ry="10" fill="#c4622d"/>
  <circle cx="200" cy="112" r="8" fill="#8b3a1c"/>
  <path d="M276 150 h48 q8 0 8 8 v6 q0 8 -8 8 h-48" fill="#8b3a1c"/>
  <path d="M150 190 q50 20 100 0" fill="none" stroke="#e8a07a" stroke-width="3" opacity="0.6"/>
  <path d="M60 104 q-10 -20 6 -36" fill="none" stroke="#adb5bd" stroke-width="3" opacity="0.6"/>
"""


@image(18, "#fff4e6", "#ffc9c9")
def frying_pan():  # 鉄のフライパン 26cm
    return """
  <rect x="250" y="138" width="130" height="22" rx="10" fill="#5c3d2e"/>
  <rect x="236" y="142" width="30" height="14" fill="#343a40"/>
  <ellipse cx="150" cy="160" rx="120" ry="70" fill="#343a40"/>
  <ellipse cx="150" cy="154" rx="104" ry="58" fill="#212529"/>
  <ellipse cx="140" cy="150" rx="40" ry="26" fill="#fff"/>
  <ellipse cx="146" cy="148" rx="15" ry="11" fill="#fab005"/>
  <path d="M90 130 q20 -12 40 -14" stroke="#868e96" stroke-width="3" fill="none" opacity="0.5"/>
"""


@image(19, "#e7f5ff", "#d0ebff")
def tshirt():  # コットン Tシャツ
    return """
  <path d="M150 50 q50 30 100 0 l80 40 l-30 60 l-34 -18 v128 h-132 v-128 l-34 18 l-30 -60 z" fill="#fff" stroke="#ced4da" stroke-width="3" stroke-linejoin="round"/>
  <path d="M170 52 q30 26 60 0" fill="none" stroke="#ced4da" stroke-width="4"/>
  <path d="M136 132 v128 M264 132 v128" stroke="#e9ecef" stroke-width="2"/>
  <text x="200" y="170" font-family="sans-serif" font-weight="700" font-size="22" fill="#1971c2" text-anchor="middle">ORGANIC</text>
"""


@image(20, "#fff5f5", "#ffc9c9")
def knit_hat():  # ニット帽
    ribs = "".join(f'<path d="M{x} 200 v44" stroke="#a61e4d" stroke-width="3"/>' for x in range(110, 300, 14))
    return f"""
  <circle cx="200" cy="58" r="30" fill="#f8f9fa"/>
  <circle cx="190" cy="50" r="8" fill="#fff"/>
  <path d="M100 210 q0 -130 100 -130 q100 0 100 130 z" fill="#e64980"/>
  <path d="M150 100 q-20 50 -20 110 M200 82 v128 M250 100 q20 50 20 110" stroke="#c2255c" stroke-width="3" fill="none"/>
  <rect x="96" y="196" width="208" height="52" rx="10" fill="#c2255c"/>
  {ribs}
"""


@image(21, "#f8f9fa", "#e9ecef")
def electric_kettle():  # 電気ケトル
    return """
  <rect x="110" y="236" width="170" height="20" rx="8" fill="#343a40"/>
  <path d="M130 236 l14 -150 q2 -16 18 -16 h70 q16 0 18 16 l14 150 z" fill="#f8f9fa" stroke="#adb5bd" stroke-width="3"/>
  <path d="M138 90 l-38 -20 l4 26 l36 14" fill="#f1f3f5" stroke="#adb5bd" stroke-width="3" stroke-linejoin="round"/>
  <path d="M262 92 q44 0 44 60 t-36 60" fill="none" stroke="#343a40" stroke-width="16" stroke-linecap="round"/>
  <ellipse cx="197" cy="74" rx="44" ry="8" fill="#343a40"/>
  <rect x="160" y="120" width="18" height="90" rx="4" fill="#a5d8ff" opacity="0.8"/>
  <circle cx="290" cy="200" r="5" fill="#40c057"/>
  <path d="M90 60 q-8 -16 4 -30" fill="none" stroke="#ced4da" stroke-width="4" stroke-linecap="round"/>
"""


@image(22, "#fff9db", "#ffe066")
def acoustic_guitar():  # アコースティックギター
    frets = "".join(f'<path d="M{x} 136 v28" stroke="#ced4da" stroke-width="2"/>' for x in range(250, 350, 14))
    strings = "".join(f'<path d="M110 {y} H370" stroke="#dee2e6" stroke-width="1"/>' for y in range(141, 162, 4))
    return f"""
  <path d="M150 150 q0 -60 -50 -60 q-50 0 -60 60 q10 60 60 60 q50 0 50 -60 z" fill="#d9480f"/>
  <path d="M200 150 q0 -48 -36 -48 q-30 0 -36 48 q6 48 36 48 q36 0 36 -48 z" fill="#d9480f"/>
  <path d="M150 150 q0 -50 -46 -50 q-44 0 -54 50 q10 50 54 50 q46 0 46 -50 z" fill="#e8590c"/>
  <path d="M196 150 q0 -40 -32 -40 q-26 0 -30 40 q4 40 30 40 q32 0 32 -40 z" fill="#e8590c"/>
  <circle cx="160" cy="150" r="18" fill="#212529"/>
  <rect x="198" y="134" width="150" height="32" fill="#5c3d2e"/>
  {frets}
  <rect x="346" y="126" width="34" height="48" rx="6" fill="#5c3d2e"/>
  <rect x="80" y="140" width="10" height="22" fill="#343a40"/>
  {strings}
"""


@image(23, "#d3f9d8", "#69db7c")
def soccer_ball():  # サッカーボール 5号
    return """
  <circle cx="200" cy="150" r="100" fill="#fff" stroke="#212529" stroke-width="4"/>
  <polygon points="200,112 236,138 222,180 178,180 164,138" fill="#212529"/>
  <g stroke="#212529" stroke-width="4" fill="none">
    <path d="M200 112 v-58 M236 138 l54 -18 M222 180 l34 46 M178 180 l-34 46 M164 138 l-54 -18"/>
  </g>
  <path d="M182 52 l18 -2 l18 2 l-4 12 h-28 z" fill="#212529"/>
  <path d="M290 112 l8 22 l-4 30 l-12 -4 l-2 -30 z" fill="#212529"/>
  <path d="M110 112 l-8 22 l4 30 l12 -4 l2 -30 z" fill="#212529"/>
  <path d="M252 222 l20 -10 l10 16 l-16 14 l-14 -6 z" fill="#212529"/>
  <path d="M148 222 l-20 -10 l-10 16 l16 14 l14 -6 z" fill="#212529"/>
  <path d="M140 90 q20 -24 50 -30" fill="none" stroke="#fff" stroke-width="6" opacity="0.6"/>
"""


@image(24, "#fff4e6", "#ffd8a8")
def alarm_clock():  # 目覚まし時計
    return """
  <path d="M120 70 a40 40 0 0 1 60 -10 z" fill="#c92a2a"/>
  <path d="M280 70 a40 40 0 0 0 -60 -10 z" fill="#c92a2a"/>
  <path d="M200 60 v-20 M186 40 h28" stroke="#868e96" stroke-width="6" stroke-linecap="round"/>
  <path d="M140 230 l-20 30 M260 230 l20 30" stroke="#495057" stroke-width="10" stroke-linecap="round"/>
  <circle cx="200" cy="155" r="92" fill="#e03131"/>
  <circle cx="200" cy="155" r="76" fill="#fff"/>
  <g font-family="sans-serif" font-size="20" font-weight="700" fill="#212529" text-anchor="middle">
    <text x="200" y="100">12</text><text x="262" y="162">3</text><text x="200" y="224">6</text><text x="138" y="162">9</text>
  </g>
  <path d="M200 155 L200 112" stroke="#212529" stroke-width="6" stroke-linecap="round"/>
  <path d="M200 155 L236 170" stroke="#212529" stroke-width="5" stroke-linecap="round"/>
  <circle cx="200" cy="155" r="6" fill="#212529"/>
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for pid, (bg1, bg2, fn) in sorted(IMAGES.items()):
        path = OUT / f"{pid}.svg"
        path.write_text(frame(bg1, bg2, fn()), encoding="utf-8")
        print(f"generated {path.relative_to(OUT.parents[3])}  ({fn.__name__})")


if __name__ == "__main__":
    main()
