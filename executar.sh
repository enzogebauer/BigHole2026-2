#!/usr/bin/env bash
# Executa o Static Checker. Uso: ./executar.sh Teste  (ou ./executar.sh caminho/Teste)
# Não troca de pasta, para que caminhos relativos do texto fonte continuem valendo.
DIR="$(cd "$(dirname "$0")" && pwd)"
if command -v uv >/dev/null 2>&1; then
  uv run --project "$DIR" "$DIR/programa_principal.py" "$@"
else
  python3 "$DIR/programa_principal.py" "$@"
fi
