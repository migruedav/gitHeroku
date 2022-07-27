
from binance.client import Client

#FastAPI
from fastapi import FastAPI
from fastapi import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI()

origins = [

    "http://localhost",
    "http://localhost:8080",
    "https://56d.835.myftpupload.com",
    "https://56d.835.myftpupload.com/:271",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"conecction":"Success"}

@app.get("/html/", response_class=HTMLResponse)
async def html():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
            <p>Momo TVAPEC</p>
        </body>
    </html>
"""

@app.get("/coin/{coin}")
async def crypto(
    coin:str = Path(
        ...,
        title="Coin",
        description="The Coin to get the power, Its Required")
    ):

    api_key    = 'glrxacPAoL82BwKAfWvsqEYmM4pWys6wXfBZOwWYXGKAnCW4nplV62SUDLqsC1b2'
    api_secret = '8bllLJnlvLogsbOAflT8N32oSuKrV6aDM8efdze7XdEgW5oYio6cyKOejH4SpPoT'
    client = Client(api_key, api_secret)
    days_fact = []
    for i in range(1,457):
        d = 19-((18/456)*i)
        days_fact.append(d)
    
    coin=coin.upper()


    klines = client.get_historical_klines(coin+"USDT", Client.KLINE_INTERVAL_1HOUR, "19 day ago UTC")
    close = []
    for i in range(len(klines)):
        close.append(float(klines[i][4]))
    open = []
    for i in range(len(klines)):
        open.append(float(klines[i][1]))
    change = []
    for i in range(len(close)):
        chg = ((close[i]/open[i])-1)*100
        change.append(chg)
    power_all = []
    for i in range(len(days_fact)):
        ch = change[i]/days_fact[i]
        power_all.append(ch)
    win_list = []
    lose_list =[]
    for i in range(len(power_all)):
        if power_all[i]>=0:
            win_list.append(power_all[i])
        else:
            lose_list.append(power_all[i])
    win = sum(win_list)
    lose = sum(lose_list)
    lose = lose*-1
    win_perc = win/(win+lose)
    lose_perc = lose/(win+lose)
    if win_perc>lose_perc:
        power=round(win_perc*100,2)
        direction = "bullish"
    else:
        power=round(lose_perc*100,2)
        direction = "bearish"
    data = {"coin":coin, "power":power, "direction":direction}

        return f"""
        <html>
            <head>
                <title>Some HTML in here</title>
            </head>
            <body>
                <h1>Look ma! HTML!</h1>
                <p>{coin}</p>
            </body>
        </html>"""