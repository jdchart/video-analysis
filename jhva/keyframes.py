import cv2
from .utils import time_region_kwarg_parse, extract_frame
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import numpy as np

class Keyframer:
    def __init__(self, video_path, **kwargs) -> None:
        self.src = video_path
        self.frame_jump = kwargs.get("frame_jump", 2)
        self.num_clusters = kwargs.get("num_clusters", 3)
    
    def run(self, out_path, **kwargs):
        video_capture = cv2.VideoCapture(self.src)

        start, end = time_region_kwarg_parse(video_capture, **kwargs)

        video_capture.set(cv2.CAP_PROP_POS_FRAMES, start)

        frame_corp = None
        frame_count = 0
        kept_frame_count = 0
        
        success, frame = video_capture.read()

        while success and frame_count <= end - start:
            if frame_count % self.frame_jump == 0:
                this_frame = frame.astype(float)
                this_frame = this_frame.flatten()
                
                if frame_corp is None:
                    frame_corp = this_frame
                else:
                    frame_corp = np.vstack((frame_corp, this_frame))

                kept_frame_count = kept_frame_count + 1
            
            frame_count += 1
            success, frame = video_capture.read()
        
        if kept_frame_count == 1:
            to_export_idx = start

            to_export = extract_frame(video_capture, to_export_idx)
            to_export = to_export.astype('uint8')
            cv2.imwrite(f"{out_path}_cluster_0.jpg", to_export)
        elif kept_frame_count <= self.num_clusters:
            for i, frame in enumerate(frame_corp):
                to_export_idx = (i * self.frame_jump) + start

                to_export = extract_frame(video_capture, to_export_idx)
                to_export = to_export.astype('uint8')
                cv2.imwrite(f"{out_path}_cluster_{i}.jpg", to_export)
        else:
            frame_corp = StandardScaler().fit_transform(frame_corp)
            frame_corp = TSNE(n_components = 2, perplexity=2).fit_transform(frame_corp)
            kmeans = KMeans(n_clusters = self.num_clusters, random_state = 0, n_init = "auto")
            clusters = kmeans.fit(frame_corp).labels_   

            for i in range(self.num_clusters):
                # We should probably get the image that is closest to the centre of the cluster,
                # but who's got time for that ? Just get a random image...
                
                to_export_idx = -1

                for j, cluster in enumerate(clusters):
                    if cluster == i:
                        to_export_idx = (j * self.frame_jump) + start # should probably check that this is getting the right frame
                        break
                
                to_export = extract_frame(video_capture, to_export_idx)
                to_export = to_export.astype('uint8')
                cv2.imwrite(f"{out_path}_cluster_{i}.jpg", to_export)
            
        video_capture.release()