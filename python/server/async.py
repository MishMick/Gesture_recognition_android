from aiohttp import web
import os
import ml
import vidproc
import time
from sklearn.preprocessing import StandardScaler

data, target = ml.load_data()
scaler = StandardScaler()
scaler.fit(data)
data = scaler.transform(data)
models = ml.make_models(data, target)


class Handler:

    async def handle(self, request):
        print("hello rec")
        return web.Response(text="Hello4")

    async def jsonhandle(self, request):
        print("json req rec")
        folder = "json"
        if not os.path.exists(folder):
                os.makedirs(folder)
        data = await request.text()
        #for key in data.keys():
        #    #print(data)
        #    #print()
        #    #print(data[key])
        #    f = data[key]
        #    #print(f)

        path = folder + "/keypoints.json"
        with open(path, 'w') as w:
            w.write(data)

        return web.Response(text=ml.query_models(models, scaler, folder))

    #async def classifyhandle(self, request):
    #    folder = "classify"
    #    if not os.path.exists(folder):
    #            os.makedirs(folder)
    #    data = await request.post()
    #    for key in data.keys():
    #        f = data[key].file.read()
    #        #print(f)

    #        name = str(int(time.time()))
    #        fn = name + ".mp4"
    #        path = folder + fn
    #        with open(path, 'wb') as w:
    #            w.write(f)
    #    
    #        vidproc.extract_df(folder + "/", fn)

    #        return web.Response(text=ml.query_models(models, folder + "/" + name))
    #    return web.Response(text="errored")

app = web.Application()
handler = Handler()
app.router.add_get('/', handler.handle)
app.router.add_post('/json', handler.jsonhandle)
#app.router.add_post('/classify', handler.classifyhandle)
#app.add_routes([web.get('/', handle), web.post('/json', jsonhandle), web.post('/json', vidhandle)])

if __name__ == '__main__':
    web.run_app(app)