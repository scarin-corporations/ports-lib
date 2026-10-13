# Memória do projeto

## Objetivo e escopo — 2026-10-13

Solicitação: biblioteca viva que encontra e prioriza projetos GitHub relacionados a ports de jogos PS3/PS4/Xbox para PC, macOS e Linux, permitindo continuidade por contribuidores.

Decisões: começar com app web em vez de extensão; Python sem dependências para coleta; frontend estático; GitHub Actions a cada seis horas e GitHub Pages. Usar estrelas e atividade, pois tráfego de terceiros não é público. Não afirmar que resultados de busca são ports. Revisão humana confirma tipo e plataformas com evidência. Emuladores ficam separados.

## Estado

MVP implementado: descoberta limitada por consultas, metadados, ranking, filtros, curadoria, preservação em falhas, testes e publicação declarativa. Ativação externa depende de enviar arquivos ao GitHub e habilitar Pages/Actions. A validação real da API e os resultados de testes devem ser reportados na entrega, sem assumir implantação.

Validação local: testes automatizados de ranking, candidatura sem compatibilidade inventada, preservação em falha e coleta com revisão/exclusões. A API real respondeu e o workflow gerou 154 candidatos com zero erros. O workflow de dados passou; Pages ainda não foi habilitado porque o token automático recebeu `Resource not accessible by integration` ao chamar a API de criação de site. Não foi realizado teste de navegador.

## Acesso global e financiamento — 2026-10-13

Interface disponível em português brasileiro e inglês. Idioma fica salvo no navegador; descrições de projetos continuam na língua original do repositório. Não adicionar outra língua sem solicitação explícita.

`.github/FUNDING.yml` aponta para a organização do projeto e `docs/SPONSORSHIP.md` documenta a ativação. A organização ainda precisa concluir inscrição, elegibilidade, dados fiscais/financeiros e aprovação no GitHub Sponsors. Não anunciar recebimento ativo antes de a página pública oferecer tiers.

O token padrão de GitHub Actions não pôde criar Pages via API. O workflow segue coletando e salvando o catálogo e pula deploy quando Pages não está habilitado; um owner deve habilitar Pages em Settings → Pages → GitHub Actions.

## Próximas etapas

1. Revisar candidatos e incluir evidências, jogo e estado de jogabilidade.
2. Histórico diário de estrelas para tendência real, não apenas popularidade acumulada.
3. Validar schema de curadoria e automatizar PRs de revisão.
4. Paginação com orçamento de API, políticas de remoção e metadados de releases.
5. Testes de navegador e acessibilidade; traduções adicionais somente mediante solicitação.

## Critérios de conclusão

Testes passando; falhas de rede preservam catálogo; candidaturas claramente identificadas; nenhum segredo no cliente; reprodução documentada. Descoberta não promete cobertura total nem compatibilidade testada. Atualize este documento a cada decisão duradoura; registre limitações e evite depender do histórico do chat.
