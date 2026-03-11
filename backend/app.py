from flask import Flask, jsonify,request
from sqlalchemy import or_
from model import db, User,Role,Company,Student,PlacementDrive,Application,Interview
from flask_caching import Cache
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS
from flask_jwt_extended import create_access_token,JWTManager,jwt_required,get_jwt_identity,get_jwt
from datetime import datetime
from flask_mail import Mail

# from test import genratetestdata
from celeryapp import celery



app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'himanshu966081406412345648987897'
jwt = JWTManager(app)







CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///palcment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/1"
app.config["CACHE_DEFAULT_TIMEOUT"] = 60
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'seervihimanshu51@gmail.com'
app.config['MAIL_USERNAME'] = 'seervihimanshu51@gmail.com'
app.config['MAIL_PASSWORD'] = 'bwkcuarwhigzvakz'

cache = Cache(app)
mail = Mail(app)
db.init_app(app)
celery.conf.update(app.config)

def preadminecreate():
    with app.app_context():
        if not User.query.filter_by(email='admin@hms.com').first():
            admin = User(
            email='admin@hms.com', 
            password_hash=generate_password_hash('admin123'), 
            role=Role.ADMIN,
            name='himanshu'
        )
            db.session.add(admin)
            db.session.commit()

        else:print("phela sa bana hua hai ")
    

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/login", methods=["POST","GET"])
def login():
    data= request.json
    # print(data)
    email=data['email']
    pasword=data['password']
    
    # print(email,pasword)

    try:
        existuser=User.query.filter_by(email=email).first()
        if not existuser:
            return jsonify({"msg": "User not found"}), 404
        if existuser and check_password_hash(existuser.password_hash, pasword) and existuser.role.value=="admin":
            token = create_access_token(
            identity=str(existuser.id),
            additional_claims={"role": existuser.role.value}
            )
        
            return jsonify({
                'suscess':'true',
                'role':'admin',
                'msg':'login',
                "token": token,
                "userid":existuser.id
                })
        elif existuser and check_password_hash(existuser.password_hash, pasword) and existuser.role.value=="student" and existuser.is_active   :
            token = create_access_token(
            identity=str(existuser.id),
            additional_claims={"role": existuser.role.value}
            )
            return jsonify({
                'suscess':'true',
                'role':'student',
                'msg':'login',
                "token":token,
                "userid":existuser.id})
        elif existuser and check_password_hash(existuser.password_hash, pasword) and existuser.role.value=="company" and existuser.is_active:
            token = create_access_token(
            identity=str(existuser.id),
            additional_claims={"role": existuser.role.value}
            )
            return jsonify({
                'suscess':'true',
                'role':'company',
                'msg':'login',
                "token": token,
                "userid":existuser.id})
        else:
            if not existuser.is_active:
                return jsonify({'msg':"request pending or user id block "})
            return jsonify({'msg':'email or password is wrong'})

    except Exception as e:
        # print('some eror aa gaya')
        print(e)
        return jsonify({
        'msg':'kuch eroro aa gaya'
    })

@app.route("/register", methods=["POST","GET"])
def register():
    data= request.json
    # print(data)
    if data['role']=='COMPANY':
        
        is_active = False
    else:is_active=True
    role = data.get("role")

    
    new_user=User(
        email=data["email"],
        password_hash=generate_password_hash(data["password"]),
        name=data["name"],

        role=data['role'],

        is_active=is_active
        
        
    )
    
         
    
    
    
    try:

        db.session.add(new_user)
        db.session.flush()
        if data['role']=='COMPANY':
            new_company = Company(
            user_id=new_user.id,
            company_name=data["name"]
            ,hr_contact=data['contact']
            ,website=data['website'])

            db.session.add(new_company)
        if data['role']=='STUDENT':
            new_student = Student(
            user_id=new_user.id,
            Student_name=data["name"])
            db.session.add(new_student)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("eroro aa gaya mera bhai",e)
        return jsonify({
            'msg':'ya phela sa exist hai ya kuch or eror acourer'
        })
    

    
    return jsonify({
        'msg':'ho gaya mera bhai '
    })


















