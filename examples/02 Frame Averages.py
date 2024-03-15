import jhva
import os
import utils

vid = "/Users/jacob/Documents/Repos/video-analysis/test-corpus/short_multishot_test.mp4"
shots = utils.read_json("/Users/jacob/Documents/Repos/video-analysis/output/short_multishot_test_shots.json")["shots"]
out_dest = os.path.join(os.getcwd(), "output", "frame_averages")

if os.path.isdir(out_dest) == False:
    os.makedirs(out_dest)

for i, shot_data in enumerate(shots):
    print(f"Treating shot {i + 1}/{len(shots)}")
    averager = jhva.FrameAverager(vid)
    out_path =  os.path.join(out_dest, f"frame_average_shot_{i}.jpg")
    averager.run(out_path, start_s = shot_data[0], end_s = shot_data[1])