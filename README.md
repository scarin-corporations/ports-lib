# Ports Lib

Living library of projects bringing console games to computers. The interface is available in Portuguese and English, with search, console/platform/type filters, and ranking by stars and activity. This index links to code and documentation; it does not host games.

## Live catalog and star chart

<!-- BEGIN LIVE CATALOG -->
<p><a href="https://scarin-corporations.github.io/ports-lib/">Open the Ports Lib app →</a></p>

![Top 10 repositories by GitHub stars](data/top-stars.svg)

| # | Repository | Stars | Last push | Status |
|---:|---|---:|---|---|
| 1 | [hedge-dev/UnleashedRecomp](https://github.com/hedge-dev/UnleashedRecomp) | 5,163 | 2026-06-29 | Candidate |
| 2 | [ran-j/PS2Recomp](https://github.com/ran-j/PS2Recomp) | 3,416 | 2026-10-10 | Candidate |
| 3 | [ammaarreshi/Generals-Mac-iOS-iPad](https://github.com/ammaarreshi/Generals-Mac-iOS-iPad) | 1,668 | 2026-07-05 | Candidate |
| 4 | [LoreanXavier/pt-pc](https://github.com/LoreanXavier/pt-pc) | 1,626 | 2026-10-12 | Candidate |
| 5 | [jhaizhou-ops/d2r-mobile](https://github.com/jhaizhou-ops/d2r-mobile) | 1,050 | 2026-10-13 | Candidate |
| 6 | [rexglue/rexglue-sdk](https://github.com/rexglue/rexglue-sdk) | 1,049 | 2026-10-02 | Candidate |
| 7 | [Sebastrion/awesome-unofficial-pc-ports](https://github.com/Sebastrion/awesome-unofficial-pc-ports) | 877 | 2026-10-07 | Candidate |
| 8 | [SlickAmogus/silent-hill-decomp](https://github.com/SlickAmogus/silent-hill-decomp) | 670 | 2026-10-13 | Candidate |
| 9 | [sonicnext-dev/MarathonRecomp](https://github.com/sonicnext-dev/MarathonRecomp) | 663 | 2026-10-13 | Candidate |
| 10 | [arcanite24/pinyon-shift](https://github.com/arcanite24/pinyon-shift) | 461 | 2026-10-13 | Candidate |
<!-- END LIVE CATALOG -->

## Development

Requer Python 3.12+. Sem dependências externas.

```sh
python -m unittest discover -s tests -v
python scripts/sync.py && python scripts/update_readme.py
python -m http.server 8000 --bind 0.0.0.0
```

Open `/web/` on the local server. Discovery uses `api.github.com`, takes about a minute, and returns an error if any query fails. `GITHUB_TOKEN` is optional locally and recommended for higher rate limits; configure it in the environment, never in source files. GitHub Actions uses its automatic token.

## Atualização e publicação

The workflow runs every six hours, manually, and on pushes to `main`. It tests, collects metadata, and commits the catalog. For the website, an organization owner must enable **Settings → Pages → Build and deployment → Source: GitHub Actions**. Until Pages is enabled, catalog updates continue and deployment is skipped. The schedule runs on the default branch and can be delayed or disabled by GitHub after inactivity. Branch protection must allow bot commits or a future pull-request strategy.

Search is limited to 30 results per query, without pagination, so this MVP does not cover all of GitHub. Failed syncs preserve old data. Push dates indicate code activity, not a playable release. This version does not track star growth over time.

## Ranking and curation

`score = 20 × log10(stars + 1) + 30 × exp(-diasDesdePush / 180)`.

Public metadata includes stars, description, last push, license, and archive status. Traffic is unavailable for third-party repositories. Popularity does not prove quality. Automatically discovered projects remain **candidates** until reviewed; console and platform support must have evidence.

See [CONTRIBUTING.md](CONTRIBUTING.md), [project memory](docs/PROJECT_MEMORY.md), and [architecture](docs/ARCHITECTURE.md).

## Sponsorship

The repository funding link is prepared. Organization enrollment and payout approval are required before the Sponsor button can accept contributions; see [sponsorship setup](docs/SPONSORSHIP.md).
