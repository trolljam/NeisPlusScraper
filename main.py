from selenium.webdriver.support.select import Select
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import matplotlib.font_manager as fm
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import getpass
import re
import matplotlib
import matplotlib.pyplot as plt


def findSubjectPer(input_string): #"과목(단위수)"에서 단위수 검색
    pattern = r'\((\d)\)'
    matches = re.findall(pattern, input_string)
    single_digit_numbers = [int(match) for match in matches]
    return single_digit_numbers[0]

def score(input_string : str): #"등수(동석차수)/응시생수"로 등급 계산
    tie_rank = None
    
    matches = re.findall(r'[0-9]+', input_string) #함수의 매개변수인 input_string중 있는 모든 숫자를 검색함
    
    if len(matches) ==2 : #숫자가 두개("등수/응시생수"의 형태일때 -> 동점자 0명 )
        my_rank = int(matches[0])
        total_students = int(matches[1])
    elif len(matches) == 3: #숫자가 세개 ("등수(동석차수)/응시생수"의 형태일때 -> 동점자 존재)
        my_rank = int(matches[0])
        tie_rank = int(matches[1])
        total_students = int(matches[2])
    else:
        raise "func score ERROR"
    
    if tie_rank is None:
        # 동점자가 없는 경우
        percentile = my_rank / total_students * 100
    else:
        # 동점자가 있는 경우
        percentile = (my_rank - 1 + (tie_rank - 1) / 2) / total_students * 100

    if percentile <= 4:
        return 1
    elif percentile <= 11:
        return 2
    elif percentile <= 23:
        return 3
    elif percentile <= 40:
        return 4
    elif percentile <= 60:
        return 5
    elif percentile <= 77:
        return 6
    elif percentile <= 89:
        return 7
    elif percentile <= 96:
        return 8
    else:
        return 9

def nextcomb(input_list):
    if input_list[2] == 2:
        if input_list[1] ==2:
            return [input_list[0]+1, 1,1]
        else:
            return [input_list[0], 2, 1]
    else:
        return [input_list[0], input_list[1], input_list[2]+1] #다음 시험의 리스트값

def combination(start, end): #nexcomb함수를 이용한 범위내 모든 시험의 리스트값 반환 ex) 1-1-1 ~ 1-2-1 -> [[1,1,1], [1,1,2], [1,2,1]] 
    result = [start]
    while not(end in result):
        start = nextcomb(start)
        result.append(start)
    return result


total = []

