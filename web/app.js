const translations = {
  'pt-BR': {
    languageLabel: 'Idioma', contribute: 'Contribuir ↗', eyebrow: 'DESCOBERTA OPEN SOURCE', searchAria: 'Buscar repositórios', consoleAria: 'Console', platformAria: 'Plataforma', kindAria: 'Tipo', sortAria: 'Ordenação',
    hero: 'Jogos, além do console.', intro: 'Explore projetos que levam jogos de console ao computador. Comunidade, código aberto e novas possibilidades.',
    loading: 'Carregando catálogo…', filters: 'Filtros', search: 'Buscar jogo, projeto ou descrição…', allConsoles: 'Todos os consoles',
    allPlatforms: 'Todas as plataformas', allTypes: 'Todos os tipos', nativePort: 'Port nativo', recompilation: 'Recompilação',
    emulator: 'Emulador', candidate: 'Candidato', relevance: 'Relevância', mostStars: 'Mais estrelas', recentActivity: 'Atividade recente',
    explore: 'Explore a biblioteca', note: 'Candidatos são resultados automáticos, ainda sem revisão. Plataformas e consoles só são confirmados com evidências. Emuladores aparecem como categoria própria.',
    repositories: 'Repositórios', footer: 'Índice de código e metadados. Sem ROMs, firmware ou arquivos de jogos. Estrelas não garantem qualidade ou compatibilidade.',
    count: n => `${n} projetos`, unknownDescription: 'Descrição não informada.', unknownCompatibility: 'Compatibilidade não revisada',
    lastPush: 'Último push', noMatches: 'Nenhum projeto para estes filtros.', empty: 'O catálogo ainda não tem projetos. Execute a sincronização ou contribua com uma indicação.',
    archived: 'Arquivado', license: 'Licença', unknown: 'não informada', refreshed: 'Última coleta', pending: 'Primeira coleta pendente',
    stale: 'Coleta com falhas; dados anteriores preservados', loadError: 'Não foi possível carregar o catálogo. Tente novamente.',
    kinds: {port: 'Port nativo', recompilation: 'Recompilação', emulator: 'Emulador', candidate: 'Candidato · não revisado'}
  },
  en: {
    languageLabel: 'Language', contribute: 'Contribute ↗', eyebrow: 'OPEN SOURCE DISCOVERY', searchAria: 'Search repositories', consoleAria: 'Console', platformAria: 'Platform', kindAria: 'Type', sortAria: 'Sort order',
    hero: 'Games beyond the console.', intro: 'Explore projects bringing console games to computers. Community, open source, and new possibilities.',
    loading: 'Loading catalog…', filters: 'Filters', search: 'Search games, projects, or descriptions…', allConsoles: 'All consoles',
    allPlatforms: 'All platforms', allTypes: 'All types', nativePort: 'Native port', recompilation: 'Recompilation',
    emulator: 'Emulator', candidate: 'Candidate', relevance: 'Relevance', mostStars: 'Most stars', recentActivity: 'Recent activity',
    explore: 'Explore the library', note: 'Candidates are automatically discovered and have not been reviewed. Platforms and consoles are confirmed only when supported by evidence. Emulators are listed separately.',
    repositories: 'Repositories', footer: 'Code and metadata index. No ROMs, firmware, or game files. Stars do not guarantee quality or compatibility.',
    count: n => `${n} projects`, unknownDescription: 'No description provided.', unknownCompatibility: 'Compatibility not reviewed',
    lastPush: 'Last push', noMatches: 'No projects match these filters.', empty: 'The catalog is empty. Run a sync or suggest a project.',
    archived: 'Archived', license: 'License', unknown: 'not specified', refreshed: 'Last refreshed', pending: 'Initial sync pending',
    stale: 'Sync errors; previous data preserved', loadError: 'Could not load the catalog. Please try again.',
    kinds: {port: 'Native port', recompilation: 'Recompilation', emulator: 'Emulator', candidate: 'Candidate · unreviewed'}
  }
};
const ids = ['search', 'console', 'platform', 'kind', 'sort'];
const controls = Object.fromEntries(ids.map(id => [id, document.getElementById(id)]));
const languageControl = document.getElementById('language');
let locale = localStorage.getItem('ports-lib-language') === 'en' ? 'en' : 'pt-BR';
let projects = [];
let catalogState = null;
let catalogFailed = false;
const t = () => translations[locale];
function applyLocale() {
  locale = languageControl.value;
  localStorage.setItem('ports-lib-language', locale);
  document.documentElement.lang = locale;
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    if (t()[key]) el.textContent = t()[key];
  });
  document.querySelectorAll('[data-i18n-aria]').forEach(el => el.setAttribute('aria-label', t()[el.dataset.i18nAria]));
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => el.placeholder = t()[el.dataset.i18nPlaceholder]);
  document.title = locale === 'en' ? 'Ports Lib — Games beyond the console' : 'Ports Lib — Jogos, além do console';
  updateStatus();
  render();
}
function updateStatus() {
  const status = document.getElementById('status');
  if (catalogFailed) status.textContent = t().loadError;
  else if (!catalogState) status.textContent = t().loading;
  else {
    const updated = catalogState.updatedAt ? `${t().refreshed}: ${new Date(catalogState.updatedAt).toLocaleString(locale)}` : t().pending;
    status.textContent = `${updated}${catalogState.discovery.status === 'partial' || catalogState.discovery.status === 'failed' ? ' · ' + t().stale : ''}`;
  }
}
function element(tag, text, className) {
  const el = document.createElement(tag); el.textContent = text;
  if (className) el.className = className;
  return el;
}
function render() {
  if (!projects) return;
  const term = controls.search.value.toLowerCase();
  const filtered = projects.filter(p => `${p.name} ${p.description}`.toLowerCase().includes(term)
    && (!controls.console.value || p.consoles.includes(controls.console.value))
    && (!controls.platform.value || p.platforms.includes(controls.platform.value))
    && (!controls.kind.value || p.kind === controls.kind.value));
  const key = controls.sort.value;
  filtered.sort((a, b) => key === 'pushedAt' ? b[key].localeCompare(a[key]) : b[key] - a[key]);
  const grid = document.getElementById('projects'); grid.replaceChildren();
  document.getElementById('count').textContent = t().count(filtered.length);
  for (const p of filtered) {
    const card = element('article', '', 'card');
    card.append(element('div', t().kinds[p.kind] || t().kinds.candidate, 'badge'));
    const link = element('a', p.name); link.href = p.url; link.rel = 'noopener noreferrer'; link.target = '_blank';
    const title = element('h3', ''); title.append(link); card.append(title);
    card.append(element('p', p.description || t().unknownDescription));
    card.append(element('div', [...p.consoles, ...p.platforms].join(' · ') || t().unknownCompatibility, 'meta'));
    card.append(element('div', `★ ${p.stars.toLocaleString(locale)} · ${t().lastPush} ${new Date(p.pushedAt).toLocaleDateString(locale)}`, 'meta'));
    card.append(element('div', `${p.archived ? t().archived + ' · ' : ''}${t().license}: ${p.license || t().unknown}`, 'meta'));
    grid.append(card);
  }
  if (!filtered.length) grid.append(element('p', projects.length ? t().noMatches : t().empty));
}
ids.forEach(id => controls[id].addEventListener('input', render));
languageControl.value = locale;
languageControl.addEventListener('change', applyLocale);
applyLocale();
try {
  const response = await fetch('../data/catalog.json');
  if (!response.ok) throw new Error('HTTP ' + response.status);
  catalogState = await response.json(); projects = catalogState.projects;
  updateStatus();
  render();
} catch {
  catalogFailed = true;
  updateStatus();
}
