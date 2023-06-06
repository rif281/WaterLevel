import numpy as np
import cv2

def top_level(image, rows, cols):
    sum1 = 0
    mx_sum = 0
    row_mx = 0
    total_sum = 0
    for i in range(0, int(0.6*rows)):
        for j in range(int(cols / 2) - 80, int(cols / 2) + 80):
            sum1 += image[i, j]
            total_sum += image[i, j]
            if i % 15 == 0:
                sum2 = sum1
                sum1 = 0
                if sum2 >= mx_sum:
                    row_mx = i
                    mx_sum = sum2
    return row_mx, total_sum

def water_level_check(image, last, cols,glass):
    sum1 = 0
    mx_sum = 0
    water_mx = 0
    for i in range(glass+20, last):
        for j in range(int(cols / 2) - 35, int(cols / 2) + 35):
            sum1 += image[i, j]
            if i % 25 == 0 and i < last:
                sum2 = sum1
                sum1 = 0
                if sum2 >= mx_sum and sum2 > 10000:
                    water_mx = i
                    last = water_mx
                    mx_sum = sum2
                else:
                    water_mx = last
    return water_mx, last

cap = cv2.VideoCapture(2)

frames = 0
movement_check = 1
total_sum_B = 0
top_row_index_B = 0
glass_height = 0
flag = 0
empty_glass = np.zeros((480,640))
edges2 = np.zeros((480,640))
lower_limit = 470
water_level = 470


while True:
    ret, frame = cap.read() #frame=video, ret- checks if the video is ok
    width = int(cap.get(3))
    height = int(cap.get(4))

    frames += 1

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if frames%15 == 0 or frames == 1: #make the line more stable
        edges = cv2.Canny(gray_frame, 15, 130)

    if frames%10 == 0 or frames == 1: #make the line more stable
        top_row_index_A, total_sum_A = top_level(edges, height, width)

    if frames%15 == 0 :
        top_row_index_B, total_sum_B = top_level(edges, height, width)
        if abs(top_row_index_A - top_row_index_B) == 0:
            movement_check += 1
        else:
            movement_check = 0

    if movement_check > 10 and flag == 0:
        glass_height = top_row_index_A
        empty_glass = edges
        flag = 1

    if glass_height > 0:
        if water_level-glass_height >= 70:
            draw = cv2.putText(frame, "water puring began :)", (110, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            draw = cv2.line(frame, (0, glass_height), (width, glass_height), (255, 0, 255), 15)
            edges2 = edges-empty_glass
            water_level, lower_limit = water_level_check(edges2, lower_limit, width, glass_height)
            print("water level is: ", water_level)
            draw = cv2.line(frame, (270, water_level), (370, water_level), (255, 255, 0), 5)
        else:
            draw = cv2.putText(frame, "water pouring was finished", (110, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)



    else:
        draw = cv2.line(frame, (0, top_row_index_A), (width, top_row_index_A), (255, 0, 0), 15)


    #cv2.imshow('edges',edges)
    cv2.imshow('frame', frame)
    #cv2.imshow('edges2', edges2)
    #cv2.imshow('empty glass', empty_glass)


    if cv2.waitKey(1) == ord('q'): #quit when q is pressed. check every 1msec
        break

cap.release() #let other apps use the camera
cv2.destroyAllWindows()

