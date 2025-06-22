# MST entre POIs (Bibliotecas) em Natal

### Maria Eduarda Lima da Luz
### Matrícula: 20250051776
---
Este repositório contém o código em Python para extrair e conectar pontos de interesse (POIs), especificamente bibliotecas, em Natal (RN) por meio da construção de uma Árvore Geradora Mínima (MST) usando OSMnx e NetworkX. Também inclui o resultado da análise em forma de imagem e links para o podcast e artigo no Medium.

---

## 📁 Estrutura do Repositório

```
├── README.md              # Documento de apresentação e instruções
├── bibliotecas_natal.py   # Script principal em Python
└── bibliotecas_natal.png  # Visualização da MST sobre o mapa de Natal
```

---

## 🚀 Como Executar

### 1. Pré-requisitos

* Python 3.7+
* Bibliotecas Python: `osmnx`, `networkx`, `matplotlib`, (instale via `pip install osmnx networkx matplotlib`)

### 2. Executar o Script

```bash
python bibliotecas_natal.py
```

Isso irá:

1. Baixar o grafo de ruas de Natal (tipo "drive").
2. Coletar coordenadas das bibliotecas (fallback para escolas).
3. Construir o grafo de interesse e aplicar o algoritmo de Kruskal para obter a MST.
4. Imprimir no terminal o comprimento total da MST (em km) e salvar ou exibir o mapa.

---

## Visualização

![MST entre POIs (bibliotecas) em Natal](bibliotecas_natal.png)

**Figura:** MST conectando bibliotecas municipais de Natal. Pontos em rosa representam bibliotecas, linhas roxas mostram as rotas da árvore geradora mínima.

---

## 🔗 Links Úteis

* 🎙️ Podcast sobre este projeto: [Ouça aqui](https://link-para-o-podcast.com)
* 📝 Artigo no Medium: [Leia no Medium](https://medium.com/seu-usuario/seu-artigo)

