# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module which contains afk-related commands """

from asyncio import sleep
from random import choice, randint

from telethon.events import StopPropagation

from userbot import AFKREASON, BOTLOG, BOTLOG_CHATID, CMD_HELP, PM_AUTO_BAN
from userbot.events import register

# ========================= CONSTANTS ============================
AFKSTR = [
    "Aku sedang sibuk sekarang. Tolong bicara di dalam tas dan ketika aku kembali kamu bisa memberikanku tas itu!",
    "Aku sedang pergi sekarang. Jika kamu butuh sesuatu, tinggalkan pesan setelah bunyi bip:\n`beeeeeeeeeeeeeeeeeeeeeeeeeeeeeeep`!",
    "Kamu merindukanku, lain kali bidik lebih baik.",
    "Aku akan kembali dalam beberapa menit dan jika tidak ...,\nmenunggu lebih lama.",
    "Saya tidak di sini sekarang, jadi saya mungkin di tempat lain.",
    "Mawar itu merah,\nViolet itu biru,\nTinggalkan aku pesan,\nDan aku akan menghubungi kamu kembali.",
    "Terkadang hal terbaik dalam hidup layak untuk ditunggu…\nAku akan segera kembali.",
    "Aku akan segera kembali,\ntapi jika aku tidak segera kembali,\nAku akan kembali nanti.",
    "Jika kamu belum mengetahuinya,\nAku tidak di sini.",
    "Halo, selamat datang di pesan tandang saya, bagaimana saya bisa mengabaikan Anda hari ini?",
    "Saya berada di 7 lautan dan 7 negara,\n7 perairan dan 7 benua,\n7 gunung dan 7 bukit,\n7 dataran dan 7 gundukan,\n7 kolam dan 7 danau,\n7 mata air dan 7 padang rumput,\n7 kota dan 7 lingkungan,\n7 blok dan 7 rumah ... \n\nDi mana bahkan pesan Anda tidak bisa sampai ke saya! ",
    "Saya sedang tidak menggunakan keyboard saat ini, tetapi jika Anda akan berteriak cukup keras di layar, saya mungkin akan mendengar Anda.",
    "Saya pergi ke sana\n ---->",
    "Aku pergi ke sini\n <----",
    "Silakan tinggalkan pesan dan buat saya merasa lebih penting daripada sebelumnya.",
    "Saya tidak di sini jadi berhentilah menulis kepada saya,\nAnda juga tidak akan menemukan diri Anda dengan layar yang penuh dengan pesan Anda sendiri.",
    "Jika aku ada di sini,\nAku akan memberitahumu di mana aku berada.\N\nTapi aku tidak,\njadi tanya aku kapan aku kembali ...",
    "Aku pergi!\nAku tidak tahu kapan aku akan kembali!\nSemoga beberapa menit dari sekarang!",
    "Aku sedang tidak ada saat ini jadi tolong tinggalkan nama, nomor, dan alamatmu dan aku akan menguntitmu nanti.",
    "Maaf, saya tidak di sini sekarang.\nJangan ragu untuk berbicara dengan userbot saya selama Anda suka.\nSaya akan menghubungi Anda lagi nanti.",
    "Saya yakin Anda mengharapkan pesan tandang!",
    "Hidup ini sangat singkat, begitu banyak hal yang harus dilakukan ...\nSaya akan melakukan salah satunya ..",
    "Aku tidak di sini sekarang ...\ntapi jika aku ...\n\nbukankah itu keren?",
]
# =================================================================


