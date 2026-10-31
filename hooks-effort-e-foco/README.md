# Hooks do Claude Code: effort certo e janela de foco

Dois hooks `UserPromptSubmit` para o [Claude Code](https://code.claude.com), em Python 3.8+ sem dependências. Cada um imprime um aviso curto que o Claude lê antes de responder a cada mensagem.

## `modelo-effort.py`: o nível certo para cada pedido
O Claude não troca o próprio modelo nem o effort. Este hook diz a ele, a cada mensagem, qual é o modelo e o effort atuais e manda classificar o pedido pela sua tabela (`docs/escolha-por-pedido.md`):
- pede **mais** que o atual: avisa em 1 linha e **para** até você trocar (`/effort` ou `/model`);
- dá para **menos**: avisa e segue;
- **no meio da tarefa**, se ela se mostrar mais difícil do que parecia, para num ponto seguro e pede o nível certo.

Ele descobre o nível lendo o histórico da sessão (último `/effort` ou `/model`); sem nenhum, tenta o padrão salvo em `~/.claude/settings.json` e, se não achar, mostra "auto". Lê os dois formatos de histórico conhecidos (terminal e Claude Code na web).

## `janela-de-foco.py`: ferramenta só na hora dela
Para quem perde o dia "melhorando o setup" em vez de trabalhar. Fora das janelas configuradas, o hook pede ao Claude que não comece a construir ferramenta, anote o pedido para a próxima janela e só siga se você disser a palavra de liberação (padrão: `libera`). Usar uma ferramenta pronta no trabalho não conta.

Configuração no topo do arquivo, ou num `janela-de-foco.json` ao lado dele:
```json
{
  "janelas": [{"dia": "qui", "ini": "19:00", "fim": "23:00"}],
  "palavra_libera": "libera",
  "onde_anotar": "tasks/todo.md",
  "log": ""
}
```

## Instalar
1. Copie os arquivos para `.claude/hooks/` do seu projeto e a tabela para `docs/` (ou mude o `TABELA` no topo do `modelo-effort.py`).
2. Em `.claude/settings.json`:
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          { "type": "command", "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/modelo-effort.py\"" },
          { "type": "command", "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/janela-de-foco.py\"" }
        ]
      }
    ]
  }
}
```
No Linux e no Mac, troque `python` por `python3` se for o caso.

## Limites conhecidos
- O formato do histórico do Claude Code pode mudar de uma versão para outra. Se o aviso mostrar sempre "auto" depois de um `/effort`, é isso.
- A janela usa o relógio do computador. Em servidor ou na nuvem o relógio costuma estar em UTC.
- Janela que passa da meia-noite (ex.: 22:00 às 01:00) precisa ser dividida em duas.
- A palavra de liberação vale também dentro de outra palavra ("libera" casa com "liberado").
- O hook só **avisa**. Quem decide parar é o Claude, e ele pode errar a classificação.

## Licença
MIT.
