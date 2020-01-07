import uuid
from aiohttp import web
import list_products
import urllib.parse


from urls import conn, update_db_user_profile, insert_db_new_orders, pull_db_orders_history, pull_db_order_status,\
    update_db_cancel_orders, update_db_return_orders, update_db_order_quantity, insert_db_new_users,\
    select_db_notify_delivery_team, select_db_notify_emergency_team, \
    select_db_notify_large_order_team, select_db_notify_products_management_team, select_db_notify_refunds_team, \
    select_db_notify_returns_management_team, select_db_notify_sales_team, select_db_notify_vip_assistance_team

from views import get_order_history, get_view_products, get_make_order, get_order_status, get_return_order, \
    get_cancel_order, get_employee_login, get_user_login, get_user_signup, get_user_profile, get_update_order_quantity, \
    get_error_returns, get_delivery_team, get_emergency_team, get_large_order_team, get_products_mgmt_team, \
    get_refunds_team, get_returns_team, get_sales_team, get_vip_assistance_team, get_employee_login


###############################################################################
# NOTE: all "notify_*"" functions in this section represent important business actions.
#       It would be too much for the assessment to go with an actual implementation,
#       but please assume that the logic of these functions is of a critical importance.
#       Nonetheless, feel free to change "notify_*"" functions as you
#       like, but make sure that the business action is preserved.

async def request_data_dict(request):
    data = await request.text()
    try:
        dict([i.split("=") for i in data.split("&")])
    except:
        data
    else:
        data = dict([i.split("=") for i in data.split("&")])
    return data


async def view_products(request):
    data = await request.text()
    try:
        dict([i.split("=") for i in data.split("&")])
    except:
        data
    else:
        data = dict([i.split("=") for i in data.split("&")])
    products = list_products.list_products()
    if 'user' in data:
        user = data['user']
    else:
        user = request.cookies['user']
    if 'vip_user' in data:
        vip_user = data['vip_user']
    else:
        vip_user = 'off'
    await update_your_profile(user, data)
    return await get_view_products(user, vip_user, products, request)


async def update_your_profile(user, data):
    if 'address' in data and 'email' in data:
        data['email'] = urllib.parse.unquote(data['email'])
        data['address'] = urllib.parse.unquote_plus(data['address'])
        await update_db_user_profile(user, data)


async def collect_order_quantity(request):
    data = await request.text()
    dict_val = {}
    order = {}
    for i in data.split("&"):
        dict_val.update(dict([i.split("=")]))
        if all(k in dict_val for k in ("product", "quantity")):
            if dict_val.get('product') != '' and dict_val.get('quantity') != '':
                dict_val['quantity'] = int(dict_val['quantity'])
                if 'order_uid' in locals():
                    order = {'uid': order_uid, 'product': dict_val['product'], 'quantity': dict_val['quantity'],
                             'status': 'Placed'}
                else:
                    order = {'uid': uuid.uuid4().hex, 'product': dict_val['product'], 'quantity': dict_val['quantity'],
                             'status': 'Placed'}
                order_uid = order['uid']
                await insert_db_new_orders(order, request.cookies['user'])
                dict_val.clear()
    return order


async def make_order(request):
    user = request.cookies['user']
    order = await collect_order_quantity(request)
    return await get_make_order(user, order, request)


async def orders_history(request):

    data = await request_data_dict(request)
    if 'user' in data:
        user = data['user']
    else:
        user = request.cookies['user']
    if 'vip_user' in data:
        vip_user = data['vip_user']
    elif 'vip_user' in request.cookies:
        vip_user = request.cookies['vip_user']
    else:
        vip_user = ''

    data = await pull_db_orders_history(user)
    return await get_order_history(user, data)


async def order_status(request):
    user = request.cookies['user']
    if 'returned_quantity' in request.cookies:
        returned_quantity = request.cookies['returned_quantity']
    else:
        returned_quantity = 0
    data = await pull_db_order_status(request)
    return await get_order_status(user, data)


async def return_order(request):
    cursor = conn.cursor()
    check_data = cursor.execute('''SELECT quantity from orders where uid = '%s' and product= '%s' '''
                                % (request.query['order'], request.query['product'])).fetchone()
    check_data = dict(zip(('order', 'product'), check_data))
    if check_data['order'] == 0:
        try:
            raise ValueError
        except ValueError:
            return await get_error_returns(request)
    else:
        data = await update_db_return_orders(request)
        order = dict(zip(('uid', 'product', 'quantity', 'returned_qty', 'user', 'status'), data))
        user = request.cookies['user']
        return await get_return_order(order, request)


async def cancel_order(request):
    data = await update_db_cancel_orders(request)
    order = dict(zip(('uid', 'product', 'quantity', 'user', 'status', 'user_type', 'returned_qty', 'cancelled_qty'), data))
    return await get_cancel_order(order)


async def update_order_quantity(request):
    data = await update_db_order_quantity(request)
    order = dict(zip(('uid', 'product', 'quantity', 'user', 'status', 'returned_qty'), data))
    user = request.cookies['user']
    return await get_update_order_quantity(order, request)


async def update_profile(request):
    user = request.cookies['user']
    vip_user = request.cookies['vip_user']
    return await get_user_profile(user, request)


async def notify_products_management_team(request):
    user = request.query['employee']
    data = await select_db_notify_products_management_team()
    return await get_products_mgmt_team(user, data)


async def notify_returns_management_team(request):
    user = request.query['employee']
    data = await select_db_notify_returns_management_team()
    return await get_returns_team(user, data)


async def notify_refunds_team(request):
    user = request.query['employee']
    data = await select_db_notify_refunds_team()
    return await get_refunds_team(user, data)


async def notify_delivery_team(request):
    user = request.query['employee']
    data = await select_db_notify_delivery_team()
    return await get_delivery_team(user, data)


async def notify_emergency_team(request):
    user = request.query['employee']
    data = await select_db_notify_emergency_team()
    return await get_emergency_team(user, data)


async def notify_large_order_team(request):
    user = request.query['employee']
    data = await select_db_notify_large_order_team()
    return await get_large_order_team(user, data)


async def notify_sales_team(request):
    user = request.query['employee']
    data = await select_db_notify_sales_team()
    return await get_sales_team(user, data)


async def notify_vip_assistance_team(request):
    user = request.query['employee']
    data = await select_db_notify_vip_assistance_team()
    return await get_vip_assistance_team(user, data)


async def signup(request):
    return await get_user_signup(request)


async def login(request):
    data = request.text()
    if request.query['user'].find('%s') != -1 and request.query['checkbox'].find('%s') != -1:
        pass
    else:
        await insert_db_new_users(request)

    return await get_user_login(request)


async def employee_login(request):
    return await get_employee_login(request)


async def main(request):
    try:
        return await eval(request.query['action'], globals(), locals())(request)
    except:
        return await signup(request)


app = web.Application()
app.add_routes([web.view('/', main)])

if __name__ == '__main__':
    web.run_app(app)
