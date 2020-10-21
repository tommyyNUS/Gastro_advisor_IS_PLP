import rpa as r
import pandas as pd 
import time
import pickle

#Get URLs
r.init()

URL = f'https://www.tripadvisor.com.sg/Restaurants-g294265-Singapore.html'
r.url(URL)
time.sleep(10)



maxpage = int(r.read('//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/div/a[6]/@data-page-number'))
for j in range (0,maxpage):
    URL_list = []
    if j!=0: 
        if r.present(f'(//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/a)[2]'):
            r.click(f'(//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/a)[2]')
        else:
            r.click(f'(//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/a)[1]')

    time.sleep(10)
    for i in range (1,100):
        if r.exist(f'(//*[@id="component_2"]/div/div[*]/span/div[1]/div[2]/div[1]/div/span/a/@href)[{i}]') == False: break
        URL_list.append("https://www.tripadvisor.com.sg" + r.read(f'(//*[@id="component_2"]/div/div[*]/span/div[1]/div[2]/div[1]/div/span/a/@href)[{i}]'))
        #print(URL_list)
        with open(f'url_list_{j}.txt', 'wb') as filehandle: pickle.dump(URL_list, filehandle)


#Load Bookmark
listnumber = 0
iteminlist = 0
with open(f'url_list_{listnumber}.txt', 'rb') as filehandle: URL_list = pickle.load(filehandle)
print(URL_list)



#Get Reviews from URLs
author_loc=""
for y in range (listnumber,len(URL_list)):    
    with open(f'url_list_{y}.txt', 'rb') as filehandle: URL_list = pickle.load(filehandle)
    reviews_df=pd.DataFrame()
    if y == listnumber: init = iteminlist
    else: init = 0
    for x in range (init,100):
        if len(URL_list) <= x: break
        r.url(URL_list[x])
        time.sleep(10)
        if r.present('//*[@id="taplc_detail_filters_rr_resp_0"]/div/div[1]/div/div[2]/div[4]/div/div[2]/div[1]/div[2]/label/span[2]') == False: continue
        num_reviews=r.read('//*[@id="taplc_detail_filters_rr_resp_0"]/div/div[1]/div/div[2]/div[4]/div/div[2]/div[1]/div[2]/label/span[2]')
        num_reviews=int(num_reviews.replace(' reviews','').replace(' review','').replace(',','').replace('(','').replace(')',''))
        #print(num_reviews)
        j=1
        while j <= num_reviews:
            r.click('//*[contains(@id,"review")]/div/div[2]/div[2]/div/p/span')
            i0=0
            for i in range (1,11):
                name = r.read('//*[@data-test-target="top-info-header"]')
                location = ""
                address = r.read('//*/div/div[3]/span[1]/span/a')
                if r.present('//*/div/div[2]/span[3]/a[2]'):
                    type = r.read('//*/div/div[2]/span[3]/a[2]')+","+r.read('//*/div/div[2]/span[3]/a[3]')+","+r.read('//*/div/div[2]/span[3]/a[4]')
                else:
                    type = r.read('//*/div/div[2]/span[3]/a[1]') 
                if r.read(f'(//*[contains(@id,"review")]/div/div/span[1]/@class)[{i}]').replace("ui_bubble_rating bubble_","") == '': break    
                if r.read(f'(//*[contains(@id,"review")]/div/div/span[1]/@class)[{i}]').replace("ui_bubble_rating bubble_","") != 'ui_icon star-fill':
                    rating = int(r.read(f'(//*[contains(@id,"review")]/div/div/span[1]/@class)[{i+i0}]').replace("ui_bubble_rating bubble_",""))/10
                else:
                    i0=1
                    rating = int(r.read(f'(//*[contains(@id,"review")]/div/div/span[1]/@class)[{i+i0}]').replace("ui_bubble_rating bubble_",""))/10

                author = r.read(f'(//*[@class="memberOverlayLink clickable"]/div[2])[{i}]/div[1]')
                if r.exist(f'(//*[@class="memberOverlayLink clickable"]/div[2])[{i}]/div[2]'):
                    author_loc = r.read(f'(//*[@class="memberOverlayLink clickable"]/div[2])[{i}]/div[2]')
                date = r.read(f'(//*[@class="ratingDate"]/@title)[{i}]')
                review = r.read(f'(//*[contains(@id,"review")]/div/div/div[2]/div/p)[{i}]')
                origin = "TripAdvisor"
                #print(name)
                #print(location)
                #print(address)
                #print(type)
                #print(rating)
                #print(author)
                #print(author_loc)
                #print(date)
                #print(review)
                #print(origin)

                review_dict = {'restaurant' : name,
                        'location' : location,      
                        'address' : address,                           
                        'type' : type,               
                        'rating': rating, 
                        'author': author,
                        'author_loc': author_loc,                     
                        'date': date,
                        'Review': review,
                        'origin': origin,
                    }

                reviews_df = reviews_df.append(review_dict, ignore_index=True)
                reviews_df.to_csv(f'{y}.csv', sep=',')

                j=j+1
                if j>num_reviews: break
            if num_reviews>j: r.click('//*[contains(@class,"next ui_button")]')