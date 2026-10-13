import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError
from scripts.sync import normalize, score, sync


class SyncTests(unittest.TestCase):
    def test_ranking_rewards_popularity_and_activity(self):
        now = datetime(2026, 10, 13, tzinfo=timezone.utc)
        self.assertGreater(score(1000, '2026-10-12T00:00:00Z', now), score(10, '2026-10-12T00:00:00Z', now))
        self.assertGreater(score(1000, '2026-10-12T00:00:00Z', now), score(1000, '2020-01-01T00:00:00Z', now))

    def test_discovery_does_not_invent_compatibility(self):
        repo = dict(full_name='a/b', html_url='https://github.com/a/b',
                    stargazers_count=5, pushed_at='2026-10-12T00:00:00Z', archived=False)
        project = normalize(repo)
        self.assertFalse(project['reviewed'])
        self.assertEqual(project['platforms'], [])
        self.assertEqual(project['kind'], 'candidate')

    def test_network_failure_preserves_catalog_and_timestamp(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'data').mkdir()
            (root / 'data/curation.json').write_text(json.dumps(dict(projects=[], excluded=[], queries=['test'])))
            project = normalize(dict(full_name='a/b', html_url='https://github.com/a/b',
                                     stargazers_count=5, pushed_at='2026-10-12T00:00:00Z', archived=False))
            (root / 'data/catalog.json').write_text(json.dumps(dict(updatedAt='old', projects=[project])))
            with patch('scripts.sync.github', side_effect=URLError('blocked')), patch('scripts.sync.time.sleep'):
                self.assertEqual(sync(root), 1)
            result = json.loads((root / 'data/catalog.json').read_text())
            self.assertEqual(result['updatedAt'], 'old')
            self.assertEqual(result['projects'][0]['name'], 'a/b')
            self.assertEqual(result['discovery']['status'], 'failed')

    def test_success_merges_curated_and_discovered_and_excludes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'data').mkdir()
            review = dict(name='a/b', kind='port', consoles=['PS3'], platforms=['Linux'], evidence='https://github.com/a/b')
            (root / 'data/curation.json').write_text(json.dumps(dict(projects=[review], excluded=['a/excluded'], queries=[dict(q='test', sort='stars')])))
            (root / 'data/catalog.json').write_text(json.dumps(dict(updatedAt=None, projects=[])))
            def repo(name):
                return dict(full_name=name, html_url='https://github.com/' + name,
                            stargazers_count=10, pushed_at='2026-10-12T00:00:00Z', archived=False)
            with patch('scripts.sync.github', side_effect=[repo('a/b'), {'items': [repo('a/b'), repo('a/new'), repo('a/excluded')], 'total_count': 3}]), patch('scripts.sync.time.sleep'):
                self.assertEqual(sync(root), 0)
            result = json.loads((root / 'data/catalog.json').read_text())
            projects = {p['name']: p for p in result['projects']}
            self.assertEqual(set(projects), {'a/b', 'a/new'})
            self.assertEqual(projects['a/b']['platforms'], ['Linux'])
            self.assertTrue(projects['a/b']['reviewed'])
            self.assertFalse(projects['a/new']['reviewed'])
            self.assertEqual(result['discovery']['candidates'], 1)
            self.assertEqual(result['discovery']['status'], 'ok')

    def test_search_paginates_past_first_hundred_results(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'data').mkdir()
            (root / 'data/curation.json').write_text(json.dumps(dict(projects=[], excluded=[], queries=[dict(q='test', sort='stars')])))
            (root / 'data/catalog.json').write_text(json.dumps(dict(updatedAt=None, projects=[])))
            def repo(index):
                name = f'a/game-{index}'
                return dict(full_name=name, html_url='https://github.com/' + name,
                            stargazers_count=index, pushed_at='2026-10-12T00:00:00Z', archived=False)
            first_page = {'items': [repo(index) for index in range(100)], 'total_count': 101}
            second_page = {'items': [repo(100)], 'total_count': 101}
            with patch('scripts.sync.github', side_effect=[first_page, second_page]) as github, patch('scripts.sync.time.sleep'):
                self.assertEqual(sync(root), 0)
            result = json.loads((root / 'data/catalog.json').read_text())
            self.assertEqual(len(result['projects']), 101)
            self.assertEqual(result['discovery']['searches'][0]['pages'], 2)
            self.assertEqual(result['discovery']['cappedQueries'], [])
            self.assertEqual(github.call_count, 2)


if __name__ == '__main__':
    unittest.main()
