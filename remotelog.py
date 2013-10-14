from flask import Flask, request, render_template
from flask.ext.paginate import Pagination
from sqlalchemy import *
from sqlalchemy import event
from sqlalchemy.orm import *
import os, pdb

# ORM initialization
metadata = MetaData()

if os.environ.get('REMOTELOGDB', False):
    db_engine = create_engine(os.environ.get('REMOTELOGDB'), pool_recycle=3600)
else:
    db_engine = create_engine('sqlite:///remotelog.db')

metadata.bind = db_engine

# log table
log_table = Table('Log', metadata,
                Column('Id', Integer, primary_key=True),
                Column('AppSlug', String(20), nullable = False),
                Column('process', String(20)),
                Column('args', String(100)),
                Column('module', String(100)),
                Column('funcName', String(100)),
                Column('exc_text', String(100)),
                Column('name', String(100)),
                Column('thread', String(100)),
                Column('created', String(100)),
                Column('threadName', String(100)),
                Column('msecs', String(100)),
                Column('filename', String(100)),
                Column('levelno', String(10)),
                Column('processName', String(100)),
                Column('pathname', String(300)),
                Column('lineno', String(10)),
                Column('msg', String(5000)),
                Column('exc_info', String(100)),
                Column('levelname', String(50)),
                Column('CreatedDate', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')))

class Log(object):
    pass

# create tables on boot
metadata.create_all(db_engine, checkfirst=True)
mapper(Log, log_table)

# flask app initialization
app = Flask(__name__)
app.debug = True

@app.route("/view_log/<appSlug>",methods=['GET',])
def viewlog(appSlug):
    db = Session()
    search = False


    q = request.args.get('q')
    if q:
        search = True

    #dboperation.query(model.System).get(tw_sys_id)
    logrecords = db.query(Log).filter_by(AppSlug = appSlug).order_by(desc(Log.CreatedDate)).all()

    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    pagination = Pagination(page=page, total=logrecords.__len__(), search=search, record_name='logrecords')
    return render_template('view_log.html',
                           logrecords=logrecords,
                           pagination=pagination,
                           )

@app.route("/log/<appSlug>",methods=['POST',])
def store_log(appSlug):

    d = request.form
    db = Session()

    log = Log()
    log.AppSlug = appSlug
    log.relativeCreated = d['relativeCreated']
    log.process = d['process']
    log.args = d['args']
    log.module = d['module']
    log.funcName = d['funcName']
    log.exc_text = d['exc_text']
    log.name = d['name']
    log.thread = d['thread']
    log.created = d['created']
    log.threadName = d['threadName']
    log.filename = d['filename']
    log.levelno = d['levelno']
    log.processName = d['processName']
    log.pathname = d['pathname']
    log.lineno = d['lineno']
    log.msg = d['msg']
    log.msecs = d['msecs']
    log.exc_info = d['exc_info']
    log.levelname = d['levelname']

    db.add(log)
    db.commit()
    db.close()

    return ''

if __name__ == "__main__":
    #app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 33507)))
    app.run(host='0.0.0.0')