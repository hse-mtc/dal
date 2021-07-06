import asyncio

from aiohttp import web

from aiogram.bot import Bot

import config

from api.auth import fetch_session
from api.student import fetch_milgroup_leader_phones

from proto.uniforms import Uniform

routes = web.RouteTableDef()


@routes.post("/uniforms/")
async def post_uniforms(request: web.Request) -> web.Response:
    body = await request.json()
    uniform = Uniform.from_raw(body)

    bot: Bot = request.app[config.BOT]
    phones = await fetch_milgroup_leader_phones(milfaculty=uniform.milfaculty)

    sessions = await asyncio.gather(*[
        fetch_session(params={"phone": phone})
        for phone in phones
    ])

    await asyncio.gather(*[
        bot.send_message(chat_id=session.chat_id, text=f"{uniform}")
        for session in sessions
    ])

    return web.Response(body={"detail": "Successful uniform notification."})
