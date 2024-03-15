import cv2
from .utils import time_region_kwarg_parse

class FrameAverager:
    def __init__(self, video_path) -> None:
        self.src = video_path

    def run(self, out_path, **kwargs):
        video_capture = cv2.VideoCapture(self.src)

        start, end = time_region_kwarg_parse(video_capture, **kwargs)

        video_capture.set(cv2.CAP_PROP_POS_FRAMES, start)

        total_pixels = None
        frame_count = 0
        
        success, frame = video_capture.read()

        while success and frame_count <= end - start:
            if total_pixels is None:
                total_pixels = frame.astype(float)
            else:
                total_pixels += frame.astype(float)
            
            frame_count += 1
            success, frame = video_capture.read()

        average_pixels = total_pixels / frame_count

        average_pixels = average_pixels.astype('uint8')

        cv2.imwrite(out_path, average_pixels)
        video_capture.release()