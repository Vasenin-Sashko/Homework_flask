import flask
from flask import Flask
from flask import request
from flask.views import MethodView
from sqlalchemy import create_engine, Integer, DateTime, Column, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask('app')
Base = declarative_base()
engine = create_engine('postgresql://app:12345@localhost:5431/advertisement')
Session = sessionmaker(bind=engine)


class ADV(Base):
    __tablename__ = 'Advs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    heading = Column(String(80), nullable=False)
    description = Column(String(500), nullable=False)
    user_name = Column(String(50), nullable=False, unique=True)
    date_reg = Column(DateTime, server_default=func.now())


Base.metadata.create_all(engine)


class ADV_View(MethodView):

    def get(self, adv_id):
        with Session() as session:
            adv = session.query(ADV).get(adv_id)
            if adv is None:
                responce = flask.jsonify({'status': 'error'})
                responce.status_code = 404
                return responce
            return flask.jsonify({'heading': adv.heading,
                                  'user_name': adv.user_name,
                                  'description': adv.description,
                                  'date_reg': adv.date_reg.isoformat()
                                  })

    def post(self):
        adv_data = dict(request.json)
        with Session() as session:
            new_adv = ADV(heading=adv_data['heading'],
                          description=adv_data['description'],
                          user_name=adv_data['user_name'],
                          )
            session.add(new_adv)
            session.commit()
            return flask.jsonify({'status': 'ok!',
                                  'id': new_adv.id,
                                  'heading': new_adv.heading,
                                  'user_name': new_adv.user_name,
                                  'description': new_adv.description,
                                  })

    def delete(self, adv_id):
        with Session() as session:
            adv = session.query(ADV).get(adv_id)
            session.delete(adv)
            session.commit()
        return flask.jsonify({'status': 'ok!'})


app.add_url_rule('/advs', view_func=ADV_View.as_view('advs'), methods=['POST'])
app.add_url_rule('/advs/<int:adv_id>', view_func=ADV_View.as_view('advs_get'), methods=['GET', 'DELETE'])
app.run()
