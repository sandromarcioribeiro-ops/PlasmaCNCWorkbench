# Plasma CNC Workbench para FreeCAD

Addon experimental para gerar G-code de plasma CNC no FreeCAD, começando por
um fluxo simples e seguro para Mach3.

## Objetivo

Este projeto nasceu para tirar o uso de plasma CNC da "cara de fresadora" no
FreeCAD. A meta e ter uma bancada autoexplicativa, em portugues, com:

- ferramentas de plasma prontas para uso;
- ajuste simples de kerf, velocidade, altura e tempo de perfuracao;
- ordem correta de corte: furos e recortes internos primeiro, contorno externo por ultimo;
- G-code Mach3 com tocha ligando em `M3` e desligando em `M5`;
- caminho para evoluir ate deteccao automatica de furos/contornos em faces do FreeCAD.

## Colaboradores

- Sandro Ribeiro - colaborador do projeto, testes reais em plasma CNC Mach3 e definicao do fluxo de oficina.
- Codex - implementacao inicial, arquitetura e documentacao.

## Estado atual

Versao MVP. Ja existe um gerador Mach3 independente da interface grafica, com
presets de plasma e testes. A bancada FreeCAD aparece como "Plasma CNC" e
inclui comando inicial para abrir uma explicacao do fluxo.

## Instalar manualmente no FreeCAD

1. Feche o FreeCAD.
2. Copie a pasta `PlasmaCNCWorkbench` para a pasta de addons do usuario:
   `C:\Users\sandr\AppData\Roaming\FreeCAD\Mod\PlasmaCNCWorkbench`
3. Abra o FreeCAD.
4. No seletor de bancadas, escolha `Plasma CNC`.

## Exemplo rapido sem FreeCAD

Rode:

```powershell
python .\PlasmaCNCWorkbench\example_mach3_catarina.py
```

Ele cria um arquivo `.tap` de exemplo com dois furos e um contorno externo.

## Fontes usadas para estrutura de addon

O Addon Manager do FreeCAD usa repositorios Git e metadados `package.xml` para
addons Python. O arquivo `InitGui.py` registra a bancada na interface do FreeCAD.

## Repositorio

GitHub: https://github.com/sandromarcioribeiro-ops/PlasmaCNCWorkbench
