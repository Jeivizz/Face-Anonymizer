# Face Anonymizer

Detecta rostos em imagens e aplica borrão (blur) automático para anonimização, usando MediaPipe e OpenCV.

## Requisitos

- Python 3.9–3.13
- pip

## Instalação

1. Clone o repositório e entre na pasta do projeto:

```bash
git clone <url-do-repositorio>
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

> Alternativa: use `blaze_face_short_range.tflite` (troque a URL por `blaze_face_short_range`) se as imagens de entrada forem sempre próximas da câmera (ex: webcam/selfie). O full-range é mais robusto para fotos com distâncias e ângulos variados, e é o modelo padrão usado neste projeto.

## Estrutura do projeto

```
Face Anonymizer/
├── censor_img.py                    # Script principal
├── blaze_face_full_range.tflite     # Modelo de detecção facial (baixado, não versionado)
├── data/                            # Imagens de entrada (não versionadas)
│   └── person.jpg
├── requirements.txt
├── .gitignore
└── README.md
```

## Uso

1. Coloque a imagem que deseja processar em `./data/`.
2. Ajuste o caminho da imagem na variável `img_path` em `main.py`, se necessário.
3. Execute:

```bash
python3 main.py
```

Uma janela será aberta mostrando a imagem com os rostos detectados borrados. Pressione qualquer tecla para fechar.

## Como funciona

O script:

1. Carrega o modelo `FaceDetector` do MediaPipe Tasks (API atual — a API legada `mediapipe.solutions` foi descontinuada pela Google e removida nas versões mais recentes da biblioteca).
2. Converte a imagem para o formato `mp.Image` (RGB) exigido pela API.
3. Detecta os rostos presentes e obtém a caixa delimitadora (`bounding_box`) de cada um.
4. Aplica `cv2.blur` na região de cada rosto, cobrindo a área com um borrão de kernel 35×35.
5. Exibe o resultado com `cv2.imshow`.

## Notas técnicas

- **Python**: qualquer versão 3.9–3.13 funciona a partir do MediaPipe `1.0.1` (wheels `py3-none`, sem dependência de versão específica do CPython). Versões anteriores do MediaPipe (`0.10.x`) tinham suporte limitado a Python 3.9–3.12.
- **Avisos de fonte do Qt** (`QFontDatabase: Cannot find font directory`): cosméticos, causados pela ausência de fontes no pacote Qt embutido no OpenCV. Para eliminar:
  ```bash
  sudo apt install fonts-dejavu-core
  export QT_QPA_FONTDIR=/usr/share/fonts/truetype/dejavu
