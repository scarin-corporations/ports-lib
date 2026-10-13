"""Render the README's live repository ranking and its star chart."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- BEGIN LIVE CATALOG -->'
END = '<!-- END LIVE CATALOG -->'


def render(projects):
    ranked = sorted(projects, key=lambda p: (-p['stars'], p['name'].lower()))[:10]
    if not ranked:
        return '<p>The live catalog is waiting for its first successful GitHub sync.</p>', empty_chart()
    lines = [
        '<p><a href="https://scarin-corporations.github.io/ports-lib/">Open the Ports Lib app →</a></p>',
        '',
        f"**{len(projects):,} repositories indexed.** Search matches remain candidates until reviewed.",
        '',
        '![Top 10 repositories by GitHub stars](data/top-stars.svg)',
        '',
        '| # | Repository | Stars | Last push | Status |',
        '|---:|---|---:|---|---|',
    ]
    for index, project in enumerate(ranked, 1):
        name = project['name'].replace('|', r'\|').replace('[', r'\[').replace(']', r'\]')
        status = 'Reviewed' if project.get('reviewed') else 'Candidate'
        if project.get('archived'):
            status += ' · Archived'
        lines.append(f"| {index} | [{name}]({project['url']}) | {project['stars']:,} | {project['pushedAt'][:10]} | {status} |")
    return '\n'.join(lines), make_chart(ranked)


def empty_chart():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 180" role="img">'
            '<rect width="900" height="180" fill="#101211"/><text x="32" y="92" fill="#dce8d0" '
            'font-family="sans-serif" font-size="22">Waiting for the first successful GitHub sync</text></svg>')


def make_chart(projects):
    width, row, top = 1000, 38, 58
    height = top + row * len(projects) + 24
    max_stars = max(p['stars'] for p in projects) or 1
    pieces = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img">',
        '<title>Top GitHub repositories by stars</title>',
        '<desc>Bar chart of the ten most starred repositories in the Ports Lib catalog.</desc>',
        f'<rect width="{width}" height="{height}" rx="14" fill="#101211"/>',
        '<text x="24" y="34" fill="#c5f567" font-family="sans-serif" font-size="18" font-weight="700">TOP REPOSITORIES BY STARS</text>',
    ]
    for i, project in enumerate(projects):
        y = top + i * row
        name = html.escape(project['name'])
        stars = project['stars']
        bar_width = max(3, round(620 * stars / max_stars))
        pieces.extend([
            f'<text x="24" y="{y + 19}" fill="#e8eddf" font-family="sans-serif" font-size="14">{name}</text>',
            f'<rect x="310" y="{y + 4}" width="620" height="20" rx="6" fill="#20271e"/>',
            f'<rect x="310" y="{y + 4}" width="{bar_width}" height="20" rx="6" fill="#c5f567"/>',
            f'<text x="{min(950, 324 + bar_width)}" y="{y + 19}" fill="#f0f3eb" font-family="sans-serif" font-size="13">{stars:,} ★</text>',
        ])
    pieces.append('</svg>')
    return ''.join(pieces)


def update(root=ROOT):
    readme = root / 'README.md'
    content = readme.read_text()
    if content.count(START) != 1 or content.count(END) != 1:
        raise ValueError('README must contain one live catalog marker pair')
    catalog = json.loads((root / 'data/catalog.json').read_text())
    if catalog['discovery']['status'] != 'ok':
        raise ValueError('Refusing to refresh README from an incomplete catalog')
    section, chart = render(catalog['projects'])
    before, rest = content.split(START, 1)
    _, after = rest.split(END, 1)
    readme.write_text(before + START + '\n' + section + '\n' + END + after)
    (root / 'data/top-stars.svg').write_text(chart + '\n')


if __name__ == '__main__':
    update()