@app.route("/company")
@cache.cached(timeout=5, query_string=True)
@jwt_required()
def get_companies():
    
    user = get_jwt_identity()
    claim = get_jwt()
    role = claim["role"]
    if role!="admin":
        return jsonify({'msg':"aceese denied"}),403
    

    search = request.args.get("q")
    
    
    
    if search:
        # print(search)
        companies = (
            Company.query
            .join(User)
            .filter(or_(User.name.ilike("%" + search + "%"),User.email.ilike("%" +search+ "%")))
            .all()
        )
    else:
    
        # print("ya per aa haya")
        companies = Company.query.all()

    Placementdrive=PlacementDrive.query.all()
    total_student = Student.query.count()
    total_company = Company.query.count()
    total_drive = PlacementDrive.query.count()
    total_application=Application.query.count()
    
    companieslist=[

        {
        
        "id": c.id,
        "name": c.user.name,
        "hr_contact":c.hr_contact,
        "website":c.website,
        "approval_status":c.approval_status,
        "is_active": c.user.is_active,

        }
        for c in companies
        
    ]
    drivelist=[p.to_json() for p in Placementdrive]
    # print(companieslist)
    return jsonify({"companieslist":companieslist,'drivelist':drivelist,'total_drive':total_drive,'total_student':total_student,'total_company':total_company,'total_application':total_application})

@app.route("/student")
@jwt_required()
def getstudent():
    user = get_jwt_identity()
    claim = get_jwt()
    role = claim["role"]
    if role!="admin":
        return jsonify({'msg':"aceese denied"}),403
    
    search = request.args.get("q")
    
    
    if search:
        student = (
            Student.query
            .join(User)
            .filter(or_(User.name.ilike("%" + search + "%"),
                    User.email.ilike("%"+search+"%")))
            .all()
        )
    else:



        student = Student.query.all()
    return jsonify([{
        'id':s.id,

        'name':s.Student_name,
        'email':s.user.email,
        "is_active":s.user.is_active
        
    } for s in student]
    )

@app.route('/activate/<int:id>', methods=['PUT'])
@jwt_required()
def activatecompany(id):
    user = get_jwt_identity()
    claim = get_jwt()
    role = claim["role"]
    if role!="admin":
        return jsonify({'msg':"aceese denied"}),403
    compnay=Company.query.get(id)
    if compnay:
        try:
            compnay.approval_status=True
            compnay.user.is_active=True
            db.session.commit()
            return jsonify({'msg':'acive susseful'})
        except Exception as e:
            return jsonify({'msg':'some eroro acure'})
    
    return jsonify({
        'msg':'compnay not found'
    })

@app.route('/sblacklist/<int:id>',methods=["PUT"])
@jwt_required()
def sblacklist(id):
    user = get_jwt_identity()
    claim = get_jwt()
    role = claim["role"]
    if role!="admin":
        return jsonify({'msg':"aceese denied"}),403
    student=Student.query.get(id)
    if student:
        student.user.is_active=False
        db.session.commit()
        return jsonify({'msg':'blacklist'})
    return jsonify({
        'msg':'student not find'
    })
@app.route('/usblacklist/<int:id>',methods=["PUT"])
@jwt_required()
def usblacklist(id):
    user = get_jwt_identity()
    claim = get_jwt()
    role = claim["role"]
    if role!="admin":
        return jsonify({'msg':"aceese denied"}),403
    student=Student.query.get(id)
    if student:
        student.user.is_active=True
        db.session.commit()
        return jsonify({'msg':'unblacklist'})
    return jsonify({
        'msg':'student not find'
    })


@app.route('/cblacklist/<int:id>',methods=["PUT"])
@jwt_required()
def cblacklist(id):
    user = get_jwt_identity()
    claim = get_jwt()
    role = claim["role"]
    if role!="admin":
        return jsonify({'msg':"aceese denied"}),403
    compnay=Company.query.get(id)
    if compnay:
        try:
            compnay.approval_status=False
            compnay.user.is_active=False
            db.session.commit()
            return jsonify({'msg':'blacklist '})
        except Exception as e:
            return jsonify({'msg':'some eroro acure'})
    
    return jsonify({
        'msg':'compnay not found'
    })
