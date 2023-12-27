from django.shortcuts import render
from upload.models import *

def read_page(request, title):
    audio_objects = DatabaseAudio.objects.filter(database_audio_title=title).order_by('database_audio_number')
    text_objects = DatabaseText.objects.filter(database_text_title=title).order_by('database_text_number')
    image_objects = DatabaseImage.objects.filter(database_image_title=title).order_by('database_image_number')
    entire_objects = {
        'title' : title, # title variable for template
        'objects' : zip(text_objects, image_objects, audio_objects) # objects variable for template
    }
    return render(request, 'read_page_v1.html', entire_objects)