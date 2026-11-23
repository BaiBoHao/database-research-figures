"""Render the palette card and check color contrast on intended backgrounds."""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle


ASSETS = Path(__file__).resolve().parents[1] / "assets"


def luminance(color):
    def linear(channel):
        return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4

    channels = [linear(int(color[i:i + 2], 16) / 255) for i in (1, 3, 5)]
    return sum(weight * channel for weight, channel in zip((0.2126, 0.7152, 0.0722), channels))


def contrast(foreground, background):
    low, high = sorted((luminance(foreground), luminance(background)))
    return (high + 0.05) / (low + 0.05)


def check_contrast(theme):
    neutral = theme["neutral"]
    for role, spec in theme["architecture"].items():
        for background in (spec["base"], spec["fill"]):
            assert contrast(neutral["text"], background) >= 4.5, role
        assert contrast(spec["ink"], spec["fill"]) >= 3, role
    for styles in (theme["plot"]["services"], theme["plot"]["methods"]):
        for key, spec in styles.items():
            assert contrast(spec["color"], neutral["background"]) >= 3, key


def draw(theme):
    plt.style.use(ASSETS / "paper.mplstyle")
    color = theme["neutral"]
    fig, ax = plt.subplots(figsize=(10, 4.25), layout="none")
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set(xlim=(0, 1000), ylim=(425, 0))
    ax.axis("off")

    def text(x, y, value, size, *, bold=False, fill=None):
        ax.text(x, y, value, fontsize=size, color=fill or color["text"],
                fontweight="bold" if bold else "normal", va="center")

    text(36, 42, "Color for Computer Systems Research", 20, bold=True)
    text(36, 78, "Architecture: use light fills for component roles", 12, bold=True)
    for i, spec in enumerate(theme["architecture"].values()):
        x = 36 + 188 * i
        ax.add_patch(FancyBboxPatch((x, 100), 176, 94, boxstyle="round,pad=0,rounding_size=9",
                                    facecolor=spec["fill"], edgecolor=spec["ink"], linewidth=1))
        ax.add_patch(Rectangle((x + 14, 114), 18, 17, facecolor=spec["base"], edgecolor=spec["ink"], linewidth=.6))
        text(x + 42, 122, spec["label"], 11, bold=True)
        text(x + 14, 158, spec["base"], 10)
        text(x + 14, 179, f'Fill  {spec["fill"]}', 8.5, fill=color["muted"])

    ax.plot((36, 964), (219, 219), color=color["rule"], linewidth=.9)
    text(36, 244, "Results: keep color, line style and marker consistent", 12, bold=True)
    entries = [*theme["plot"]["services"].values(), *theme["plot"]["methods"].values()]
    for i, spec in enumerate(entries):
        x = 36 + 188 * i
        ax.plot([x + 2, x + 35, x + 68], [301] * 3, color=spec["color"],
                linestyle=spec["linestyle"], marker=spec["marker"], markevery=[1],
                markersize=6, linewidth=2.1)
        text(x + 79, 301, spec["label"], 10.5, bold=True)
        text(x + 2, 328, spec["color"], 10, fill=color["muted"])
    text(36, 386, "First three: compare services. Last two: compare methods.", 10, fill=color["muted"])
    fig.savefig(ASSETS / "palette-card.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    palette = json.loads((ASSETS / "palette.json").read_text(encoding="utf-8"))
    check_contrast(palette)
    draw(palette)
    print("Palette card rendered; text, icon and curve contrast checked.")
