# Hook UserPromptSubmit do Claude Code: modelo e effort atuais + "esse pedido pede mais?".
# A cada mensagem, descobre o modelo e o effort da sessão e lembra o Claude de classificar
# o pedido pela sua tabela (TABELA abaixo) antes de agir: se pede mais que o atual, avisa e para.
# Ordem: último /effort ou /model da conversa > padrão salvo em ~/.claude/settings.json > auto.
# Licença MIT. Python 3.8+, sem dependências.
import json, sys, os, re

# Caminho da tabela "pedido x modelo/effort", relativo à pasta do projeto. Ajuste para o seu.
TABELA = "docs/escolha-por-pedido.md"

sys.stdout.reconfigure(encoding="utf-8")

try:
    entrada = json.loads(sys.stdin.buffer.read().decode("utf-8") or "{}")
except Exception:
    entrada = {}

EFFORT = re.compile(r"(?:Effort level set to|Set effort level to) (\w+)(.*?)</local-command-stdout>", re.S)
MODELO = re.compile(r"Set model to ([^<\n]+)")

modelo, effort, so_sessao = None, None, False


def ler_comando(texto):
    """Lê a saída de /effort e /model gravada no histórico."""
    global modelo, effort, so_sessao
    if "<local-command-stdout>" not in texto:
        return
    m = EFFORT.search(texto)
    if m:
        resto = m.group(2).lower()
        effort = m.group(1).lower()
        so_sessao = "session" in resto and "default" not in resto
    m = MODELO.search(texto)
    if m:
        modelo = re.sub(r"\x1b\[[0-9;]*m", "", m.group(1)).strip()


try:
    with open(entrada.get("transcript_path") or "", encoding="utf-8") as f:
        for linha in f:
            try:
                item = json.loads(linha)
            except Exception:
                continue
            msg = item.get("message") or {}
            if item.get("type") == "assistant" and msg.get("model"):
                modelo = msg["model"]
            # O formato muda conforme a versão: no terminal a saída do comando veio como mensagem
            # do usuário; no Claude Code na web, como evento de sistema "local_command".
            if item.get("type") == "user" and isinstance(msg.get("content"), str):
                ler_comando(msg["content"])
            elif item.get("type") == "system" and isinstance(item.get("content"), str):
                ler_comando(item["content"])
except Exception:
    pass

if not effort:
    try:
        cfg = json.load(open(os.path.expanduser("~/.claude/settings.json"), encoding="utf-8"))
        effort = ((cfg.get("modelSettings") or {}).get(modelo or "", {}) or {}).get("effortLevel") or cfg.get("effortLevel")
    except Exception:
        pass

effort = effort or "auto"
nota = " (só nesta sessão)" if so_sessao else ""

print(
    f"<modelo-effort>Atual: {modelo or 'desconhecido'}, effort {effort}{nota}. Antes de agir, classifique o pedido "
    f"pela tabela de {TABELA}. Pede MAIS que o atual: avise em 1 linha com o porquê e PARE até o usuário trocar "
    "(/effort ou /model). Dá para MENOS sem perder qualidade: avise em 1 linha e siga. Atual certo: não comente. "
    "No meio da tarefa: se ela se mostrar mais difícil que a classificação (causa que não aparece, tentativas falhando, "
    "escopo maior, dado sensível ou algo que vai ficar público), pare num ponto seguro, avise em 1 linha o que mudou "
    "e peça o nível certo antes de seguir.</modelo-effort>"
)
