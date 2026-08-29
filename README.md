# Face Anonymizer

Detecta rostos em imagens, vídeos ou webcam e aplica borrão (blur) automático para anonimização, usando MediaPipe e OpenCV.

## Requisitos

- Python 3.9–3.13
- pip

## Instalação

1. Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/Jeivizz/Face-Anonymizer
cd "Face Anonymizer"
```

2. Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Baixe o modelo de detecção facial (não versionado no repositório por ser um binário grande):

```bash
wget -O blaze_face_full_range.tflite https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_full_range/float16/latest/blaze_face_full_range.tflite
```

> Alternativa: use `blaze_face_short_range.tflite` (troque a URL por `blaze_face_short_range`) se as imagens/vídeos de entrada forem sempre próximos da câmera (ex: webcam/selfie). O full-range é mais robusto para fotos com distâncias e ângulos variados, e é o modelo padrão usado neste projeto.

## Estrutura do projeto

```
Face Anonymizer/
├── main.py                          # Script principal (CLI com suporte a imagem, vídeo e webcam)
├── process_img.py                   # Processa imagens e frames (conversão de cor + detecção de rostos + blur)
├── utils.py                         # Funções auxiliares (salvar imagem, configurar vídeo de saída, etc.)
├── blaze_face_full_range.tflite     # Modelo de detecção facial (baixado, não versionado)
├── data/                            # Imagens/vídeos de entrada (não versionados)
│   └── example.jpg
├── output/                          # Mídias censuradas salvas (imagens e vídeos)
│   └── example-blurred.png
├── requirements.txt                 # Dependências
├── .gitignore
└── README.md
```

## Uso

O script é executado via linha de comando com o argumento `--mode`, que define a fonte de entrada:

```bash
python3 main.py --mode <image|video|webcam> --file_path <caminho>
```

### Argumentos

| Argumento | Descrição | Padrão |
|---|---|---|
| `--mode` | Modo de operação: `image`, `video` ou `webcam` | `webcam` |
| `--file_path` | Caminho do arquivo de entrada (usado nos modos `image` e `video`) | `./data/example.jpg` |

### Modo imagem

Detecta e borra rostos em uma imagem estática, exibe o resultado numa janela e salva a versão censurada em `./output/`:

```bash
python3 main.py --mode image --file_path ./data/example.jpg
```

Pressione qualquer tecla para fechar a janela.

### Modo vídeo

Processa um arquivo de vídeo frame a frame, borrando os rostos detectados, e salva o vídeo resultante em `./output/`:

```bash
python3 main.py --mode video --file_path ./data/example.mp4
```

### Modo webcam (padrão)

Captura a webcam em tempo real e exibe o vídeo com os rostos borrados ao vivo:

```bash
python3 main.py --mode webcam
```

Pressione `q` para encerrar.

## Como funciona

1. Carrega o modelo `FaceDetector` do MediaPipe Tasks (API atual — a API legada `mediapipe.solutions` foi descontinuada pela Google e removida nas versões mais recentes da biblioteca).
2. Para cada imagem/frame, `process_img.py` converte para o formato `mp.Image` (RGB) exigido pela API, detecta os rostos e aplica `cv2.blur` na região de cada `bounding_box` encontrada.
3. Dependendo do `--mode`:
   - **image**: processa uma única imagem, exibe e salva o resultado.
   - **video**: lê o vídeo frame a frame, processa e escreve num novo arquivo de vídeo via `utils.video_parameters`.
   - **webcam**: processa o fluxo da câmera em tempo real, exibindo o resultado até `q` ser pressionado.
4. Os resultados salvos (imagem/vídeo) vão para a pasta `./output/`, via `utils.save_img`.

## Notas técnicas

- **Python**: qualquer versão 3.9–3.13 funciona a partir do MediaPipe `1.0.1` (wheels `py3-none`, sem dependência de versão específica do CPython). Versões anteriores do MediaPipe (`0.10.x`) tinham suporte limitado a Python 3.9–3.12.
- **Avisos de fonte do Qt** (`QFontDatabase: Cannot find font directory`): cosméticos, causados pela ausência de fontes no pacote Qt embutido no OpenCV. Para eliminar:
  ```bash
  sudo apt install fonts-dejavu-core
  export QT_QPA_FONTDIR=/usr/share/fonts/truetype/dejavu
  ```
