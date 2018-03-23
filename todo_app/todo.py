from flask import Flask ,jsonify
from flask_restful import reqparse, abort, Api, Resource

from dbconnect import connection
app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
cursor,conn=connection()


class Add(Resource):
    def post(self):
        try:
                #Arguments Which needs to be entered by Clients
            parser.add_argument('taskid', type=int)
            parser.add_argument('taskname', type=str)
            parser.add_argument('isdone', type=str)
            parser.add_argument('createdat', type=str)
            parser.add_argument('doneat', type=str)

            args = parser.parse_args()

            taskid = args['taskid']      #taskid is mandatory
            if args['taskname'] == None or args['taskname'] == "":  #if taskname is missing then by default taskname will be "default"
                taskname="Default"
            else:
                taskname = args['taskname']

            if args['isdone'] == None or args['isdone'] == "":  #if this argument is missing i.e not mentioned that task is done or not then by default isdone will be "no"
                isdone="no"#by default isdone will "No"
            else:
                isdone = args['isdone']

            if args['createdat'] == None or args['createdat'] == "":   #if this argument is missing i.e not mentioned that when task is created or not then by default createdat will be "NA"
                createdat="NA"#by default isdone will "NA"
            else:
                createdat = args['createdat']

            if args['doneat'] == None or args['doneat'] == "" or args['isdone'] == "no": #if doneat is missing or task is not done yet (isdone =no) then by default doneat will be NA
                    doneat = "NA"  # by default isdone will "NA"
            else:
                    doneat = args['doneat']

            cursor.execute("insert into task values(%s,'%s','%s','%s','%s');"%(taskid,taskname,isdone,createdat,doneat))

            conn.commit()
            return {'StatusCode':'200','Message': 'Success'}

        except Exception as e:
            return {'error': str(e)}

class edit(Resource):
    def put(self,task_id):
        try:
            cursor.execute('''select taskname,isdone,createdat,doneat from task where taskid=%s'''%task_id)
            task = [dict((cursor.description[i][0], value)
                      for i, value in enumerate(r)) for r in cursor.fetchall()]


            parser.add_argument('taskname', type=str)
            parser.add_argument('isdone', type=str)
            parser.add_argument('createdat', type=str)
            parser.add_argument('doneat', type=str)

            args = parser.parse_args()

            if args['taskname'] == None or args['taskname'] == "":  #if this field is missing then remain the taskname be same as previous othervise updated with new value
                taskname = task[0].get('taskname')
            else:
                taskname = args['taskname'] #updated with new value

            if args['isdone'] == None or args['isdone'] == "": #if this field is missing then remain isdone status be same as previous othervise updated with new value
                isdone = task[0].get("isdone")  # by default isdone will "No"
            else:
                isdone = args['isdone'] #updated with new value

            if args['createdat'] == None or args['createdat'] == "": # if this field is missing then remain createdat be same as previous othervise updated with new value
                createdat = task[0].get('createdat')  # by default isdone will "No"
            else:
                createdat = args['createdat'] #updated with new value

            if args['doneat'] == None or args['doneat'] == "" or args['isdone'] == "no":# if this field is missing or (isDone =No)then remain doneat be same as previous othervise updated with new value
                doneat = task[0].get('doneat')  # by default isdone will "NA"
            else:
                doneat = args['doneat']   #updated with new value


            cursor.execute("UPDATE task SET taskname='%s',isdone='%s',createdat='%s',doneat='%s' where taskid=%s ;" % (taskname,isdone,createdat,doneat,task_id))

            conn.commit()

            return {'StatusCode': '200', 'Message': 'Success'}
        except Exception as e:
            return {'error': str(e)}


class Read(Resource):
    def get(self):
        try:

            #get all the tasks from database
            cursor.execute('''select * from task''')
            task = [dict((cursor.description[i][0], value)
                      for i, value in enumerate(row)) for row in cursor.fetchall()]
            return jsonify({'TODO List': task})   # return all data in json format
        except Exception as e:
            return {'error': str(e)}

#API Calling
api.add_resource(Add, '/add')
api.add_resource(Read, '/read')
api.add_resource(edit, '/edit/<task_id>')

if __name__ == '__main__':
    app.run(debug=True)