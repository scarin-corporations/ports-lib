# Contribuir

Para indicar um projeto, abra uma issue com URL GitHub, jogo, console de origem, tipo de projeto e links que comprovem sistemas suportados. Propostas podem ser incompletas; devem permanecer candidatas.

A página [Jogos](https://scarin-corporations.github.io/ports-lib/web/games.html) lista projetos ligados a cada título. Os estados são declarações dos repositórios e não indicam teste independente. O assistente de revisão atualiza `data/review-report.json` com dados públicos, compatibilidade mencionada e trechos de evidência do README; todas as recomendações ficam pendentes para uma pessoa. Ele não baixa nem executa código e não aprova compatibilidade.

Para revisar, edite `data/curation.json`, adicionando em `projects`:

```json
{"name":"owner/repository","kind":"recompilation","consoles":["PS3"],"platforms":["Linux"],"evidence":"https://github.com/owner/repository#documentation"}
```

O exemplo é um formato, não uma indicação real. Tipos: `port`, `recompilation`, `emulator`. Registre somente capacidades explicitamente documentadas. Windows não implica Linux ou macOS. Não marque um projeto como jogável só porque compila. Adicione nomes a `excluded` para excluir resultados irrelevantes. Não envie ROMs, chaves, firmware ou downloads de jogos.

Rode testes e coleta antes do PR. Falhas de API devem ser relatadas, não ocultadas. Para mudanças no frontend, verifique busca, filtros, estados vazio/erro e layout móvel. Atualize `data/games.json` apenas com links e evidências para a associação jogo/projeto. Atualize a memória quando mudar critérios ou arquitetura.
