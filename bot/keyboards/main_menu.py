from telegram import ReplyKeyboardMarkup

ASSETS_KB = ReplyKeyboardMarkup([["Yes"], ["No"]], one_time_keyboard=True, resize_keyboard=True)
FAMILY_KB = ReplyKeyboardMarkup(
    [["Не женат(а)"], ["Женат(а)"], ["Разведён(а)"], ["Вдовец/Вдова"]],
    one_time_keyboard=True,
    resize_keyboard=True,
)