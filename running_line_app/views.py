from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from .models import GeneratedText

def generate(request):
    return render(request, 'running_line_app/generate_running_line.html')

def generate_running_line(request, text):

    width, height = 100, 100
    font_size = 75
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(r'/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf', font_size)
    draw.text((100, 100), text, font=font, fill='black')
    temp_image_path = 'temp_image.png'
    image.save(temp_image_path)
    x_position = width
    output_file = "running_line.mp4"
    fps = 30
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    num_frames = 90
    total_length_char = len(text) * width / 3
    total_letter_spacing = (len(text) - 1) * width / 7.5
    total_length_string = total_length_char + total_letter_spacing
    delta_x_1 = (total_length_string + width + width / 3) / num_frames  # Изменение x, чтобы бегущая строка заканчивалась белым экраном
    delta_x_2 = (total_length_string + width) / num_frames  # Изменение x, чтобы бегущая строка заканчивалась последним символом
    for frame in range(num_frames):
        draw.rectangle((0, 0, width, height), fill=(255, 255, 255))
        draw.text((x_position, 0), text, font=font, fill=(0, 0, 0))
        x_position -= delta_x_1
        frame_array = np.array(image)
        # Инвертирую цвета (OpenCV использует BGR, а не RGB)
        frame_array = cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)
        video_writer.write(frame_array)
    video_writer.release()
    # Отдаем видеофайл пользователю для скачивания
    with open(output_file, 'rb') as video_file:
        response = HttpResponse(video_file.read(), content_type='video/mp4')
        response['Content-Disposition'] = f'attachment; filename={output_file}'
        return response

