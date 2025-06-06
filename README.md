# OpenAI Whisper API

**IF YOU FIND THIS REPOSITORY HELPFUL, PLEASE CONSIDER STARRING IT.**

![github clones](https://img.shields.io/badge/clones-220%2B-blueviolet)
![docker pulls](https://img.shields.io/docker/pulls/matusstas/openai-whisper-microservice)
![docker stars](https://img.shields.io/docker/stars/matusstas/openai-whisper-microservice)
![contributors](https://img.shields.io/github/contributors/matusstas/openai-whisper-microservice)
![license](https://img.shields.io/github/license/matusstas/openai-whisper-microservice)
![last commit](https://img.shields.io/github/last-commit/matusstas/openai-whisper-microservice)

This microservice provides the same API as OpenAI's API.

The authors claim that Whisper is a general-purpose speech recognition model. It is trained on a large dataset of diverse audio and is also a multitasking model that can perform multilingual speech recognition, speech translation, and language identification.

A Transformer sequence-to-sequence model is trained on various speech processing tasks, including multilingual speech recognition, speech translation, spoken language identification, and voice activity detection. These tasks are jointly represented as a sequence of tokens to be predicted by the decoder, allowing a single model to replace many stages of a traditional speech-processing pipeline. The multitask training format uses a set of special tokens that serve as task specifiers or classification targets.


## Available models and languages

There are five model sizes, four with English-only versions, offering speed and accuracy tradeoffs. Below are the names of the available models and their approximate memory requirements and relative speed. 


|  Size  | Parameters | English-only model | Multilingual model | Required VRAM | Relative speed |
|:------:|:----------:|:------------------:|:------------------:|:-------------:|:--------------:|
|  tiny  |    39 M    |     `tiny.en`      |       `tiny`       |     ~1 GB     |      ~32x      |
|  base  |    74 M    |     `base.en`      |       `base`       |     ~1 GB     |      ~16x      |
| small  |   244 M    |     `small.en`     |      `small`       |     ~2 GB     |      ~6x       |
| medium |   769 M    |    `medium.en`     |      `medium`      |     ~5 GB     |      ~2x       |
| large  |   1550 M   |        N/A         |      `large`       |    ~10 GB     |       1x       |
| turbo  |   809 M    |        N/A         |      `turbo`       |     ~6 GB     |      ~8x       |

The `.en` models for English-only applications tend to perform better, especially for the `tiny.en` and `base.en` models. We observed that the difference becomes less significant for the `small.en` and `medium.en` models.

Whisper's performance varies widely depending on the language. The figure below shows a WER (Word Error Rate) breakdown by languages of the Fleurs dataset using the `large-v2` model. More WER and BLEU scores corresponding to the other models and datasets can be found in Appendix D in [the paper](https://arxiv.org/abs/2212.04356). The smaller, the better.

## Original repository

https://github.com/openai/whisper


# Run

```bash
git clone https://github.com/matusstas/openai-whisper-microservice.git
cd openai-whisper-microservice

# Optional: Configure environment variables
cp server/.env.example server/.env
# Edit server/.env with your preferred settings

# Run with Docker Compose
docker-compose up -d --build
```

# Environment Variables

The service supports the following environment variables:

- `ENVIRONMENT`: Set to `development` to disable API key authentication or `production` (default) to enable it
- `API_KEY`: Your custom API key to secure the API endpoints in production mode

You can set these variables in three ways:

1. Create a `.env` file in the server directory
2. Pass them directly to docker-compose:
   ```bash
   ENVIRONMENT=development API_KEY=your-secret docker-compose up -d
   ```
3. Edit the docker-compose.yml file and set the values directly

# API Authentication

When running in production mode with an API key set, all endpoints require authentication with the `X-API-Key` header:

```
X-API-Key: your-secret-key-here
```

Authentication is automatically disabled when:
- `ENVIRONMENT` is set to `development`, or
- No `API_KEY` is provided in production mode

# Docker Hub

* repository

https://hub.docker.com/r/matusstas/openai-whisper-microservice

* latest

`docker pull matusstas/openai-whisper-microservice:latest`

* 1.0.0

`docker pull matusstas/openai-whisper-microservice:1.0.0`

# Swagger API documentation

After successfully starting the image, the Swagger documentation will be available at http://localhost:10000/docs



# Endpoints

The API currently provides 12 endpoints, which are divided into 4 groups according to their use.

![Endpoints](https://github.com/matusstas/openai-whisper-microservice/blob/main/documentation/endpoints.png)

## Model

<details>
  <summary><code><span style="color:blue"><b>GET</b></span> /models-available</code></summary>
  
#### Description

Return a list of all available Whisper ASR models.

#### Response 200

```json
[
  "tiny.en",
  "tiny",
  "base.en",
  "base",
  "small.en",
  "small",
  "medium.en",
  "medium",
  "large-v1",
  "large-v2",
  "large"
]
```
</details>


<details>
  <summary><code><span style="color:blue"><b>GET</b></span> /models-downloading</code></summary>
  
#### Description

Return a list of all downloading Whisper ASR models.

#### Response 200

```json
[
  "tiny.en"
]
```
</details>


<details>
  <summary><code><span style="color:blue"><b>GET</b></span> /models-downloaded</code></summary>
  
#### Description

Return a list of all downloaded Whisper ASR models.

#### Response 200

```json
[
  "tiny.en",
  "tiny"
]
```
</details>


<details>
  <summary><code><span style="color:green"><b>POST</b></span> /model</code></summary>
  
#### Description

Download a Whisper ASR model using background task.

#### Parameters

* `model_name`
    * required
    * string (path)
    * Name of the model

#### Response 201

```json
{
  "detail": "Model is being downloaded"
}
```

#### Response 400

```json
{
  "detail": "Invalid model"
}
```

#### Response 400

```json
{
  "detail": "Model not downloaded yet"
}
```

#### Response 409

```json
{
  "detail": "Model already exist"
}
```
</details>


<details>
  <summary><code><span style="color:blue"><b>GET</b></span> /model/{model_name}</code></summary>
  
#### Description

Return a Whisper ASR model.

#### Parameters

* `model_name`
    * required
    * string (path)
    * Name of the model

#### Response 200

```json
JSON RESPONSE IS TOO LONG TO DISPLAY
```


#### Response 400

```json
{
  "detail": "Model not downloaded yet"
}
```

#### Response 404

```json
{
  "detail": "Model not found"
}
```
</details>


<details>
  <summary><code><span style="color:red"><b>DELETE</b></span> /model/{model_name}</code></summary>
  
#### Description

Delete a downloaded Whisper ASR model.

#### Parameters

* `model_name`
    * required
    * string (path)
    * Name of the model

#### Response 200

```json
{
  "detail": "Model was deleted"
}
```


#### Response 400

```json
{
  "detail": "Model not downloaded yet"
}
```

#### Response 404

```json
{
  "detail": "Model not found"
}
```
</details>


<details>
  <summary><code><span style="color:green"><b>POST</b></span> /model/{model_name}/language</code></summary>
  
#### Description

Return a sorted list of all detected languages by their score.

#### Parameters

* `model_name`
    * required
    * string (path)
    * Name of the model
    
#### Request body

* `file`
    * required
    * string ($binary)
    * Chosen audiofile

#### Response 200

```json
{
  "en": 0.38421738147735596,
  "cy": 0.2614089846611023,
  "zh": 0.10288530588150024,
  "nn": 0.04161091521382332,
  "ko": 0.03617018833756447,
  ...
  "uz": 9.862478833611021e-9
}
```



#### Response 400

```json
{
  "detail": "Model not multilingual"
}
```

#### Response 400

```json
{
  "detail": "Model not downloaded yet"
}
```

#### Response 404

```json
{
  "detail": "Model not found"
}
```
</details>


<details>
  <summary><code><span style="color:green"><b>POST</b></span> /model/{model_name}/transcript</code></summary>
  
#### Description

Transcribe audio with a Whisper ASR model.

#### Parameters

* `model_name`
    * required
    * string (path)
    * Name of the model
    
#### Request body

* `task`
    * required
    * string
    * Task: [`transcribe`, `translate`]

* `language_code`
    * required
    * string
    * Language code: [`af`, `am`, `ar`, `as`, `az`, ..., `zh`]

* `media_type`
    * required
    * string
    * Media type: [`application/json`, `text/plain`]

* `format`
    * required
    * string
    * Output format: [`json`, `srt`, `tsv`, `txt`, `vtt`]


* `file`
    * required
    * string ($binary)
    * Chosen audiofile

#### Response 200

```json
{
  "text": " I found that nothing in life is worthwhile unless you take risks. Nothing. Nelson Mandela said, there is no passion to be found playing small and settling for a life that's less than the one you're capable of living. Now I'm sure in your experiences in school and applying to college and...",
  "segments": [
    {
      "id": 0,
      "seek": 0,
      "start": 0,
      "end": 7,
      "text": " I found that nothing in life is worthwhile unless you take risks.",
      "tokens": [
        50363,
        314,
        1043,
        326,
        2147,
        287,
        1204,
        318,
        24769,
        4556,
        345,
        1011,
        7476,
        13,
        50713
      ],
      "temperature": 0,
      "avg_logprob": -0.19224673257747166,
      "compression_ratio": 1.5508021390374331,
      "no_speech_prob": 0.013612011447548866
    },
    {
      "id": 1,
      "seek": 0,
      "start": 7,
      "end": 9,
      "text": " Nothing.",
      "tokens": [
        50713,
        10528,
        13,
        50813
      ],
      "temperature": 0,
      "avg_logprob": -0.19224673257747166,
      "compression_ratio": 1.5508021390374331,
      "no_speech_prob": 0.013612011447548866
    },
    {
      "id": 2,
      "seek": 0,
      "start": 9,
      "end": 15,
      "text": " Nelson Mandela said, there is no passion to be found playing small",
      "tokens": [
        50813,
        12996,
        40233,
        531,
        11,
        612,
        318,
        645,
        7506,
        284,
        307,
        1043,
        2712,
        1402,
        51113
      ],
      "temperature": 0,
      "avg_logprob": -0.19224673257747166,
      "compression_ratio": 1.5508021390374331,
      "no_speech_prob": 0.013612011447548866
    },
    {
      "id": 3,
      "seek": 0,
      "start": 15,
      "end": 20,
      "text": " and settling for a life that's less than the one you're capable of living.",
      "tokens": [
        51113,
        290,
        25446,
        329,
        257,
        1204,
        326,
        338,
        1342,
        621,
        262,
        530,
        345,
        821,
        6007,
        286,
        2877,
        13,
        51363
      ],
      "temperature": 0,
      "avg_logprob": -0.19224673257747166,
      "compression_ratio": 1.5508021390374331,
      "no_speech_prob": 0.013612011447548866
    },
    {
      "id": 4,
      "seek": 0,
      "start": 20,
      "end": 24,
      "text": " Now I'm sure in your experiences in school and applying to college and...",
      "tokens": [
        51363,
        2735,
        314,
        1101,
        1654,
        287,
        534,
        6461,
        287,
        1524,
        290,
        11524,
        284,
        4152,
        290,
        986,
        51563
      ],
      "temperature": 0,
      "avg_logprob": -0.19224673257747166,
      "compression_ratio": 1.5508021390374331,
      "no_speech_prob": 0.013612011447548866
    }
  ],
  "language": "en"
}
```

#### Response 400

```json
{
  "detail": "Model not downloaded yet"
}
```

#### Response 404

```json
{
  "detail": "Model not found"
}
```
</details>


## Language

<details>
  <summary><code><span style="color:blue"><b>GET</b></span> /languages</code></summary>
  
#### Description

Return all available languages.

#### Response 200

```json
{
  "af": "afrikaans",
  "am": "amharic",
  "ar": "arabic",
  "as": "assamese",
  "az": "azerbaijani",
  ...
  "zh": "chinese"
}
```
</details>

<details>
  <summary><code><span style="color:blue"><b>GET</b></span> /language/{language_code}</code></summary>
  
#### Description

Return an english language name.

#### Response 200

```json
"italian"
```

#### Response 404

```json
{
  "detail": "Language not found"
}
```
</details>

## Miscellaneous


<details>
  <summary><code><span style="color:blue"><b>GET</b></span> /cuda</code></summary>
  
#### Description

Check whether a GPU with CUDA support is available on the current system. Return boolean value.

#### Response 200

```json
true
```
</details>

## Root

<details>
  <summary><code><span style="color:blue"><b>GET</b></span> /language/{language_code}</code></summary>
  
#### Description

Return message from container to check if it is running.

#### Response 200

```json
{
  "detail": "Whisper API is running"
}
```

</details>


# Data Persistence with Docker Volumes

In order not to lose important data, we added volumes. This is ensured by a specific command in the `docker-compose.yml` file.

## Volume: models

All downloaded Whisper ASR models are stored in the `/root/.cache/whisper` folder. These are the models we work with.

## Volume: db

Due to the fact that I also provide management of individual models (download or delete), I needed a simple database that would allow me to do this. So I work with TinyDB (document-oriented database written in pure Python with no external dependencies), where the important file `models.json` is stored in the `db` folder. 

For example, the data in the file might looks like this:

```json
{
   "_default":{
      "1":{
         "name":"tiny",
         "downloaded":false
      },
      "2":{
         "name":"tiny.en",
         "downloaded":true
      }
   }
}
```

* downloaded: true = Whisper ASR model was downloaded
* downloaded: false = Whisper ASR model is still downloading

# Star History

[![Star History Chart](https://api.star-history.com/svg?repos=matusstas/openai-whisper-microservice&type=Date)](https://star-history.com/#matusstas/openai-whisper-microservice)

# Todo

* GPU support (I'm working on it right now)
