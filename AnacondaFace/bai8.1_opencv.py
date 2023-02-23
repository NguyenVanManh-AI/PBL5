import cv2
import face_recognition

imgElon = face_recognition.load_image_file("train/Elon_Musk_Train.jpg")
# chuyen lai thanh RGB
imgElon = cv2.cvtColor(imgElon, cv2.COLOR_BGR2RGB)

imgElonCheck = face_recognition.load_image_file("check/Elon_Musk_Check.jpg")
imgElonCheck = cv2.cvtColor(imgElonCheck, cv2.COLOR_BGR2RGB)

#xác định vị trí khuôn mặt
faceLoc = face_recognition.face_locations(imgElon)[0]
print(faceLoc) #(y1, x2, y2, x1)
#mã hóa hình ảnh
encodeElon = face_recognition.face_encodings(imgElon)[0]
cv2.rectangle(imgElon,(faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255,0,255), 2)



faceCheck = face_recognition.face_locations(imgElonCheck)[0]
encodeCheck = face_recognition.face_encodings(imgElonCheck)[0]
cv2.rectangle(imgElonCheck,(faceCheck[3], faceCheck[0]), (faceCheck[1], faceCheck[2]), (255,0,255), 2)

#kiểm tra nhận diện
result = face_recognition.compare_faces([encodeElon], encodeCheck)
#tính sai số (khoản cách) giữa train và check là bao nhiêu?
faceDis = face_recognition.face_distance([encodeElon], encodeCheck)
print(result, faceDis)
cv2.putText(imgElonCheck, f"{result}{round(1-faceDis[0], 2)}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


#hiển thị ra màn hình
cv2.imshow("Elon", imgElon)
cv2.imshow("ElonCheck", imgElonCheck)
cv2.waitKey()