def main():
    username = input("아이디: ")
    pw = getpass.getpass('비밀번호: ')
    
    
    print("2-1-2 -> 2학년 1학기 기말 / 1-2-2 -> 1학년 2학기 기말\n")
    
    while True:
        start_exam = input("From? ")
        end_exam = input("To? ")
        print("\n")
        
        start_matches = re.findall(r"[1-3]+", start_exam) #"1-1-1" -> [1,1,1]형태(리스트 형)로 변환
        end_matches = re.findall(r"[1-3]+", end_exam) #1-1-1 -> [1,1,1]형태(리스트 형)로 변환
        
        if len(start_matches) != 3 or len(end_matches) != 3 or start_matches[0] > end_matches[0] or (start_matches[0] == end_matches[0] and start_matches[1] > end_matches[1]) or (start_matches[0] == end_matches[0] and start_matches[1] == end_matches[1] and start_matches[2] > end_matches[2]):
            print("유효한 값을 입력해주세요.\n")
            time.sleep(2)
            continue
        else: break
        
    start_matches = [eval(i) for i in start_matches]
    end_matches = [eval(j) for j in end_matches] 
        
        
        
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36')
    options.add_argument('--mute-audio') #음소거 옵션
    options.add_argument('incognito') #시크릿 모드
    options.add_experimental_option('excludeSwitches', ['enable-logging']) #로그메세지 출력하지 않음
    
    driver = webdriver.Chrome(options)
    driver.get("https://www.neisplus.kr/")
    driver.maximize_window()
    
    driver.execute_script("window.open()")
    driver.switch_to.window(driver.window_handles[0])
    
    try:
        WebDriverWait(driver, 0.3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/img'))).click()
    except Exception:
        pass
    
    driver.find_element(By.XPATH, '//*[@id="scroll-section-0"]/div[1]/div/a').click() #"들어가기" 버튼
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/div[1]/div/div[3]/div/div/div')))
        
    driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/div[1]/div/div[3]/div/div/div/div/div/div[5]/div/div[1]/div[2]/div/div/img').click()
    time.sleep(0.1)
    
    driver.find_element(By.XPATH, '//*[@id="mainframe.VFrameSet.frameMain.form.divAll.form.divWork.form.tabLogin.tpgID.form.edtUsrid:input"]').send_keys(username) 
    driver.find_element(By.XPATH, '//*[@id="mainframe.VFrameSet.frameMain.form.divAll.form.divWork.form.tabLogin.tpgID.form.edtPass:input"]').send_keys(pw)
    
    driver.find_element(By.XPATH, '//*[@id="mainframe.VFrameSet.frameMain.form.divAll.form.divWork.form.tabLogin.tpgID.form.btnConfirm:icontext"]').click() #로그인
    
    time.sleep(0.3)
    
    driver.close()
    driver.switch_to.window(driver.window_handles[0]) #자동화 프로그램으로 로그인 버튼을 누를시 다음으로 넘어가지 않는 현상이 일어남 -> 시작할때 열어둔 다른 탭에서 작업을 이어가도록 설정
    
    driver.get("https://neisplus.kr/csp-std/#/std-edi/edi-sel/edi-sel-ls030") #성적 확인 주소로 이동
    
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/csp-std-edi/div/csppage/csp-page/csp-wygwyg-hr-layout/div[2]/cspview/csp-view/csp-cond/form/div/button')))
    except:
        print("틀린 사용자 이름 / 비밀번호이거나 로딩이 너무 오래걸립니다")
        return False
    
    time.sleep(0.1)
    
    grade_sel = Select(driver.find_element(By.XPATH, '/html/body/app-root/csp-std-edi/div/csppage/csp-page/csp-wygwyg-hr-layout/div[2]/cspview/csp-view/csp-cond/form/div/div/div[1]/select'))
    semester_sel = Select(driver.find_element(By.XPATH, '/html/body/app-root/csp-std-edi/div/csppage/csp-page/csp-wygwyg-hr-layout/div[2]/cspview/csp-view/csp-cond/form/div/div/div[2]/select'))
    exam_sel = Select(driver.find_element(By.XPATH, '/html/body/app-root/csp-std-edi/div/csppage/csp-page/csp-wygwyg-hr-layout/div[2]/cspview/csp-view/csp-cond/form/div/div/div[3]/select'))
    
    
    
    
    count = 0
    for i in combination(start_matches, end_matches): #시험 지정 -> 조회버튼 누름 -> 테이블에서 2차원 데이터(과목, 과목별 데이터) 읽어옴 -> 과목별로 분류 -> 과목별 데이터를 정리후 3차원 배열인 total에 저장(total[시험][과목][과목(단위수), 전교석차를 포함한 과목별 데이터])
        grade    = int(i[0])
        semester = int(i[1])
        exam     = int(i[2])
        
        try:
            grade_sel.select_by_visible_text(str(grade))
            semester_sel.select_by_visible_text(f"{semester}학기")
            exam_sel.select_by_visible_text("중간" if exam==1 else "기말")
        except:
            print("범위내 아직 나이스에 기록되지 않은 시험이 있습니다")
            return False
        
        driver.find_element(By.XPATH, '/html/body/app-root/csp-std-edi/div/csppage/csp-page/csp-wygwyg-hr-layout/div[2]/cspview/csp-view/csp-cond/form/div/button').click()
        
        try:
            WebDriverWait(driver, 2).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/app-root/csp-std-edi/div/csppage/csp-page/csp-wygwyg-hr-layout/div[2]/cspview/csp-view/div/div/csp-header/div/div/h2'), f"성적 - {grade}학년 {semester}학기 {'중간고사' if exam == 1 else '기말고사'}"))
        except:
            print("범위내 아직 나이스에 기록되지 않은 시험이 있습니다")
            return False

        time.sleep(0.2)
        
        try:
            table_datas = driver.find_elements(By.XPATH, '/html/body/app-root/csp-std-edi/div/csppage/csp-page/csp-wygwyg-hr-layout/div[2]/cspview/csp-view/div/div/csp-table/div/div/p-table/div/div/table/tbody//td//div')
        except:
            try:
                driver.find_element(By.XPATH("/html/body/app-root/csp-std-edi/div/csppage/csp-page/csp-wygwyg-hr-layout/div[2]/cspview/csp-view/div[2]/p"))
            except:
                return False
            else:
                print("범위내 아직 나이스에 기록되지 않은 시험이 있습니다")
                return False
            
        
        lecture_datas = (np.split(np.array(table_datas), len(table_datas)//11))
        #lecture_datas:  [국어(4), 지필 ,1차 지필평가(100.00%) ,100.00 ,85.90 ,85.90 ,86,None ,None ,54(5)/252	,64.8(24.0)]                                                      
        # [수학, ~~~]
        # [영어, ~~~]
        # [한국사, ~~~]
        # [통합사회, ~~~]
        # [통합과학, ~~~]
        
        temp =[]
        
        for list_lecture in lecture_datas:
            temp.append(list_lecture.tolist())
        
        
        total_temp =[]
        for lecture_data in temp:
            total_temp2 = []
            
            total_temp2.append(lecture_data[0].text)
            total_temp2.append(lecture_data[9].text)
            
            total_temp.append(total_temp2)
            
        
        total.append(total_temp)
        
        
        total[count].insert(0, f"{grade}-{semester}-{exam}")
        
        
        count += 1
        
    driver.quit()
    
    a=0
    subjectPerWeek = 0
    point_sum =0
    
    x=[]
    y=[]
    xAxis =[]
    
    for exam in total:
        exam_period = exam[0].split('-')
        
        grade = exam_period[0]
        semester = exam_period[1]
        MF_exam = int(exam_period[2])
        
        print(f"--- {grade}학년 {semester}학기 {'중간고사' if MF_exam == 1 else '기말고사'} ---") #시험 시기
        
        b=1
        for lecture in exam:
            if type(lecture) == str:
                continue
            total[a][b].append(score(total[a][b][1]))
            total[a][b].append(findSubjectPer(total[a][b][0]))
            
            subjectPerWeek += findSubjectPer(lecture[0])
            
            point_sum += lecture[2] * lecture[3]
            
            print(f"[+] {total[a][b][0]} - {total[a][b][2]}등급")
            b += 1
        a += 1
        
        test_average =round(point_sum / subjectPerWeek, 2)
        
        xAxis.append(f"{grade}학년 {semester}학기 {'중간고사' if MF_exam == 1 else '기말고사'} - ({test_average})")
        y.append(test_average)
        print(f"===  평균 등급: {test_average}  ===\n\n")

    for temp in range(1, len(xAxis)+1):
        x.append(temp)
    
    #시각화
    plt.rc('font', family='Malgun Gothic') #한글 사용시 글자 깨짐 해결
    plt.ylim(y[0]-1, y[-1]+1)

    plt.xticks(np.array(x), xAxis)
    plt.plot(np.array(x), np.array(y))
    
    plt.show()
    return True


if __name__ == "__main__":
    print("loaded")
    
    while True:
        time.sleep(1)
        os.system("cls")
        main()
