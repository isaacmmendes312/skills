@echo off
rem Fila agendada do Claude Code: roda o pedido de prompt-fila.txt sozinho e grava a saida em fila-log.txt.
rem Configure as 3 linhas abaixo. Licenca MIT.
set "PROJETO=C:\caminho\do\seu\projeto"
set "MODELO=opus"
set "EFFORT=high"

rem Pasta deste arquivo (onde ficam o pedido e o log).
set "PASTA=%~dp0"
cd /d "%PROJETO%"

rem --allowedTools: so o que a fila pode rodar sem perguntar. Para ler uma pasta fora do projeto, acrescente --add-dir "C:\outra\pasta".
call claude -p --model %MODELO% --effort %EFFORT% --permission-mode acceptEdits --allowedTools "Bash(git *)" "Bash(ls *)" "Bash(cat *)" "Bash(grep *)" "Bash(head *)" "Bash(wc *)" "WebSearch" "WebFetch" --output-format text < "%PASTA%prompt-fila.txt" > "%PASTA%fila-log.txt" 2>&1
