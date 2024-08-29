from bs4 import BeautifulSoup
import requests
import mysql.connector

 
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="kec_faculty_details",
    auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()

 
irins_id = 233656

 
url = f'https://kongu.irins.org/profile/{irins_id}'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

 
id_name = soup.find('h4', class_='badge-blue')
id_number = int(id_name.text.split(':')[1].strip())

 
header_profile = soup.find('div', class_='profile-blog')
name1 = header_profile.find('li').find('h1').text.strip()
profession = header_profile.find_all('li')[1].text.strip()
college = header_profile.find_all('li')[2].text.strip()

 
journel = soup.find('div', class_='panel-body').find_all('li', class_='Pub_li_br_dashed')[0].find('div', class_='p0').text.strip()

 
expertise_header = soup.find('div', class_='tag-box-v1')
expertise = expertise_header.find('h2').text.strip()
expertise_desc = expertise_header.find('h5').text.strip()

 
sql = """CREATE TABLE IF NOT EXISTS basic_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vidwan_id INT UNIQUE,
    name VARCHAR(255),
    profession VARCHAR(255),
    college VARCHAR(255),
    publications TEXT,
    expertise VARCHAR(255)
)"""
mycursor.execute(sql)

 
sql = "INSERT INTO basic_details (vidwan_id, name, profession, college, publications, expertise) VALUES (%s, %s, %s, %s, %s, %s)"
val = (id_number, name1, profession, college, journel, expertise)
mycursor.execute(sql, val)
mydb.commit()

 
sql = """CREATE TABLE IF NOT EXISTS personal_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vidwan_id INT,
    name VARCHAR(255),
    gender VARCHAR(255),
    department VARCHAR(255),
    location VARCHAR(255),
    FOREIGN KEY (vidwan_id) REFERENCES basic_details(vidwan_id)
)"""
mycursor.execute(sql)

 
personal_info = soup.find('div', class_='margin-bottom-10')
name = personal_info.find('h4').text.strip()
gender = personal_info.find('span', class_='col-sm-3').text.strip()
department = personal_info.find_all('div', class_='name-location')[1].find('span').text.strip()
location = personal_info.find_all('span')[-2].text.strip()

 
sql = "INSERT INTO personal_info (vidwan_id, name, gender, department, location) VALUES (%s, %s, %s, %s, %s)"
val = (id_number, name, gender, department, location)
mycursor.execute(sql, val)
mydb.commit()

 
sql = """CREATE TABLE IF NOT EXISTS experience (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vidwan_id INT,
    time_period VARCHAR(255),
    job_title VARCHAR(255),
    department VARCHAR(255),
    college VARCHAR(255),
    FOREIGN KEY (vidwan_id) REFERENCES basic_details(vidwan_id)
)"""
mycursor.execute(sql)

 
experience_items = soup.find_all('li', id='edit-experience-view')

for experience_item in experience_items:
    time_period = experience_item.find('time', class_='cbp_tmtime').text.strip()
    time_period = time_period.replace('\r\n', '').replace('                              ', '')  # Clean up unwanted spaces and line breaks
    job_title = experience_item.find('h2').text.strip()
    department = experience_item.find('p').text.strip()
    college = experience_item.find_all('p')[1].text.strip()

     
    sql = "INSERT INTO experience (vidwan_id, time_period, job_title, department, college) VALUES (%s, %s, %s, %s, %s)"
    val = (id_number, time_period, job_title, department, college)
    mycursor.execute(sql, val)
    mydb.commit()

 
sql = """CREATE TABLE IF NOT EXISTS qualification (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vidwan_id INT,
    year VARCHAR(255),
    degree VARCHAR(255),
    institution VARCHAR(255),
    FOREIGN KEY (vidwan_id) REFERENCES basic_details(vidwan_id)
)"""
mycursor.execute(sql)

 
qualification_items = soup.find_all('li', id='qualification-view')

for qualification_item in qualification_items:
    year = qualification_item.find('time', class_='cbp_tmtime').text.strip()
    degree = qualification_item.find('h2').text.strip()
    institution = qualification_item.find('p').text.strip()

   
    sql = "INSERT INTO qualification (vidwan_id, year, degree, institution) VALUES (%s, %s, %s, %s)"
    val = (id_number, year, degree, institution)
    mycursor.execute(sql, val)
    mydb.commit()

print("Data inserted into MySQL database successfully.")

mycursor.close()
mydb.close()
