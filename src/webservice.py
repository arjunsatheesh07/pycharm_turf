import pymysql
con = pymysql.connect(host='localhost', user='root', password='Admin@123', port=3306, db='turf')
cmd = con.cursor()
from flask import *

from datetime import datetime
app=Flask(__name__)

@app.route('/login',methods=['get','post'])
def login():
    name=request.form['uname']
    pword=request.form['pass']
    print("select * from login where username='"+str(name)+"' and password='"+str(pword)+"' ")
    cmd.execute("select * from login where username='"+str(name)+"' and password='"+str(pword)+"' and type!='pending' ")
    s=cmd.fetchone()
    print(s)
    if s==None:
        return jsonify({'task':'fail'})
    else:
        return jsonify({'task':str(s[0]),"type":s[3]})

@app.route('/signupturf',methods=['post','get'])
def signupturf():
    try:
        print(request.form)
        name = request.form['name']
        place = request.form['place']
        landmark = request.form['landmark']
        phno = request.form['phone']
        print(phno)
        email = request.form['email']
        print(email)
        latt = request.form['lat']
        long = request.form['long']
        img=request.files['files']
        fn=datetime.now().strftime("%Y%m%d_%H%M%S")+".jpg"
        img.save("static/turfimg/"+fn)
        un = request.form['un']
        print(un)
        pw = request.form['pw']
        print(pw)
        cmd.execute("insert into login values(NULL,'"+un+"','"+pw+"','pending')")
        id = con.insert_id()
        cmd.execute("insert into turf_registration  values(null,'"+str(id)+"','"+name+"','"+place+"','"+landmark+"','"+phno+"','"+email+"','"+fn+"','"+latt+"','"+long+"')")
        con.commit()
        return jsonify({'task':"success"})
    except Exception as e:
        print(str(e))
        return jsonify({'task': "Faild"})

# addnewturf

@app.route('/addnewturf',methods=['post','get'])
def addnewturf():
    try:
        print(request.form)
        name = request.form['name']
        place = request.form['place']
        landmark = request.form['landmark']
        phno = request.form['phone']
        print(phno)
        email = request.form['email']
        print(email)
        latt = request.form['lat']
        long = request.form['long']
        img=request.files['files']
        fn=datetime.now().strftime("%Y%m%d_%H%M%S")+".jpg"
        img.save("static/turfimg/"+fn)
        id = request.form['id']
        cmd.execute("insert into turf_registration  values(null,'"+str(id)+"','"+name+"','"+place+"','"+landmark+"','"+phno+"','"+email+"','"+fn+"','"+latt+"','"+long+"')")
        con.commit()
        return jsonify({'task':"success"})
    except Exception as e:
        print(str(e))
        return jsonify({'task': "Faild"})

#for adding facilities of turf
@app.route('/addfacility',methods=['post'])
def addfacility():
    try:
        facility = request.form['facility']
        description = request.form['description']
        lid = request.form['tid']
        img = request.files['files']

        fn = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
        print(fn)
        path1="static/fecility/"
        img.save("static/fecility/"+fn)
        print("ok")
        cmd.execute("insert into facilities values(NULL,'"+str(lid)+"','"+str(facility)+"','"+str(description)+"','"+fn+"')")
        con.commit()
        return jsonify({'task': "success"})
    except Exception as e:
        print(str(e))
        return jsonify({'task': "Failed"})


@app.route('/signupuser',methods=['post','get'])
def signupuser():
    try:
        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']
        phno = request.form['phone']
        print(phno)
        email = request.form['email']
        print(email)
        un = request.form['un']
        print(un)
        pw = request.form['pw']
        print(pw)
        cmd.execute("insert into login values(NULL,'"+un+"','"+pw+"','user')")
        id = con.insert_id()
        cmd.execute("insert into user_reg values(null,'"+str(id)+"','"+fname+"','"+mname+"','"+lname+"','"+phno+"','"+email+"')")
        con.commit()
        return jsonify({'task':"success"})
    except Exception as e:
        print(str(e))
        return jsonify({'task': "Faild"})


