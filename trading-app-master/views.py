import os
from aiohttp import web

cur_path = os.path.dirname(__file__)


async def get_order_history(user, data):
    with open(os.path.join(cur_path, "static/html/order_history.html"), "r") as f:
        page = f.read()
        html_products = "\n".join(["""
                    <tr>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                    </tr> 
                    """ % i for i in data])
        resp = web.Response(body=page % (user, html_products), headers={"Content-Type": "text/html"})
        resp.set_cookie('user', user)
        return resp


async def get_view_products(user, vip_user, products, request):
    with open(os.path.join(cur_path, "static/html/view_products.html"), "r") as f:
        page = f.read()
        html_products = "\n".join(["""
                <tr> 
                    <td>%(name)s <input type="hidden" name="product" value="%(name)s"></td>
                    <td>%(description)s</td>
                    <td>%(price)s</td>
                    <td>%(type)s</td>
                    <td><input type="number" name="quantity" min="1"></td>
                </tr>
                """ % i for i in products])
        data = await request.text()
        if data:
            data = dict([i.split("=") for i in data.split("&")])
        else:
            data = {}
        resp = web.Response(body=page % (user, html_products), headers={"Content-Type": "text/html"})
        resp.set_cookie('user', user)
        resp.set_cookie('vip_user', vip_user)
        return resp


async def get_make_order(user, order, request):
    with open(os.path.join(cur_path, "static/html/make_order.html"), "r") as f:
        page = f.read()
        resp = web.Response(body=page % (user, order['uid'], order['uid'], order['uid']),
                            headers={"Content-Type": "text/html"})
        resp.set_cookie('user', request.cookies['user'])
        return resp


async def get_order_status(user, data):
    with open(os.path.join(cur_path, "static/html/order_status.html"), "r") as f:
        page = f.read()
        html_products = "\n".join(["""
                <tr>
                    <td>%s</td>
                    <td> TBD </td>
                    <td>%s</td>
                    <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                    <td> TBD </td>
                    <td>%s</td>
                </tr>
                """ % i for i in data])
        return web.Response(body=page % (user, html_products), headers={"Content-Type": "text/html"})


async def get_return_order(order, request):
    with open(os.path.join(cur_path, "static/html/return_order.html"), "r") as f:
        page = f.read()
        resp = web.Response(body=page % (order['user'], order['uid'], request.query['quantity'], order['uid']),
                            headers={"Content-Type": "text/html"})
        resp.set_cookie('returned_quantity', request.query['quantity'])
        return resp


async def get_cancel_order(order):
    with open(os.path.join(cur_path, "static/html/cancel_order.html"), "r") as f:
        page = f.read()
        return web.Response(text=page % (order['user'], order['uid'], order['cancelled_qty'], order['uid']),
                            headers={"Content-Type": "text/html"})


async def get_employee_login(request):
    with open(os.path.join(cur_path, "static/html/employee_login.html"), "r") as f:
        page = f.read()
        data = await request.text()
        if data:
            data = dict([i.split("=") for i in data.split("&")])
        else:
            data = {}
        resp = web.Response(body=page, headers={"Content-Type": "text/html"})
        resp.set_cookie('employee', data.get('employee'))
        return resp


async def get_user_login(request):
    with open(os.path.join(cur_path, "static/html/user_login.html"), "r") as f:
        page = f.read()
        return web.Response(body=page, headers={"Content-Type": "text/html"})


async def get_user_signup(request):
    with open(os.path.join(cur_path, "static/html/user_signup.html"), "r") as f:
        page = f.read()
        if all(k in request.query for k in ("user", "email", "address", "checkbox")):
            return web.Response(body=page % (
                request.query['user'], request.query['email'], request.query['address'], request.query['checkbox']),
                                headers={"Content-Type": "text/html"})
        else:
            return web.Response(body=page, headers={"Content-Type": "text/html"})


async def get_user_profile(user, request):
    with open(os.path.join(cur_path, "static/html/user_profile_update.html"), "r") as f:
        page = f.read()
        return web.Response(body=page % (user, user), headers={"Content-Type": "text/html"})