@app.route('/ucblacklist/<int:id>',methods=["PUT"])
@jwt_required()
def ucblacklist(id):
    user = get_jwt_identity()
    claim = get_jwt()
    role = claim["role"]
    if role!="admin":
        return jsonify({'msg':"aceese denied"}),403
    compnay=Company.query.get(id)
    if compnay:
        try:
            compnay.approval_status=True
            compnay.user.is_active=True
            db.session.commit()
            return jsonify({'msg':'acive susseful'})
        except Exception as e:
            return jsonify({'msg':'some eroro acure'})
    
    return jsonify({
        'msg':'compnay not found'
    })


@app.route('/changedrivestatus/<int:id>',methods=["PUT"])
@jwt_required()
def chagnedrvestatus(id):
    user = get_jwt_identity()
    claim = get_jwt()
    role = claim["role"]
    if role!="admin":
        return jsonify({'msg':"aceese denied"}),403
    drive=PlacementDrive.query.get(id)
    drive.is_active = not drive.is_active
    db.session.commit()
    return jsonify({'msg':"ho gaya"})

@app.route('/getapplication')
@jwt_required()
def getapplication():
    user = get_jwt_identity()
    claim = get_jwt()
    role = claim["role"]
    if role!="admin":
        return jsonify({'msg':"aceese denied"}),403
    application=Application.query.all()
    return jsonify([{'id':a.id,"student_id":a.student_id,"drive_id":a.drive_id,'status':a.status,} for a in application])

@app.route('/getstudentforadmin/<int:id>')
@jwt_required()
def getstudnetforadmin(id):
    user = get_jwt_identity()
    claim = get_jwt()
    role = claim["role"]
    if role!="admin":
        return jsonify({'msg':"aceese denied"}),403
    student=Student.query.get(id)
    user=student.user
    
    return jsonify( {
            "id": student.id,
            "user_id": student.user_id,
            "Student_name": student.Student_name,
            "education": student.education,
            "skills": student.skills,
            "experience": student.experience,
            "resume_link": student.resume_link,
            'email':user.email
        })






























# ya compnay ka sare function






@app.route("/getcompanydata/<int:id>")
@jwt_required()
def getcompanydata(id):

    user = get_jwt_identity()
    claim = get_jwt()
    role = claim["role"]
    if role!="company":
        return jsonify({'msg':"aceese denied"}),403
    

    company=User.query.get(id).company
    # company = Company.query.filter_by(id=company.id).first()
    drives = company.drives
    drivelist = [d.id for d in drives]
    # print(company.drives)

   
    
    applicationlist=Application.query.filter(Application.drive_id.in_(drivelist)).all()
    # print(applicationlist)
    
    
    
    applicationlist=Application.query.filter_by()
    
    return jsonify({
        'compnayid':company.id,
        'email':company.user.email,
    'company_name':company.company_name
    ,'hr_contact':company.hr_contact,
    'website':company.website,
    "shortlistapplication":[{'id':a.id,'student_id':a.student_id,'drive_id':a.drive_id,'status':a.status}for a in applicationlist],
    'drive':[d.to_json() for d in drives]
    })

@app.route("/createdrive",methods=["POST"])
@jwt_required()
def createdrive():

    user = get_jwt_identity()
    companyid=User.query.get(user).company
    claim = get_jwt()
    role = claim["role"]
    if role!="company":
        return jsonify({'msg':"aceese denied"}),403
    

    data=request.json
    try:
        deadline = datetime.strptime(data['deadline'], "%Y-%m-%d")
        palcemntdrive=PlacementDrive(
            company_id=companyid.id,
            job_title=data['job_title'],
            job_description=data['job_description'],
            eligibility_criteria=data['eligibility'],
            application_deadline=deadline


        )
        db.session.add(palcemntdrive)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"msg":'some eroer acure'}),500
    # print(data)
    return jsonify({'msg':''})





