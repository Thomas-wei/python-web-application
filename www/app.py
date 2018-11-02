import logging
logging.basicConfig(level=logging.INFO)

import asyncio,time
from datetime import datetime
from aiohttp import web

def index(request):
    # 必须加content_type，否则就会自动变成下载
    return web.Response(body=b'<h1>Awesome1</h1>', content_type='text/html', charset='utf-8')

# coroutine（协程）是一种函数类型，与Generator类似，不同的是yield写法，Generator：yield XXX;coroutine: xxx = (yield);
# coroutine（协程）函数需要调用next(),然后通过send(xxx)传入值
@asyncio.coroutine
async def init(): # 协程 不能直接运行，要放到loop中运行
    # web.Application的loop参数弃用了
    app = web.Application(logger=logging.getLogger('aiohttp.web'))
    app.router.add_route('GET', '/', index)
    app_runner = web.AppRunner(app)
    await app_runner.setup()
    srv = await loop.create_server(app_runner.server, '127.0.0.1', 8091)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

# 获取当前线程的默认缺省loop
loop = asyncio.get_event_loop()
# 协程函数运行会返回一个协程对象，并不是直接开始运行 init()执行的不是内部代码，而是返回的一个协程函数，要想执行需要交给loop执行
# 把定义的协程交给loop执行，3.6版本需要把loop也传进去（init(loop)）
# run_until_complete的参数应该是个future，这里传入一个协程也能执行是因为对参数做了隐式转换asyncio.ensure_future(do_some_work(3)
# futu = asyncio.ensure_future(init())
# 协程执行完增加回调
# futu.add_done_callback(done_callback)
loop.run_until_complete(init())
# 知道loop.stop()运行之前，协程不会结束，这样也就相当于一直处于监听状态
loop.run_forever()