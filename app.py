# Importing Neccessary Libraries
import requests
from flask import Flask,request,render_template
from flask_cors import CORS
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen , Request as url_req

app=Flask(__name__)
CORS(app)

@app.route("/",methods=["GET"])
def homepage():
    return render_template("index.html")

@app.route("/newspage",methods=["POST"])
def NewsScrapping():
    if request.method=='POST':
        ShowValue =[]
        # defining header which will help in avoiding 403 forbidden error
        header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                        'AppleWebKit/537.11 (KHTML, like Gecko) '
                                        'Chrome/91.0.4472.77 Safari/537.11',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none',
                    'Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}
        if request.form['NewsType']=="AllNews":
            try:
                # Scrapping Hindi News from AmarUjala 
                news_web = "https://www.amarujala.com/"           # the URL where you are requesting at
                req_page = url_req(url=news_web, headers=header)  # This step is performed to avoid 403 forbidden error
                news_page = urlopen(req_page)                     # Opening the page
                news_content = news_page.read()                   # getting the content from the page
                news_page.close()                                 # Closing the connection

                news_html = bs(news_content, "html.parser")
                news_section = news_html.findAll(["h3", "h2"])
                headingNo = 0
                for i in range(len(news_section)):
                    try:
                        news_heading = news_section[i].a['title']
                        news_link="https://www.amarujala.com"+news_section[i].a['href']                     
                        headingNo += 1
                    except:
                        try:
                            # Some news_headings are inside other tag So accessing those news_headings here
                            news_heading = news_section[i].h3.a['title']
                            news_link="https://www.amarujala.com"+news_section[i].h3.a['href']
                            headingNo += 1
                        except:
                            continue
                    values = {"newsNo": headingNo, "newsheading": news_heading,"newslink":news_link}  # Storing Values in dictionary
                    ShowValue.append(values)              # storing that dictionary in a list which will be used in html page
                htmlPage = "allnews.html"
                del headingNo  # Destructing headingNo variable as soon as its work is over as it will consume the memory till this function runs
            except:
                print("Error Occured In AllNews Section")
        elif request.form['NewsType']=="CricketNews":
            try:
                # Scrapping Sports news from cricbuzz
                cricnews_web = "https://www.cricbuzz.com/"           
                req_page = url_req(url=cricnews_web,headers=header)  
                cricnews_page = urlopen(req_page)                    
                cricnews_content = cricnews_page.read()              
                cricnews_page.close()                                

                cricnews_html = bs(cricnews_content, "html.parser")

                more_cricnews = "https://www.cricbuzz.com" + cricnews_html.findAll("div", {'class': "cb-hm-mr-lnk"})[0].a['href']

                link_cont = requests.get(more_cricnews)
                link_cont_html = bs(link_cont.text, "html.parser")
                cricnews_heading = link_cont_html.findAll("div",
                                                      {'class': 'cb-col-67 cb-nws-lst-rt cb-col cb-col-text-container'})
                for i in range(len(cricnews_heading)):
                    try:
                        title = cricnews_heading[i].find('div', {'class': 'cb-nws-time'}).text
                        heading = cricnews_heading[i].find('h2',{'class':'cb-nws-hdln'}).a['title']
                        link = "https://www.cricbuzz.com"+cricnews_heading[i].find('h2',{'class':'cb-nws-hdln'}).a['href']
                    except:
                        continue
                    values = {"Title": title, "Headline": heading,"Link":link}  
                    ShowValue.append(values)                                    
                htmlPage="cricnews.html"

            except:
                print("Error Occured in CricketNews Section")
        else:
            try:
                # Scrapping Tech news from gadget360
                technews_web = "https://gadgets.ndtv.com/"           
                req_page = url_req(url=technews_web,headers=header)  
                technews_page = urlopen(req_page)                    
                technews_content = technews_page.read()              
                technews_page.close()                                

                # All tech news Section
                technews_html = bs(technews_content, "html.parser")                
                more_technews_link = technews_html.find("div", {'class': "more-link"}).a['href']

                open_all_technews_page = requests.get(more_technews_link)

                all_tech_news_html = bs(open_all_technews_page.text, "html.parser")

                technews_headline = all_tech_news_html.findAll("div", {'class': 'caption_box'})  
                technews_time = all_tech_news_html.findAll("div", {'class': 'dateline'})  
                technews_category = all_tech_news_html.findAll("a", {'class': 'catname'})  
                try:
                    for i in range(len(technews_headline)):
                        tech_news_heading = technews_headline[i].span.text
                        tech_news_time = technews_time[i].text.split(",")[-1][1:]
                        tech_news_category = technews_category[i].text
                        tech_news_link = technews_headline[i].a['href']
                        values = {"Time": tech_news_time,"Category":tech_news_category, "Headline": tech_news_heading, "tech-link":tech_news_link}  # Storing Values in dictionary
                        ShowValue.append(values)  
                    htmlPage="technews.html"
                except:
                    print("Error in All Tech News Section")
            except:
                print("Error Occured in TechNews Section")
    return render_template(htmlPage,headlines=ShowValue)



if __name__ == '__main__':
    app.run(debug=True)