@app.route("/studentwhoappplyfordrive/<int:id>")
@jwt_required()
def studentwhoapplyfordrive(id):

    user = get_jwt_identity()
    claim = get_jwt()
    role = claim["role"]
    if role!="company":
        return jsonify({'msg':"aceese denied"}),403
    
    drive=PlacementDrive.query.get(id)
    studentapplication=drive.applications
    # print(studentapplication)
    applciationlist=[]
    # print([s.student for s in studentapplication ])
    for ap in studentapplication:
        applciationlist.append({
            "application_id": ap.id,
            "student_id": ap.student_id,
            "student_name": ap.student.Student_name,
            "email": ap.student.user.email,
            "status": ap.status,
            "drive_id":ap.drive_id
        })
    return jsonify(applciationlist)


@app.route("/update-status", methods=["POST"])
@jwt_required()
def update_status():

    user = get_jwt_identity()
    claim = get_jwt()
    role = claim["role"]
    if role!="company":
        return jsonify({'msg':"aceese denied"}),403
    

    data = request.json

    application_id = data.get("application_id")
    role = data.get("role")

    application = Application.query.get(application_id)
    application.status = role
    db.session.commit()

    return jsonify({"message": "Updated"})

@app.route("/completedrive/<int:id>",methods=["GET","POST"])
@jwt_required()
def completedrive(id):
    claim = get_jwt()
    role = claim["role"]
    if role!="company":
        return jsonify({'msg':"aceese denied"}),403
    drive=PlacementDrive.query.get(id)
    drive.is_active=False
    db.session.commit()
    return jsonify({"message":"complter drive"})


@app.route('/profile/<int:id>', methods=['GET',"PUT"])
def get_profile(id):
    
    if request.method=="GET":
    
        user=User.query.get(id)
        company=user.company
        # print(company)
        return jsonify({
            "name": company.company_name,
            "website": company.website ,
            "phone": company.hr_contact
        })
    if request.method=="PUT":
        user=User.query.get(id)
        company=user.company

        data=request.json
        # print(data)
        company.company_name=data['name']
        company.website=data['phone']
        company.hr_contact=data['website']
        db.session.commit()
        return jsonify({
            'msg':'run perfictly'
        })


@app.route("/interview", methods=["POST","PUT"])
def schedule_interviewe():
    if request.method=="PUT":
        data=request.json
        # print(data['cid'])
        interview=Interview.query.filter_by(company_id=data['cid']).all()
        # print(interview)

        return jsonify({'intervielist':[{'appid':i.application_id,'sutentid':i.student_id,'company_id':i.company_id,"id":i.id,"d":i.interview_date ,"status":i.status}for i in interview]})
    
    data = request.json
    interview_date = datetime.strptime(
        data["interview_date"], "%Y-%m-%d"
    ).date()
    print(data)
    interview = Interview(
        application_id = data["application_id"],
        student_id = data["student_id"],
        company_id=data["cid"],
        interview_date =interview_date,
        status = data["status"],
        feedback = data["feedback"]
    )

    db.session.add(interview)
    db.session.commit()

    return {"message":"Interview Scheduled"}
@app.route("/interviewupdate/<int:id>", methods=["POST","GET"])
def interwive_update(id):
    if request.method=="GET":
        sd=Interview.query.get(id).student
        # print(sd)
        return jsonify({'student':{"id":sd.id,"student_name":sd.Student_name,"resume_link":sd.resume_link,"skills":sd.skills,"experience":sd.experience}})

        
    else:
        data=request.json
        print(data)
        uinterview=Interview.query.get(id)
        uinterview.offer_letter=data['offer_letter']
        uinterview.status=data['new_status']
        uinterview.feedback=data['feedbacke']
        uinterview.application.status=data['new_status']
        uinterview.placed=data['placed']
        
        db.session.commit()


        return {"message":"Interview Scheduled"}











                   

# ya se studetn a funciton ane wale hai 








