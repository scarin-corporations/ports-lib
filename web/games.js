const words = {
  'pt-BR': {home:'Início',languageLabel:'Idioma',eyebrow:'BIBLIOTECA DE JOGOS',hero:'Jogos e projetos.',intro:'Encontre projetos por jogo e veja o estado informado pelos próprios repositórios.',loading:'Carregando catálogo…',search:'Buscar jogos…',allConsoles:'Todos os consoles',allStates:'Todos os estados',playable:'Jogável informado',preview:'Prévia / teste',experimental:'Experimental',early:'Em desenvolvimento',alpha:'Alfa',released:'Versão publicada',notFound:'Projeto não encontrado',games:'Jogos mapeados',caveat:'Os estados e plataformas são declarações nos READMEs dos projetos. O Ports Lib não baixa nem testa jogos.',footer:'Não incluímos arquivos de jogos, ROMs ou firmware. Use apenas cópias obtidas legalmente.',count:n=>`${n} jogos`,projects:n=>`${n} projetos`,repo:'Abrir repositório ↗',evidence:'Ver evidência ↗',stars:'estrelas',lastPush:'último push',none:'Nenhum jogo encontrado para estes filtros.',error:'Não foi possível carregar os jogos. Tente novamente.',needsReview:'Estado declarado pelo projeto; ainda requer revisão da comunidade.',noRepo:'Ainda não há um repositório correspondente no catálogo.',stateNames:{playable:'Jogável informado',preview:'Prévia / teste',experimental:'Experimental',early:'Em desenvolvimento',alpha:'Alfa',released:'Versão publicada','not-found':'Projeto não encontrado'}},
  en: {home:'Home',languageLabel:'Language',eyebrow:'GAME LIBRARY',hero:'Games and projects.',intro:'Browse projects by game and see the status reported by their repositories.',loading:'Loading catalog…',search:'Search games…',allConsoles:'All consoles',allStates:'All statuses',playable:'Reported playable',preview:'Preview / test build',experimental:'Experimental',early:'In development',alpha:'Alpha',released:'Release available',notFound:'No project found',games:'Mapped games',caveat:'Statuses and platforms are claims in project READMEs. Ports Lib does not download or test games.',footer:'We do not include game files, ROMs, or firmware. Use only legally obtained copies.',count:n=>`${n} games`,projects:n=>`${n} projects`,repo:'Open repository ↗',evidence:'View evidence ↗',stars:'stars',lastPush:'last push',none:'No games match these filters.',error:'Could not load the game list. Please try again.',needsReview:'Status claimed by the project; community review is still needed.',noRepo:'No matching repository is in the catalog yet.',stateNames:{playable:'Reported playable',preview:'Preview / test build',experimental:'Experimental',early:'In development',alpha:'Alpha',released:'Release available','not-found':'No project found'}}
};
const lang=document.getElementById('language'), search=document.getElementById('search'), consoleFilter=document.getElementById('console'), stateFilter=document.getElementById('state');
let locale=localStorage.getItem('ports-lib-language')==='en'?'en':'pt-BR', games=[], projects=new Map(), catalogState=null;
const t=()=>words[locale];
function el(tag,text,cls){const e=document.createElement(tag);e.textContent=text;if(cls)e.className=cls;return e;}
function draw(){
 const term=search.value.toLocaleLowerCase(locale), list=games.filter(g=>(`${g.title} ${g.console}`).toLocaleLowerCase(locale).includes(term)&&(!consoleFilter.value||g.console===consoleFilter.value)&&(!stateFilter.value||g.status===stateFilter.value));
 const root=document.getElementById('games');root.replaceChildren();document.getElementById('count').textContent=t().count(list.length);
 for(const game of list){
  const card=el('article','','card game-card');
  card.append(el('div',`${game.year} · ${game.console}`,'badge'));
  card.append(el('h3',game.title));
  card.append(el('p',locale==='en'?game.summary:game.summaryPt));
  card.append(el('div',t().stateNames[game.status]||t().stateNames.experimental,'status-tag'));
  if(game.projects.length){
   card.append(el('div',t().projects(game.projects.length),'project-count'));
   for(const item of game.projects){
    const detail=el('div','','game-project');const repo=projects.get(item.name.toLowerCase());
    const link=el('a',item.name);link.href=repo?.url||`https://github.com/${item.name}`;link.target='_blank';link.rel='noopener noreferrer';detail.append(link);
    detail.append(el('p',locale==='en'?item.state:item.statePt));
    if(repo)detail.append(el('div',`★ ${repo.stars.toLocaleString(locale)} · ${t().lastPush} ${new Date(repo.pushedAt).toLocaleDateString(locale)}`,'meta'));
    const evidence=el('a',t().evidence);evidence.href=item.evidence;evidence.target='_blank';evidence.rel='noopener noreferrer';evidence.className='evidence';detail.append(evidence);card.append(detail);
   }
  }else card.append(el('p',t().noRepo,'meta'));
  root.append(card);
 }
 if(!list.length)root.append(el('p',t().none));
}
function localeChange(){locale=lang.value;localStorage.setItem('ports-lib-language',locale);document.documentElement.lang=locale;document.title=locale==='en'?'Ports Lib — Games':'Ports Lib — Jogos';document.querySelectorAll('[data-i18n]').forEach(e=>e.textContent=t()[e.dataset.i18n]);search.placeholder=t().search;if(catalogState)showCatalogStatus();draw();}
function showCatalogStatus(){document.getElementById('status').textContent=`${catalogState.projects.length} ${locale==='en'?'repositories indexed':'repositórios indexados'} · ${new Date(catalogState.updatedAt).toLocaleString(locale)}`;}
lang.value=locale;lang.addEventListener('change',localeChange);search.addEventListener('input',draw);consoleFilter.addEventListener('change',draw);stateFilter.addEventListener('change',draw);localeChange();
try{
 const [g,c]=await Promise.all([fetch('../data/games.json'),fetch('../data/catalog.json')]);if(!g.ok||!c.ok)throw Error('catalog unavailable');
 games=(await g.json()).games;catalogState=await c.json();projects=new Map(catalogState.projects.map(p=>[p.name.toLowerCase(),p]));
 showCatalogStatus();draw();
}catch{document.getElementById('status').textContent=t().error;}
