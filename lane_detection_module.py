import cv2
import numpy as np
import SelfDrivingCarWithOpenCV.utils as utils

curve_list = []
avg_val = 10

def get_lane_curve(img, display = 2):
    img_copy = img.copy()
    img_result = img.copy()

    # Step 1
    img_threshold = utils.thresholding(img)

    # Step 2
    h_t, w_t, c = img.shape
    points = utils.val_trackbars()
    img_warp = utils.warp_img(img_threshold, points, w_t, h_t)
    img_warp_points = utils.draw_points(img_copy, points)

    #Step 3
    mid_point, img_histogram = utils.get_histogram(img_warp, display=True, min_per=0.5, region=4)
    curve_average_point, img_histogram = utils.get_histogram(img_warp, display=True, min_per=0.5)
    curve_raw = curve_average_point - mid_point

    #Step 4
    curve_list.append(curve_raw)
    if len(curve_list) > avg_val:
        curve_list.pop(0)
    curve = int(sum(curve_list) / len(curve_list))

    #Step 5
    if display != 0:
        img_inv_warp = utils.warp_img(img_warp, points, w_t, h_t, inverse=True)
        img_inv_warp = cv2.cvtColor(img_inv_warp, cv2.COLOR_GRAY2BGR)
        img_inv_warp[0:w_t // 3, 0:w_t] = 0, 0, 0
        img_lane_color = np.zeros_like(img)
        img_lane_color[:] = 0, 255, 0
        img_lane_color = cv2.bitwise_and(img_inv_warp, img_lane_color)
        img_result = cv2.addWeighted(img_result, 1, img_lane_color, 1, 0)
        mid_y = 450
        cv2.putText(img_result, str(curve), (w_t // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(img_result, (w_t // 2, mid_y), (w_t // 2 + (curve * 3), mid_y), (255, 0, 255), 5)
        cv2.line(img_result, ((w_t // 2 + (curve * 3)), mid_y - 25), (w_t // 2 + (curve * 3), mid_y + 25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = w_t // 20
            cv2.line(img_result, (w * x + int(curve // 50), mid_y - 10),
                     (w * x + int(curve // 50), mid_y + 10), (0, 0, 255), 2)
        #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        #cv2.putText(imgResult, 'FPS ' + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 50, 50), 3);
    if display == 2:
        img_stacked = utils.stack_images(0.7, ([img, img_warp_points, img_warp],
                                             [img_histogram, img_lane_color, img_result]))
        cv2.imshow('ImageStack', img_stacked)
    elif display == 1:
        cv2.imshow('Result', img_result)

    #Normalization
    curve = curve / 100
    if curve > 1: curve == 1
    if curve < -1: curve == -1

    return curve

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    initial_trackbar_vals = [102, 80, 20, 214] # Trackbar vals must be readjusted according to the lane.
    utils.initialize_trackbars(initial_trackbar_vals)
    frame_counter = 0

    while True:
        frame_counter += 1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frame_counter:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frame_counter = 0

        success, img = cap.read()
        img = cv2.resize(img, (480, 240))
        curve = get_lane_curve(img, display=2)
        print(curve)
        #cv2.imshow('Video', img)
        cv2.waitKey(1)
