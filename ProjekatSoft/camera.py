import cv2
import datetime

class Camera:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)

    def show_webcam(self,mirror=False):

        while True:
            ret_val, img = self.camera.read()
            if mirror:
                img = cv2.flip(img, 0)
            cv2.imshow('my webcam', img)
            key = cv2.waitKey(1)

            if key == 27:
                break  # esc to quit
            #enter
            elif key == 13:
                print 'enter'
                now = datetime.datetime.now()
                img_name = str(now.year) + str(now.month)+ str(now.day) +  str(now.hour) +  str(now.minute) + str(now.second)
                print  img_name
                cv2.imwrite("images/camera/" + img_name +".jpg",img)

                cv2.destroyAllWindows()
                return img


        cv2.destroyAllWindows()
