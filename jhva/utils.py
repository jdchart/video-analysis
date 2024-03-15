import cv2

def seconds_to_frames(seconds, fr):
    return int(seconds * fr)

def time_region_kwarg_parse(vid_cap, **kwargs):

    fr = vid_cap.get(cv2.CAP_PROP_FPS)

    if "start_s" in kwargs:
        start = seconds_to_frames(kwargs.get("start_s"), fr)
    else:
        start = kwargs.get("start", 0)

    if "end_s" in kwargs:
        if kwargs.get("end_s") == -1:
            end = int(vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        else:
            end = seconds_to_frames(kwargs.get("end_s"), fr)
    else:
        end = kwargs.get("end", -1)
        if end == -1:
            end = int(vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))

    return start, end

def extract_frame(vid_cap, frame_number):
    vid_cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    ret, frame = vid_cap.read()

    return frame