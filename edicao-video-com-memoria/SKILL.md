---
name: edicao-video-com-memoria
description: Edita vídeos curtos (Reels, TikTok, Shorts) a partir do vídeo bruto com ffmpeg e transcrição local, seguindo um manual de estética (design.md) e uma memória de feedback (feedback-edicao.md) guardados na pasta do projeto, e salva cada correção para o próximo vídeo sair melhor. Use quando pedirem para editar, cortar, montar ou refazer uma versão de um vídeo, disserem "edita esse vídeo", "faz a v2", "corta essa fala" ou derem feedback sobre uma versão. Não use para escrever roteiro antes de gravar, fazer carrossel ou criar motion graphics do zero.
license: MIT
metadata:
  version: "1.0"
---

# Edição de vídeo com memória

Método: o editor humano vira diretor. A IA corta e monta; o diretor assiste e corrige; cada correção fica salva. O primeiro vídeo não fica bom: julgue depois de uns 10 (ideia do Jonny Viccari).

**Regras que não podem falhar:**
- Ler `design.md` e `feedback-edicao.md` da pasta do projeto ANTES de qualquer corte. O que não está lá vira pergunta ou 2 a 4 opções lado a lado. Não inventar estilo.
- Nunca sobrescrever o bruto nem uma versão anterior: cada render é um `vN.mp4` novo.
- Proposta de corte aprovada antes do render.
- Todo feedback vai para `feedback-edicao.md` na hora. Feedback que se repete, ou que o diretor chama de regra, sobe para o `design.md`.
- Um efeito ou recurso novo por vídeo, no máximo. Simples por padrão.
- Nada é publicado pela skill.

Primeira vez num projeto: se não existir `design.md`, juntar com a pessoa as referências (vídeos de que gosta, fontes, cores) e escrever o manual com o modelo `modelos/design.md`. Criar `feedback-edicao.md` a partir de `modelos/feedback-edicao.md`.

```text
Progresso:
- [ ] 1 Manual e feedback lidos
- [ ] 2 Fala, objetivo e CTA definidos
- [ ] 3 Transcrição com tempo por palavra
- [ ] 4 Proposta de corte aprovada
- [ ] 5 Render da vN
- [ ] 6 Conferência passou
- [ ] 7 Entrega e feedback salvo
```

## Workflow
1. Ler `design.md` e `feedback-edicao.md`.
2. Confirmar qual fala ou cena, quem fala, o CTA e o recurso novo deste vídeo (se houver). Faltando um, perguntar só esse.
3. Transcrever com tempo por palavra (ex.: faster-whisper local). Extrair o áudio com ffmpeg em 16 kHz mono antes de transcrever.
4. Escrever a proposta em tabela (ordem, arquivo, frase de início, frase de fim, tempo, o que aparece na tela) e o gancho dos 2 primeiros segundos. Gancho incerto: 2 a 4 opções. Esperar o ok.
5. Cortar só em silêncio real, com um respiro curto e fade de 15 a 25 ms. Legenda, textos e música conforme o `design.md`. Renderizar `vN.mp4`.
6. Conferir antes de mostrar:
   - transcrever o render e comparar com a proposta (nenhuma palavra comida);
   - medir o volume por trecho (LUFS) e comparar com o original; ganho fixo por trecho em vez de nivelador dinâmico;
   - extrair 4 a 6 quadros (gancho, textos, legenda, final) e olhar: nada tampa rosto, tudo legível.
   Se algo falhar, corrigir e voltar ao início deste passo.
7. Entregar no formato abaixo. Quando vier feedback, gravar em `feedback-edicao.md` (data, vídeo, versão, o que foi dito, como foi resolvido) antes da próxima versão.

## Formato de saída
```
vN pronta: <pasta>/vN.mp4 (XX,X s)
Mudou: [lista curta]
Conferido: transcrição bate · LUFS [valores] · quadros ok
Para você ver: [1 a 3 pontos onde a opinião do diretor decide]
```

## Exemplos
**1.** Input: "edita a fala da entrevista sobre o mercado". Saída do passo 4: tabela de trechos tirada da transcrição, 2 opções de gancho e a pergunta "posso renderizar a v1?".
**2.** Input: "a legenda está pequena e a música entrou alta no fim". Ação: gravar as 2 frases em `feedback-edicao.md`, mudar só a legenda e o ganho da música, renderizar a v(N+1), conferir e entregar listando só essas 2 mudanças.

## Edge cases
- Áudio com vento ou ruído: apontar o trecho e o tempo; não aplicar nivelador dinâmico às cegas.
- Fala com erro de fato (nome, data): perguntar se corta ou ajusta a legenda; nunca "consertar" a fala.
- Feedback que contradiz o `design.md`: mostrar a regra antiga e perguntar se a regra muda ou se é exceção deste vídeo.
- Efeito novo sem referência: pedir a referência ou mostrar folha numerada antes de usar.
