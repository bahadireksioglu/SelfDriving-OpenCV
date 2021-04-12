import cv2

cap = cv2.VideoCapture(0)

def get_img(display=False, size=[480,240]):
    _, img = cap.read()
    img = cv2.resize(img, (size[0], size[1]))

    if display:
        cv2.imshow("IMG", img)
    return img

if __name__ == '__main__':
    while True:
        img = get_img(True)