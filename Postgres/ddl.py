from .postgres_conn import session
from .models import User, Receipt


def create_user(u_id, user_name, last_name):
    result = session.query(User).filter(User.id == u_id).first()
    if not result:
        user = User(id=u_id, first_name=user_name, last_name=last_name)
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

    return result

def add_view(meal_id):
    receipt = session.query(Receipt).filter(Receipt.id == meal_id).first()

    receipt.reviews += 1
    session.add(receipt)
    session.commit()



