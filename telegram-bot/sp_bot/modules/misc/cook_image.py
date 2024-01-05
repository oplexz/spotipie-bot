from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

from sp_bot.modules.misc import Fonts

# Define constants
CARD_SIZE = (1280, 480)
EDGE_GAP = 40
THUMBNAIL_SIZE = CARD_SIZE[1] - 2 * EDGE_GAP
INFO_OFFSET = THUMBNAIL_SIZE + 2 * EDGE_GAP
PROFILE_PIC_SIZE = 160


FONT_OPEN_SANS = ImageFont.truetype(Fonts.OPEN_SANS, 46)
FONT_POPPINS = ImageFont.truetype(Fonts.POPPINS, 50)
FONT_ARIAL = ImageFont.truetype(Fonts.ARIAL, 50)
FONT_ARIAL_SMALLER = ImageFont.truetype(Fonts.ARIAL, 46)


def truncate(text: str, font: ImageFont, limit: int):
    edited = True if font.getbbox(text)[2] > limit else False
    while font.getbbox(text)[2] > limit:
        text = text[:-1]
    if edited:
        return (text.strip() + '..')
    else:
        return (text.strip())


def check_unicode(text: str):
    return text == str(text.encode('utf-8'))[2:-1]


def draw_album_art(canvas: Image, cover_art_url: str):
    response = requests.get(cover_art_url)
    album_art = Image.open(BytesIO(response.content))
    background = album_art.copy()
    background = background.convert('RGBA')
    background = ImageOps.fit(background, CARD_SIZE, Image.LANCZOS)
    background = background.filter(ImageFilter.GaussianBlur(10))
    dimmed_background = Image.new('RGBA', CARD_SIZE, (0, 0, 0, 128))
    canvas.paste(background, (0, 0), mask=dimmed_background)

    album_art.thumbnail((THUMBNAIL_SIZE, THUMBNAIL_SIZE), Image.LANCZOS)
    canvas.paste(album_art, (EDGE_GAP, EDGE_GAP))


def draw_profile_picture(canvas: Image, profile_picture):
    profile_pic = Image.open(BytesIO(profile_picture.content))
    canvas.paste(
        profile_pic, (CARD_SIZE[0] - EDGE_GAP - PROFILE_PIC_SIZE, EDGE_GAP))


def draw_text_on_canvas(draw: ImageDraw, username: str,
                        song_name: str, artists: str, album_name: str):
    fill_color = '#ffffff'

    username = truncate(username, FONT_POPPINS, 500)
    is_listening_to = "is listening to"
    song_name = truncate(song_name, FONT_POPPINS if check_unicode(
        song_name) else FONT_ARIAL, 630)
    artists = truncate(artists, FONT_OPEN_SANS if check_unicode(
        artists) else FONT_ARIAL_SMALLER, 630)
    album_name = truncate(album_name, FONT_OPEN_SANS if check_unicode(
        album_name) else FONT_ARIAL_SMALLER, 630)

    draw.text((INFO_OFFSET, 45), username, fill=fill_color, font=FONT_POPPINS)
    draw.text((INFO_OFFSET, 108), is_listening_to,
              fill=fill_color, font=FONT_OPEN_SANS)
    draw.text((INFO_OFFSET, 230), song_name, fill=fill_color,
              font=FONT_POPPINS if check_unicode(song_name) else FONT_ARIAL)
    draw.text((INFO_OFFSET, 300), artists, fill=fill_color,
              font=FONT_OPEN_SANS if check_unicode(artists) else FONT_ARIAL_SMALLER)
    draw.text(
        (INFO_OFFSET,
         360),
        album_name,
        fill=fill_color,
        font=FONT_OPEN_SANS if check_unicode(album_name) else FONT_ARIAL_SMALLER)


def draw_progress_bar(draw: ImageDraw, current_time: int, total_time: int):
    progress_bar_width = CARD_SIZE[0] - INFO_OFFSET - EDGE_GAP
    progress_bar_height = 4
    progress_bar_x1 = INFO_OFFSET
    progress_bar_y1 = CARD_SIZE[1] - EDGE_GAP - progress_bar_height
    progress_bar_x2 = progress_bar_x1 + \
        (current_time / total_time * progress_bar_width)
    progress_bar_y2 = progress_bar_y1 + progress_bar_height

    draw.rectangle([(progress_bar_x1, progress_bar_y1), (INFO_OFFSET +
                   progress_bar_width, progress_bar_y2)], fill='#404040')
    draw.rectangle([(progress_bar_x1, progress_bar_y1),
                   (progress_bar_x2, progress_bar_y2)], fill='#B3B3B3')


def draw_image(res: dict, username: str,
               profile_picture: requests.models.Response | str):
    song_name = res['item']['name']
    album_name = res['item']['album']['name']
    total_time = res['item']['duration_ms']
    current_time = res['progress_ms']
    cover_art_url = res['item']['album']['images'][0]['url']
    artists = ', '.join([x['name'] for x in res['item']['artists']])

    # Create a blank canvas
    canvas = Image.new('RGB', CARD_SIZE, (18, 18, 18))
    draw = ImageDraw.Draw(canvas)

    draw_album_art(canvas, cover_art_url)
    draw_profile_picture(canvas, profile_picture)

    # Draw text on canvas
    draw_text_on_canvas(draw, username, song_name, artists,
                        album_name)

    # Draw progress bar
    draw_progress_bar(draw, current_time, total_time)

    # Return the image
    image = BytesIO()
    canvas.save(image, 'PNG')
    image.seek(0)
    return image
