import sqlite3

conn = sqlite3.connect('service.db')
cursor = conn.cursor()


async def update_db_user_profile(user, data):
    cursor.execute("UPDATE users SET email= '%s', address = '%s' where user = '%s' " % (data['email'],
                                                                                        data['address'],
                                                                                        user))
    cursor.execute("UPDATE orders SET destination = '%s' where user = '%s' " % (data['address'],
                                                                                user))
    conn.commit()


async def insert_db_new_orders(order, user):
    user_info = cursor.execute("SELECT address, vip_user from users where user = '%s' " % user).fetchone()
    user_info = dict(zip(('address', 'vip_user'), user_info))
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (uid text, product text, quantity int, user text, status text, 
                        user_type text, returned_qty int, cancelled_qty int, destination text)''')
    cursor.execute("INSERT INTO orders VALUES ('%s','%s','%s','%s','%s','%s', '%s','%s','%s')" % (order['uid'],
                                                                                                  order['product'],
                                                                                                  order['quantity'],
                                                                                                  user,
                                                                                                  order['status'],
                                                                                                  user_info['vip_user'],
                                                                                                  0,
                                                                                                  0,
                                                                                                  user_info['address']))
    conn.commit()


async def pull_db_orders_history(user):
    data = cursor.execute("SELECT uid, product, quantity, returned_qty, cancelled_qty, status from "
                          "orders where user = '%s' " % user)
    conn.commit()
    return data


async def pull_db_order_status(request):
    data = cursor.execute("SELECT uid, product, quantity, returned_qty, cancelled_qty, status from "
                          "orders where uid = '%s' " %
                          request.query['ord']).fetchall()
    conn.commit()
    return data


async def update_db_return_orders(request):
    cursor.execute('''UPDATE orders SET quantity = CASE WHEN quantity >= %s THEN quantity - %s ELSE 0 END 
        where uid = '%s' and product = '%s' ''' %
                   (request.query['quantity'],
                    request.query['quantity'],
                    request.query['order'],
                    request.query['product'])).fetchone()
    cursor.execute('''UPDATE orders SET status = CASE WHEN quantity = 0 THEN 'Returned' ELSE 'Updated' END 
        where uid = '%s' and product = '%s' ''' %
                   (request.query['order'],
                    request.query['product'])).fetchone()
    cursor.execute('''UPDATE orders SET returned_qty = returned_qty + %s where uid = '%s' and product = '%s' ''' %
                   (request.query['quantity'],
                    request.query['order'],
                    request.query['product'])).fetchone()

    data = cursor.execute('''SELECT uid, product, quantity, returned_qty, user, status, user_type from orders 
        where uid = '%s' and product = '%s' ''' % (request.query['order'], request.query['product'])).fetchone()
    conn.commit()
    return data


async def update_db_cancel_orders(request):
    cursor.execute("UPDATE orders  SET cancelled_qty= cancelled_qty + quantity, quantity = 0, "
                   "status='Cancelled' where uid = '%s' and product = '%s' " % (request.query['order'],
                                                                                request.query['product'])).fetchone()
    data = cursor.execute("SELECT uid, product, quantity, user, status, user_type, returned_qty, cancelled_qty "
                          "from orders where uid = '%s' and product = '%s' " % (request.query['order'],
                                                                                request.query['product'])).fetchone()
    conn.commit()
    return data


async def update_db_order_quantity(request):
    data = cursor.execute("SELECT uid, product, quantity, user, status, user_type, returned_qty "
                          "from orders where uid = '%s' and product = '%s' " % (request.query['order'],
                                                                                request.query['product'])).fetchone()
    cursor.execute("UPDATE orders  SET quantity = %s, status= 'Updated' where uid = '%s' and product = '%s' " % (
        request.query['quantity'],
        request.query['order'],
        request.query['product'])).fetchone()
    conn.commit()
    return data


async def insert_db_new_users(request):
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (user text, email text, address text, vip_user text)''')
    cursor.execute("INSERT INTO users VALUES ('%s','%s', '%s', '%s')" % (request.query['user'],
                                                                         request.query['email'],
                                                                         request.query['address'],
                                                                         request.query['checkbox']))
    conn.commit()


async def select_db_notify_products_management_team():
    status1 = 'Cancelled'
    status2 = 'Updated'
    data = cursor.execute("SELECT uid, user, product, quantity, status, user_type, destination from orders where "
                          "status = '%s' or status = '%s' " % (status1, status2))
    conn.commit()
    return data


async def select_db_notify_returns_management_team():
    qty = 0
    data = cursor.execute(
        "SELECT uid, user, product, returned_qty, status, user_type, destination from orders where returned_qty > "
        "'%s' " % qty)
    conn.commit()
    return data


async def select_db_notify_refunds_team():
    status1 = 'Returned'
    status2 = 'Updated'
    status3 = 'Cancelled'
    data = cursor.execute("SELECT uid, user, product, returned_qty, status, user_type, destination from orders where "
                          "status = '%s' or status = '%s' or status = '%s'" % (status1, status2, status3))
    conn.commit()
    return data


async def select_db_notify_delivery_team():
    status1 = 'Placed'
    status2 = 'Updated'
    status3 = 'Returned'
    status4 = 'Cancelled'
    data = cursor.execute(
        "SELECT uid, user, product, quantity, returned_qty, cancelled_qty, status, user_type, destination from orders "
        "where status = '%s' or status = '%s' or status = '%s' or status = '%s' " % (status1, status2, status3,
                                                                                     status4))
    conn.commit()
    return data


async def select_db_notify_emergency_team():
    quantity = 1000
    returned_qty = 1000
    cancelled_qty = 1000
    data = cursor.execute(
        "SELECT uid, user, product, quantity, returned_qty, cancelled_qty, status, user_type, destination from orders "
        "where quantity > '%s' or returned_qty > '%s' or cancelled_qty > '%s'" % (quantity, returned_qty,
                                                                                  cancelled_qty))
    conn.commit()
    return data


async def select_db_notify_large_order_team():
    quantity = 100
    returned_qty = 100
    cancelled_qty = 100
    data = cursor.execute(
        "SELECT uid, user, product, quantity, returned_qty, cancelled_qty, status, user_type, destination from orders "
        "where quantity > '%s' or returned_qty > '%s' or cancelled_qty > '%s'" % (
            quantity, returned_qty, cancelled_qty))
    conn.commit()
    return data


async def select_db_notify_sales_team():
    data = cursor.execute("SELECT uid, user, product, quantity, returned_qty, cancelled_qty, status, user_type, "
                          "destination from orders")
    conn.commit()
    return data


async def select_db_notify_vip_assistance_team():
    vip_user = 'Yes'
    data = cursor.execute(
        "SELECT uid, user, product, quantity, returned_qty, cancelled_qty, status, user_type, destination "
        "from orders where user_type = '%s' " % vip_user)
    conn.commit()
    return data
