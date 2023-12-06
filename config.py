import re, os, time

id_pattern = re.compile(r'^.\d+$') 

class Config(object):
    # pyro client config
    API_ID    = os.environ.get("API_ID", "27060846")  # ⚠️ Required
    API_HASH  = os.environ.get("API_HASH", "8f39072a61dbb296f38e4ff2b6cbe478") # ⚠️ Required
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "6712788582:AAHKWFe3pcKMbnDJXiaLVa6IjXG2lddJin0") # ⚠️ Required
   
    # database config
    DB_URL  = os.environ.get("DB_URL","mongodb+srv://TEST:TEST@cluster0.ehigmtx.mongodb.net/?retryWrites=true&w=majority")  # ⚠️ Required
    DB_NAME  = os.environ.get("DB_NAME","AutoAcceptBot")
 
    # other configs
    BOT_UPTIME  = time.time()
    START_PIC   = os.environ.get("START_PIC", "")
    ADMIN       = int(os.environ.get('ADMIN', '6065594762')) # ⚠️ Required
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001971176803")) # ⚠️ Required
    WELCOME_MSG = os.environ.get("WELCOME_MSG", "Hey {user},\nYour Request Approved ✅,\n\nWelcome to **{title}**")
    LEAVE_MSG = os.environ.get("LEAVE_MSG", "By {user},\nSee You Again 👋\n\nFrom **{title}**")
    
    # wes response configuration     
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))
    PORT = int(os.environ.get("PORT", "8080"))
