#!/usr/bin/env python3
"""Check static page structure, shared layout, local files, and fragment links."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from update_layout import ROOT, sync


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.anchors = set()
        self.refs = []
        self.tags = Counter()
        self.issues = []
        self.viewport = False
        self.lang = False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags[tag] += 1
        if 'id' in attrs:
            self.ids.append(attrs['id'])
            self.anchors.add(attrs['id'])
        if tag == 'a' and 'name' in attrs:
            self.anchors.add(attrs['name'])
        if tag == 'html':
            self.lang = bool(attrs.get('lang'))
        if tag == 'meta' and attrs.get('name') == 'viewport':
            self.viewport = 'width=device-width' in attrs.get('content', '')
        if tag == 'img' and 'alt' not in attrs:
            self.issues.append('Image has no alt attribute: ' + attrs.get('src', ''))
        if tag == 'iframe' and not attrs.get('title'):
            self.issues.append('Iframe has no title')
        for key in ('href', 'src'):
            if attrs.get(key):
                self.refs.append(attrs[key])

    handle_startendtag = handle_starttag


def read_page(path):
    raw = path.read_bytes()
    try:
        source = raw.decode('utf-8')
    except UnicodeDecodeError:
        source = raw.decode('windows-1252')
    return Page(source)


def main():
    sync(check=True)
    pages = {p: read_page(p) for p in sorted(ROOT.glob('*.html'))}
    errors = []
    for path, page in pages.items():
        issues = page.issues.copy()
        duplicates = [name for name, count in Counter(page.ids).items() if count > 1]
        if duplicates:
            issues.append('Duplicate IDs: ' + ', '.join(duplicates))
        for tag in ('h1', 'main', 'title'):
            if page.tags[tag] != 1:
                issues.append(f'Expected one {tag}, found {page.tags[tag]}')
        if not page.viewport or not page.lang:
            issues.append('Missing responsive viewport or document language')
        for ref in page.refs:
            url = urlsplit(ref)
            if url.scheme or url.netloc:
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target.is_dir():
                target /= 'index.html'
            if not target.is_file():
                issues.append('Missing local file: ' + ref)
            elif url.fragment and target.suffix.lower() in {'.html', '.htm'}:
                other = pages.get(target) or read_page(target)
                if unquote(url.fragment) not in other.anchors:
                    issues.append('Missing fragment: ' + ref)
        errors.extend(f'{path.name}: {issue}' for issue in issues)
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'Checked {len(pages)} pages: structure, local resources, and fragment links pass.')


if __name__ == '__main__':
    main()
