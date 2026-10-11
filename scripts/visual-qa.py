"""Optional Chromium QA. Requires Python Playwright and a local Chromium binary.

Run: python3 scripts/visual-qa.py [--browser /path/to/chromium]
Outputs screenshots and a machine-readable report under ignored output/qa/.
"""
import argparse
import functools
import http.server
import json
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright, Error

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output' / 'qa'
OUT.mkdir(parents=True, exist_ok=True)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--browser', default='/usr/bin/chromium')
args = parser.parse_args()


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
report = {'viewports': [], 'screenshots': [], 'checks': [], 'limitations': []}
errors = []
external = []


def capture(locator, name):
    locator.screenshot(path=str(OUT / name))
    report['screenshots'].append(name)


try:
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=args.browser, args=['--no-sandbox'])
        report['browser'] = browser.version
        context = browser.new_context(viewport={'width': 1440, 'height': 1000}, device_scale_factor=1)
        page = context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('request', lambda request: external.append(request.url) if request.url.startswith(('http:', 'https:')) and not request.url.startswith('http://127.0.0.1:') else None)
        try:
            page.goto((ROOT / 'index.html').as_uri())
            report['checks'].append('Direct file URL loads')
        except Error as error:
            if 'ERR_BLOCKED_BY_ADMINISTRATOR' not in str(error):
                raise
            report['limitations'].append('Direct file URL blocked by browser policy: net::ERR_BLOCKED_BY_ADMINISTRATOR')
        page.close()
        page = context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('request', lambda request: external.append(request.url) if request.url.startswith(('http:', 'https:')) and not request.url.startswith('http://127.0.0.1:') else None)
        page.goto(f'http://127.0.0.1:{server.server_port}/index.html')
        page.evaluate('document.fonts.ready')
        page.screenshot(path=str(OUT / 'desktop.png'))
        report['screenshots'].append('desktop.png')
        for width, height in [(1440, 1000), (390, 844), (320, 740)]:
            page.set_viewport_size({'width': width, 'height': height})
            report['viewports'].append({'width': width, 'height': height})
            for stem, count in [('01-opening', 7), ('02-coins', 7), ('03-river', 8), ('overview', 22)]:
                button = page.locator(f'button[data-target="{stem}"]')
                button.click()
                section = page.locator(f'section[id="{stem}"]')
                assert page.locator('.episode:visible').count() == 1
                assert button.get_attribute('aria-pressed') == 'true'
                assert section.locator('g.node').count() == count
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Page-level horizontal overflow'
                frame = section.locator('.mapframe')
                inner = section.locator('.mapinner')
                page.locator('#fit').click()
                assert frame.evaluate('(f)=>f.scrollWidth<=f.clientWidth+1 && f.scrollHeight<=f.clientHeight+1'), f'{width} {stem}: Fit must show entire map'
                if width == 1440:
                    capture(section, f'desktop-{stem}.png')
                if width == 390:
                    capture(section, f'mobile-{stem}.png')
                fit_width = inner.bounding_box()['width']
                page.locator('#in').click()
                assert inner.bounding_box()['width'] > fit_width
                page.locator('#out').click()
                assert abs(inner.bounding_box()['width'] - fit_width) < 1
                page.locator('#read').click()
                assert page.locator('#zoomstatus').inner_text() == '100%'
                assert abs(inner.bounding_box()['width'] - section.locator('svg').evaluate('(s)=>s.viewBox.baseVal.width')) < 1
                # Check every label against its node's shape bounds at readable size.
                clipped = section.locator('svg').evaluate('''(svg)=>[...svg.querySelectorAll('g.node')].flatMap(n=>{
                    const shape=n.querySelector('path,polygon,ellipse').getBBox();
                    return [...n.querySelectorAll('text')].filter(t=>{
                        const b=t.getBBox(), slack=1;
                        return b.x<shape.x-slack || b.y<shape.y-slack || b.x+b.width>shape.x+shape.width+slack || b.y+b.height>shape.y+shape.height+slack;
                    }).map(t=>t.textContent);
                })''')
                assert not clipped, f'{stem}: text outside node bounds: {clipped}'
                if width == 1440:
                    exported = context.new_page()
                    exported.set_viewport_size({'width': 2600, 'height': 1600})
                    exported.goto(f'http://127.0.0.1:{server.server_port}/maps/{stem}.svg')
                    capture(exported.locator('svg'), f'map-{stem}.png')
                    exported.close()
                # Scroll to the far corner; no node should be permanently unreachable.
                frame.evaluate('(f)=>f.scrollTo(f.scrollWidth,f.scrollHeight)')
                assert frame.evaluate('(f)=>f.scrollLeft+f.clientWidth>=f.scrollWidth-1 && f.scrollTop+f.clientHeight>=f.scrollHeight-1')
                frame.evaluate('(f)=>f.scrollTo(0,0)')
            page.locator('button[data-target="01-opening"]').focus()
            page.keyboard.press('Enter')
            assert page.locator('section[id="01-opening"]').is_visible()
            for node in ['O5', 'C6', 'R4', 'R5', 'R6']:
                details = page.locator('details').filter(has=page.locator('summary strong', has_text=f'{node} ·'))
                details.locator('summary').focus()
                page.keyboard.press('Enter')
                assert details.get_attribute('open') is not None
                if node in ['C6', 'R4', 'R6']:
                    assert 'Rashi' in details.inner_text()
                if node == 'R5':
                    assert 'Supplied bridge' in details.inner_text()
                if width == 390 and node in ['O5', 'R4', 'R5']:
                    capture(details, f'mobile-ledger-{node}.png')
                details.locator('summary').click()
            excerpt = page.locator('details').filter(has=page.locator('summary', has_text='Bava Metzia 22b:6 · Hebrew/Aramaic excerpt'))
            excerpt.locator('summary').click()
            assert excerpt.locator('blockquote').evaluate('(b)=>getComputedStyle(b).direction==="rtl" && getComputedStyle(b).unicodeBidi==="isolate"')
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            if width == 390:
                capture(excerpt, 'mobile-hebrew.png')
            excerpt.locator('summary').click()
        report['checks'].extend(['All four tabs, node counts, keyboard activation and ledger expansion', 'Fit, Read, zoom in/out, and scroll reachability at all three viewports', 'All SVG label bounding boxes inside node shape bounds', 'No page horizontal overflow; RTL isolated Hebrew and visible attribution'])
        # The same HTML must remain interactive with every network request blocked.
        offline = browser.new_context(offline=True, viewport={'width': 1440, 'height': 1000})
        offline_page = offline.new_page()
        offline_page.on('pageerror', lambda error: errors.append(str(error)))
        offline_page.on('request', lambda request: external.append(request.url))
        offline_page.set_content((ROOT / 'index.html').read_text())
        for stem in ['01-opening', '02-coins', '03-river', 'overview']:
            offline_page.locator(f'button[data-target="{stem}"]').click()
            assert offline_page.locator(f'section[id="{stem}"]').is_visible()
            offline_page.locator('#in').click()
            offline_page.locator('#fit').click()
        offline_page.locator('details summary').first.click()
        assert offline_page.locator('details').first.get_attribute('open') is not None
        assert not errors, errors
        assert not external, external
        report['checks'].append('Identical HTML works with network disabled; zero external requests and zero page errors')
        report['status'] = 'passed'
        (OUT / 'browser-report.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps(report, indent=2))
        browser.close()
finally:
    server.shutdown()
    server.server_close()
