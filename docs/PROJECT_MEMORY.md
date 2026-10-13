# Memória do projeto

## Objetivo e escopo — 2026-10-13

Solicitação: biblioteca viva que encontra e prioriza projetos GitHub relacionados a ports de jogos PS3/PS4/Xbox para PC, macOS e Linux, permitindo continuidade por contribuidores.

Decisões: começar com app web em vez de extensão; Python sem dependências para coleta; frontend estático; GitHub Actions a cada seis horas e GitHub Pages. Usar estrelas e atividade, pois tráfego de terceiros não é público. Não afirmar que resultados de busca são ports. Revisão humana confirma tipo e plataformas com evidência. Emuladores ficam separados.

## Estado

MVP implementado: descoberta limitada por consultas, metadados, ranking, filtros, curadoria, preservação em falhas, testes e publicação declarativa. Ativação externa depende de enviar arquivos ao GitHub e habilitar Pages/Actions. A validação real da API e os resultados de testes devem ser reportados na entrega, sem assumir implantação.

Validação local: testes automatizados de ranking, candidatura sem compatibilidade inventada, preservação em falha e coleta com revisão/exclusões. HTTP do app e do JSON respondem. A API real foi bloqueada pelo proxy com 403; `api.github.com` e instruções de startup foram salvos no rascunho cloud, mas salvar não aplica nem publica. Catálogo inicial vazio, sem exemplos fictícios. Ainda não foi realizado teste de navegador ou execução do workflow hospedado.

## Próximas etapas

1. Revisar candidatos e incluir evidências, jogo e estado de jogabilidade.
2. Histórico diário de estrelas para tendência real, não apenas popularidade acumulada.
3. Validar schema de curadoria e automatizar PRs de revisão.
4. Paginação com orçamento de API, políticas de remoção e metadados de releases.
5. Testes de navegador e acessibilidade; internacionalização.

## Critérios de conclusão

Testes passando; falhas de rede preservam catálogo; candidaturas claramente identificadas; nenhum segredo no cliente; reprodução documentada. Descoberta não promete cobertura total nem compatibilidade testada. Atualize este documento a cada decisão duradoura; registre limitações e evite depender do histórico do chat.
