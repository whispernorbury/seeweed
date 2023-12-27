from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from upload.models import DatabaseAudio, DatabaseImage, DatabaseText
from openai import OpenAI, BadRequestError
import re
import g2pk
from gtts import gTTS
from sce_tts.views import normalize_multiline_text
import soundfile
import os
from django.conf import settings
from TTS.TTS.TTS.utils.synthesizer import Synthesizer
# Create your views here.
@csrf_exempt
def upload_page(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        input_v = data.get('content', '')
        input_name = data.get('name', '')
        input_model = data.get('model', '')
        input_age = data.get('age', '')
        input_key = data.get('key', '')
        callToken(input_key)
        obj = DatabaseText.objects.filter(database_text_title = input_name)
        if not obj.exists():
            try:
                ask_openai(input_v, input_name, input_model, input_age)
            except BadRequestError as e: # 400 error handling
                error_message = str(e)
                print("400 error occured!") # 잘못생성된아이들 삭제
                text_to_del = DatabaseText.objects.filter(database_text_title = input_name)
                audio_to_del = DatabaseAudio.objects.filter(database_audio_title = input_name)
                img_to_del = DatabaseImage.objects.filter(database_image_title = input_name)
                text_to_del.delete()
                audio_to_del.delete()
                img_to_del.delete()
                return JsonResponse({'error': error_message}, status=400)
        return JsonResponse({'title':input_name})
    else:
        tarPath = os.path.join(settings.BASE_DIR, 'TTS', 'data', 'glowtts-v2') 
        tarList = getTTSModels(tarPath)
        return render(request, 'upload_page.html', {'tts_models': tarList})

def adjust_volume(input_file, output_file, volume_change):
    # 음성 파일 로드
    audio, sample_rate = soundfile.read(input_file)

    # 볼륨 조절
    adjusted_audio = audio * (10**(volume_change / 20.0))

    # 조절된 음성을 새 파일로 저장
    soundfile.write(output_file, adjusted_audio, sample_rate)

client = 0

def getTTSModels(directory_path):
    ret = []
    all_files = os.listdir(directory_path)
    ret = [file for file in all_files if file.endswith(".pth.tar")]
    return ret 

# TOKEN-TOKEN-TOKEN-TOKEN-TOKEN-TOKEN-TOKEN-TOKEN-TOKEN-TOKEN-TOKEN-TOKEN-TOKEN-TOKEN
def callToken(input):
    global client
    client = OpenAI(api_key= input)

def split_text_into_sentences(text, sentences_per_group=4):
    # Split the text into sentences using regular expression
    sentences = re.split(r'(?<=[.!?\n])\s+', text)
    grouped_sentences = [' '.join(sentences[i:i + sentences_per_group]) for i in range(0, len(sentences), sentences_per_group)]
    return grouped_sentences

# Age makes different order to GPT-4
def fitMessage(input_age):
    if input_age.lower() == 'junior':
        message = [ {"role": "system", "content": "내가 주는 글을 읽기 쉽게 동화의 형식으로 한글로 바꿔줘. please response in many tokens."} ]
        return message
    else:
        message = [ {"role": "system", "content": "내가 입력하는 글을 한글로 요약해줘."} ]
        return message

def ask_openai(input_v, input_name, SelectedModel, input_age):
    message = fitMessage(input_age)
    message.append({"role": "user", "content": f"{input_v}"})
    response = client.chat.completions.create(
        model="gpt-4",
        messages=message
    )
    grouped_sentences = split_text_into_sentences(response.choices[0].message.content, 6)

    for number in range(len(grouped_sentences)):
        NewUserText = DatabaseText() # NewUserText은 AI에게 가공된 텍스트 데이터를 저장할 model의 object임.
        NewUserText.database_text_content = grouped_sentences[number]
        NewUserText.database_text_number = number + 1
        NewUserText.database_text_title = input_name
        NewUserText.save()

        
        GlowModelSource = SelectedModel+'.pth.tar'
        HifiganModelSource = SelectedModel+'.pth.tar'
        synthesizer = Synthesizer(
            "TTS/data/glowtts-v2/" + GlowModelSource,
            "TTS/data/glowtts-v2/config.json",
            None,
            "TTS/data/hifigan-v2/"+ HifiganModelSource ,
            "TTS/data/hifigan-v2/config.json",
            None,
            None,
            False,
        )
        symbols = synthesizer.tts_config.characters.characters
        for target_text in normalize_multiline_text(grouped_sentences[number], symbols):
            wav = synthesizer.tts(target_text, None, None)
        RouteToAudio = "sounddata/sce_tts_" + input_name + str(number + 1) + ".mp3"
        RouteToAudio2 = "sce_tts_" + input_name + str(number + 1) + ".mp3"
        soundfile.write(RouteToAudio, wav, 22050)
        if SelectedModel == '최지성':
            adjust_volume(RouteToAudio, RouteToAudio, 20)

        NewUserAudio = DatabaseAudio()
        NewUserAudio.database_audio_content = RouteToAudio2
        NewUserAudio.database_audio_number = number + 1
        NewUserAudio.database_audio_title = input_name
        NewUserAudio.save()


    for x in range(len(grouped_sentences)):
        response = client.images.generate(
            model="dall-e-3",
            prompt=grouped_sentences[x],
            size="1024x1024",
            quality="standard",
            n=1,
        )
        NewUserImage = DatabaseImage()
        NewUserImage.database_image_content = response.data[0].url
        NewUserImage.database_image_number = x + 1
        NewUserImage.database_image_title = input_name
        NewUserImage.save()


    # Save the data to the database
    # for sentence, image_url in zip(grouped_sentences, image_urls):
    #    GeneratedData.objects.create(sentence=sentence, image_url=image_url)


    # return grouped_sentences