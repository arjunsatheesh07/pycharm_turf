from flask import *

from src.dbop import *

obj=Flask(__name__)

@obj.route('/')
def index():
    return render_template('index1.html')

@obj.route('/home',methods=['post','get'])
def home():
    return render_template('login.html')

@obj.route('/reg')
def reg():
    return render_template('reg.html')

@obj.route('/login',methods=['POST'])
def login():
    uname=request.form['un']
    passwd=request.form['pwd']

    qry = "select * from Login where username='" + uname + "'and password='" + passwd + "'"
    print(qry)
    res=select(qry)
    if res is None:
        return '''<script>alert("invalid userename or passwod");window.location='/'</script>'''
    else:
        if res[3]=='admin':
            return  render_template('adminhome.html')
        else:
            return '''<script>alert("invalid userename or passwod");window.location='/'</script>'''

@obj.route('/viewfeedback')
def viewfeedback():
    qry="SELECT * FROM feedback JOIN user_reg ON user_reg.uid=feedback.uid"
    res=selectall(qry)
    return  render_template('viewfeedback.html',val=res)

@obj.route('/viewuser')
def viewuser():
    qry="select * from User_reg"
    res=selectall(qry)
    return  render_template('viewuser.html',val=res)

@obj.route('/viewturf')
def viewturf():
    qry = "select * from turf_registration"
    res = selectall(qry)
    return render_template('Turf_view.html', val=res)


@obj.route('/verification')
def verification():
    qry="SELECT * FROM login JOIN turf_registration ON turf_registration.lid = login.lid WHERE TYPE ='pending'"
    res=selectall(qry)
    return render_template("/Registration_verification.html",val=res)

@obj.route('/delete')
def delete():
    feedback_id=request.args.get('fid')
    qry="delete from feedback where fid="+str(feedback_id)+""
    iud(qry)
    return '''<script>alert("Deleted");window.location='/viewfeedback'</script>'''


@obj.route('/accepted')
def accept():
    turf_id=request.args.get('lid')
    qry="UPDATE login SET TYPE='turf' WHERE lid='"+turf_id+"'"
    iud(qry)
    return '''<script>alert("You are accepted");window.location='/viewfeedback'</script>'''

@obj.route('/rejected')
def reject():
    turf_id=request.args.get('lid')
    qry="UPDATE login SET TYPE='pending' WHERE lid='"+turf_id+"'"
    iud(qry)
    return '''<script>alert("You are rejected");window.location='/viewfeedback'</script>'''



@obj.route('/logout')
def logout():
    return render_template("/login.html")



obj.run(debug=True)


