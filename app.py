from flask import Flask, render_template, request, send_file
import random

app = Flask(__name__)

def generate_passwords(name, birth_year, fav_person, mobile_no):
    patterns = [
        f"{name}{birth_year}", f"{name}@{birth_year}", f"{name}{birth_year}!",
        f"{name}{fav_person}", f"{fav_person}{birth_year}", f"{mobile_no}{birth_year}",
        f"{name}123", f"{name}!", f"{name}#"
    ]
    variations = set(patterns)

    # Add common substitutions
    for word in patterns:
        variations.add(word.replace("a", "@").replace("o", "0").replace("e", "3"))

    # Generate 1000 random variations
    random_variations = set()
    while len(random_variations) < 1000:
        random_variations.add("".join(random.sample(name + birth_year + fav_person + mobile_no, len(name + birth_year + fav_person + mobile_no))))

    variations.update(random_variations)
    
    return list(variations)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        birth_year = request.form["birth_year"]
        fav_person = request.form["fav_person"]
        mobile_no = request.form["mobile_no"]

        passwords = generate_passwords(name, birth_year, fav_person, mobile_no)

        return render_template("index.html", passwords=passwords)
    
    return render_template("index.html", passwords=None)

@app.route("/download")
def download():
    with open("generated_passwords.txt", "w") as file:
        for password in generate_passwords("test", "2000", "example", "1234567890"):
            file.write(password + "\n")
    
    return send_file("generated_passwords.txt", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
