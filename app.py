from flask import Flask,render_template,url_for,request,redirect,flash
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
app.secret_key = "to think is the programmers mantra"
#database connection
db = yaml.load(open('dbconfig.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

#this path will display all tuples in the database 
mysql = MySQL(app)
@app.route('/home')
def home():
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM students");
	data = cur.fetchall()
	cur.close()
	return render_template('home.html',students=data)


#this path will insert data to the database table 
@app.route('/insert',methods=['POST'])
def insert():
	
	if request.method == "POST":
		flash("Data inserted successfully!")
		firstNameEntry = request.form['firstName']
		lastNameEntry = request.form['lastName']
		ageEntry = request.form['age']
		genderEntry = request.form['gender']
		phoneNumberEntry = request.form['phoneNumber']
		courseEntry = request.form['course']
		yearLevelEntry = request.form['yearLevel']

		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO students(firstName,lastName,age,gender,phoneNumber,course,yearLevel) VALUES (%s,%s,%s,%s,%s,%s,%s)",(firstNameEntry,lastNameEntry,ageEntry,genderEntry,phoneNumberEntry,courseEntry,yearLevelEntry));
		mysql.connection.commit()
		return redirect(url_for('home'))


#update data in the database table
@app.route("/update",methods= ['POST','GET'])
def update():
	if request.method == 'POST':
		idnoEntry = request.form['idno']
		firstNameEntry = request.form['firstName']
		lastNameEntry = request.form['lastName']
		ageEntry = request.form['age']
		genderEntry = request.form['gender']
		phoneNumberEntry = request.form['phoneNumber']
		courseEntry = request.form['course']
		yearLevelEntry = request.form['yearLevel']

		cur = mysql.connection.cursor()
		cur.execute("""UPDATE students SET firstName=%s,lastName=%s,age=%s,gender=%s,phoneNumber=%s,course=%s,yearLevel=%s WHERE idno=%s""",
			(firstNameEntry,lastNameEntry,ageEntry,genderEntry,phoneNumberEntry,courseEntry,yearLevelEntry,idnoEntry))
		flash("Data updated successfully!")
		mysql.connection.commit()
		return redirect(url_for('home'))


#delete a tuple in the database table
@app.route("/delete/<string:idno>",methods=['POST','GET'])
def delete(idno):
	if len(idno)!=0:
		cur = mysql.connection.cursor()
		cur.execute("DELETE FROM students WHERE idno=%s",(idno,))
		mysql.connection.commit()
		cur.close()
		flash("Data deleted successfully!")
	return redirect(url_for('home'))


#search data using keywords
@app.route("/search",methods=['POST','GET'])
def search():
	if request.method=='POST':
		searchEntry = request.form['search']
		cur = mysql.connection.cursor()
		cur.execute("""SELECT * FROM students WHERE idno=%s or firstName=%s or lastName=%s or age=%s or gender=%s or phoneNumber=%s or course=%s or yearLevel=%s""",
			(searchEntry,searchEntry,searchEntry,searchEntry,searchEntry,searchEntry,searchEntry,searchEntry));
		searchData = cur.fetchall()
		cur.close()
		return render_template('home.html',students=searchData)


# path for signin
@app.route("/",methods=['POST','GET'])
def signin():
	msg = ""
	if request.method=='POST':
		emailEntry = request.form['email']
		passwordEntry = request.form['password']
		
		cur = mysql.connection.cursor()
		cur.execute("""SELECT * FROM admin""");
		data = cur.fetchall()
		for datum in data:
			if  emailEntry==datum[3] and passwordEntry==datum[4]:
				return redirect(url_for('home'))
		else:
			msg = "Incorrect email or password!"
	return render_template('signin.html',msg=msg)
	
#path for registration 
@app.route("/register",methods=['POST','GET'])
def register():
	msg = ""
	if request.method=='POST':
		firstNameEntry = request.form['firstName']
		lastNameEntry = request.form['lastName']
		emailEntry = request.form['email']
		passwordEntry = request.form['password']
		cur = mysql.connection.cursor()
		cur.execute("""SELECT * FROM admin WHERE email LIKE %s""",[emailEntry])
		account = cur.fetchone()
		if account:
			msg="Account Already Exist!"
		else:
			cur.execute("""INSERT INTO admin(firstName,lastName,email,password) VALUES (%s,%s,%s,%s)""",(firstNameEntry,lastNameEntry,emailEntry,passwordEntry));
			mysql.connection.commit()
			msg="Account added successfully, Login now!"
	return render_template('register.html',msg=msg)



#debug mode for development
if __name__ == "__main__":
	app.run(debug=True)
