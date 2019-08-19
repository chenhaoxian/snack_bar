import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw

from utils.parsers import parser_camera_display_info


def pre_adjust_for_dect(frame, scale=0.25):
    assert (scale > 0)
    assert (scale < 1)
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    # rgb_small_frame = small_frame[:, :, ::-1]
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    return rgb_small_frame


def draw_info_on_frame(frame, face_info, scale=0.25, show_distance=False):
    assert (scale > 0)
    assert (scale < 1)
    fallback_scale = int(1 // scale)

    # face_info contain locations and encodings
    # Display the results
    for face in face_info:
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        face_location = face['face_location']
        top = face_location[0] * fallback_scale
        right = face_location[1] * fallback_scale
        bottom = face_location[2] * fallback_scale
        left = face_location[3] * fallback_scale

        label_height = 35
        label_width = right - left
        label_color = (0, 0, 255)
        label_text_shift = 6
        label_text_size = 20
        box_width = 2

        distance_label_height = 35
        distance_label_width = right - left
        distance_label_color = (0, 100, 255)
        distance_label_text_shift = 6
        distance_label_text_size = 20

        # Draw a box around the face
        cv2.rectangle(
            img=frame,
            pt1=(left, top),
            pt2=(right, bottom),
            color=label_color,
            thickness=box_width
        )

        # Draw a label with a name below the face
        frame = _draw_label(
            frame=frame,
            x=left,
            y=bottom,
            width=label_width,
            height=-label_height,
            background_color=label_color,
            text_shift=label_text_shift,
            text_size=label_text_size,
            text=parser_camera_display_info(face["user_info"])
        )

        # Draw a label with the encoding distance
        if show_distance:
            frame = _draw_label(
                frame=frame,
                x=left - box_width // 2,
                y=bottom,
                width=distance_label_width + box_width // 2,
                height=distance_label_height,
                background_color=distance_label_color,
                text_shift=distance_label_text_shift,
                text_size=distance_label_text_size,
                text="distance: %.3f" % (face["distance"],),
            )

    return frame


def _draw_label(frame, x, y, width, height, background_color, text_shift, text_size, text):
    cv2.rectangle(
        img=frame,
        pt1=(x, y + height),
        pt2=(x + width, y),
        color=background_color,
        thickness=cv2.FILLED
    )
    frame = _draw_font_on_frame(
        frame=frame,
        xy=(x + text_shift, y + (height / 2 - text_size / 2)),
        size=text_size,
        text=text
    )
    return frame


def _draw_font_on_frame(frame, xy, size, text):
    path_font = r'pingfangheiti.ttf'

    img = Image.fromarray(frame)
    font = ImageFont.truetype(path_font, size=size, encoding='utf-8')
    draw = ImageDraw.Draw(img)
    draw.text(xy=xy, text=text, font=font)
    frame = np.asanyarray(img)
    return frame


def post_adjust(frame, scale=1, debug=False):
    if debug:
        frame = _draw_font_on_frame(frame, (5, 0), 10, "Debug: On")
    post_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
    return post_frame


def pre_adjust(frame, flip=True):
    pre_frame = cv2.flip(frame, flip)
    return pre_frame
