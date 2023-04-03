import math
import time
import argparse

from rockx import RockX
import cv2


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="RockX Pose Demo")
    parser.add_argument('-c', '--camera', help="camera index", type=int, default=10)
    parser.add_argument('-d', '--device', help="target device id", type=str)
    args = parser.parse_args()

    pose_body_handle = RockX(RockX.ROCKX_MODULE_POSE_BODY, target_device=args.device)

    cap = cv2.VideoCapture(args.camera)
    cap.set(3, 1280)
    cap.set(4, 720)
    last_face_feature = None
    timer_on=0 #计时器开启变量
    se=0 
    start=0
    choose=0 #选择该运动
    success_time=0
    #警告初始化
    warning_time=0 
    completion_degree=0 #完成度初始化
    #新月式
    moon=0
    #女神式
    Goddess=0
    #风吹树式
    tree=0
    pose=0
    while True:
        ret, frame = cap.read()
        in_img_h, in_img_w = frame.shape[:2]
        ret, results = pose_body_handle.rockx_pose_body(frame, in_img_w, in_img_h, RockX.ROCKX_PIXEL_FORMAT_BGR888)

        index = 0
        for result in results:
            for p in result.points:
                cv2.circle(frame, (p.x, p.y), 3, (0, 255, 0), 3)
            for pairs in RockX.ROCKX_POSE_BODY_KEYPOINTS_PAIRS:
                pt1 = result.points[pairs[0]] #一对中左边的点
                pt2 = result.points[pairs[1]] #一对中右边的点
                if pt1.x <= 0 or pt1.y <= 0 or pt2.x <= 0 or pt2.y <= 0:
                    continue
                cv2.line(frame, (pt1.x, pt1.y), (pt2.x, pt2.y), (255, 0, 0), 2)

            #计算躯干斜率
            nose = result.points[0]
            neck = result.points[1]
            rsho = result.points[2]
            relb = result.points[3]
            rwr = result.points[4]
            lsho = result.points[5]
            lelb = result.points[6]
            lwr = result.points[7]
            rhip = result.points[8]
            rknee = result.points[9]
            rank = result.points[10]
            lhip = result.points[11]
            lknee = result.points[12]
            lank = result.points[13]
            reye = result.points[14]
            leye = result.points[15]
            rear = result.points[16]
            lear = result.points[17]
            #斜率初始化
            m1=2000
            m2=2000
            m3=2000
            m4=2000
            m5=2000
            m6=2000
            m7=2000
            m8=2000
            m9=2000
            m10=2000

            pose=-1  
            

            if (neck.x-rhip.x) != 0 :
                m1=(neck.y-rhip.y) / (neck.x-rhip.x)
                
            if (rhip.x-rknee.x) != 0 :
                m2=(rhip.y-rknee.y) / (rhip.x-rknee.x)
                
            if (neck.x-lhip.x) != 0:
                m4=(neck.y-lhip.y) / (neck.x-lhip.x)
                
            if (lhip.x-lknee.x) != 0:
                m5=(lhip.y-lknee.y) / (lhip.x-lknee.x)
                
            if (rknee.x-rank.x) != 0:
                m3=(rknee.y-rank.y) / (rknee.x-rank.x)
                
            if (lknee.x-lank.x) != 0:
                m6=(lknee.y-lank.y) / (lknee.x-lank.x)
                
            if (rsho.x-relb.x) != 0:
                m7=(rsho.y-relb.y) / (rsho.x-relb.x)
                
            if (relb.x-rwr.x) != 0:
                m8=(relb.y-rwr.y) / (relb.x-rwr.x)
                
            if (lsho.x-lelb.x) != 0:
                m9=(lsho.y-lelb.y) / (lsho.x-lelb.x)
                
            if (lelb.x-lwr.x) != 0:
                m10=(lelb.y-lwr.y) / (lelb.x-lwr.x)
                
            print('m2',m2)
            print('m5',m5)
            print('m3',m3)
            print('m6',m6)

            
            #判定女神式
            if m2>=-1.5 and m2<=-0.5 and m5>=0.5 and m5<=1.5 and m3>=2 and m3<=1000 and m6>=-1000 and m6<=-2 :
                pose=1
            #新月式
            #elif m7>-1 and m5<1 and m8>0 and m6<20:                
                #pose=2
            #风吹树式
            elif m7>=0.1 and m7<=10 and m8>=0.1 and m8<=10 and m9>=0.1 and m9<=10 and m10>=0.1 and m10<=10:
                pose=3
            else:
                pose=-1
             

            #进入新月式准备
            if pose==2 and se==0:
                se=1
                moon=1 #判定进入新月式
                print('New_Moon_please hold on!')
                time.sleep(4)
                timer_on=1

            #进入女神式准备
            if pose==1 and se==0 :
                se=1
                Goddess=1 #判定进入女神式
                print('Yoga_Goddess_please hold on!')
                time.sleep(4)
                timer_on=1

            #进入风吹树式准备
            if pose==3 and se==0:
                se=1
                tree=1 #判定进入风吹树式
                print('Tree_please hold on!')
                time.sleep(4)
                timer_on=1

            #判定是否开启计时器
            if timer_on==1:
                begin_time=time.time()
                timer_on=0
                start=1
                print('start timing!')
        

            #新月式计时-15s
            if start==1 and moon==1 and pose==2 :
                success_time=success_time+1
                end_time=time.time()
                during=end_time-begin_time
                print(during)
                if during>=15:
                    completion_degree=(success_time)/(success_time+warning_time)
                    print('New_Moon-Done! Congrulations!')
                    print(completion_degree)
                    success_time=0
                    warning_time=0
                    start=0
                    se=0
                    moon=0
            elif start==1 and moon==1 and pose !=2:
                warning_time=warning_time+1
                print('Not standard')
                end_time_2=time.time()
                during=end_time_2-begin_time
                if during>15:
                    completion_degree=(success_time)/(success_time+warning_time)
                    print('New_Moon-Done! Congrulations!')
                    print(completion_degree)
                    success_time=0
                    warning_time=0
                    start=0
                    se=0
                    moon=0

            #女神式计时-15s
            if start==1 and Goddess==1 and pose==1 :
                success_time=success_time+1
                end_time=time.time()
                during=end_time-begin_time
                print(during)
                if during>=15:
                    completion_degree=(success_time)/(success_time+warning_time)
                    print('Yoga_Goddess-Done! Congrulations!')
                    print(completion_degree)
                    success_time=0
                    warning_time=0
                    start=0
                    se=0
                    Goddess=0
            elif start==1 and Goddess==1 and pose !=1:
                warning_time=warning_time+1
                print('Not standard')
                end_time_2=time.time()
                during=end_time_2-begin_time
                if during>15:
                    completion_degree=(success_time)/(success_time+warning_time)
                    print('Yoga_Goddess-Done! Congrulations!')
                    print(completion_degree)
                    success_time=0
                    warning_time=0
                    start=0
                    se=0
                    Goddess=0

            #风吹树式计时-15s
            if start==1 and tree==1 and pose==3 :
                success_time=success_time+1
                end_time=time.time()
                during=end_time-begin_time
                print(during)
                if during>=15:
                    completion_degree=(success_time)/(success_time+warning_time)
                    print('Tree-Done! Congrulations!')
                    print(completion_degree)
                    success_time=0
                    warning_time=0
                    start=0
                    se=0
                    tree=0
            elif start==1 and tree==1 and pose !=3:
                warning_time=warning_time+1
                print('Not standard')
                end_time_2=time.time()
                during=end_time_2-begin_time
                if during>15:
                    completion_degree=(success_time)/(success_time+warning_time)
                    print('Tree-Done! Congrulations!')
                    print(completion_degree)
                    success_time=0
                    warning_time=0
                    start=0
                    se=0
                    tree=0
                

            
            index += 1

        cv2.imshow('RockX Pose - ' + str(args.device), frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    pose_body_handle.release()
