import jhva
import os
import utils

vid = "/Users/jacob/Documents/Repos/video-analysis/test-corpus/short_multishot_test.mp4"
shots = utils.read_json("/Users/jacob/Documents/Repos/video-analysis/output/short_multishot_test_shots.json")["shots"]
out_dest = os.path.join(os.getcwd(), "output", "keyframes")

for i, shot_data in enumerate(shots):
    print(f"Treating shot {i + 1}/{len(shots)}")
    
    if shot_data[1] - shot_data[0] > 0:
        keyframer = jhva.Keyframer(vid, frame_jump = 10)
        
        out_path =  os.path.join(out_dest, f"keyframe_shot_{i}", "keyframe")
        if os.path.isdir(os.path.join(out_dest, f"keyframe_shot_{i}")) == False:
            os.makedirs(os.path.join(out_dest, f"keyframe_shot_{i}"))
        
        keyframer.run(out_path, start_s = shot_data[0], end_s = shot_data[1])