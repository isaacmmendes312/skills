# Fila agendada do Claude Code (Windows)

Deixa o [Claude Code](https://code.claude.com) trabalhando sozinho numa lista de tarefas enquanto você está fora: o Agendador de Tarefas do Windows abre o Claude no horário marcado, ele lê o pedido de `prompt-fila.txt`, faz as tarefas uma por uma e grava um relatório no fim. Sem dependências além do próprio Claude Code.

## Arquivos
- `rodar-fila.cmd`: o lançador. Configure as 3 linhas do topo.
- `prompt-fila-exemplo.txt`: modelo do pedido. Copie para `prompt-fila.txt` e escreva as suas tarefas.

## Instalar
1. Copie esta pasta para qualquer lugar do seu PC (fora do projeto, para o log não entrar no seu git).
2. Em `rodar-fila.cmd`, ajuste `PROJETO` (a pasta onde o Claude vai trabalhar), `MODELO` e `EFFORT`.
3. Escreva o pedido em `prompt-fila.txt`, a partir do exemplo.
4. Teste uma vez à mão: dê dois cliques no `rodar-fila.cmd` e veja o `fila-log.txt`.
5. Agende. No PowerShell, para rodar uma vez hoje às 19h15 (a data segue o formato do seu Windows):
```
schtasks /create /tn ClaudeFila /tr "C:\caminho\da\pasta\rodar-fila.cmd" /sc once /sd 31/10/2026 /st 19:15
```
Para remarcar depois: `schtasks /change /tn ClaudeFila /sd <data> /st <hora>`.

## Permissões
A fila roda sem ninguém para aprovar comandos. Ela só pode o que estiver em `--allowedTools` no lançador; o resto é recusado e ela segue para a próxima tarefa (peça no pedido para anotar o que foi recusado).
- O modo `acceptEdits` deixa a fila criar e editar arquivos sem perguntar, na pasta do projeto e nas pastas de `--add-dir`. Use git no projeto para poder desfazer.
- Pasta fora do projeto só é lida se estiver em `--add-dir`. Atenção: com `acceptEdits`, ela também pode editar lá. Se a pasta for só para leitura, proíba a edição no pedido, por escrito.
- Não libere instalação (`npm`, `pip`, `winget`) nem comandos que apagam.

## Cuidados
- **O PC precisa ficar ligado e com você logado** (pode bloquear a tela). A tarefa criada assim só roda com o usuário logado.
- **Não deixe outra sessão do Claude gravando no mesmo projeto enquanto a fila roda.** Se as duas fizerem commit ao mesmo tempo, uma leva junto as mudanças da outra.
- **Limite de uso:** a fila gasta o mesmo limite do seu plano. Peça no pedido para parar numa tarefa terminada se o limite estiver acabando.
- O relatório é a única forma de saber o que aconteceu. Leia antes de abrir a próxima fila.

## Licença
MIT.
