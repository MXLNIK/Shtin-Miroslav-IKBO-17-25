
from xml.sax.saxutils import escape


NODE_WIDTH = 220
NODE_HEIGHT = 60
NODE_GAP_X = 70
NODE_GAP_Y = 110
SVG_MARGIN = 50
FONT_SIZE = 12


def generate_mermaid(graph):
    """Создает текстовую Mermaid-диаграмму"""
    lines = ["graph TD"]

    for package, dependencies in graph.items():
        for dependency in dependencies:
            lines.append(f"    {package} --> {dependency}")

    return "\n".join(lines)


def get_levels(graph):
    """Распределяет узлы графа по уровням"""
    nodes = set(graph)

    for dependencies in graph.values():
        nodes.update(dependencies)

    levels = {}
    visited = set()
    queue = [(next(iter(graph)), 0)] if graph else []

    while queue:
        package, depth = queue.pop(0)

        if package in visited:
            continue

        visited.add(package)
        levels.setdefault(depth, []).append(package)

        for dependency in graph.get(package, []):
            if dependency not in visited:
                queue.append((dependency, depth + 1))

    for package in nodes - visited:
        levels.setdefault(max(levels.keys(), 
                              default=-1) + 1, []).append(package)

    return levels


def get_positions(levels):
    """Вычисляет координаты узлов для каждого уровня"""
    positions = {}

    for depth, packages in levels.items():
        for index, package in enumerate(packages):
            x = SVG_MARGIN + index * (NODE_WIDTH + NODE_GAP_X)
            y = SVG_MARGIN + depth * (NODE_HEIGHT + NODE_GAP_Y)
            positions[package] = (x, y)

    return positions


def add_edges(elements, graph, positions):
    """Добавляет линии между узлами графа"""
    for package, dependencies in graph.items():
        for dependency in dependencies:
            x1, y1 = positions[package]
            x2, y2 = positions[dependency]

            elements.append(
                f'<line x1="{x1 + NODE_WIDTH // 2}" '
                f'y1="{y1 + NODE_HEIGHT}" '
                f'x2="{x2 + NODE_WIDTH // 2}" y2="{y2}" '
                f'stroke="black" stroke-width="1.5" '
                f'marker-end="url(#arrow)"/>'
            )


def add_nodes(elements, positions):
    """Добавляет прямоугольники и подписи узлов"""
    for package, (x, y) in positions.items():
        elements.append(
            f'<rect x="{x}" y="{y}" width="{NODE_WIDTH}" '
            f'height="{NODE_HEIGHT}" rx="8" '
            f'fill="lightblue" stroke="black"/>'
        )

        elements.append(
            f'<text x="{x + NODE_WIDTH // 2}" '
            f'y="{y + 35}" text-anchor="middle" '
            f'font-size="{FONT_SIZE}">{escape(package)}</text>'
        )


def generate_svg(graph, filename):
    """Создает SVG-изображение графа"""
    levels = get_levels(graph)
    positions = get_positions(levels)

    max_x = max(
        (x for x, y in positions.values()),
        default=SVG_MARGIN
    )
    max_y = max(
        (y for x, y in positions.values()),
        default=SVG_MARGIN
    )

    width = max_x + NODE_WIDTH + SVG_MARGIN
    height = max_y + NODE_HEIGHT + SVG_MARGIN

    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
    ]

    elements.append(
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" '
        'refX="8" refY="3" orient="auto">'
        '<path d="M0,0 L0,6 L9,3 z" fill="black"/>'
        '</marker></defs>'
    )

    add_edges(elements, graph, positions)
    add_nodes(elements, positions)
    elements.append("</svg>")

    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(elements))

    return filename
