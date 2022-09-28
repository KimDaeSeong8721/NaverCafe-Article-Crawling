
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
import csv


# csv 쓰기
f = open('write.csv','w', newline='')
wr = csv.writer(f)


browser = webdriver.Chrome('./chromedriver') # 현재파일과 동일한 경로일 경우 생략 가능

user_id = '네이버아이디'
user_pw = '네이버비밀번호'

# 1. 네이버 이동
browser.get('https://cafe.naver.com/kyerongapartment')

# 2. 로그인 버튼 클릭
browser.find_element(By.ID,'gnb').find_element(By.CLASS_NAME,'gnb_txt').click()


# 3. id 복사 붙여넣기
elem_id = browser.find_element(By.ID,'id')
elem_id.click()
time.sleep(1)
pyperclip.copy(user_id)
elem_id.send_keys(Keys.COMMAND, 'v')
time.sleep(1)

# 4. pw 복사 붙여넣기
elem_pw = browser.find_element(By.ID,'pw')
elem_pw.click()
time.sleep(1)
pyperclip.copy(user_pw)
elem_pw.send_keys(Keys.COMMAND, 'v')
time.sleep(2)

# 5. 로그인 버튼 클릭
browser.find_element(By.ID,'log.login').click()

# 미니 검색창에 층간 소음 매트 검색
textfield = browser.find_element(By.CSS_SELECTOR,'input#topLayerQueryInput')
textfield.send_keys('층간 소음 매트')
textfield.send_keys(Keys.ENTER)

time.sleep(1)


frame = browser.find_element(By.ID,'cafe_main')
browser.switch_to.frame(frame)
next_cols = browser.find_element(By.CLASS_NAME,'prev-next').find_elements(By.TAG_NAME,'a')
browser.switch_to.default_content()
wr.writerow(["번호","글 제목","글 내용","댓글"])

# 페이지별
for i in range(1, len(next_cols)):

    page = browser.get(f"""https://cafe.naver.com/kyerongapartment?iframe_url=/ArticleSearchList.nhn%3Fsearch.clubid=11512007%26search.media=0%26search.searchdate=all%26userDisplay=15%26search.option=0%26search.sortBy=date%26search.searchBy=1%26search.query=%C3%FE%B0%A3+%BC%D2%C0%BD+%B8%C5%C6%AE%26search.viewtype=title%26search.page={i}""")
    
    frame = browser.find_element(By.ID,'cafe_main')
    browser.switch_to.frame(frame)  
    board = browser.find_element(By.XPATH,'//*[@id="main-area"]/div[5]/table/tbody')
    #tableRows = board.find_elements(By.TAG_NAME,'tr')
    tableRows = board.find_elements(By.CLASS_NAME,"article")
    browser.switch_to.default_content()
    
    # 아티클별
    for j,article in enumerate(tableRows):
      #article = tr.find_element(By.CLASS_NAME,'td_article').find_element(By.CLASS_NAME,'article')
      # writtenDate = tr.find_element(By.CLASS_NAME,'td_date').text
      # print(writtenDate)

      frame = browser.find_element(By.ID,'cafe_main')
      browser.switch_to.frame(frame)  

      articleurl =article.get_attribute('href') 
      browser.switch_to.default_content()

      browser.execute_script(f'window.open("{articleurl}");')
      time.sleep(0.1)

      browser.switch_to.window(browser.window_handles[-1]) 
      wait = WebDriverWait(browser,10)
      wait.until(EC.presence_of_element_located((By.ID,'cafe_main')))
      frame = browser.find_element(By.ID,'cafe_main')
      browser.switch_to.frame(frame)  
      wait = WebDriverWait(browser,10)
      wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div/div/div[2]')))
      contentBox = browser.find_element(By.XPATH,'//*[@id="app"]/div/div/div[2]') # ArticleContentBox
      

      try :
          article_title = contentBox.find_element(By.CLASS_NAME,'title_area').find_element(By.CLASS_NAME,'title_text').text
          article_content = contentBox.find_element(By.CLASS_NAME,'article_viewer').find_element(By.CLASS_NAME,'se-module.se-module-text').text
          print(article_content)
          print()
          csvContents = [(i-1)*15+j+1,article_title,article_content]
          comment_box = contentBox.find_element(By.CSS_SELECTOR,'ul.comment_list')
          comment_list = comment_box.find_elements(By.TAG_NAME,'li')
          comment = ""
          for idx in range(len(comment_list)) :
            comment += f"댓글{idx+1}: "
            tempComment = comment_list[idx].find_element(By.CLASS_NAME,'comment_text_box').text + '\n'
            if tempComment.find("010") == -1 :
              comment += tempComment + '\n'
            print(f"댓글{idx+1} :",comment)
            print()

          csvContents.append(comment)

      except:
          print("댓글 없음")
          csvContents.append("")
  
      if  article_content.find("010") == -1  :
        wr.writerow(csvContents)
      
      browser.switch_to.default_content()
      browser.close()
      browser.switch_to.window(browser.window_handles[-1])
f.close()
