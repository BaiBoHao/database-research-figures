---
name: scientific-figure-style
description: Draw or restyle editable architecture, method, and results figures for database and computer-systems research. Use for POS diagrams, consistent scientific palettes, systems icons, and publication-size figure checks.
---

# Database Research Figures

Use the labels and requirements in the user's paper or target venue first. Read [palette.json](assets/palette.json) for the shared Okabe–Ito colors, derived tints, and series mappings. Choose at most three main hues for each figure. Neutral text, the white canvas, and lighter shades of an existing hue do not add another hue. Refer to the [icon catalog](assets/icons/ATTRIBUTION.md) for consistent SVG assets.

## Architecture and method figures

- Place clients, ingress, processing components, and deployment boundaries before styling. Attach arrows to their real endpoints. For primary–replica deployments, show where writes and eligible reads go, which node sends replication data, and which component issues control commands. Draw per-node resource targets when the controller distributes quotas. Use a dashed connector for control signals and label connections that could be misread.
- Group related elements using alignment, whitespace, short labels, and light tints without outlines. For primary–replica diagrams, use blue for request paths, bluish green for the cluster and replication, and reddish purple for both decisions and resource control. Use strokes for real connections and add icons for identifiable entities such as database instances or servers.
- Use the paper's fonts if specified. A thesis can use regular Times New Roman with Song-style CJK text, or another consistent, legible pair. Use a small size hierarchy, with normal-weight component labels. Use separate labels, ordinary punctuation, or line breaks for lists. Avoid decorative dot separators and repeated header cards.
- Preserve the proportions and transparency of product artwork supplied for the figure. Use generic icons for reusable examples. Follow the relevant asset license when sharing a figure or its source.

## Experimental plots

- Use [paper.mplstyle](assets/paper.mplstyle) and bind `plot.services` or `plot.methods` to names. Keep colors, line styles, and marker shapes stable across figures. Use a white canvas, an unframed legend, and left and bottom axes as the default for line and scatter plots. If a plot compares two dimensions, assign color to one and use panels or another channel for the other.
- Label axes and units. Distinguish measured results from illustrations. Check that legend keys and line styles remain readable in grayscale at the paper's actual width.

## Delivery

- For a ProcessOn drawing, deliver one editable `.pos` master by default. Keep text and connectors as native elements and embed licensed image assets so the file does not depend on a local path. Use one preview for review if helpful. Export additional formats when requested or needed for the target venue.
- Check boundaries, endpoints, labels, and embedded resources. `python scripts/check_pos.py FILE.pos` checks the JSON structure and asset references. Record an editor import only when tested in that editor.
- See [related workflows](references/related-workflows.md) for focused guidance on layouts and experimental plots.
