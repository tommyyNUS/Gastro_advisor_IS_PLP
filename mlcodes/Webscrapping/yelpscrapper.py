import rpa as r
import pandas as pd 
import time

r.init()
area_list=['Telok_Kurau','Thomson','Tiong_Bahru','Toa_Payoh','Tuas','Ubi','Ulu_Pandan'
,'Upper_Bukit_Timah','Wessex_Estate','West_Coast','Woodlands','Yio_Chu_Kang','Yishun','one-north']
#area_list=['Alexandra','Ang_Mo_Kio','Ann_Siang_Hill','Arab_Street','Bayfront','Bedok_North',
# 'Bedok_Reservoir','Bedok_South','Bencoolen','Bishan','Boat_Quay','Boon_Keng','Boon_Lay','Bras_Brasah','Buangkok','Bugis',
# 'Bukit_Batok','Bukit_Panjang','Bukit_Timah','Changi','Chinatown','Choa_Chu_Kang','City_Hall','Clarke_Quay','Clementi','Dempsey_Hill','Dhoby_Ghaut','Dover','Duxton_Hill','Eunos','Farrer_Park','Geylang','Ghim_Moh','Harbourfront','Holland_Hill'
#,'Holland_Village','Hougang','Joo_Chiat','Jurong','Jurong_Island','Kallang','Katong','Kembangan','Kent_Ridge','Keppel','Labrador_Park'
#,'Lavender','Lim_Chu_Kang','Little_India','Macpherson','Mandai','Marine_Parade','Mount_Sophia','Mountbatten','Newton','Novena','Orchard'
#,'Outram','Pasir_Panjang','Pasir_Ris','Paya_Lebar','Potong_Pasir','Pulau_Ubin','Punggol','Queenstown','Raffles_Place','Redhill','River_Valley'
#,'Robertson_Quay','Seletar','Sembawang','Sengkang','Sentosa','Serangoon','Serangoon_Gardens','Siglap','Simei','Sixth_Avenue','Somerset','Tampines'
#,'Tanglin','Tanglin_Halt','Tanjong_Pagar','Tanjong_Rhu','Telok_Blangah',]
size = len(area_list)


for a in range(size):
    
    URL = f'https://www.yelp.com/search?find_desc=Restaurants&find_loc=Singapore&l=p%3ASG-SG%3ASingapore%3A%3A{area_list[a]}'
    r.url(URL)
    time.sleep(10)


    URL_list = []
    maxpage = int(r.read('//*[@id="wrap"]/div[3]/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/span').replace("1 of ",""))
    for j in range (0,maxpage):

        if j!=0: 
            if r.present(f'(//*[@id="wrap"]/div[3]/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/span/a/span)[2]'):
                r.click(f'(//*[@id="wrap"]/div[3]/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/span/a/span)[2]')
            else:
                r.click(f'(//*[@id="wrap"]/div[3]/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/span/a/span)[1]')

        time.sleep(10)
        for i in range (1,31):
            if r.exist(f'//*[@id="wrap"]/div[3]/div[2]/div/div[1]/div[1]/div[2]/div[2]/ul/li[{i}]/div/div/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div/h4/span/a/@href') == False: break
            URL_list.append("https://www.yelp.com" + r.read(f'//*[@id="wrap"]/div[3]/div[2]/div/div[1]/div[1]/div[2]/div[2]/ul/li[{i}]/div/div/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div/h4/span/a/@href'))
            print(URL_list)


    reviews_df=pd.DataFrame()


    for x in range (0,30):
        if len(URL_list) <= x: break
        r.url(URL_list[x])
        time.sleep(10)
        if r.present('//*[@id="wrap"]/div[3]/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div/div/div[2]/div[2]/p') == False: continue
        num_reviews=r.read('//*[@id="wrap"]/div[3]/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div/div/div[2]/div[2]/p')
        num_reviews=int(num_reviews.replace(' reviews','').replace(' review',''))
        print(num_reviews)
        j=1
        while j <= num_reviews:
            for i in range (1,21):
                name = r.read('//*[@id="wrap"]/div[3]/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div/div/div[1]/h1')
                location = area_list[a]
                address = r.read('(//*[contains(@class,"lemon--address")]/p)[1]')+" "+r.read('(//*[contains(@class,"lemon--address")]/p)[2]')
                if r.present('//*[@id="wrap"]/div[3]/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div/div/span[2]'):
                    type = r.read('//*[@id="wrap"]/div[3]/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div/div/span[2]')
                else:
                    type = r.read('//*[@id="wrap"]/div[3]/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div/div/span')                
                rating = r.read(f'//*[@id="wrap"]/div[3]/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div[3]/section/div[2]/div/ul/li[{i}]/div/div[2]/div[1]/div/div[1]/span/div/@aria-label')
                author = r.read(f'//*[@id="wrap"]/div[3]/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div[3]/section/div[2]/div/ul/li[{i}]/div/div[1]/div[1]/div/div/div[2]/div[1]/span/a')
                author_loc = r.read(f'//*[@id="wrap"]/div[3]/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div[3]/section/div[2]/div/ul/li[{i}]/div/div[1]/div[1]/div/div/div[2]/div[1]/div/span')
                date = r.read(f'//*[@id="wrap"]/div[3]/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div[3]/section/div[2]/div/ul/li[{i}]/div/div[2]/div[1]/div/div[2]/span')
                review = r.read(f'//*[@id="wrap"]/div[3]/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div[3]/section/div[2]/div/ul/li[{i}]/div/div[2]/div/p/span')
                origin = "Yelp"
                print(name)
                print(location)
                print(address)
                print(type)
                print(rating)
                print(author)
                print(author_loc)
                print(date)
                print(review)
                print(origin)

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
                reviews_df.to_csv(f'{location}.csv', sep=',')

                j=j+1
                if j>num_reviews: break
            if num_reviews>j: r.click('//*[@id="wrap"]/div[3]/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div[3]/section/div[2]/div/div[4]/div[1]/div/div[7]/span/a/span')