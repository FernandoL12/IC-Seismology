# Resumo das modificações (pré-push)

## Commit preparado
- **Hash:** `cfa2475`
- **Mensagem:** `feat: update BL tunnel workflow, docs, specs and output figures`
- **Branch:** `codex_repo_mapeamento_inicial`

## O que foi alterado

### 1) Correções no código
- `correlation.py`
  - `plot_matrix(...)` e `plot_offset(...)` passaram a receber `station` por parâmetro (sem depender de variável global).
  - Adicionado guard para Python `3.14+` (fluxo atual depende de ObsPy em versões suportadas).
  - Ajuste para evitar IDs fixos em `plot_all`: agora usa os IDs passados na execução (`events[0]`, `events[1]`).
- `analysis.py`
  - Guard explícito para Python `3.14+` não suportado.
- `cluster_map.py`
  - Guard explícito para Python `3.14+` não suportado.

### 2) Ambiente e dependências
- `requirements.txt` (novo)
  - Stack científica e ObsPy com restrição para evitar fluxo em Python `3.14+`.
- `README.md`
  - Setup com `venv` e instalação por `requirements.txt`.
  - Nova seção de smoke tests.

### 3) Makefile alinhado ao túnel da seisarc
- `Makefile`
  - Default de estação para `BL.RVDE..HHZ`.
  - Default de FDSN para `http://127.0.0.1:28080/`.
  - Novo alvo `make check_fdsn` para validar conectividade.
  - Exemplos atualizados para IDs `usp...`.

### 4) Documentação de mapeamento do repositório
- Novos arquivos em `.specs/codebase/`:
  - `STACK.md`
  - `ARCHITECTURE.md`
  - `CONVENTIONS.md`
  - `STRUCTURE.md`
  - `TESTING.md`
  - `INTEGRATIONS.md`

### 5) Figuras incluídas no commit
- `all-graphs.png`
- `matrix-corr.png`
- `matrix-off.png`
- `process.png`

## Validação executada
- `python correlation.py --help` ✅
- `make check_fdsn` com `http://127.0.0.1:28080/` ✅
- `make test_ids ids="usp2026doac usp2026dmwl usp2026dmvw"` (BL+túnel) ✅
- `make test_file` com os mesmos eventos (BL+túnel) ✅

## Status de push
- O `git push` foi iniciado, mas interrompido antes da confirmação de conclusão.
- Estado atual local: commit pronto para envio.
