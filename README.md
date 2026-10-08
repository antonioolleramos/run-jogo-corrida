# 🏍️ RUN! — Jogo de corrida e sobrevivência em Python

Jogo arcade 2D desenvolvido em **Python**, utilizando **Pygame** para interface, colisões e áudio, e **Esper** para organizar a lógica com o padrão **Entity Component System (ECS)**.

O jogador controla uma moto, desvia de carros e acumula pontos pelo tempo em que permanece na pista. A velocidade e a frequência dos obstáculos aumentam conforme a pontuação, tornando a partida progressivamente mais difícil.

## 🎮 Como jogar

| Tecla | Ação |
|---|---|
| `Enter` | Iniciar a partida |
| `W`, `A`, `S`, `D` | Movimentar a moto |
| `R` | Recomeçar após colisão |
| `Esc` | Sair |

**Regras:** desvie dos carros, sobreviva pelo maior tempo possível e tente superar a sua pontuação.

## 🧰 Tecnologias e estrutura

- **Python** — lógica de jogo.
- **Pygame** — renderização, sprites, eventos de teclado, máscaras para colisão e reprodução de áudio.
- **Esper** — componentes, entidades e sistemas responsáveis por entrada, movimentação, geração de inimigos, colisão, pontuação, limpeza e renderização.

`RUN!.py` contém a implementação; os arquivos PNG e a fonte TTF são recursos visuais. `requirements.txt` contém as bibliotecas e `tests/` contém verificações básicas de integridade.

## ▶️ Executar localmente

Tenha **Python 3.10–3.13** instalado. Abra um terminal nesta pasta e execute:

```powershell
py -m pip install -r requirements.txt
py "RUN!.py"
```

No Windows, se `py` não existir, tente `python` nos dois comandos. Em outros sistemas operacionais, use `python3`.

## 🧪 Verificação rápida

```powershell
py -m unittest discover -s tests -v
```

> Esses testes verificam os arquivos e a sintaxe; não substituem uma partida real para conferir áudio, controles e colisões.

## 🎵 Trilha sonora original

A trilha usada no projeto original é **“Riders on the Storm (Fredwreck Remix)” — Snoop Dogg & The Doors**, conhecida pela trilha sonora de *Need for Speed: Underground 2*.

O programa procura automaticamente o arquivo com este nome na mesma pasta de `RUN!.py`:

`Snoop Dogg  The Doors - Riders On The Storm (Fredwreck Remix) (NFS Underground 2 OST).mp3`

Se o arquivo estiver presente, o jogo tenta reproduzi-lo em loop. Se estiver ausente, o jogo continua normalmente, sem música. A faixa pertence aos seus respectivos titulares; ter uma cópia para uso pessoal **não concede autorização para republicá-la**.

## 🖼️ Créditos e licença dos recursos

- **Fonte Sixtyfour:** Copyright 2021 The Sixtyfour Project Authors (https://github.com/jenskutilek/homecomputer-fonts). Licenciada sob **SIL Open Font License 1.1**; consulte `LICENSE-FONTE-SIXTYFOUR.txt`.
- **Sprites e imagens:** preservados do projeto enviado; a procedência e o direito de redistribuição das artes devem ser confirmados antes de tornar o repositório público.
- **Código:** exercício de programação apresentado como parte do portfólio. A distribuição dos recursos artísticos depende de autorização de seus respectivos titulares.

## 🔒 Observações para GitHub

O repositório não exige banco de dados, servidor ou contas. Os arquivos são carregados de forma relativa ao diretório do script, então o jogo pode ser executado de qualquer pasta de trabalho.

**Antes de publicar publicamente:** confirme se os sprites podem ser redistribuídos. Não inclua o MP3 comercial no repositório, em seus commits ou nos Releases sem autorização.

> **Esta cópia pessoal inclui o MP3 original preservado, apenas para uso local. Não envie este ZIP para um repositório público.**
