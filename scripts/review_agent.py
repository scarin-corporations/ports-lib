"""Collect public README evidence for mapped games; never auto-approve projects."""
import base64
import json
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from sync import github

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = re.compile(r'\b(status|playable|gameplay|loading|windows|linux|macos|android|release|stable|alpha|experimental|compatib|tested|not intended)\b', re.I)
PLATFORMS = {
    'Windows': re.compile(r'\bwindows\b', re.I),
    'Linux': re.compile(r'\blinux\b|steam deck|steamos', re.I),
    'macOS': re.compile(r'\bmacos\b|\bmac os\b|apple silicon', re.I),
    'Android': re.compile(r'\bandroid\b', re.I),
}


def snippets(text):
    lines = [re.sub(r'\s+', ' ', line).strip(' #-*>') for line in text.splitlines()]
    return [line[:240] for line in lines if EVIDENCE.search(line)][:8]


def review(root=ROOT):
    games = json.loads((root / 'data/games.json').read_text())['games']
    report = []
    failures = 0
    seen = set()
    for game in games:
        for project in game['projects']:
            name = project['name']
            if name.lower() in seen:
                continue
            seen.add(name.lower())
            entry = dict(name=name, game=game['title'], recommendation='needs-human-review',
                         approved=False, evidence_url=project['evidence'])
            try:
                repo = github('/repos/' + name)
                readme = github('/repos/' + name + '/readme')
                if readme.get('encoding') == 'base64':
                    content = base64.b64decode(readme['content']).decode('utf-8', 'replace')
                else:
                    content = readme.get('content', '')
                entry.update(exists=True, archived=repo['archived'], stars=repo['stargazers_count'],
                             pushedAt=repo['pushed_at'], license=(repo.get('license') or {}).get('spdx_id'),
                             platforms_mentioned=[p for p, pattern in PLATFORMS.items() if pattern.search(content)],
                             title_mentioned=game['title'].casefold() in content.casefold(),
                             evidence=snippets(content[:30000]),
                             note='README evidence only; compatibility and playability are not tested by this agent.')
            except Exception as exc:
                failures += 1
                entry.update(exists=None, error=type(exc).__name__, evidence=[],
                             note='Could not verify this project automatically; human review required.')
            report.append(entry)
    output = dict(generatedAt=datetime.now(timezone.utc).isoformat(),
                  reviewed=len(report), requiringHumanReview=len(report), failures=failures,
                  policy='This assistant gathers repository metadata and README evidence. It never approves a game, confirms compatibility, or runs downloaded code.',
                  projects=report)
    target = root / 'data/review-report.json'
    with tempfile.NamedTemporaryFile(mode='w', dir=target.parent, delete=False) as handle:
        json.dump(output, handle, ensure_ascii=False, indent=2)
        temporary = handle.name
    Path(temporary).replace(target)
    print(f"Review assistant: {len(report)} projects, {failures} fetch errors; all remain for human review")
    return 0


if __name__ == '__main__':
    raise SystemExit(review())
