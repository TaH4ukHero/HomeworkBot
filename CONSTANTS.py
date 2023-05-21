from telegram.ext import ConversationHandler

CHECK_HW, CREATE_HW, SELECTION_ACTION, SUCCESS_DT, SAVE_TASK, SUCCESS_SAVE, CHOOSE_ITEM, \
    CHECK_SPECIFIC, SHOWING_TEXT = map(chr, range(9))
END = ConversationHandler.END
