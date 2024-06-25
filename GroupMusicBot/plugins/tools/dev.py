import os
import re
import sys
import traceback
import subprocess

from time import time
from io import StringIO
from inspect import getfullargspec

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from GroupMusicBot import app
from GroupMusicBot.misc import SUDOERS


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})


@app.on_edited_message(
    filters.command("ev")
    & SUDOERS
    & ~filters.forwarded
    & ~filters.via_bot
)
@app.on_message(
    filters.command("ev")
    & SUDOERS
    & ~filters.forwarded
    & ~filters.via_bot
)
async def executor(client: app, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>What you wanna execute..</b>")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.delete()
    t1 = time()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = "\n"
    if exc:
        evaluation += exc
    elif stderr:
        evaluation += stderr
    elif stdout:
        evaluation += stdout
    else:
        evaluation += "Success"
    final_output = f"<b>Result :</b>\n<pre language='python'>{evaluation}</pre>"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation))
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳",
                        callback_data=f"runtime {t2-t1} Seconds",
                    )
                ]
            ]
        )
        await message.reply_document(
            document=filename,
            caption=f"<b>Eval :</b>\n<code>{cmd[0:980]}</code>\n\n<b>Result :</b>\nAttached Document",
            quote=False,
            reply_markup=keyboard,
        )
        await message.delete()
        os.remove(filename)
    else:
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳",
                        callback_data=f"runtime {round(t2-t1, 3)} Seconds",
                    ),
                    InlineKeyboardButton(
                        text="🗑",
                        callback_data=f"forceclose abc|{message.from_user.id}",
                    ),
                ]
            ]
        )
        await edit_or_reply(message, text=final_output, reply_markup=keyboard)


@app.on_callback_query(filters.regex(r"runtime"))
async def runtime_func_cq(_, cq):
    runtime = cq.data.split(None, 1)[1]
    await cq.answer(runtime, show_alert=True)


@app.on_callback_query(filters.regex("forceclose"))
async def forceclose_command(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer(
                "» It'll be better if you stay in your limits.", show_alert=True
            )
        except(ValueError, AttributeError):
            return
    await CallbackQuery.message.delete()
    try:
        await CallbackQuery.answer()
    except(ValueError, AttributeError):
        return


@app.on_message(
    filters.command("bash") 
    & SUDOERS
    & ~filters.forwarded 
    & ~filters.via_bot
    & ~filters.bot
    & ~filters.private
)
@app.on_edited_message(
    filters.command("bash") 
    & SUDOERS
    & ~filters.forwarded 
    & ~filters.via_bot
    & ~filters.bot
    & ~filters.private
)
async def shellrunner(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("<b>Example :</b>\n/bash git pull")

    text = message.text.split(None, 1)[1]
    output_message = await message.reply("Executing...")

    try:
        if "\n" in text:
            code = text.split("\n")
            output = ""
            for x in code:
                shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
                process = subprocess.Popen(shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = process.communicate()
                output += f"<b>{x}</b>\n"
                output += out.decode("utf-8") if out else ""
                output += err.decode("utf-8") if err else ""
                output += "\n"
        else:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", text)
            shell = [cmd.replace('"', "") for cmd in shell]
            process = subprocess.Popen(shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            output = out.decode("utf-8") if out else ""
            output += err.decode("utf-8") if err else ""

        if not output.strip():
            output = "<code>None</code>"
        else:
            if len(output) > 4096:
                with open("output.txt", "w+") as file:
                    file.write(output)
                await client.send_document(
                    message.chat.id,
                    "output.txt",
                    reply_to_message_id=message.message_id,
                    caption="<code>Output</code>",
                )
                os.remove("output.txt")
                await output_message.delete()
                return
            else:
                output = f"<b>OUTPUT :</b>\n<pre>{output}</pre>"

        await output_message.edit(text=output)
    except Exception as err:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        errors = traceback.format_exception(exc_type, exc_value, exc_traceback)
        await output_message.edit(text=f"<b>ERROR :</b>\n<pre>{''.join(errors)}</pre>")

    await message.stop_propagation()
