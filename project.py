from flask import Flask,render_template, request,redirect, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
input = ""
@app.route("/",methods=["GET", "POST"])
def home_page():
    if request.method == "POST":
        genre = request.form.get("genre")
        return redirect(url_for("results", genre=genre))
    return render_template("index.html")

def scraping(g):
    url ="https://www.imdb.com/search/title/?genres="+g

    # works with all the links with similar UI 

    response = requests.get(url)
    data = []
    soup = BeautifulSoup(response.text,features="html.parser")

    movie_cards = soup.find_all("div", class_="lister-item mode-advanced")

    for x in movie_cards:
        image= x.find("div",class_="lister-item-image float-left").find("img")
        image_url = image['loadlate']
        
        movie_name = x.find("h3", class_="lister-item-header")     
        movie_name = movie_name.find("a").getText()
        
        a_tag = x.find("div", class_="lister-item-content")
        if a_tag:
            ratings = a_tag.find("div", class_="inline-block ratings-imdb-rating")
            if ratings:
                ratings = ratings.find("strong").getText()
        
            duration = a_tag.find("span",class_="runtime")
            if duration:
                duration = duration.getText()
                
            genre = a_tag.find("span",class_="genre")
            if genre:
                genre = genre.getText()

        info = (image_url,movie_name,ratings,duration,genre)    
        data.append(info)
    return data




@app.route("/results",methods=["GET", "POST"])
def results():
    g = request.args.get("genre")
    list = scraping(g)
    return render_template("results.html",DATA=list)
    

app.run(debug=True)