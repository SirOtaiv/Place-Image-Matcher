# 🚀 Comparador de Imagens

Este projeto Python compara duas imagens para determinar se representam o mesmo local ou cena.

---

## 📋 Pré-requisitos

Certifique-se de ter o Python (versão 3.x recomendada) instalado no seu sistema.

## ⚙️ Instalação das Dependências

Para rodar o script, você precisa instalar as bibliotecas listadas no seu `requirements.txt`. Use o `pip` para isso:

```bash
pip install -r requirements.txt
```

## 📂 Estrutura Necessária

Para a execução, você deve ter a seguinte estrutura no diretório:

```
/seu_projeto/
├── main.py
├── requirements.txt
├── imagem_a.jpg
├── imagem_b.jpg
└── ...
```

> Nota: Os nomes das suas imagens (imagem_a.jpg, imagem_b.jpg) devem corresponder aos nomes usados na chamada de função dentro do script.

## ▶️ Como Rodar o Script

1. Clone o repositório

Faça o clone do projeto em um repositório local

2. Prepare a Execução

Verifique a última linha do arquivo `main.py` e ajuste-a, se necessário, com os nomes dos arquivos que você deseja comparar e o número mínimo de correspondências robustas (o último número):

```python
place_image_matcher('colonia1.jpg', 'colonia2.jpg', 10)
```

3. Execute no Terminal

Abra o terminal ou prompt de comando no diretório onde o arquivo main.py está e execute o script:

```bash
python main.py
```

## 📊 Onde Encontrar o Resultado

Após a execução, o script irá:

- Imprimir no console a DECISÃO final (se as imagens são ou não do mesmo local) e o número de correspondências robustas encontradas.

- Salvar uma imagem de resultado chamada `track_avancado_resultado.png` no mesmo diretório do script.

O arquivo `track_avancado_resultado.png` mostrará as duas imagens lado a lado com linhas desenhadas conectando os pontos que foram considerados correspondentes de forma robusta.