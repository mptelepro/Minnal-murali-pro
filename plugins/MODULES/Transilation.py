import os
# from plugins.helpers.vars import ADMINS, DATABASE, DEFAULT_LANGUAGE
from plugins.helpers.admin import Katabase
from io import BytesIO
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from googletrans import Translator, constants

from googletrans import Translator
from pyrogram import Client, filters, enums
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from plugins.helpers.database import find , insert
from plugins.helpers.list import list
from Script import script
from info import SP


ADMINS = int(os.environ.get("ADMINS"))
DATABASE = os.environ.get("DATABASE_URL")
DEFAULT_LANGUAGE = os.environ.get("DEFAULT_LANGUAGE", "ml")

SETTINGS_TEXT = "Select your language for translating. Current default language is `{}`."

BUTTONS = [InlineKeyboardButton('⚙ Join Updates Channel ⚙', url='https://telegram.me/FayasNoushad')]

db = Katabase(DATABASE)

LANGUAGES = constants.LANGUAGES

LANGUAGES_TEXT = "**Languages**\n"
for language in LANGUAGES:
    LANGUAGES_TEXT += f"\n`{LANGUAGES[language].capitalize()}` -> `{language}`"






@Client.on_message(filters.group & filters.command(["ml"]))
async def command_filter(bot, update):
    if update.reply_to_message:
        if update.reply_to_message.text:
            text = update.reply_to_message.text
        elif update.reply_to_message.caption:
            text = update.reply_to_message.caption
        else:
            return 
    else:
        if update.text:
            text = update.text.split(" ", 1)[1]
        elif update.caption:
            text = update.caption.split(" ", 1)[1]
        else:
            return
    await translate(bot, update, text)


@Client.on_message(filters.command(["mll"]) & (filters.text | filters.caption))
async def get_message(_, message):
    text = message.text if message.text else message.caption
    await translate(message, text)


async def translate(update, text):
    await update.reply_chat_action(enums.ChatAction.TYPING)
    message = await update.reply_text("`Translating...`")
    try:
        language = await db.get_lang(update.from_user.id)
    except:
        language = DEFAULT_LANGUAGE
    translator = Translator()
    try:
        translate = translator.translate(text, dest=language)
        translate_text = f"**Translated to {language}**"
        translate_text += f"\n\n`{translate.text}`"
        if len(translate_text) < 4096:
            await message.edit_text(
                text=translate_text,
                disable_web_page_preview=True
            )
        else:
            with BytesIO(str.encode(str(translate_text))) as translate_file:
                translate_file.name = language + ".txt"
                await update.reply_document(
                    document=translate_file
                )
                await message.delete()
                try:
                    os.remove(translate_file)
                except:
                    pass
    except Exception as error:
        print(error)
        await message.edit_text("Something wrong. Contact @TheFayas.")
        return



@Client.on_message(filters.group & filters.command(["tr"]))
async def left(client,message):
	if (message.reply_to_message):
		try:
			lgcd = message.text.split("/tr")
			lg_cd = lgcd[1].lower().replace(" ", "")
			tr_text = message.reply_to_message.text
			translator = Translator()
			translation = translator.translate(tr_text,dest = lg_cd)
			try:
				for i in list:
					if list[i]==translation.src:
						fromt = i
					if list[i] == translation.dest:
						to = i 
				await message.reply_text(f"Translated from **{fromt.capitalize()}** To **{to.capitalize()}**\n\n```{translation.text}```")
			except:
			   	await message.reply_text(f"Translated from **{translation.src}** To **{translation.dest}**\n\n```{translation.text}```")      			
							
		

		except :
			print("error")
	else:
	                 m = await message.reply_photo(
                         photo=(SP),
                         caption=f"translated from {fromt.capitalize()} to {to.capitalize()}\n\n```{translation.text}```",
                         reply_markup=InlineKeyboardMarkup(
                                   [[
                                     InlineKeyboardButton('Close', callback_data="close_data"),
                                                                         
                                   ]]
                         ),
                         parse_mode=enums.ParseMode.HTML
) 

                     

#list py   


list = {
"afrikaans":"af",
"albanian":"sq",
"amharic":"am",
"arabic":"ar",
"armenian":"hy",
"azerbaijani":"az",
"basque":"eu",
"belarusian":"be",
"bengali":"bn",
"bosnian":"bs",
"bulgarian":"bg",
"catalan":"ca",
"cebuano":"ceb",
"chinese": "zh",
"corsican":"co",
"croatian":"hr",
"czech":"cs",
"danish":"da",
"dutch":"nl",
"english":"en",
"esperanto":"eo",
"estonian":"et",
"finnish":"fi",
"french":"fr",
"frisian":"fy",
"galician":"gl",
"georgian":"ka",
"german":"de",
"greek":"el",
"gujarati":"gu",
"haitian creole":"ht",
"hausa":"ha",
"hawaiian":"haw",
"hebrew":"he",
"hindi":"hi",
"hmong":"hmn",
"hungarian":"hu",
"icelandic":"is",
"igbo":"ig",
"indonesian":"id",
"irish":"ga",
"italian":"it",
"japanese":"ja",
"javanese":"jv",
"kannada":"kn",
"kazakh":"kk",
"khmer":"km",
"kinyarwanda":"rw",
"korean":"ko",
"kurdish":"ku",
"kyrgyz":"ky",
"lao":"lo",
"latin":"la",
"latvian":"lv",
"lithuanian":"lt",
"luxembourgish":"lb",
"macedonian":"mk",
"malagasy":"mg",
"malay":"ms",
"malayalam":"ml",
"maltese":"mt",
"maori":"mi",
"marathi":"mr",
"mongolian":"mn",
"myanmar":"my",
"nepali":"ne",
"norwegian":"no",
"nyanja":"ny",
"odia":"or",
"pashto":"ps",
"persian":"fa",
"polish":"pl",
"portuguese":"pt",
"punjabi":"pa",
"romanian":"ro",
"russian":"ru",
"samoan":"sm",
"scots gaelic":"gd",
"serbian":"sr",
"sesotho":"st",
"shona":"sn",
"sindhi":"sd",
"sinhala":"si",
"slovak":"sk",
"slovenian":"sl",
"somali":"so",
"spanish":"es",
"sundanese":"su",
"swahili":"sw",
"swedish":"sv",
"tagalog":"tl",
"tajik":"tg",
"tamil":"ta",
"tatar":"tt",
"telugu":"te",
"thai":"th",
"turkish":"tr",
"turkmen":"tk",
"ukrainian":"uk",
"urdu":"ur",
"uyghur":"ug",
"uzbek":"uz",
"vietnamese":"vi",
"welsh":"cy",
"xhosa":"xh",
"yiddish":"yi",
"yoruba":"yo",
"zulu":"zu"}