@app.route('/viewfacility',methods=['post'])
def viewfacility():
    tid=request.form['tid']
    print(tid)
    cmd.execute("SELECT * FROM facilities where tid='"+tid+"'")

    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(results, json_data)
    return jsonify(json_data)

# view available slots
@app.route('/viewslots',methods=['post'])
def viewslots():
    date=request.form['date']
    tid=request.form['tid']
    cmd.execute("SELECT sid FROM `sloat_status` WHERE `tid`='"+tid+"' AND `date`='"+date+"' ")
    con.commit()
    return jsonify({'task': "success"})

@app.route('/viewuser',methods=['post'])
def viewuser():

    cmd.execute("SELECT * FROM user_reg  ")

    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(results, json_data)
    return jsonify(json_data)

@app.route('/viewturf',methods=['post'])
def viewturf():
    name = request.form['name']
    place = request.form['place']
    landmark = request.form['fname']
    phno = request.form['phno']
    mail_id = request.form['mail_id']
    cmd.execute("SELECT * FROM turf_registration WHERE name='"+str(name)+"',place='"+str(place)+"',landmark='"+str(landmark)+"',phno='"+str(phno)+"',mail_id='"+str(mail_id)+"'")

    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(results, json_data)
    return jsonify(json_data)

# turfviewby user

@app.route('/turfviewuser',methods=['post'])
def turfviewuser():


    cmd.execute("SELECT `turf_registration`.*,`turfrating`.`rating` ,`facilities`.`facility`,`facilities`.`description` , facilities.image as fimage FROM `turfrating` JOIN `turf_registration` ON `turf_registration`.`lid`=`turfrating`.`tid` JOIN `facilities` ON `facilities`.`tid`=`turf_registration`.`lid` ")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(results, json_data)
    return jsonify(json_data)

@app.route('/owneruniqueturf',methods=['post'])
def owneruniqueturf():
    logid = request.form['lid']
    cmd.execute("SELECT turf_registration.*,AVG(rating) as rating FROM  `turf_registration` left JOIN turfrating ON  `turfrating`.`tid`=`turf_registration`.`tid` WHERE turf_registration.lid='"+logid+"'   GROUP BY `turfrating`.tid ")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(results, json_data)
    return jsonify(json_data)



# feedbackturfview
@app.route('/feedbackturfview',methods=['post'])
def feedbackturfview():

    cmd.execute("SELECT tid,name  FROM turf_registration ")
    con.commit()

#for turf owner

