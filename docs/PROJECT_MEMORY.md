# Memória do projeto

## Objetivo e escopo — 2026-10-13

Solicitação: biblioteca viva que encontra e prioriza projetos GitHub relacionados a ports de jogos PS3/PS4/Xbox para PC, macOS e Linux, permitindo continuidade por contribuidores.

Decisões: começar com app web em vez de extensão; Python sem dependências para coleta; frontend estático; GitHub Actions a cada seis horas e GitHub Pages. Usar estrelas e atividade, pois tráfego de terceiros não é público. Não afirmar que resultados de busca são ports. Revisão humana confirma tipo e plataformas com evidência. Emuladores ficam separados.

## Estado

O catálogo pesquisa termos alternativos por console, ordenação por popularidade e data recente, pagina resultados até o limite da API, salva os dados e atualiza o gráfico/tabela do README. A coleta de 2026-10-13 encontrou 651 repositórios únicos em 25 consultas, sem consultas truncadas nem erros; 640 são candidatos de busca ainda não revisados e 11 estão ligados manualmente à página `web/games.html`. As afirmações de compatibilidade vêm dos READMEs externos e não são testes do Ports Lib.

O assistente `scripts/review_agent.py` coleta README/metadados dos projetos mapeados, extrai sinais e trechos para revisão. Sua recomendação é sempre `needs-human-review`; não aprova automaticamente, não executa código dos repositórios e não confirma que um jogo funciona. `data/curation.json` continua sendo a curadoria humana e `data/games.json` a associação por título.

Validação anterior: testes automatizados de ranking, candidatura sem compatibilidade inventada, preservação em falha e coleta com revisão/exclusões. GitHub Pages está configurado; confirmação de um deploy novo deve vir da execução e do endpoint público. A API real de coleta respondeu anteriormente e o workflow de dados completou com sucesso.

## Acesso global e financiamento — 2026-10-13

Interface disponível em português brasileiro e inglês. Idioma fica salvo no navegador; descrições de projetos continuam na língua original do repositório. Não adicionar outra língua sem solicitação explícita.

`.github/FUNDING.yml` aponta para a organização do projeto e `docs/SPONSORSHIP.md` documenta a ativação. A organização ainda precisa concluir inscrição, elegibilidade, dados fiscais/financeiros e aprovação no GitHub Sponsors. Não anunciar recebimento ativo antes de a página pública oferecer tiers.

O workflow usa `actions/configure-pages` como sinal de prontidão e pula deploy se o Pages estiver desativado. Uma repetição de um evento antigo causou push não fast-forward porque Actions fez checkout do SHA antigo; o checkout agora usa `main` mais recente para coletas não PR.

## Próximas etapas

1. Revisar candidatos, confirmar evidências, jogo e estado de jogabilidade.
2. Histórico diário de estrelas para tendência real, não apenas popularidade acumulada.
3. Validar schema de curadoria e automatizar PRs de revisão.
4. Mais consultas de descoberta com orçamento de API, políticas de remoção e metadados de releases.
5. Testes de navegador e acessibilidade; traduções adicionais somente mediante solicitação.

## Critérios de conclusão

Testes passando; falhas de rede preservam catálogo; candidaturas claramente identificadas; nenhum segredo no cliente; reprodução documentada. Descoberta não promete cobertura total nem compatibilidade testada. Atualize este documento a cada decisão duradoura; registre limitações e evite depender do histórico do chat.
