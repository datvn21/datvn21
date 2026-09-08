from html import escape
from pathlib import Path


ASCII_NAME = [
    r" ____  _       _      _____ _             ____        _   ",
    r"|  _ \(_)_ __ | |__  |_   _(_) ___ _ __  |  _ \  __ _| |_ ",
    r"| | | | | '_ \| '_ \   | | | |/ _ \ '_ \ | | | |/ _` | __|",
    r"| |_| | | | | | | | |  | | | |  __/ | | || |_| | (_| | |_ ",
    r"|____/|_|_| |_|_| |_|  |_| |_|\___|_| |_||____/ \__,_|\__|",
]

WIDTH = 920
HEIGHT = 145
FONT_SIZE = 20
CHAR_WIDTH = 10
LINE_HEIGHT = 24
START_Y = 34


def glyphs(lines: list[str], class_name: str, shadow: bool = False) -> str:
    max_width = max(len(line) for line in lines)
    start_x = (WIDTH - max_width * CHAR_WIDTH) / 2
    rendered = []

    for row, line in enumerate(lines):
        y = START_Y + row * LINE_HEIGHT
        for col, char in enumerate(line):
            if char == " ":
                continue

            x = start_x + col * CHAR_WIDTH
            delay = -(((row * 17) + (col * 7)) % 37) / 10
            duration = 4.2 + (((row * 5) + col) % 9) / 10
            style = ""

            if not shadow:
                style = f' style="animation-delay:{delay:.1f}s;animation-duration:{duration:.1f}s"'

            rendered.append(
                f'<text x="{x:.1f}" y="{y}" class="{class_name}"{style}>{escape(char)}</text>'
            )

    return "\n  ".join(rendered)


def build_svg() -> str:
    shadow = glyphs(ASCII_NAME, "ascii-shadow", shadow=True)
    foreground = glyphs(ASCII_NAME, "ascii")

    return f"""<svg width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
  <title id="title">Dinh Tien Dat</title>
  <desc id="desc">Transparent animated ASCII profile banner for Dinh Tien Dat</desc>
  <style>
    text {{
      font-family: Cascadia Code, Consolas, Monaco, monospace;
      font-size: {FONT_SIZE}px;
      font-weight: 800;
      letter-spacing: 0;
      white-space: pre;
    }}

    .ascii-shadow {{
      fill: #0ea5e9;
      opacity: .1;
      transform: translate(2px, 2px);
    }}

    .ascii {{
      fill: #0f172a;
      animation: flicker 4.8s steps(1, end) infinite;
    }}

    @media (prefers-color-scheme: dark) {{
      .ascii-shadow {{ fill: #0ea5e9; opacity: .2; }}
      .ascii {{ fill: #f8fafc; }}
    }}

    @keyframes flicker {{
      0%, 100% {{ opacity: .92; }}
      8% {{ opacity: .45; }}
      9% {{ opacity: 1; }}
      12% {{ opacity: .68; }}
      13% {{ opacity: .96; }}
      44% {{ opacity: .88; }}
      45% {{ opacity: .28; fill: #0ea5e9; }}
      46% {{ opacity: .98; }}
      72% {{ opacity: .75; }}
      73% {{ opacity: 1; }}
    }}
  </style>

  {shadow}
  {foreground}
</svg>
"""


def main() -> None:
    output = Path(__file__).resolve().parents[1] / "assets" / "name-banner.svg"
    output.write_text(build_svg(), encoding="utf-8", newline="\n")
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
