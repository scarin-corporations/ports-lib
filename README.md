# Ports Lib

Biblioteca viva de projetos que levam jogos de console ao computador. Interface em português, busca, filtros de console/plataforma/tipo e ranking por estrelas e atividade. O índice referencia código e documentação; não hospeda jogos.

## Desenvolvimento

Requer Python 3.12+. Sem dependências externas.

```sh
python -m unittest discover -s tests -v
python scripts/sync.py
python -m http.server 8000 --bind 0.0.0.0
```

Abra `/web/` no servidor. A coleta usa `api.github.com`, leva cerca de um minuto e retorna erro quando alguma consulta falha. `GITHUB_TOKEN` é opcional localmente e recomendado para limites maiores; configure-o no ambiente, nunca no código. GitHub Actions usa seu token automático.

## Atualização e publicação

O workflow roda a cada seis horas, manualmente e em pushes para `main`. Testa, coleta metadados, persiste o catálogo e publica em GitHub Pages. Ative **Settings → Pages → Source: GitHub Actions** após enviar o projeto a `main`. A agenda só funciona no branch padrão e pode sofrer atrasos ou ser desativada por inatividade pelo GitHub. Proteção de branch deve permitir commits do bot ou exigir uma futura estratégia por PR. Nenhum serviço foi publicado automaticamente durante a implementação.

A busca inicial é limitada a 30 resultados por consulta, sem paginação: este MVP não cobre todo o GitHub. A coleta preserva dados antigos em falhas; o workflow sinaliza falha e mantém a última publicação. Datas de push indicam atividade no código, não uma versão jogável. Não há histórico de crescimento das estrelas nesta versão.

## Ranking e curadoria

`score = 20 × log10(stars + 1) + 30 × exp(-diasDesdePush / 180)`.

São públicos: estrelas, descrição, data de push, licença e arquivamento. Acessos não estão disponíveis para repositórios de terceiros. Popularidade não comprova qualidade. Resultados encontrados são **candidatos**, nunca automaticamente ports confirmados. Consoles e sistemas suportados vêm de curadoria com evidência.

Veja [CONTRIBUTING.md](CONTRIBUTING.md), [memória do projeto](docs/PROJECT_MEMORY.md) e [arquitetura](docs/ARCHITECTURE.md).
