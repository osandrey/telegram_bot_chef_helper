from sqlalchemy import desc
from  sqlalchemy.sql.expression import func
from .postgres_conn import session
from .models import User, Receipt


def create_user(u_id, user_name, last_name, language):
    result = session.query(User).filter(User.id == u_id).first()
    if not result:
        user = User(id=u_id, first_name=user_name, last_name=last_name, language=language)
        session.add(user)
        session.commit()
        print('New user was successfully added')


def post_receipt(meal_id, title, instructions, image, user_id):

    receipt = Receipt(id=meal_id, title=title, instructions=instructions, image=image, user_id=user_id)
    session.add(receipt)
    session.commit()
    print(f'New receipt was added to DB!')


def get_reciept_from_db(meal_id: int):

    result = session.query(Receipt).filter(Receipt.id == meal_id).first()
    add_view(meal_id)
    return result

def add_view(meal_id):
    receipt = session.query(Receipt).filter(Receipt.id == meal_id).first()

    receipt.reviews += 1
    session.add(receipt)
    session.commit()


def get_users():
    users = session.query(User).filter(User.active == True).all()
    return users


def get_most_common_reciept():
    reciept = session.query(Receipt).order_by(desc(Receipt.reviews)).first()
    add_view(reciept.id)
    return reciept


def get_random_reciept():
    reciept = session.query(Receipt).order_by(func.random()).first()
    add_view(reciept.id)
    return reciept


if __name__ == '__main__':
    print(get_most_common_reciept())
