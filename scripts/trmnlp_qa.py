"""Exercise actual TRMNLP Liquid renders; preserve screenshots for visual review.

Run at the repository root with Docker available. No TRMNL credentials required.
Only the local preview config is temporarily modified, then restored.
"""
import json
from pathlib import Path
import re
import struct
import subprocess
import time
from urllib.parse import urlencode
from urllib.request import urlopen

VIEWS = ('full', 'half_horizontal', 'half_vertical', 'quadrant')
DEVICES = {
    'og': (800, 480, 1, 'screen screen--og screen--md screen--density-1x screen--1bit'),
    'x': (1872, 1404, 4, 'screen screen--v2 screen--lg screen--density-2x screen--4bit'),
    'x-portrait': (1404, 1872, 4, 'screen screen--v2 screen--lg screen--density-2x screen--4bit screen--portrait'),
}
TITLES = ['See the northern lights', 'Build a home server', 'Visit Japan',
          'Learn Italian', 'Sleep in a mountain hut', 'Write a short story',
          'Ride the Glacier Express', 'Learn to sail', 'Plant a fruit tree',
          'Run a half marathon', 'Make a ceramic bowl', 'Visit Iceland']
MIXED = '\n'.join(f'[{"x" if i < 4 else " "}] {t} | Personal | Someday' for i, t in enumerate(TITLES[:5]))
ALL_DONE = MIXED.replace('[ ]', '[x]')
TWELVE = '\n'.join(f'[ ] {t} | Personal | Someday' for t in TITLES)
LONG = '\n'.join(f'[ ] {t} with family and friends on a memorable adventure | Experiences | Plan a relaxed weekend and make time to enjoy the journey' for t in TITLES)
MANY = '\n'.join(f'[ ] Bucket item {i:02d} | Test | Overflow' for i in range(1, 31))
OUT = Path('qa-artifacts')
OUT.mkdir(exist_ok=True)
CONFIG = Path('.trmnlp.yml')
ORIGINAL = CONFIG.read_bytes()
checks = []

def stop():
    subprocess.run(['docker', 'stop', 'bucketlist-qa'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def start(mode, show, items, limit=12):
    stop()
    CONFIG.write_text(json.dumps({'watch': False, 'transform_runtime': 'disabled', 'custom_fields': {
        'list_title': 'Bucket List', 'display_mode': mode, 'show_completed': show,
        'bucket_items': items, 'max_items': limit}}))
    subprocess.run(['docker', 'run', '--rm', '-d', '--name', 'bucketlist-qa', '-p', '4567:4567',
                    '-v', f'{Path.cwd()}:/plugin', '-e', 'RUBYOPT=-r/plugin/scripts/trmnlp_wait.rb',
                    'trmnl/trmnlp', 'serve', '--bind', '0.0.0.0'], check=True)
    for _ in range(60):
        try:
            with urlopen('http://127.0.0.1:4567/data', timeout=2):
                return
        except Exception:
            time.sleep(1)
    subprocess.run(['docker', 'logs', 'bucketlist-qa'])
    raise RuntimeError('Preview did not become ready')

def html(view):
    with urlopen(f'http://127.0.0.1:4567/render/{view}.html', timeout=30) as r:
        body = r.read().decode()
    assert 'Liquid error' not in body and 'Liquid syntax error' not in body
    return body

def names(body):
    return re.findall(r'class="(?:title|description)[^"]*"[^>]*>([^<]+)</span>', body)

def render(name, portrait=False):
    for device, (width, height, depth, classes) in DEVICES.items():
        if device == 'x-portrait' and not portrait:
            continue
        for view in VIEWS:
            params = urlencode(dict(screen_classes=classes, width=width, height=height, color_depth=depth))
            with urlopen(f'http://127.0.0.1:4567/render/{view}.png?{params}', timeout=120) as r:
                image = r.read()
            assert image[:8] == b'\x89PNG\r\n\x1a\n'
            assert struct.unpack('>II', image[16:24]) == (width, height)
            (OUT / f'{name}-{device}-{view}.png').write_bytes(image)

try:
    for show in (True, False, 'true', 'false', '1', '0', 'yes', 'no', 'on', 'off'):
        start('list', show, MIXED)
        enabled = str(show).lower() in ('true', '1', 'yes', 'on')
        expected = TITLES[:5] if enabled else TITLES[4:5]
        for view in VIEWS:
            body = html(view)
            present = [t for t in TITLES if t in names(body)]
            assert present == expected, (show, view, present)
            checks.append(f'list toggle {show!r}: {view}')

    for show in (False, True):
        start('list', show, ALL_DONE)
        for view in VIEWS:
            body = html(view)
            assert ('All items completed' in body) == (not show), view
            assert (TITLES[0] in names(body)) == show, view
            checks.append(f'all complete {show}: {view}')
        if not show:
            render('complete')

    for mode in ('list', 'focus'):
        start(mode, False, '  \n   ')
        for view in VIEWS:
            assert 'Add your first item' in html(view)
            checks.append(f'empty {mode}: {view}')

    start('focus', False, MIXED)
    for view in VIEWS:
        assert TITLES[4] in html(view)
        checks.append(f'focus hidden: {view}')
    # All-done + show is deterministic: no probabilistic random-pool assertion.
    start('focus', True, ALL_DONE)
    for view in VIEWS:
        body = html(view)
        assert any(t in body for t in TITLES[:5]) and 'All items completed' not in body
        checks.append(f'focus completed eligible: {view}')

    start('list', True, TWELVE, limit=3)
    for view in VIEWS:
        present = [t for t in TITLES if t in names(html(view))]
        assert present == TITLES[:3], present
            checks.append(f'limit 3: {view}')

    start('list', True, MANY, limit=25)
    for view in VIEWS:
        body = html(view)
        assert 'Bucket item 25' in body and 'Bucket item 26' not in body
        checks.append(f'limit 25: {view}')
    render('twentyfive', portrait=True)

    for name, items in [('five', MIXED), ('twelve', TWELVE), ('long', LONG)]:
        start('list', True, items)
        for view in VIEWS:
            body = html(view)
            assert 'lg:title--large' in body
            assert 'title title--small' not in body and 'description description--small' not in body
            assert 'data-overflow-counter="true"' in body
            (OUT / f'{name}-{view}.html').write_text(body)
        render(name, portrait=True)
    geometry = [json.loads(line) for line in (OUT / 'geometry.jsonl').read_text().splitlines()]
    clipped = [(g['screen'], g['view'], item) for g in geometry for item in g['items'] if item['clipped']]
    assert not clipped, clipped
    print(f'PASS: {len(checks)} semantic assertions; {len(list(OUT.glob("*.png")))} PNG renders; no out-of-bounds list items')
finally:
    CONFIG.write_bytes(ORIGINAL)
    stop()
    (OUT / 'results.json').write_text(json.dumps({'passed_assertions': checks}, indent=2))
