#!/usr/bin/env python3
"""Sync shared header/footer into static pages. Python 3, no dependencies."""
import argparse
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PEOPLE_PAGES = {'faculty.html', 'students.html', 'postdocs_visitors.html', 'alumni.html'}


def render_header(filename):
    header = (ROOT / 'templates/header.html').read_text()
    current = 'events.html' if filename == 'pastseminars.html' else filename
    header = header.replace(f'href="{current}">', f'href="{current}" aria-current="page">')
    if filename in PEOPLE_PAGES:
        header = header.replace('class="people-menu"', 'class="people-menu is-current"')
    return header.strip()


def render_footer():
    return (ROOT / 'templates/footer.html').read_text().strip()


def sync(check=False):
    stale = []
    for path in sorted(ROOT.glob('*.html')):
        original = path.read_text()
        if '<!-- site-header:start -->' not in original:
            continue
        updated = original
        for part, replacement in [('header', render_header(path.name)), ('footer', render_footer())]:
            pattern = rf'<!-- site-{part}:start -->.*?<!-- site-{part}:end -->'
            block = f'<!-- site-{part}:start -->\n{replacement}\n<!-- site-{part}:end -->'
            updated, count = re.subn(pattern, lambda _: block, updated, flags=re.S)
            if count != 1:
                raise ValueError(f'{path.name}: expected exactly one {part} block')
        if updated != original:
            stale.append(path.name)
            if not check:
                path.write_text(updated)
    if check and stale:
        raise SystemExit('Shared layout needs updating: ' + ', '.join(stale))
    print('Shared layout is up to date.' if not stale else 'Updated: ' + ', '.join(stale))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if generated layout differs')
    sync(parser.parse_args().check)