async def get_update_order_quantity(order, request):
    with open(os.path.join(cur_path, "static/html/update_order_quantity.html"), "r") as f:
        page = f.read()
        return web.Response(text=page % (order['user'], order['uid'],
                                         request.query['quantity'],
                                         order['uid']), headers={"Content-Type": "text/html"})


async def get_error_returns(request):
    with open(os.path.join(cur_path, "static/html/error_return.html"), "r") as f:
        page = f.read()
        return web.Response(text=page, headers={"Content-Type": "text/html"})


async def get_products_mgmt_team(user, data):
    with open(os.path.join(cur_path, "static/html/notify_product_mgmt_team.html"), "r") as f:
        page = f.read()
        html_products = "\n".join(["""
                    <tr>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>VIP %s</td>
                    <td>%s</td>
                    </tr>
                    """ % i for i in data])

        return web.Response(body=page % (user, html_products), headers={"Content-Type": "text/html"})


async def get_returns_team(user, data):
    with open(os.path.join(cur_path, "static/html/notify_returns_team.html"), "r") as f:
        page = f.read()
        html_products = "\n".join(["""
                    <tr>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>VIP %s</td>
                    <td>%s</td>
                    </tr>

                    """ % i for i in data])

        return web.Response(body=page % (user, html_products), headers={"Content-Type": "text/html"})


async def get_refunds_team(user, data):
    with open(os.path.join(cur_path, "static/html/notify_returns_team.html"), "r") as f:
        page = f.read()
        html_products = "\n".join(["""
                    <tr>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>VIP %s</td>
                    <td>%s</td>
                    </tr>

                    """ % i for i in data])

        return web.Response(body=page % (user, html_products), headers={"Content-Type": "text/html"})


async def get_delivery_team(user, data):
    with open(os.path.join(cur_path, "static/html/notify_delivery_team.html"), "r") as f:
        page = f.read()
        html_products = "\n".join(["""
                     <tr>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                     <td>VIP %s</td>
                     <td>%s</td>
                     </tr>

                     """ % i for i in data])

        return web.Response(body=page % (user, html_products), headers={"Content-Type": "text/html"})


async def get_emergency_team(user, data):
    with open(os.path.join(cur_path, "static/html/notify_emergency_team.html"), "r") as f:
        page = f.read()
        html_products = "\n".join(["""
                      <tr>
                      <td>%s</td>
                      <td>%s</td>
                      <td>%s</td>
                      <td>%s</td>
                      <td>%s</td>
                      <td>%s</td>
                      <td>%s</td>
                      <td>VIP %s</td>
                      <td>%s</td>
                      </tr>

                      """ % i for i in data])

        return web.Response(body=page % (user, html_products), headers={"Content-Type": "text/html"})


async def get_large_order_team(user, data):
    with open(os.path.join(cur_path, "static/html/notify_large_orders_team.html"), "r") as f:
        page = f.read()
        html_products = "\n".join(["""
                     <tr>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                      <td>%s</td>
                     <td>VIP %s</td>
                     <td>%s</td>
                     </tr>

                     """ % i for i in data])

        return web.Response(body=page % (user, html_products), headers={"Content-Type": "text/html"})


async def get_sales_team(user, data):
    with open(os.path.join(cur_path, "static/html/notify_sales_team.html"), "r") as f:
        page = f.read()
        html_products = "\n".join(["""
                     <tr>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                     <td>VIP %s</td>
                     <td>%s</td>
                     </tr>

                     """ % i for i in data])

        return web.Response(body=page % (user, html_products), headers={"Content-Type": "text/html"})


async def get_vip_assistance_team(user, data):
    with open(os.path.join(cur_path, "static/html/notify_vip_assistance_team.html"), "r") as f:
        page = f.read()
        html_products = "\n".join(["""
                    <tr>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                     <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                     <td>%s</td>
                    </tr>

                    """ % i for i in data])

        return web.Response(body=page % (user, html_products), headers={"Content-Type": "text/html"})


async def get_employee_login(request):
    with open(os.path.join(cur_path, "static/html/employee_login.html"), "r") as f:
        page = f.read()
        data = await request.text()
        if data:
            data = dict([i.split("=") for i in data.split("&")])
        else:
            data = {}
        resp = web.Response(body=page, headers={"Content-Type": "text/html"})
        resp.set_cookie('employee', data.get('employee'))
        return resp




