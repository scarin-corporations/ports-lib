# Instruções para agentes

Leia README.md, CONTRIBUTING.md e docs/PROJECT_MEMORY.md antes de modificar o projeto. Use o checkout existente; cada tarefa cloud já é isolada, não crie worktrees sem solicitação.

Execute `python -m unittest discover -s tests -v`. Mantenha frontend estático e coleta fora do navegador. Nunca exponha tokens. Não confunda emulação com port nativo, nem invente compatibilidade, estrelas ou datas. Novas decisões relevantes devem entrar em docs/PROJECT_MEMORY.md. Não hospede assets proprietários. Não remova dados anteriores por falha de rede.
