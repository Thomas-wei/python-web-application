import asyncio
import orm
from models import User, Blog, Comment

loop = asyncio.get_event_loop()
async def test():
    await orm.create_pool(loop, user='root', password='root*123', database='awesome')

    u = User(name='Test', email='test6@example.com', passwd='1234567890', image='about:blank')
    print(u)

    await u.save()


loop.run_until_complete(test())