# Arquitetura

GitHub REST → `scripts/sync.py` → `data/catalog.json` → frontend estático.

`curation.json` guarda consultas, exclusões e revisão manual; `catalog.json` guarda observações públicas. Consultas são sequenciais, com sete segundos entre buscas; timeout de 30 segundos. Escrita é atômica. Em erros, preservamos observações antigas, marcamos estado parcial/falho e retornamos exit code 1. `updatedAt` é a última coleta com alguma resposta válida, não garantia de que todo item foi atualizado.

Coleta tem escopo fixo e não executa código dos repositórios encontrados. O navegador não recebe token e usa textContent para conteúdo externo. O ranking combina estrelas acumuladas com decaimento por último push. Não há dados de visitas, tendência histórica ou teste de jogos.

O workflow coleta fora de PRs; PRs rodam testes. Falhas de rede fazem a coleta terminar com erro e preservam catálogo anterior. Pages é opcional até que a organização o habilite: se `configure-pages` não puder ler uma configuração ativa, a coleta continua e o deploy é ignorado. Processos locais não sobrevivem necessariamente ao snapshot cloud; reinicie o servidor para desenvolver.