@app.route('/studentdata/<int:id>')
def studentdata(id):
    student=User.query.get(id).student
    email=student.user.email
    studntname=student.Student_name
    student_id=student.id
    # print(student)
    company = Company.query.all()
    application=Application.query.filter_by(student_id=student.id).all()
    applicationl=[]

    for app in application:
        applicationl.append({
            "id":app.id,
            "student_id":app.student_id,
            "drive_id":app.drive_id,
            "status":app.status

        })
    company 

    

    company_list = []
    
    for company in company:
        company_list.append({
            "id": company.id,
            "company_name": company.company_name,
            'hr_contact':company.hr_contact,
            'website':company.website,
            "email": company.user.email,
            "is_active": company.approval_status
        })
        # print(company_list)
    return jsonify({
        "compnaylist":company_list,
        "applicationlist":applicationl,
        
        "email":email,
        "studentname":studntname,
        "studentid":student_id

    })
    

@app.route('/getdrive/<int:companyid>')
def getdrive(companyid):
    
    drive=PlacementDrive.query.filter_by(company_id=companyid).all()
    # print(drive)
    # return jsonify({'drive':[d.to_json() for d in drive]})
    result=[]
    for d in drive:
        result.append({
        "drive": d.to_json(),
        "applications": [
            {
                "id": ap.id,
                "student_id": ap.student_id,
                "status": ap.status
            }
            for ap in d.applications
            ]
        })
    return jsonify({"data": result})


@app.route('/applydrive',methods=["POST"])
def applydrive():
    data=request.json
    # print(data)
    new_application=Application(
        student_id=data['studentid'],
        drive_id=data['driveid']

    )
    try:

        db.session.add(new_application)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("alerady apply kar rkhahai ")
    return f"retut hiifjidfji"

@app.route('/detailofapplication/<int:id>')
def detailofapplication(id):
    application=Application.query.get(id)
    Placementdrive=PlacementDrive.query.get(application.drive_id)
    company=application.drive.company
    # print(application.drive.company,Placementdrive)
    return jsonify({
        "company": {
            "id": company.id,
            "compnayname": company.company_name,
            "companywebsite": company.website,
            "hrcontact":company.hr_contact
        },
        "drive": {
            "id": Placementdrive.id,
            "job_title": Placementdrive.job_title,
            "job_description":Placementdrive.job_description,
            "eligibiltiy":Placementdrive.eligibility_criteria,
            "application_deadline":Placementdrive.application_deadline

        }
    })



@app.route("/studentprofile/<int:user_id>", methods=["GET","PUT"])
def student_profile(user_id):

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message": "Student not found"}), 404
    
    if request.method == "GET":

        return jsonify({
            "student_name": student.Student_name,
            "education": student.education,
            "skills": student.skills,
            "experience": student.experience,
            "resume_link": student.resume_link
        })
    
    if request.method == "PUT":

        data = request.json

        student.Student_name = data.get("student_name")
        student.education = data.get("education")
        student.skills = data.get("skills")
        student.experience = data.get("experience")
        student.resume_link = data.get("resume_link")

        db.session.commit()

        return jsonify({"message": "Profile updated"})

@app.route("/supcominginterview/<int:id>")
def upcominginterview(id):
    stu=User.query.get(id).student
    
    ui=Interview.query.filter_by(student_id=stu.id).all()
    # print(ui)
    print(ui)
    return jsonify({'intervielist':[{'appid':i.application_id,'sutentid':i.student_id,'company_id':i.company_id,"id":i.id,"d":i.interview_date ,"status":i.status}for i in ui]})




@app.route("/exportapplications/<int:id>", methods=["POST"])

def export_applications(id):
    from task import export_application_history
    export_application_history.delay(id)

    return {
        "message": "CSV export started. You will receive email soon."
    }

# testing 


@app.route("/test")
def test():
    from task import  send_interview_reminders, send_placement_report, export_application_history
   
    send_interview_reminders.delay()
    send_placement_report.delay()
    # export_application_history.delay("1")
    return "Task Triggered!"





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        preadminecreate()
    app.run(debug=True)
