from SelfDrivingCarWithOpenCV import lane_detection_module as ldm
from SelfDrivingCarWithOpenCV import webcam_module as wcm
from SelfDrivingCarWithOpenCV import motor_driver_module as mdm

##################################################
motor = mdm(2, 3, 4, 17, 22, 27)


##################################################

def main():
    img = wcm.get_img()
    curve_val = ldm(img, 1)

    sen = 1.3  # SENSITIVITY
    max_val = 0.3  # MAX SPEED
    if curve_val > max_val: curve_val = max_val
    if curve_val < -max_val: curve_val = -max_val
    # print(curveVal)
    if curve_val > 0:
        sen = 1.7
        if curve_val < 0.05: curve_val = 0
    else:
        if curve_val > -0.08: curve_val = 0
    motor.move(0.20, -curve_val * sen, 0.05)
    # cv2.waitKey(1)


if __name__ == '__main__':
    while True:
        main()
