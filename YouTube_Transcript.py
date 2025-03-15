from youtube_transcript_api import YouTubeTranscriptApi
import re


def extrair_id_video(url):
    """
    Extrai o ID do vídeo a partir da URL do YouTube.

    Parâmetros:
    url (str): URL completa do vídeo do YouTube.

    Retorno:
    str: ID do vídeo.
    """
    match = re.search(r'v=([A-Za-z0-9_-]{11})', url)
    return match.group(1) if match else None


def coletar_transcricao_somente_texto(video_id):
    """
    Coleta a transcrição de um vídeo do YouTube e organiza apenas o texto.

    Parâmetros:
    video_id (str): ID do vídeo no YouTube.

    Retorno:
    str: Texto completo da transcrição do vídeo (sem tempos).
    """
    try:
        transcricao = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
        texto = "\n".join([segmento['text'] for segmento in transcricao])
        return texto
    except Exception as e:
        print("Erro ao coletar a transcrição:", e)
        return None


def salvar_transcricao(texto, nome_arquivo="transcricao_somente_texto.txt"):
    """
    Salva o texto da transcrição em um arquivo de texto.

    Parâmetros:
    texto (str): Texto da transcrição.
    nome_arquivo (str): Nome do arquivo onde a transcrição será salva.
    """
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto)
    print(f"Transcrição salva em {nome_arquivo}")


if __name__ == "__main__":
    url = "linkdovideo"  # URL do vídeo no YouTube
    video_id = extrair_id_video(url)

    if not video_id:
        print("ID do vídeo não encontrado na URL.")
    else:
        transcricao_texto = coletar_transcricao_somente_texto(video_id)

        if transcricao_texto:
            print("Transcrição do vídeo:")
            print(transcricao_texto)
            salvar_transcricao(transcricao_texto)
        else:
            print("Não foi possível obter a transcrição.")
