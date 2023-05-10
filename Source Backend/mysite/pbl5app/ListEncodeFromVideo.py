import cv2
import os
import face_recognition
import pandas as pd

resize = 300
def Mahoa (images):
    
    # encodeList = []
    # for img, index in zip(images, range(len(images))):
    #     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #     locationFace = face_recognition.face_locations(img)
    #     if len(locationFace) != 0:
    #         # img = cv2.resize(img, (0, 0), None, fx=0.5, fy=0.5)
    #         # #print ten len frame
    #         # y1, x2, y2, x1 = locationFace[0]
    #         # # y1, x2, y2, x1 = y1*2, x2*2, y2*2, x1*2
    #         # cv2.rectangle(img, (x1//2, y1//2), (x2//2, y2//2), (255, 0, 255), 2)
    #         # print("vao day")
    #         # cv2.imshow('anh khuon mat', img)
            
    #         y1, x2, y2, x1 = locationFace[0]
    #         print(locationFace[0])
    #         paddingX = int((x2-x1)*0.2)
    #         paddingY = int((y2-y1)*0.2)
    #         # Get original height and width
    #         h, w, c = img.shape
    #         print("Original Height and Width:", h, "x", w)
    #         cropped_img = img[max(y1-paddingY,0):min(y2+paddingY, h), max(x1-paddingX,0):min(x2+paddingX, w)]
    #         down_width = int(resize)
    #         down_height = int((y2-y1)*resize/(x2-x1))
    #         down_points = (down_width, down_height)
    #         resize_down = cv2.resize(cropped_img, down_points, interpolation=cv2.INTER_LINEAR)
    #         # Get original height and width
    #         h1, w1, c1 = resize_down.shape
    #         print("Original Height and Width:", h1, "x", w1)
    #         encode = face_recognition.face_encodings(resize_down)
    #         if len(encode) != 0:
    #             encode = encode[0]
    #             encodeList.append(encode)

    #     if cv2.waitKey(1)==ord("q"): #độ trễ 1/1000s, nếu bấm q sẽ thoát
    #         break
    # return encodeList
    list_encodes = []
    for image in images:
        framS = cv2.resize(image, (0, 0), None, fx=0.5, fy=0.5)
        framS = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(framS)
        for encode in encodes:
            list_encodes.append(encode)
    return list_encodes

def ListEncodeVideo(cap):
    # Thời điểm của 11 khung hình bạn muốn cắt ra
    # # print("##########################################################################################")
    # # print("da nhan duoc video")
    # # if os.path.exists(path):
    # #     print("File video tồn tại!")
    # # else:
    # #     print("Đường dẫn đến file video không đúng hoặc file video không tồn tại!")
    # # # Lấy tổng số khung hình của video
    # # total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # # print("tong frames:")
    # # print(total_frames)
    # # Lấy tần số khung hình của video
    # fps = cap.get(cv2.CAP_PROP_FPS)

    # # Đặt con trỏ đến khung hình cuối cùng
    # cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)

    # # Đọc khung hình cuối cùng
    # ret, frame = cap.read()

    # # Lấy thời gian tính bằng mili giây của khung hình cuối cùng
    # end_time_ms = cap.get(cv2.CAP_PROP_POS_MSEC)

    # Tính thời gian của video
    # duration_sec = end_time_ms / 1000

    # print(f"Thời gian của video là: {duration_sec} giây")
    times = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5]

    # Tạo thư mục folder1 nếu nó không tồn tại
    if not os.path.exists('folder1'):
        os.makedirs('folder1')

    images = []
    # Lặp qua các thời điểm và cắt ảnh
    for i, t in enumerate(times):
        # Đặt chỉ số khung hình
        frame_idx = int(t * cap.get(cv2.CAP_PROP_FPS))
        # Đặt con trỏ đến khung hình cần cắt
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        # Đọc khung hình
        ret, frame = cap.read() 
        
        cv2.imwrite(f'folder1/frame{i}.jpg', frame)
        images.append(frame) 

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return Mahoa(images)

if __name__ == "__main__":
    # Đường dẫn đến video của bạn
    video_path = r'C:\Users\cuong\OneDrive\Desktop\GIthub\PBL5\Source Backend\mysite\static\videos\275256075_1345597292551162_374868419468071193_n.mp4'
    # Load video
    cap = cv2.VideoCapture(video_path)
    # lấy danh sách encode từ video
    list_encodes = ListEncodeFromVideo(cap)
    # lưu encode vào file
    df = pd.DataFrame(list_encodes)
    df.to_csv("AnacondaFace/system/SaveDir/list_encodes_client.csv", index=False)