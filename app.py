from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
data = pd.read_csv("ambitionbox_companies.csv")

@app.route("/")
def home():
    locations = sorted(data['location'].dropna().unique())
    companies = sorted(data['Company'].dropna().unique())
    ratings = sorted(data['rating'].dropna().unique())
    abouts = sorted(data['about'].dropna().unique())
   
   
    return render_template(
        "index.html",
        locations=locations,
        companies=companies,
        ratings=ratings,
        abouts=abouts
    )
@app.route("/submit", methods=["POST"])
def submit():



    filtered_data = data.copy()

    location = request.form.get("location")
    company = request.form.get("Company")
    rating = request.form.get("rating")
    about = request.form.get("about")
    output = request.form.get("output")
    if location:
        val = location.split('+')[0].strip()
        filtered_data = filtered_data[
            filtered_data['location'].str.contains(val, na=False)
        ]

    if company:
        filtered_data = filtered_data[
            filtered_data['Company'].str.contains(company, na=False)
        ]

    if rating:
        filtered_data = filtered_data[
            filtered_data['rating'] >= float(rating)
        ]

    if about:
        val = about.split('+')[0].strip()
        filtered_data = filtered_data[
            filtered_data['about'].str.contains(val, na=False)
        ]
    if output == "visual":
      if not os.path.exists("static"):
        os.makedirs("static")

   
      filtered_data = filtered_data.head(10)

      plt.figure(figsize=(6,4))
      plt.scatter(filtered_data["rating"], filtered_data["Company"])
      plt.xlabel("Company Rating")
      plt.ylabel("Company Name")
      plt.title("Rating vs Company Name")
      plt.tight_layout()
      plt.savefig("static/scatter.png")
      plt.close()

      plt.figure(figsize=(6,4))
      plt.hist(filtered_data["rating"], bins=8)
      plt.xlabel("Rating")
      plt.ylabel("Count")
      plt.title("Distribution of Company Ratings")
      plt.tight_layout()
      plt.savefig("static/hist.png")
      plt.close()
 
      top_companies = filtered_data.sort_values(by="rating", ascending=False)

      plt.figure(figsize=(6,4))
      plt.barh(top_companies["Company"], top_companies["rating"])
      plt.xlabel("Rating")
      plt.title("Top Companies by Rating")
      plt.tight_layout()
      plt.savefig("static/bar.png")
      plt.close()

    
      pie_data = filtered_data["Company"].value_counts()

      plt.figure(figsize=(6,4))
      plt.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%")
      plt.title("Company Ratings Distribution")
      plt.tight_layout()
      plt.savefig("static/pie.png")
      plt.close()
      return render_template("result.html", chart=True)
          
         
    
    
        
    

    return render_template(
         "result.html",
        table=filtered_data.head(10).to_dict(orient="records"),
        chart = False
    )

print(data.columns)
if __name__ == "__main__":
    app.run(debug=True, port=5500)