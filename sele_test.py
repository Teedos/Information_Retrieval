
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, random
from selenium.webdriver.firefox.service import Service

def get_google_links(url, driver):
    driver.get(url)
    author_list = []
    title_list = []
    while True:
        time.sleep(2)
        button = driver.find_element(By.ID, 'gsc_bpf_more')
        if not button.is_enabled():
            break
        else:
            button.click()
    publication_list = driver.find_elements(By.CLASS_NAME, 'gsc_a_tr')
    print(len(publication_list))
    for item in publication_list:
        author_list.append(item.find_element(By.CLASS_NAME, 'gs_gray').text)
        title_list.append(item.find_element(By.CLASS_NAME, 'gsc_a_at').text)
    return author_list, title_list

def get_random_publication(author_list, title_list):
    rand = random.randint(0,len(title_list))
    return author_list[rand], title_list[rand]
  
def search_google_sele(title, authors, driver):
    url = 'https://scholar.google.com/scholar?q=' + title + ',' + authors
    driver.get(url)
    author_list = []
    title_list = []
    print("Google search results \n")
    title_tag = driver.find_elements(By.CLASS_NAME, 'gs_rt')
    author_tag = driver.find_elements(By.CLASS_NAME,'gs_a')
    #print(len(title_tag))
    for i in range(len(title_tag)):
        title_link = title_tag[i].find_elements(By.CSS_SELECTOR, 'a')
        if len(title_link) == 0:
            continue
        title_text = title_tag[i].find_element(By.CSS_SELECTOR, 'a').text
        title_list.append(title_text)
        author = author_tag[i].text
        author_list.append(author)
    check_results(title, authors, title_list, author_list)

def search_aminer_sele(title, authors, driver):
    url = 'https://www.aminer.org/search/pub?q=' +title +',' +authors
    driver.get(url)
    search_authors = []
    search_titles = []
    print("Aminer search results \n")
    title_tag = driver.find_elements(By.CLASS_NAME, 'paper-title')
    author_tag = driver.find_elements(By.CLASS_NAME,'authors')
    for i in range(len(title_tag)):
        title_text = title_tag[i].text
        search_titles.append(title_text)
        search_authors.append(author_tag[i].text)
    check_results(title, authors, search_titles, search_authors)

def check_results(title, authors, search_titles, search_authors):
    if len(search_titles)==0:
        print("No matching found")
        return
    words = title.split() 
    total_words = len(words)
    treshold = total_words * 80 // 100
    print("treshold", treshold)
    print("original title has ",total_words)
    for i in range (len(search_titles)):
        matching_words = 0
        for word in words:
            if word in search_titles[i]:
                matching_words = matching_words + 1
        print("matching words", matching_words)
        if matching_words > treshold:
            if 'W. Bruce Croft' or 'WB Croft' or 'W.B. Croft' or 'W B Croft' in search_authors[i]:
                print(search_titles[i])
                print(search_authors[i])
                return
            else:
                continue
        else:
            continue
    print("No matching found")
    
url = 'https://scholar.google.com/citations?user=ArV74ZMAAAAJ&hl=en' 
service = Service('/opt/homebrew/bin/geckodriver')
driver = webdriver.Firefox(service=service)
authors, title = get_google_links(url, driver)
authors, title = get_random_publication(authors, title)
print(authors, "\n", title)
search_google_sele(title, authors, driver)
search_aminer_sele(title, authors, driver)
