# -*- coding: UTF-8 -*-
import cv2
import face_recognition

video = cv2.VideoCapture("short_biden.mp4")
fps = video.get(cv2.CAP_PROP_FPS)
frameCount = video.get(cv2.CAP_PROP_FRAME_COUNT)
size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))

biden_image = face_recognition.load_image_file("biden.jpg")



videoWriter = cv2.VideoWriter('result.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, size)  
# videoWriter = cv2.VideoWriter('result.mp4', cv2.VideoWriter_fourcc(*'MP4V'), fps, size)  
# OpenCV: FFMPEG: tag 0x5634504d/'MP4V' is not supported with codec id 12 and format 'mp4 / MP4 (MPEG-4 Part 14)'
# OpenCV: FFMPEG: fallback to use tag 0x7634706d/'mp4v'
success, frame = video.read()  

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
index = 1

if success:
    # def encoding_imgs(src_imgs):
    # TODO: 解耦合 
    # Get the face encodings for each face in each image file
    # Since there could be more than one face in each image, it returns a list of encodings.
    # But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
    try:
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        gb_frame = frame[:, :, ::-1]
        # first_face_encoding = face_recognition.face_encodings(gb_frame)[0]
        biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
        # obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
        # unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
    except IndexError:
        print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
        quit()

    known_faces = [
        # first_face_encoding,
        biden_face_encoding,
        # obama_face_encoding
    ]

# 为了输出片段时间起止的变量们
time_zones = []
pre_time_i = -1
cur_time_i = 0
left_time = ()
right_time = ()

def get_ms():
    milliseconds = video.get(cv2.CAP_PROP_POS_MSEC)

    seconds = milliseconds//1000
    milliseconds = milliseconds%1000
    minutes = 0
    hours = 0
    if seconds >= 60:
        minutes = seconds//60
        seconds = seconds % 60

    if minutes >= 60:
        hours = minutes//60
        minutes = minutes % 60

    return (int(hours), int(minutes), int(seconds), int(milliseconds))


while success:  
    # cv2.putText(frame, 'fps: ' + str(fps), (0, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,255), 5)
    # cv2.putText(frame, 'count: ' + str(frameCount), (0, 300), cv2.FONT_HERSHEY_SIMPLEX,2, (255,0,255), 5)
    # cv2.putText(frame, 'frame: ' + str(index), (0, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,255), 5)
    # cv2.putText(frame, 'time: ' + str(round(index / 24.0, 2)) + "s", (0,500), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,255), 5)
    
    # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # results = face_recognition.compare_faces(known_faces, gb_frame)
    '''
        Traceback (most recent call last):
    File "v2v_test.py", line 54, in <module>
        results = face_recognition.compare_faces(known_faces, gb_frame)
    File "/Users/linmin/opt/anaconda3/envs/opencv/lib/python3.6/site-packages/face_recognition/api.py", line 226, in compare_faces
        return list(face_distance(known_face_encodings, face_encoding_to_check) <= tolerance)
    File "/Users/linmin/opt/anaconda3/envs/opencv/lib/python3.6/site-packages/face_recognition/api.py", line 75, in face_distance
        return np.linalg.norm(face_encodings - face_to_compare, axis=1)
    ValueError: operands could not be broadcast together with shapes (1,128) (720,1280,3)
    '''

    # Find all the faces and face encodings in the current frame of video

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_names = []
    cur_time_i += 1
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.50)

        # If you had more than 2 faces, you could make this logic a lot prettier
        # but I kept it simple for the demo
        name = None
        if match[0]:
            name = "binden"
        # elif match[1]:
        #     name = "Alex Lacamoire"

        face_names.append(name)
    # Label the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if not name:
            continue

        if pre_time_i == -1:
            pre_time_i = cur_time_i
            left_time = get_ms()
        elif pre_time_i + 1 == cur_time_i:
            pre_time_i += 1
            right_time = get_ms()
        else:
            time_zones.append((left_time, right_time))
            # 下一轮时间区间开始
            pre_time_i = cur_time_i
            left_time = get_ms()

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
    # if not results[0]:
    #     cv2.imshow("not binden", frame)
    #     # 一秒显示帧数张： 因为1000是1秒，然后后面是帧数
    #     # 所以 每帧`1/fps`秒， 1秒 fps帧，所以 fps帧 * 1/fps秒 = 1秒 
    #     # cv2.waitKey(1000 / int(fps))
    #     cv2.waitKey(1000)
    # else:
    #     videoWriter.write(frame)
    # TODO: 这里直接不写帧，然后直接后面通过time_zone用FFmpeg来写帧，这样就可以保存视频了
    # TODO: 但是速度问题需要考虑
    videoWriter.write(frame)
    success, frame = video.read()



    # Write the resulting image to the output video file
    print("Writing frame {} / {}".format(index, frameCount))
    index += 1

print("各片段时间区间集合如下: ")
for time_zone in time_zones:
    print("({}:{}:{}.{}->{}:{}:{}.{})".format(time_zone[0][0], time_zone[0][1],
                                              time_zone[0][2], time_zone[0][3],
                                              time_zone[1][0], time_zone[1][1],
                                              time_zone[1][2], time_zone[1][3]))

video.release()
