# Prisma — Dashboard Multimédia

Projeto escolar em Python e Streamlit, desenvolvido com apoio de IA.

## Executar no Visual Studio Code

Instala Python 3.11 ou superior. Abre esta pasta no VS Code e executa no terminal:

```powershell
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m streamlit run app.py
```

Abre o endereço local apresentado no terminal. Para terminar, usa Ctrl+C.

## Publicar

1. Cria um repositório no GitHub e envia `app.py`, `ui.py`, `calculators.py`, `cloud_renderer.py`, `typography_lab.py`, a pasta `assets`, `.streamlit/config.toml`, `requirements.txt` e este README.
2. No Streamlit Community Cloud, associa o repositório e escolhe `app.py` como ficheiro principal.
3. Publica e guarda o endereço para a entrega.

GitHub Pages não executa aplicações Python/Streamlit; usa Streamlit Cloud para este projeto.

## Funcionalidades e conceitos

- Poema: strings, expressões regulares, listas, contagem de palavras e versos; nuvem personalizável com exportação PNG; sugestões de um dicionário local.
- Imagem: condições para identificar HD/Full HD/4K UHD, cálculo de proporções com máximo divisor comum, conversão de dimensões e seleção de cores hexadecimais.
- Quiz: 20 perguntas, condições, estado de sessão, dicas após erros e pontuação de 1 a 3 pontos por pergunta (máximo 60).
- Campos de dimensões: aceitam expressões com +, -, *, /, %, parênteses e decimais. Enter substitui a conta pelo resultado inteiro em píxeis. Contas inválidas mantêm a última dimensão válida. Não existe calculadora separada.
- Nuvem poética: largura e altura configuráveis (1–2048 px), palavras a excluir personalizadas, fundo transparente, cor sólida ou imagem PNG/JPEG carregada pelo utilizador. As opções são aplicadas ao PNG exportado.
- Teoria da cor: harmonias complementar, análoga, triádica, complementar dividida e monocromática, calculadas em HSL, exportáveis e aplicáveis à paleta editável.

## Papel da IA

A IA apoiou a escrita do código, o layout, as perguntas e as sugestões. A aplicação funciona sem chaves ou serviços de IA: sinonímia e dicas usam dados locais e regras. Revê os sinónimos no contexto do poema. Para avaliação, explica esta distinção e adapta o código às tuas fichas de outubro, que não foram fornecidas.

Sugestão de prompt para documentar o trabalho: «Ajuda-me a melhorar um dashboard Streamlit com strings, listas e condições. Explica cada alteração e cria dicas pedagógicas para um quiz multimédia.»

## Identidade visual

Paleta clara: creme `#FFFCF5`, tinta `#243D43`, verde `#237664`, pêssego `#FCE5D9`, menta `#DCF0E7` e amarelo `#FBEDBD`. Tipografia Segoe UI com alternativas locais. Espaçamento em múltiplos de 4/8 px, cantos discretos, foco visível e movimento reduzido quando solicitado pelo sistema. Cada laboratório tem uma ilustração SVG própria.

O cabeçalho fixo inclui menu móvel com acesso direto aos quatro separadores: Poesia (rosa), Imagem & cor (verde), Quiz (amarelo) e Tipografia (azul). Cada separador aplica a sua cor a botões, métricas e destaques. A interface tem um único tema claro, sem FAQ nem secção de apoio. Mantém indicador de leitura, carregamento da nuvem, confirmação de reinício e estilos de impressão.

## Laboratório de tipografia

Compara duas composições com fontes locais, tamanho, entrelinha, espaçamento entre letras e palavras, peso, itálico, alinhamento e maiúsculas. As recomendações de combinações foram preparadas com apoio de IA e adaptam-se por regras locais; não existe ligação a um modelo em tempo real. Uma combinação pode ser aplicada à composição A, e ambas podem ser exportadas num ficheiro HTML. As fontes disponíveis dependem do dispositivo e têm alternativas locais.

A Tipografia tem um banner SVG azul próprio. Os controlos React Aria da versão instalada do Streamlit recebem cores por separador, incluindo campos de texto, caixas de seleção, opções de quiz e sliders.

A página de erro personalizada está disponível em `/?pagina=inexistente`. Streamlit não permite substituir a resposta HTTP 404 de todos os caminhos do servidor nesta aplicação; essa configuração depende do alojamento. A impressão contém o separador ativo. As melhorias do cabeçalho usam JavaScript num componente Streamlit e exigem um navegador que permita acesso ao documento da aplicação.

A nuvem é desenhada com Pillow, sem matriz de ocupação NumPy. Apenas o último PNG é guardado por sessão e reutilizado enquanto as opções não mudarem. As imagens de fundo estão limitadas a 16 megapíxeis. Falta de memória apresenta uma mensagem recuperável. As entradas discretas de títulos, métricas e imagens usam IntersectionObserver; os conteúdos continuam visíveis se o JavaScript estiver indisponível. O sistema respeita a preferência de movimento reduzido.

Verificação visual recomendada: abrir a aplicação a 1440, 900 e 390 px; testar o menu e Escape, navegação por teclado, os três separadores, exportações, reinício do quiz e pré-visualização de impressão. Confirmar a página de erro com `?pagina=inexistente`.
