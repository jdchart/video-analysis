import dvt
import os
import utils

vid = "/Users/jacob/Documents/Repos/video-analysis/test-corpus/short_multishot_test.mp4"
out_path = os.path.join(os.getcwd(), "output", os.path.splitext(os.path.basename(vid))[0] + "_shots.json")

def parse_results(analysis_result, frame_rate):
    ret = {"shots" : []}
    for i in range(len(analysis_result["scenes"]["start"])):
        ret["shots"].append([analysis_result["scenes"]["start"][i] / frame_rate, analysis_result["scenes"]["end"][i] / frame_rate])
    return ret

anno_breaks = dvt.AnnoShotBreaks("/Users/jacob/Documents/Repos/video-analysis/models/dvt_detect_shots.pt")
frame_rate = dvt.video_info(vid)["fps"]
out_breaks = anno_breaks.run(vid)
result_parse = parse_results(out_breaks, frame_rate)

utils.write_json(result_parse, out_path)