@app.route('/viewmyslot',methods=['post'])
def viewmyslot():
    tid=request.form['tid']
    print(tid)
    cmd.execute("SELECT * from sloat_status  WHERE `tid`='"+tid+"' and status='booked'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(results, json_data)
    return jsonify(json_data)



#slot view for user
@app.route('/viewmyslotavail',methods=['post'])
def viewmyslotavail():
    print(request.form)
    date=request.form['date']
    tid = request.form['tid']
    cmd.execute("SELECT `sloat` FROM `sloat_status` WHERE `status`='booked' AND `date`='"+date+"' AND  `tid`='"+tid+"' UNION SELECT `slot` FROM `booking` WHERE `tid`='"+tid+"' AND `bdate`='"+date+"' and status!='pending'")
    s=cmd.fetchall()

    lis=[]
    for i in s:
        lis.append(i[0])
    sloats=[]
    sloats.append("01 to 02");
    sloats.append("02 to 03");
    sloats.append("03 to 04");
    sloats.append("04 to 05");
    sloats.append("05 to 06");
    sloats.append("06 to 07");
    sloats.append("07 to 08");
    sloats.append("08 to 09");
    sloats.append("09 to 10");
    sloats.append("10 to 11");
    sloats.append("11 to 12");
    sloats.append("12 to 13");
    sloats.append("13 to 14");
    sloats.append("14 to 15");
    sloats.append("15 to 16");
    sloats.append("16 to 17");
    sloats.append("17 to 18");
    sloats.append("18 to 19");
    sloats.append("19 to 20");
    sloats.append("20 to 21");
    sloats.append("21 to 22");
    sloats.append("22 to 23");
    sloats.append("23 to 00");
    sloats.append("00 to 01");


    row_headers =["sloat"]

    json_data = []
    for result in sloats:
        if result not in lis:
            json_data.append(dict(zip(row_headers, [result])))
    con.commit()
    print( json_data)
    return jsonify(json_data)


@app.route('/ownerviewturf', methods=['post'])
def ownerviewturf():
    id=request.form['uid']
    cmd.execute("SELECT `turf_registration`.*,`login`.* FROM `login` JOIN `turf_registration` ON `turf_registration`.`lid`=`login`.`lid` WHERE `login`.`type`='owner' AND `turf_registration`.`lid`='"+str(id)+"'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(results, json_data)
    return jsonify(json_data)



@app.route('/insertslots',methods=['post'])
def insertslots():
    try:
        slot = request.form['slot']
        tid=request.form['tid']
        date=request.form['date']
        cmd.execute("SELECT * FROM `sloat_status` WHERE `tid`='"+tid+"' AND `date`='"+date+"' AND `sloat`='"+slot+"' ")
        s=cmd.fetchone()
        if s is None:
            cmd.execute("insert into sloat_status values(null,'"+str(tid)+"','"+date+"','"+slot+"','booked')")
            con.commit()
            return jsonify({'task':'ok'})
        else:
            return jsonify({'task': "Duplicate Enryyyy"})


    except Exception as e:
        print(str(e))
        return jsonify({'task': "Duplicate Enryyyy"})

# booked details
@app.route('/bookinghistory',methods=['post'])
def bookinghistory():
    tid=request.form['tid']
    print(tid)
    cmd.execute("SELECT `booking`.*,`turf_registration`.* ,`user_reg`.`fname`,`lname`,`mname` FROM `booking` JOIN `turf_registration` ON `booking`.`tid`=`turf_registration`.`lid` JOIN `user_reg` ON `user_reg`.`lid`=`booking`.`uid` WHERE `booking`.`tid`='"+tid+"' AND `booking`.`status`='pending'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(results, json_data)
    return jsonify(json_data)


# Booking for user
@app.route('/userbooking',methods=['post','get'])
def userbooking():
    print(request.form)
    try:
        uid=request.form['uid']
        tid = request.form['tid']
        bdate = request.form['date']

        nos = request.form['slot']

        ss=nos.split("@")
        print(ss)
        bookingids=""
        for i in ss:
            print(i)
            if i!="":
                cmd.execute("select *  from booking where uid='" + uid + "'and  slot='"+i+"' and date='"+bdate+"'")
                dd=cmd.fetchone()
                if dd is None:

                    cmd.execute("insert into booking values(null,'"+uid+"','"+tid+"',curdate(),'"+bdate+"','"+i+"','pending')")
                    bookingids=bookingids+str(con.insert_id())+"#"

                else:
                    return jsonify({'task': "already..."})
        con.commit()
        print(bookingids)
        return jsonify({'task': "success","bid":bookingids})



    except Exception as e:
        print("error================================="+str(e))
        return jsonify({'task': "Faild"})


@app.route('/bookstatusupdate',methods=['post'])
def bookstatusupdate():
    tid=request.form['bid']
    print(tid)
    cmd.execute("UPDATE booking  set status='booked' WHERE `bid`='"+tid+"'")
    con.commit()
    return jsonify({'task': "success"})


# feedback for app
@app.route('/feedback',methods=['post','get'])
def feedback():
    uid=request.form['uid']
    print(uid)
    fdback = request.form['feed']
    print(fdback)
    rate = request.form['rating']
    print(rate)
    cmd.execute("SELECT * FROM `feedback` where uid='"+uid+"'")
    s=cmd.fetchall()

    if s is None:

        cmd.execute("insert into feedback values(null,'" + uid + "','" + fdback + "','" + rate + "',curdate())")
        con.commit()
        return jsonify({'task': "success"})

    else:
        cmd.execute("update feedback set feedback='" + fdback + "',rating='" + rate + "',date=curdate() where feedback.uid='" + str(uid) + "'")
        con.commit()
        return jsonify({'task': "success"})

# feedback by user
@app.route('/feedbackbyuser',methods=['post','get'])
def feedbackbyuser():
    uid=request.form['uid']
    print(uid)
    tid = request.form['tid']
    fdback = request.form['feed']
    print(fdback)
    rate = request.form['rating']
    print(rate)
    cmd.execute("SELECT * FROM `turfrating` where uid='"+uid+"'")
    s=cmd.fetchone()

    # if s is None:

    cmd.execute("insert into turfrating values(null,'" + tid + "','" + uid + "','" + rate + "','" + fdback + "')")
    con.commit()
    return jsonify({'task': "success"})

    # else:
    #     cmd.execute("update turfrating set rating='" + rate + "',feedback='" + fdback + "' where feedback.uid='" + str(uid) + "'")
    #     con.commit()
    #     return jsonify({'task': "success"})



# payment by user
@app.route('/payment',methods=['post','get'])
def payment():
    bid=request.form['bid']
    amt = request.form['amt']
    cmd.execute("insert into payment values(null,'"+bid+"','"+amt+"',curdate(),'pending')")
    con.commit()
    return jsonify({'task': "success"})



#final payment
@app.route('/finalpay',methods=['post','get'])
def finalpay():
    print(request.form)

    bid=request.form['bid']
    bidd=bid.split("#")

    bname = request.form['bname']
    accno = request.form['accno']
    ifsc = request.form['ifsc']
    phno = request.form['phno']
    amt = request.form['amt']
    cmd.execute("SELECT `balance`,`bank_id` FROM `bank` WHERE `bname`='"+bname+"' AND `accno`='"+accno+"' AND `ifsc`='"+ifsc+"' AND `phno`='"+phno+"' ")
    s=cmd.fetchone()
    if s is not None:
        if float(s[0])>float(amt):
            for i in bidd:
                if i!='':
                    cmd.execute("UPDATE `booking` SET `status`='booked' WHERE `bid`='"+i+"'")
                    con.commit()
            cmd.execute("SELECT `tid` FROM `booking` WHERE `bid`='"+bidd[0]+"'")
            ss=cmd.fetchone()
            cmd.execute("insert into payment values(null,'"+str(ss[0])+"','"+amt+"',curdate(),'pending')")
            cmd.execute("UPDATE `bank` SET `balance`=`balance`-"+amt+" WHERE `bank_id`='"+str(s[1])+"'")
            con.commit()
            return jsonify({'task': "success"})
        else:
            for i in bidd:
                if i!='':
                    cmd.execute("delete from `booking`  WHERE `bid`='"+i+"'")
                    con.commit()
            return jsonify({'task': "no balance"})
    else:
        return jsonify({'task': "Invalid data"})

# @app.route('/viewwork')
# def viewwork():
#     dta=(cmd.execute("select * from works "))
#     row_headers = [x[0] for x in cmd.description]
#     results = cmd.fetchall()
#     json_data = []
#     for result in results:
#         json_data.append(dict(zip(row_headers, result)))
#     con.commit()
#     print(results, json_data)
#     return jsonify(json_data)

# @app.route('/viewmessage')
# def viewmessage():
#     id=request.arg
# s.get('id')
#     session['myid']=id
#     dta =(cmd.execute("select * from message where to_id='"+id+"' "))
#     row_headers = [x[0] for x in cmd.description]
#     results = cmd.fetchall()
#     json_data = []
#     for result in results:
#         json_data.append(dict(zip(row_headers, result)))
#     con.commit()
#     print(results, json_data)
#     return jsonify(json_data)
@app.route('/viewcomplaint',methods=['post'])
def viewcomplaint():
    id=request.form['uid']
    # session['myid']=id
    dta =(cmd.execute("select * from complaints where from_id='"+str(id)+"' "))
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(results, json_data)
    return jsonify(json_data)


@app.route('/viewfeedback',methods=['post'])
def viewfeedback():


    results =cmd.execute("SELECT `user_reg`.`fname`,`user_reg`.`mname`,`user_reg`.`lname`,`feedback`.* FROM `feedback` JOIN `user_reg` ON `feedback`.`uid`=`user_reg`.`lid`")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(results, json_data)
    return jsonify(json_data)


@app.route('/replymsg',methods=['post'])
def replymsg():
    session['toid']=request.args.get('to_id')
    msgid=request.args.get('frmid')
    msg=request.args.get('msg')
    dta=(cmd.execute("select * from message where id='"+msgid+"'"))
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(results, json_data)
    return jsonify(json_data)

# @app.route('/replyclick')
# def replyclick():
#     fid=session['myid']
#     toid=session['toid']
#     msg = request.args.get('msg')
#     cmd.execute("insert into message values(NULL,,'"+fid+"','"+toid+"',curdate(),'"+msg+"')")
#     return jsonify({'task', "success"})



@app.route('/complaints',methods=['post'])
def addcomplaint():
    try:
        complaint=request.form['com']
        user_id=request.form['lid']
        # print("insert into complaints values(NULL,'"+str(user_id)+"','"+str(complaint)+"','pending',curdate())")
        cmd.execute("insert into complaints values(NULL,'"+user_id+"','"+complaint+"','pending',curdate())")
        con.commit()
        print("okkkkkk")
        return jsonify({'task': "success"})
    except Exception as e:
        print(str(e))
        return jsonify({'task': "Faild"})

@app.route('/addcustomplan',methods=['post'])
def addcustomplan():
    try:
        pname=request.form['pname']
        area=request.form['area']
        rooms=request.form['rooms']
        stories=request.form['stories']
        desc=request.form['desc']
        archname=request.form['archname']
        print(archname,"arch")
        userid=request.form['lid']
        print("insert into customized_plan values(NULL,'"+str(pname)+"','"+str(userid)+"','"+str(area)+"','"+str(rooms)+"','"+str(stories)+"','"+str(archname)+"','"+str(desc)+"','pending')")
        cmd.execute("insert into customized_plan values(NULL,'"+str(pname)+"','"+str(userid)+"','"+str(area)+"','"+str(rooms)+"','"+str(stories)+"','"+str(archname)+"','"+str(desc)+"','pending')")
        con.commit()
        print("okkkkkk")
        return jsonify({'task': "success"})

    except Exception as e:
        print(str(e))
        return jsonify({'task': "Faild"})

@app.route('/addcustomplans',methods=['post'])
def addcustomplans():
     try:
         dta =cmd.execute("select id,architectname from architect")
         row_headers = [x[0] for x in cmd.description]
         results = cmd.fetchall()
         json_data = []
         for result in results:
             json_data.append(dict(zip(row_headers, result)))
         con.commit()
         print(results, json_data)
         return jsonify(json_data)

     except Exception as e:
         print(str(e))
         return jsonify({'task': "Faild"})




@app.route('/names',methods=['post'])
def names():
    try:

                dta = cmd.execute("select id,architectname from architect")
                row_headers = [x[0] for x in cmd.description]
                results = cmd.fetchall()
                print(results,"pppp")
                json_data = []
                for result in results:
                    json_data.append(dict(zip(row_headers, result)))
                con.commit()
                print(results, json_data)
                return jsonify(json_data)

                # elif(type=="Exteriordesigner"):
            #     dta = cmd.execute("select id,designer_name from exteriordesigner")
            #     row_headers = [x[0] for x in cmd.description]
            #     results = cmd.fetchall()
            #     json_data = []
            #     for result in results:
            #         json_data.append(dict(zip(row_headers, result)))
            #     con.commit()
            #     print(results, json_data)
            #
            # elif (type == "Worker"):
            #     dta = cmd.execute("select id,workername from worker")
            #     row_headers = [x[0] for x in cmd.description]
            #     results = cmd.fetchall()
            #     json_data = []
            #     for result in results:
            #         json_data.append(dict(zip(row_headers, result)))
            #     con.commit()
            #     print(results, json_data)

    except Exception as ex:
            print(str(ex))
            return jsonify({'task': "Faild"})

@app.route('/replyclick',methods=['post'])
def replyclick():
    fid=request.form['from_id']
    toid = request.form['toid']
    msg = request.form['msg']
    cmd.execute("insert into message values(NULL,'"+str(fid)+"','"+str(toid)+"',curdate(),'"+str(msg)+"')")
    con.commit()
    return jsonify({'task': "success"})

@app.route('/viewchat',methods=['post'])
def viewchat():
    fid = request.form['from_id']
    toid = request.form['toid']
    dta=cmd.execute("select * from message where from_id='"+fid+"' and to_id='"+toid+"' or from_id='"+toid+"' and to_id='"+fid+"'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(results, json_data)
    return jsonify(json_data)

@app.route('/viewplans',methods=['post'])
def viewplans():
    dta = (cmd.execute("select * from plan "))
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(results, json_data)
    return jsonify(json_data)

@app.route('/profile',methods=['post'])
def profile():
    id=request.form['lid']
    print(id)
    (cmd.execute("select * from user where id='"+str(id)+"'"))
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(results, json_data)
    return jsonify(json_data)

@app.route('/updateprof',methods=['post'])
def updateprof():
    try:
        id = request.form['lid']
        nam = request.form['name']
        age = request.form['age']
        pho = request.form['phno']
        email = request.form['eid']
        cmd.execute("update user set name='"+nam+"',age='"+age+"',phone_number='"+pho+"',email_id='"+email+"' where id='"+id+"' ")
        con.commit()
        print("okkkkkk")
        return jsonify({'task': "success"})
    except Exception as ee:
        print(str(ee))
        return jsonify({'task': "Faild"})

# booking details for payment
@app.route('/bookingdet',methods=['post'])
def bookingdet():
    try:
            type=request.form['type']
            uid=request.form['lid']
            # did=request.form['dsid']
            print(type)
            # if(type=="plan"):
            cmd.execute("select booking.id as bid,plan.plan_name,plan.price,plan.id from booking,plan where booking.design_id=plan.id and booking.user_id='"+str(uid)+"' and booking.status='approved' ")
            row_headers = [x[0] for x in cmd.description]
            results = cmd.fetchall()
            print(results,"pppp")
            json_data = []
            for result in results:
                json_data.append(dict(zip(row_headers, result)))
            con.commit()
            print(results, json_data)
            return jsonify(json_data)

            #
            # elif(type=="exteriordesign"):
            #     cmd.execute("select booking.id as bid,exterior_design.design_name,exterior_design.price,exterior_design.id from booking,exterior_design where booking.design_id=exterior_design.id and booking.user_id='"+str(uid)+"' and booking.status='approved'")
            #     row_headers = [x[0] for x in cmd.description]
            #     results = cmd.fetchall()
            #     json_data = []
            #     for result in results:
            #         json_data.append(dict(zip(row_headers, result)))
            #     con.commit()
            #     print(results, json_data)
            #
            # else:
            #     cmd.execute("select booking.id as bid,works.name_of_work,works.price,works.id from booking,works where booking.design_id=works.id and booking.user_id='"+str(uid)+"' and booking.status='approved'")
            #     row_headers = [x[0] for x in cmd.description]
            #     results = cmd.fetchall()
            #     json_data = []
            #     for result in results:
            #         json_data.append(dict(zip(row_headers, result)))
            #     con.commit()
            #     print(results, json_data)

    except Exception as ex:
            print(str(ex))
            return jsonify({'task': "Faild"})
@app.route('/pay',methods=['post'])
def pay():
     try:
         ifsc=request.form['ifs']
         accno=request.form['accno']
         lid = request.form['lid']
         desid = request.form['desid']
         print(desid)
         amt=request.form['amt']
         print(amt)
         bname = request.form['bnam']
         print("select amount from bank where bankname='"+bname+"' and  and ifsc='"+ifsc+"' and `accountno`='"+accno+"'")
         cmd.execute("select amount from bank where bankname='"+bname+"' and ifsc='"+ifsc+"' and `accountno`='"+accno+"' and uid='"+str(lid)+"'")
         s=cmd.fetchone()
         print(s[0])
         if s is None:
             print("invalid details")
             return jsonify({'task': "Faild"})
         elif(str(s[0])<str(amt)):
             print("insufficient balance")
             return jsonify({'task': "insufficient balance"})
         else:
             res = float(s[0])-float(amt)
             print("result", res)
             cmd.execute("update bank set amount='"+str(res)+"' where bankname='"+str(bname)+"' and ifsc='"+str(ifsc)+"'")
             cmd.execute("update booking set status='paid' where user_id='"+str(lid)+"' and design_id='"+str(desid)+"'")
             con.commit()
             print("+++++ success" )
             return jsonify({'task': "success"})

     except Exception as ex:
         print(str(ex)+"failed")
         return jsonify({'task': "Faild"})

@app.route('/rating',methods=['post'])
def rating():
            try:
                rating=request.form['rate']
                uid=request.form['lid']
                desid=request.form['desid']
                print(desid)
                print(rating)
                print(uid)
                d=desid.replace('[','').replace(']','')
                print(d)
                cmd.execute("insert into rating values(NULL,'"+str(uid)+"','"+str(d)+"','"+rating+"')")
                con.commit()
                print("+++++ success")
                return jsonify({'task': "success"})
            except Exception as ex:
                print(str(ex) + "failed")
                return jsonify({'task': "failed"})

# @app.route('/workbooking',methods=['get'])
# def workbooking():
#     try:
#

#plan ext design booking
@app.route('/addbooking',methods=['post'])
def addbooking():
    uid=request.form['lid']

    # cmd.execute("select id from plan where id='"+did+"'")
    # cmd.execute("select id from exterior_design where id="+did+"")
    # c=cmd.fetchone()
    did=request.form['planid']
    cmd.execute("insert into booking values(NULL,'"+str(uid)+"','"+str(did)+"',curdate(),'pending')")
    con.commit()
    return jsonify({'task': "success"})

@app.route('/areachoose',methods=['post'])
def areachoose():
    area=request.form['area']
    cmd.execute("select * from plan where area<'"+str(area)+"' and status='approved'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(results, json_data)
    return jsonify(json_data)

@app.route('/viewext',methods=['post'])
def viewext():
    dta = (cmd.execute("select * from exterior_design"))
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(results, json_data)
    return jsonify(json_data)



# remove soat

@app.route('/removeslot',methods=['post'])
def removeslot():
    sid = request.form['ssid']

    print(sid)
    cmd.execute("delete from sloat_status where ssid='"+str(sid)+"'")
    con.commit()
    return jsonify({'task': "success"})

# insertfeedetails
@app.route('/feeinsert',methods=['post'])
def feeinsert():
    amount = request.form['amount']
    tid = request.form['tid']
    cmd.execute("insert into fee_details values(null,'"+tid+"','"+amount+"')")
    con.commit()
    return jsonify({'task': "success"})

#for getting same turf info of a particular user
@app.route('/turfunique',methods=['post'])
def turfunique():
    ttid = request.form['lid']

    cmd.execute("select * from turf_registration where lid='"+ttid+"'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(results, json_data)
    return jsonify(json_data)





@app.route('/viewnearst_turf',methods=['post'])
def viewnearst_turf():
    latitude = request.form['latti']
    print(latitude)
    longitude = request.form['longi']
    print(longitude)
    # aid=request.form['aid']
    # print(cid,"cidddd")
    print(latitude, longitude)
    # cmd.execute("SELECT distinct `turf_registration`.*,`fee_details`.`amount`,(3959 * ACOS ( COS ( RADIANS('"+str(latitude)+"') ) * COS( RADIANS(`turf_registration`.`latti`) ) * COS( RADIANS(`turf_registration`.`longi`) - RADIANS('"+str(longitude)+"') ) + SIN ( RADIANS('"+str(latitude)+"') ) * SIN( RADIANS(`turf_registration`.`latti`) ))) AS user_distance FROM `turf_registration` LEFT JOIN `fee_details` ON  `turf_registration`.`tid`=`fee_details`.`tid` HAVING user_distance  < 6.2137")
    cmd.execute("SELECT DISTINCT `facilities`.`facility`,`facilities`.`description`,`turf_registration`.*,`fee_details`.`amount`,(3959 * ACOS ( COS ( RADIANS('11.2578106') ) * COS( RADIANS(`turf_registration`.`latti`) ) * COS( RADIANS(`turf_registration`.`longi`) - RADIANS('75.7845282') ) + SIN ( RADIANS('11.2578106') ) * SIN( RADIANS(`turf_registration`.`latti`) ))) AS user_distance FROM `turf_registration` LEFT JOIN `fee_details` ON  `turf_registration`.`tid`=`fee_details`.`tid` JOIN `facilities` ON `facilities`.`tid`=`turf_registration`.`tid`HAVING user_distance  < 6.2137")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(json_data)
    return jsonify(json_data)


@app.route('/updateturfinfo',methods=['post'])
def updateturfinfo():
    tid=request.form['uid']
    print(tid)
    name = request.form['name']
    print(name)
    place = request.form['place']
    print(place)
    landmark = request.form['landmark']
    print(landmark)
    phno = request.form['phno']
    print(phno)
    mail = request.form['email']
    print(mail)
    latt = request.form['latti']
    print(latt)
    long = request.form['longi']
    print(long)


    cmd.execute("update  turf_registration set name='"+str(name)+"',place='"+str(place)+"',landmark='"+str(landmark)+"',phno='"+str(phno)+"',mail_id='"+str(mail)+"',latti='"+str(latt)+"',longi='"+str(long)+"' where lid='"+str(tid)+"'")
    con.commit()
    return jsonify({'task': "success"})

# incomeview
@app.route('/incomeview',methods=['post'])
def incomeview():
    logid = request.form['lid']

    mth = request.form['month']
    if(mth=="January"):

        month=1
    if(mth=="February"):
        month=2

    if (mth == "March"):
        month = 3

    if (mth == "April"):
        month = 4

    if (mth == "May"):
        month = 5

    if (mth == "June"):
        month = 6

    if (mth == "July"):
        month = 7

    if (mth == "August"):
        month = 8

    if (mth == "September"):
        month = 9

    if (mth == "October"):
        month = 10

    if (mth == "November"):
        month = 11

    if (mth == "December"):
        month = 12

    year = request.form['year']


    cmd.execute("SELECT SUM(amount),turf_registration.`name` FROM `payment`  JOIN `turf_registration` ON `turf_registration`.`tid`=`payment`. tid AND `turf_registration`.lid='"+str(logid)+"'  WHERE MONTH(DATE)='"+str(month)+"' AND YEAR(DATE)='"+str(year)+"'   GROUP BY `payment`.tid ")

    s=cmd.fetchone()
    print(s)
    if s is None:
        return jsonify({'task':'none'})
    else:
        return jsonify({'task':s[0]})


@app.route('/viewallturf',methods=['post'])
def viewallturf():

    cmd.execute("select * from turf_registration")
    con.commit()
    return jsonify({'task': "success"})



if __name__=="__main__":
    app.run(host='0.0.0.0',port=5000)
