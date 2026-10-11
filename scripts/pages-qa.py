"""Check the deployed static viewer and its exact assets at an explicit base URL."""
import argparse
import hashlib
import io
import json
from pathlib import Path
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--url', required=True)
parser.add_argument('--browser', default='/usr/bin/chromium')
args = parser.parse_args()
base_url = args.url.rstrip('/') + '/'
OUT = ROOT / 'output/pages-qa'
OUT.mkdir(parents=True, exist_ok=True)
specs = json.loads((ROOT / 'docs/build-report.json').read_text())
report = {'url': base_url, 'viewports': [], 'assets': [], 'errors': []}
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=args.browser, args=['--no-sandbox'])
    context = browser.new_context()
    page = context.new_page()
    page.on('pageerror', lambda error: report['errors'].append(str(error)))
    response = page.goto(base_url)
    assert response and response.status == 200
    assert page.locator('h1').inner_text() == 'Before awareness.'
    for width, height in [(1440, 1000), (390, 844), (320, 740)]:
        page.set_viewport_size({'width': width, 'height': height})
        page.evaluate('window.scrollTo(0,0)')
        page.screenshot(path=str(OUT / f'header-{width}.png'))
        for spec in specs:
            stem = spec['file'].removesuffix('.argdown')
            page.locator(f'button[data-target="{stem}"]').click()
            section = page.locator(f'section[id="{stem}"]')
            assert section.is_visible() and page.locator('.episode:visible').count() == 1
            assert section.locator('g.node').count() == spec['nodes']
            page.locator('#fit').click()
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            if width == 390:
                section.screenshot(path=str(OUT / f'mobile-{stem}.png'))
        report['viewports'].append([width, height])
    paths = [f"maps/{s['file'].removesuffix('.argdown')}.svg" for s in specs]
    pdf_link = page.get_by_role('link', name='Download the 15-page PDF')
    assert pdf_link.count() == 1
    paths.append(pdf_link.get_attribute('href'))
    for path in paths:
        asset = context.request.get(urljoin(base_url, path))
        assert asset.status == 200, f'{path}: HTTP {asset.status}'
        data = asset.body()
        digest = hashlib.sha256(data).hexdigest()
        assert digest == hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), f'{path}: differs from local release'
        if path.endswith('.pdf'):
            assert len(PdfReader(io.BytesIO(data)).pages) == 15
        report['assets'].append({'path': path, 'status': asset.status, 'sha256': digest})
    assert not report['errors'], report['errors']
    report['status'] = 'passed'
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    browser.close()
