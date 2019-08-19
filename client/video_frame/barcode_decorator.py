from pyzbar.pyzbar import decode
import cv2
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import requests
# from config import configuration, logger
import os
import cv2
from skimage.measure import compare_ssim
from utils.store_snack import StoreSnack
from multiprocessing import Process
import time
from config import config_option


class BarcodeDetection(object):
    def __init__(self):
        self.old_frame = None
        self.store_snack = StoreSnack()
        self.have_detection = False


    def _draw_font_on_frame(self,frame, xy, barcode, text):
        path_font = r'pingfangheiti.ttf'

        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)
        draw.rectangle(((barcode.rect.left,barcode.rect.top),(barcode.rect.left+barcode.rect.width, barcode.rect.top+barcode.rect.height)),outline='#e945ff')
        draw.text(xy=(barcode.rect.left,barcode.rect.top+barcode.rect.height+10), text=text)
        frame = np.asanyarray(img)
        return frame


    def _draw_barcode_frame(self, frame, barcode_infos, product_info):
        for barcode in barcode_infos:
            top = barcode.rect.top
            bottom = top+barcode.rect.height
            left = barcode.rect.left
            right = left+barcode.rect.width

            frame = self._draw_font_on_frame(frame, (left + 6, bottom - 27.5),
                                        barcode, product_info)
        return frame

    def barcode_decorator_(self, frame, order_data):
        now_time = time.time()
        self.have_detection = False
        if (self.old_frame is not None and self.old_frame.any()):
            self.old_frame = {'frame':frame, time:time.time()}
        elif(now_time - self.old_frame['time'] > 2):
            self.old_frame = {'frame': frame, time: time.time()}
            barcode_info = decode(frame)
            if (any(barcode_info)):
                stock_snack_process = Process(target=self.store_snack.store, args=(barcode_info, order_data))
                stock_snack_process.start()
                product_info = 'test'
                frame = self._draw_barcode_frame(frame, barcode_info[0:1], product_info)
                self.have_detection = True
        return self.have_detection, frame


    def barcode_decorator(self,frame, order_data):

        # frame_change = self._is_object_font_of_camera_change(frame)
        # if(frame_change):
        #     self.have_detection = False

        #
        # print(self.haveDetectBarcode)
        # if(frame_change and not self.have_detection):
            # product_info = get_product_info(barcode_info[0:1])
            # haveDetectBarcode = True
        barcode_info = decode(frame)
        if(any(barcode_info)):
                # stock_snack_process = Process(target=self.store_snack.store, args=(barcode_info, order_data))
            self.store_snack.store(barcode_info, order_data)
                # stock_snack_process.start()
                # stock_snack_process.join()
            product_info = 'test'
            frame = self._draw_barcode_frame(frame, barcode_info[0:1], product_info)
            self.have_detection = True
        return self.have_detection, frame


    def _is_object_font_of_camera_change(self, new_frame):
        if (self.old_frame is not None and self.old_frame.any()):
            old_gray = cv2.cvtColor(self.old_frame, cv2.COLOR_BGR2GRAY)
            new_gray = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
            (score, diff) = compare_ssim(old_gray, new_gray, full=True)
            self.old_frame = new_frame
            # print(score)
            if (score > 0.75):
                return False
            else:
                return True
        else:
            self.old_frame = new_frame
            return True
        # return True


if __name__=='__main__':
    # image = Image.open('/home/deeplearning/snack_bar/client/barcode.png')
    image = cv2.imread('/home/deeplearning/snack_bar/client/barcode.png')
    height, width = image.shape[:2]
    # cv2.cvtColor(image, cv2.COLOR_BAYER_BG2GRAY)
    code = decode((image[:,:,0].astype('uint8').tobytes(),width,height))
    print(code)