from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_IG(account="rack_3952",password='IG@f5ca1666'):
    browser = webdriver.Firefox()
    browser.get('https://www.instagram.com/')

    #休息2秒
    sleep(2)    

    #登入IG(預設為我的假帳號)
    username_input = browser.find_element(By.CSS_SELECTOR,"input[name='username']")
    password_input = browser.find_element(By.CSS_SELECTOR,"input[name='password']")
    username_input.send_keys(account)
    password_input.send_keys(password)
    login_button = browser.find_element(By.XPATH,"//button[@type='submit']")
    login_button.click()

    #休息5秒
    sleep(5)

    #回傳IG首頁
    return browser



def get_content(browser):

    #貼文內容
    content=browser.find_element(By.XPATH,'//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/span').text

    return content    



def get_likes_number(browser):

    #按讚數
    n_like=browser.find_element(By.CSS_SELECTOR,"a[class='zV_Nj']").text
    
    return n_like



def get_comment_number(browser,contain_reply=False):
    index=0
    while True:
        index+=1
        try:
            print(index)
            # 等待直到Button出現
            WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/li/div/button")))
            
            # 找到Button的網頁元素(class)
            more_btn = browser.find_element(By.XPATH,"/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/li/div/button")

            # 自動點擊Button
            
            more_btn.click()
           
        except:
            
            break
    
    if contain_reply==True:
        rp_bts=browser.find_elements(By.CSS_SELECTOR,"button[class*='sqdOP']")

        for b in rp_bts:
            browser.execute_script("arguments[0].click();", b)
    
    comments=browser.find_elements(By.CSS_SELECTOR,"div[class*='C4VMK']")
    comments=comments[1:len(comments)]
  

    return len(comments)



def get_post_info(browser,tag_list=[],post_amount=10,contain_reply=False):

    tag_url="https://www.instagram.com/explore/tags/"
    
    if len(tag_list)==0:
        print("請輸入要查詢的標籤")

    else:
        for t in tag_list:

            #搜尋標籤
            url=tag_url+t+"/"
            browser.get(url)
            sleep(6)
            
            #回傳貼文網址
            elems=browser.find_elements(By.CSS_SELECTOR,"div[class*='v1Nh3'] a")
            links = [elem.get_attribute('href') for elem in elems]

            if post_amount>len(links):
                print("此標籤文章數不足! 僅會抓取%d篇" %len(links))
                post_amount=len(links)

            links=links[0:post_amount]
            for l in links:
                sleep(1)
                browser.get(l)
                content=get_content(browser)
                like_numbers=get_likes_number(browser)
                coment_number=get_comment_number(browser,contain_reply)
                
                print(content)
                print(like_numbers)
                print("留言數: %d" %coment_number)

if __name__=='__main__':
    browser=login_IG()
    tag_lists=["百岳"]
    get_post_info(browser,tag_lists,1,contain_reply=True)



    # browser = login_IG()
    # browser.get('https://www.instagram.com/p/CWpAk3dPKHI/')
    # coment_number=get_comment_number(browser,False)
    # print("留言數: %d" %coment_number)
    # coment_number1=get_comment_number(browser,True)
    # print("留言數: %d" %coment_number1)


