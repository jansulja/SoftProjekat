import cv2


class Camera:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)

    def show_webcam(self,mirror=False):

        while True:
            ret_val, img = self.camera.read()
            if mirror:
                img = cv2.flip(img, 1)
            cv2.imshow('my webcam', img)
            if cv2.waitKey(1) == 27:
                break  # esc to quit
            #enter
            elif cv2.waitKey(1) == 13:
                cv2.imwrite("IMAGE.jpg",img)

        cv2.destroyAllWindows()
