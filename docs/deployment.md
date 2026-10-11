# GitHub Pages deployment

The public [live presentation](https://ashebson.github.io/yeush-shelo-midaat-argdown/) is deployed from main/root. Repository visibility and Pages administration were completed separately; ordinary content updates require only a push.

This repository is a static site. Publish branch **main**, directory **/ (root)**. The tracked `.nojekyll` file tells GitHub Pages to serve the already-generated HTML, SVGs and PDF directly. No server, custom domain, dependency installation or paid build service is needed.

The HTML uses relative paths, so the same file works both offline and under a GitHub project-site prefix. The top of the viewer links directly to `docs/yeush-shelo-midaat.pdf`; each map has an Open SVG link.

Repository visibility and Pages configuration are GitHub settings, not effects of committing `.nojekyll`. Before making a repository public, review its full history and commit metadata as well as the current files.

With an authenticated administrator and any publication decisions resolved, configure **Settings → Pages → Deploy from a branch → main → / (root)**. Alternatively:

```sh
gh api --method POST repos/ashebson/yeush-shelo-midaat-argdown/pages \
  -f build_type=legacy -f 'source[branch]=main' -f 'source[path]=/'
gh api repos/ashebson/yeush-shelo-midaat-argdown/pages --jq '{status,html_url,source}'
gh api repos/ashebson/yeush-shelo-midaat-argdown/pages/builds/latest --jq '{status,commit,error}'
```

For an existing Pages configuration, inspect it first and use the corresponding update operation instead of creating a second configuration. The authoritative URL is `html_url` returned by GitHub; do not treat an expected URL as a verified deployment.

Once the build is successful, validate that URL:

```sh
python3 scripts/pages-qa.py --url '<html_url returned by GitHub>'
```

This checks all eleven views at desktop and mobile widths, Graph/Code keyboard interactions, exact source and actual clipboard copy, denied-clipboard fallback, exact deployed HTML, source URLs and SVG bytes, the visible PDF link and exact PDF bytes, PDF page count, page errors and horizontal overflow. Screenshots and the report go to ignored `output/pages-qa/`. Inspect the screenshots as well as the checks. A successful local preview is not evidence that GitHub Pages is live.
