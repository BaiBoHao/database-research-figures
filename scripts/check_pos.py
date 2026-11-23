"""Check the structure of a self-contained ProcessOn diagram without network access."""
import argparse
import base64
import binascii
import json
from pathlib import Path


def inspect_pos(path):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if data["meta"]["type"] != "ProcessOn Schema File":
        raise ValueError("Expected a ProcessOn Schema File")
    shapes = data["diagram"]["elements"]["elements"]
    if not isinstance(shapes, dict) or not shapes:
        raise ValueError("The diagram must contain editable elements")
    links = images = 0
    for identifier, shape in shapes.items():
        if identifier != shape.get("id"):
            raise ValueError("Element key and id differ")
        if shape.get("name") == "linker":
            links += 1
            for key in ("from", "to"):
                endpoint = shape[key]
                if not all(isinstance(endpoint.get(axis), (int, float)) for axis in ("x", "y")):
                    raise ValueError("A connector is missing its endpoint coordinates")
                if endpoint.get("id") and endpoint["id"] not in shapes:
                    raise ValueError("A connector refers to a missing element")
        fill = shape.get("fillStyle", {})
        if fill.get("type") == "image":
            images += 1
            header, separator, payload = fill.get("fileId", "").partition(",")
            if not separator or not header.startswith("data:image/") or not header.endswith(";base64"):
                raise ValueError("Image fills must embed their assets as data URIs")
            image = base64.b64decode(payload, validate=True)
            if not image or (header == "data:image/png;base64" and not image.startswith(b"\x89PNG\r\n\x1a\n")):
                raise ValueError("An embedded image has invalid data")
    return len(shapes), links, images


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    try:
        shapes, links, images = inspect_pos(args.file)
    except (OSError, KeyError, TypeError, ValueError, binascii.Error) as exc:
        parser.exit(1, f"POS check failed: {exc}\n")
    print(f"POS structure OK: {shapes} elements, {links} connectors, {images} embedded images.")


if __name__ == "__main__":
    main()
