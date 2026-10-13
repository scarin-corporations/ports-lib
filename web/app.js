const ids = ['search', 'console', 'platform', 'kind', 'sort'];
const controls = Object.fromEntries(ids.map(id => [id, document.getElementById(id)]));
let projects = [];
const labels = {port: 'Port nativo', recompilation: 'Recompilação', emulator: 'Emulador', candidate: 'Candidato · não revisado'};
function element(tag, text, className) {
  const el = document.createElement(tag); el.textContent = text;
  if (className) el.className = className;
  return el;
}
function render() {
  const term = controls.search.value.toLowerCase();
  const filtered = projects.filter(p => `${p.name} ${p.description}`.toLowerCase().includes(term)
    && (!controls.console.value || p.consoles.includes(controls.console.value))
    && (!controls.platform.value || p.platforms.includes(controls.platform.value))
    && (!controls.kind.value || p.kind === controls.kind.value));
  const key = controls.sort.value;
  filtered.sort((a, b) => key === 'pushedAt' ? b[key].localeCompare(a[key]) : b[key] - a[key]);
  const grid = document.getElementById('projects'); grid.replaceChildren();
  document.getElementById('count').textContent = `${filtered.length} projetos`;
  for (const p of filtered) {
    const card = element('article', '', 'card');
    card.append(element('div', labels[p.kind] || 'Candidato', 'badge'));
    const link = element('a', p.name); link.href = p.url; link.rel = 'noopener noreferrer'; link.target = '_blank';
    const title = element('h3', ''); title.append(link); card.append(title);
    card.append(element('p', p.description || 'Descrição não informada.'));
    card.append(element('div', [...p.consoles, ...p.platforms].join(' · ') || 'Compatibilidade não revisada', 'meta'));
    card.append(element('div', `★ ${p.stars.toLocaleString('pt-BR')} · Último push ${new Date(p.pushedAt).toLocaleDateString('pt-BR')}`, 'meta'));
    card.append(element('div', `${p.archived ? 'Arquivado · ' : ''}Licença: ${p.license || 'não informada'}`, 'meta'));
    grid.append(card);
  }
  if (!filtered.length) grid.append(element('p', projects.length ? 'Nenhum projeto para estes filtros.' : 'O catálogo ainda não tem projetos. Execute a sincronização ou contribua com uma indicação.'));
}
ids.forEach(id => controls[id].addEventListener('input', render));
try {
  const response = await fetch('../data/catalog.json');
  if (!response.ok) throw new Error('HTTP ' + response.status);
  const catalog = await response.json(); projects = catalog.projects;
  document.getElementById('status').textContent = `${catalog.updatedAt ? 'Última coleta: ' + new Date(catalog.updatedAt).toLocaleString('pt-BR') : 'Primeira coleta pendente'}${catalog.discovery.status === 'partial' || catalog.discovery.status === 'failed' ? ' · Coleta com falhas; dados anteriores preservados' : ''}`;
  render();
} catch {
  document.getElementById('status').textContent = 'Não foi possível carregar o catálogo. Tente novamente.';
}
