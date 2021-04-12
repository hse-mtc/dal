from aiohttp import web

from proto.uniforms import Uniform

routes = web.RouteTableDef()


@routes.post("/uniforms/")
async def post_uniforms(request: web.Request) -> web.Response:
    body = await request.json()
    uniform = Uniform.from_raw(body)
    # TODO(TmLev): fetch milgroup commanders from `uniform.milfaculty`
    #              and send them uniform update. Remove debug print.
    print(uniform)
    return web.Response(text="Hello!")
