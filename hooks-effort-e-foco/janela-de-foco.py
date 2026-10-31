# Hook UserPromptSubmit do Claude Code: janela de foco para construir ferramentas.
# Fora das janelas configuradas, avisa o Claude para não começar a construir ferramenta
# (o "projeto paralelo" que come o tempo do trabalho principal) e anotar o pedido para depois.
# A palavra de liberação (padrão "libera") na mensagem abre uma exceção só para aquele pedido.
# Licença MIT. Python 3.8+, sem dependências.
import json, sys, os, datetime

# Configuração: edite aqui ou crie um janela-de-foco.json ao lado deste arquivo com as mesmas chaves.
CONFIG = {
    # Dias: seg, ter, qua, qui, sex, sab, dom. Horas no formato HH:MM, no relógio do computador.
    "janelas": [{"dia": "qui", "ini": "19:00", "fim": "23:00"}],
    "palavra_libera": "libera",
    "o_que_trava": "construir ou mexer em ferramentas (código de ferramenta própria, skills novas, plugins, testes de ferramenta)",
    "onde_anotar": "a sua lista de tarefas",
    "log": "",  # caminho de um arquivo para registrar cada liberação; vazio = não registra
}

sys.stdout.reconfigure(encoding="utf-8")
DIAS = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]
NOMES = {"seg": "segunda", "ter": "terça", "qua": "quarta", "qui": "quinta", "sex": "sexta", "sab": "sábado", "dom": "domingo"}

extra = os.path.join(os.path.dirname(os.path.abspath(__file__)), "janela-de-foco.json")
if os.path.exists(extra):
    try:
        CONFIG.update(json.load(open(extra, encoding="utf-8")))
    except Exception:
        pass

try:
    entrada = json.loads(sys.stdin.buffer.read().decode("utf-8") or "{}")
except Exception:
    entrada = {}
prompt = (entrada.get("prompt") or "").lower()

janelas = [j for j in CONFIG.get("janelas", []) if j.get("dia") in DIAS and j.get("ini")]
if not janelas:
    sys.exit(0)

agora = datetime.datetime.now()
dia = DIAS[agora.weekday()]
hhmm = agora.strftime("%H:%M")

for j in janelas:
    fim = j.get("fim") or "24:00"
    if j["dia"] == dia and j["ini"] <= hhmm < fim:
        print(f"<janela-de-foco>Janela de ferramentas aberta até {fim}: pode construir e testar. Avise quando faltarem uns 15 min para fechar.</janela-de-foco>")
        sys.exit(0)

prox = " e ".join(f"{NOMES[j['dia']]} {j['ini']} às {j.get('fim') or '24:00'}" for j in janelas)
palavra = (CONFIG.get("palavra_libera") or "libera").lower()

if palavra in prompt:
    if CONFIG.get("log"):
        try:
            with open(CONFIG["log"], "a", encoding="utf-8") as f:
                f.write(f"{agora:%Y-%m-%d %H:%M} ({NOMES[dia]}): {prompt[:120]}\n")
        except Exception:
            pass
    print(f"<janela-de-foco>O usuário disse \"{palavra}\": a trava está aberta só para este pedido. Faça o mínimo pedido, sem puxar etapa nova.</janela-de-foco>")
    sys.exit(0)

print(
    f"<janela-de-foco>Agora é {NOMES[dia]} {hhmm}, fora da janela de ferramentas ({prox}). "
    f"{CONFIG['o_que_trava'][0].upper()}{CONFIG['o_que_trava'][1:]} só na janela. "
    f"Se o pedido for isso, NÃO comece: diga em 1 a 2 linhas que agora não é a hora, anote o pedido em {CONFIG['onde_anotar']} "
    f"para a próxima janela e só siga se o usuário responder \"{palavra}\". Usar uma ferramenta pronta no trabalho, "
    "ou consertar o mínimo de uma que está travando o trabalho, não conta como construir.</janela-de-foco>"
)