@register(incoming=True, disable_edited=True)
async def mention_afk(mention):
    """ This function takes care of notifying the people who mention you that you are AFK."""
    global COUNT_MSG
    global USERS
    global ISAFK
    if mention.message.mentioned and ISAFK:
        is_bot = False
        if (sender := await mention.get_sender()) :
            is_bot = sender.bot
        if not is_bot and mention.sender_id not in USERS:
            if AFKREASON:
                await mention.reply("I'm AFK right now." f"\nBecause `{AFKREASON}`")
            else:
                await mention.reply(str(choice(AFKSTR)))
            USERS.update({mention.sender_id: 1})
        else:
            if not is_bot and sender:
                if USERS[mention.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        await mention.reply(
                            f"I'm still AFK.\
                                \nReason: `{AFKREASON}`"
                        )
                    else:
                        await mention.reply(str(choice(AFKSTR)))
                USERS[mention.sender_id] = USERS[mention.sender_id] + 1
        COUNT_MSG = COUNT_MSG + 1


@register(incoming=True, disable_errors=True)
async def afk_on_pm(sender):
    """ Function which informs people that you are AFK in PM """
    global ISAFK
    global USERS
    global COUNT_MSG
    if (
        sender.is_private
        and sender.sender_id != 777000
        and not (await sender.get_sender()).bot
    ):
        if PM_AUTO_BAN:
            try:
                from userbot.modules.sql_helper.pm_permit_sql import is_approved

                apprv = is_approved(sender.sender_id)
            except AttributeError:
                apprv = True
        else:
            apprv = True
        if apprv and ISAFK:
            if sender.sender_id not in USERS:
                if AFKREASON:
                    await sender.reply(
                        f"Saya AFK sekarang.\
                    \nKarena: `{AFKREASON}`"
                    )
                else:
                    await sender.reply(str(choice(AFKSTR)))
                USERS.update({sender.sender_id: 1})
            else:
                if USERS[sender.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        await sender.reply(
                            f"Saya masih AFK.\
                        \nKarena: `{AFKREASON}`"
                        )
                    else:
                        await sender.reply(str(choice(AFKSTR)))
                USERS[sender.sender_id] = USERS[sender.sender_id] + 1
            COUNT_MSG = COUNT_MSG + 1


@register(outgoing=True, pattern=r"^\.afk(?: |$)(.*)", disable_errors=True)
async def set_afk(afk_e):
    """ For .afk command, allows you to inform people that you are afk when they message you """
    afk_e.text
    string = afk_e.pattern_match.group(1)
    global ISAFK
    global AFKREASON
    if string:
        AFKREASON = string
        await afk_e.edit("Pergi AFK!" f"\nKarena: `{string}`")
    else:
        await afk_e.edit("Pergi AFK!")
    if BOTLOG:
        await afk_e.client.send_message(BOTLOG_CHATID, "#AFK\nYou went AFK!")
    ISAFK = True
    raise StopPropagation


@register(outgoing=True)
async def type_afk_is_not_true(notafk):
    """ This sets your status as not afk automatically when you write something while being afk """
    global ISAFK
    global COUNT_MSG
    global USERS
    global AFKREASON
    if ISAFK:
        ISAFK = False
        msg = await notafk.respond("I'm no longer AFK.")
        await sleep(2)
        await msg.delete()
        if BOTLOG:
            await notafk.client.send_message(
                BOTLOG_CHATID,
                "Anda telah menerima "
                + str(COUNT_MSG)
                + " pesan dari "
                + str(len(USERS))
                + " obrolan saat Anda pergi",
            )
            for i in USERS:
                name = await notafk.client.get_entity(i)
                name0 = str(name.first_name)
                await notafk.client.send_message(
                    BOTLOG_CHATID,
                    "["
                    + name0
                    + "](tg://user?id="
                    + str(i)
                    + ")"
                    + " sent you "
                    + "`"
                    + str(USERS[i])
                    + " messages`",
                )
        COUNT_MSG = 0
        USERS = {}
        AFKREASON = None


CMD_HELP.update(
    {
        "afk": ">`.afk [Alasan]`"
        "\nUsage: Menetapkan Anda sebagai afk. \ NBalas kepada siapa saja yang memberi tag / PM "
        "Anda memberi tahu mereka bahwa Anda AFK(alasan)."
        "\n\nMematikan AFK saat Anda mengetik kembali apa pun, di mana pun."
    }
)
