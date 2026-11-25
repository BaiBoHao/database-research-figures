"""Render the palette card and check color contrast on intended backgrounds."""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle


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
    anchors = {spec["color"] for spec in theme["okabe_ito"].values()}
    for role, spec in theme["architecture"].items():
        assert spec["base"] in anchors, role
        assert contrast(neutral["text"], spec["fill"]) >= 4.5, role
        assert contrast(spec["ink"], spec["fill"]) >= 3, role
    for styles in (theme["plot"]["services"], theme["plot"]["methods"]):
        for key, spec in styles.items():
            assert spec["color"] in anchors, key
            assert contrast(spec["color"], neutral["background"]) >= 3, key


def draw(theme):
    plt.style.use(ASSETS / "paper.mplstyle")
    color = theme["neutral"]
    headings = theme["card_labels"]
    fig, ax = plt.subplots(figsize=(10, 4.75), layout="none")
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set(xlim=(0, 1000), ylim=(475, 0))
    ax.axis("off")

    def text(x, y, value, size, *, bold=False, fill=None):
        ax.text(x, y, value, fontsize=size, color=fill or color["text"],
                fontweight="bold" if bold else "normal", va="center")

    text(36, 35, theme["name"], 20, bold=True)
    text(36, 73, headings["swatches"], 12, bold=True)
    for i, spec in enumerate(theme["okabe_ito"].values()):
        x = 36 + 117 * i
        ax.add_patch(Circle((x + 18, 108), 17, facecolor=spec["color"], edgecolor="none", linewidth=0))
        text(x, 142, spec["label"], 10)
        text(x, 162, spec["color"], 9, fill=color["muted"])

    text(36, 206, headings["architecture"], 12, bold=True)
    for i, spec in enumerate(theme["architecture"].values()):
        x = 36 + 188 * i
        ax.add_patch(Rectangle((x, 228), 176, 58, facecolor=spec["fill"], edgecolor="none", linewidth=0))
        text(x + 13, 247, spec["label"], 11)
        text(x + 13, 269, spec["fill"], 9, fill=color["muted"])

    text(36, 328, headings["results"], 12, bold=True)
    entries = [*theme["plot"]["services"].values(), *theme["plot"]["methods"].values()]
    for i, spec in enumerate(entries):
        x = 36 + 188 * i
        ax.plot([x, x + 27, x + 54], [374] * 3, color=spec["color"],
                linestyle=spec["linestyle"], marker=spec["marker"], markevery=[1],
                markersize=6, linewidth=2.1)
        text(x + 67, 374, spec["label"], 10.5)
        text(x, 402, spec["color"], 10, fill=color["muted"])
    text(36, 449, headings["note"], 10, fill=color["muted"])
    fig.savefig(ASSETS / "palette-card.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    palette = json.loads((ASSETS / "palette.json").read_text(encoding="utf-8"))
    check_contrast(palette)
    draw(palette)
    print("Palette card rendered; text, icon and curve contrast checked.")
