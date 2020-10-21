import rpa as r
import pandas as pd 
import time

#Read all restaurant names in csv
yelp=pd.read_csv("yelpindex.csv")
yelp["URL"].head

r.init()

#Fill up table with URLs
for i in (0,len(yelp["URL"])):
    r.url(yelp["URL"][i])
    if r.present("//*[@id='rso']/div[1]/div/div[1]/a/@href"): name = r.read("//*[@id='rso']/div[1]/div/div[1]/a/@href")
    else: name = r.read("//*[@id='rso']/div[2]/div/div[1]/a/@href")
    print(name)
    yelp["URL"][i] = name
    time.sleep(5)

    yelp.to_csv("yelpindex_updated.csv")

    yelp2TA=pd.read_csv("yelpindex_updated.csv")
    yelp2TA.reset_index(drop=True)
    yelp2TA["URL"].head


#Get Reviews
author_loc=""
reviews_df=pd.DataFrame()
#if y == 9: init = 33
#else: init = 0
for x in range (0,len(yelp2TA["URL"])):
    if len(yelp2TA["URL"]) <= x: break
    r.url(yelp2TA["URL"][x])
    time.sleep(10)
    if r.present('//*[@id="taplc_detail_filters_rr_resp_0"]/div/div[1]/div/div[2]/div[4]/div/div[2]/div[1]/div[2]/label/span[2]') == False: continue
    num_reviews=r.read('//*[@id="taplc_detail_filters_rr_resp_0"]/div/div[1]/div/div[2]/div[4]/div/div[2]/div[1]/div[2]/label/span[2]')
    num_reviews=int(num_reviews.replace(' reviews','').replace(' review','').replace(',','').replace('(','').replace(')',''))
    #print(num_reviews)
    j=1
    while j <= num_reviews or j<= 100:
        r.click('//*[contains(@id,"review")]/div/div[2]/div[2]/div/p/span')
        r.click('//*[contains(@id,"review")]/div/div[2]/div[2]/div/p/span[2]')
        i0=0
        for i in range (1,11):
            name = yelp2TA["Name"][x]
            location = ""
            address = r.read('//*/div/div[3]/span[1]/span/a')
            if r.present('//*/div/div[2]/span[3]/a[4]'):
                type = r.read('//*/div/div[2]/span[3]/a[2]')+","+r.read('//*/div/div[2]/span[3]/a[3]')+","+r.read('//*/div/div[2]/span[3]/a[4]')
            elif r.present('//*/div/div[2]/span[3]/a[3]'):
                type = r.read('//*/div/div[2]/span[3]/a[2]')+","+r.read('//*/div/div[2]/span[3]/a[3]')
            elif r.present('//*/div/div[2]/span[3]/a[2]'):
                type = r.read('//*/div/div[2]/span[3]/a[2]')
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
            reviews_df.to_csv(f'yelp2tripadvisor.csv', sep=',')

            j=j+1
            if j>num_reviews or j>100: break
        if j>num_reviews or j>100: break
        elif num_reviews>j: r.click('//*[contains(@class,"next ui_button")]')