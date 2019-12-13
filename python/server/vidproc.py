
#import cv2
import os
import json
import numpy as np
import pandas as pd

def convert_to_csv(folder):
    columns = ['score_overall', 'nose_score', 'nose_x', 'nose_y', 'leftEye_score', 'leftEye_x', 'leftEye_y',
               'rightEye_score', 'rightEye_x', 'rightEye_y', 'leftEar_score', 'leftEar_x', 'leftEar_y',
               'rightEar_score', 'rightEar_x', 'rightEar_y', 'leftShoulder_score', 'leftShoulder_x', 'leftShoulder_y',
               'rightShoulder_score', 'rightShoulder_x', 'rightShoulder_y', 'leftElbow_score', 'leftElbow_x',
               'leftElbow_y', 'rightElbow_score', 'rightElbow_x', 'rightElbow_y', 'leftWrist_score', 'leftWrist_x',
               'leftWrist_y', 'rightWrist_score', 'rightWrist_x', 'rightWrist_y', 'leftHip_score', 'leftHip_x',
               'leftHip_y', 'rightHip_score', 'rightHip_x', 'rightHip_y', 'leftKnee_score', 'leftKnee_x', 'leftKnee_y',
               'rightKnee_score', 'rightKnee_x', 'rightKnee_y', 'leftAnkle_score', 'leftAnkle_x', 'leftAnkle_y',
               'rightAnkle_score', 'rightAnkle_x', 'rightAnkle_y']
    data = json.loads(open(folder + 'keypoints.json', 'r').read())
    csv_data = np.zeros((len(data), len(columns)))
    for i in range(csv_data.shape[0]):
        one = []
        one.append(data[i]['score'])
        for obj in data[i]['keypoints']:
            one.append(obj['score'])
            one.append(obj['position']['x'])
            one.append(obj['position']['y'])
        csv_data[i] = np.array(one)
    df = pd.DataFrame(csv_data, columns=columns)#, index_label='Frames#')
    df.to_csv(folder + 'keypoints.csv')
    return df

#def extract_frames(folder, file):
#    video = cv2.VideoCapture(folder + file)
#    flip =True
#    count = 0
#    success = 1
#    arr_img = []
#    # If such a directory doesn't exist, creates one and stores its Images
#    if not os.path.isdir(folder + os.path.splitext(file)[0] + "/"):
#        os.mkdir(folder + os.path.splitext(file)[0])
#        new_path = folder + os.path.splitext(file)[0]
#        while success:
#            success, image = video.read()
#            # Frames when generated are getting rotated clockwise by above method, so #correcting it
#            if flip:
#                image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
#            arr_img.append(image)
#            count += 1
#        # Sub sampling the number of frames
#        # numbers = sorted(random.sample(range(len(arr_img)), 45))
#        count = 0
#        for i in range(len(arr_img)):
#            cv2.imwrite(new_path + "/%d.png" % count, arr_img[i])
#            count += 1
#
#
#def extract_df(folder, file):
#    extract_frames(folder, file)
#    os.system("node posenet/scale_to_videos.js")
#    frames, _ = os.path.splitext(file)
#    return convert_to_csv(folder + frames + '/')