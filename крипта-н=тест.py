from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import requests

# Глобальный словарь с точными названиями монет (расширен до 30+ штук)
crypto_currencies = {
    'BTC': 'Bitcoin (BTC)',
    'ETH': 'Ethereum (ETH)',
    'BNB': 'Binance Coin (BNB)',
    'XRP': 'Ripple (XRP)',
    'SOL': 'Solana (SOL)',
    'ADA': 'Cardano (ADA)',
    'DOGE': 'Dogecoin (DOGE)',
    'LTC': 'Litecoin (LTC)',
    'DOT': 'Polkadot (DOT)',
    'MATIC': 'Polygon (MATIC)',
    'AVAX': 'Avalanche (AVAX)',
    'SHIB': 'Shiba Inu (SHIB)',
    'TRX': 'TRON (TRX)',
    'LINK': 'Chainlink (LINK)',
    'NEAR': 'Near Protocol (NEAR)',
    'ATOM': 'Cosmos (ATOM)',
    'XLM': 'Stellar (XLM)',
    'BCH': 'Bitcoin Cash (BCH)',
    'UNI': 'Uniswap (UNI)',
    'APT': 'Aptos (APT)',
    'SUI': 'Sui (SUI)',
    'HBAR': 'Hedera (HBAR)',
    'ICP': 'Internet Computer (ICP)',
    'GRT': 'The Graph (GRT)',
    'TAO': 'Bittensor (TAO)',
    'STX': 'Stacks (STX)',
    'FIL': 'Filecoin (FIL)',
    'IMX': 'Immutable (IMX)',
    'LDO': 'Lido DAO (LDO)',
    'PEPE': 'Pepe (PEPE)',
    'TON': 'Toncoin (TON)',
    'NOT': 'Notcoin (NOT)'
}


def update_crypto_label(event):
    code = crypto_combobox.get()
    if code in crypto_currencies:
        name = crypto_currencies[code]
        crypto_label.config(text=name)


def show_custom_info(title, crypto_name, price_str):
    """Кастомное окно сообщения с авторазмером, которое открывается строго по центру главного окна"""
    custom_win = Toplevel(window)
    custom_win.title(title)
    custom_win.configure(bg="#E0F7FA")
    custom_win.resizable(False, False)

    # Сначала скрываем окно, чтобы пользователь не видел процесс перемещения
    custom_win.withdraw()

    # Формируем и настраиваем текст сообщения
    msg_text = f"Текущая стоимость:\n1 {crypto_name} = ${price_str} USDT"

    lbl = Label(
        custom_win,
        text=msg_text,
        font=("PT Serif", 14, "bold"),
        fg="#0D47A1",
        bg="#E0F7FA",
        justify="center"
    )
    lbl.pack(padx=30, pady=20)

    close_btn = Button(custom_win, text="OK", width=10, command=custom_win.destroy)
    close_btn.pack(pady=(0, 15))

    # Обновляем геометрию, чтобы узнать точные размеры созданного окна под текст
    custom_win.update_idletasks()

    # Размеры всплывающего окна
    win_w = custom_win.winfo_width()
    win_h = custom_win.winfo_height()

    # Координаты и размеры главного окна программы
    main_x = window.winfo_x()
    main_y = window.winfo_y()
    main_w = window.winfo_width()
    main_h = window.winfo_height()

    # Математический расчет центра всплывающего окна относительно главного
    pos_x = main_x + int((main_w / 2) - (win_w / 2))
    pos_y = main_y + int((main_h / 2) - (win_h / 2))

    # Задаем позицию и отображаем окно
    custom_win.geometry(f"+{pos_x}+{pos_y}")
    custom_win.deiconify()

    # Делаем окно модальным (поведение как у messagebox)
    custom_win.transient(window)
    custom_win.grab_set()
    window.wait_window(custom_win)


def get_price():
    selected_key = crypto_combobox.get()
    if not selected_key:
        mb.showwarning('Внимание', 'Выберите криптовалюту из списка')
        return

    try:
        url = "https://api.binance.com/api/v3/ticker/price"

        # Исправлено обратно на стабильную торговую пару USDT
        query_params = {
            'symbol': f"{selected_key}USDT"
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, params=query_params, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        if 'price' in data:
            price = float(data['price'])
            crypto_name = crypto_currencies[selected_key]

            if price < 0.0001:
                price_str = f"{price:.8f}"
            elif price < 1:
                price_str = f"{price:.6f}"
            else:
                price_str = f"{price:,.2f}"

            show_custom_info('Курс криптовалюты', crypto_name, price_str)
        else:
            mb.showerror('Ошибка', 'Не удалось извлечь цену для этой валюты')

    except Exception as er:
        mb.showerror('Ошибка', f'Не удалось получить данные:\n{er}')


# Инициализация графического окна
window = Tk()
window.title("Курс криптовалют")

# Задаем размеры окна
window_width = 380
window_height = 240

# Получаем размеры вашего экрана автоматически
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Математически точный расчет центра экрана для главного окна
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))

# Принудительно открываем главное окно строго по центру экрана
window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Комбобокс выбора
crypto_combobox = ttk.Combobox(window, values=sorted(list(crypto_currencies.keys())), state="readonly",
                               font=("Arial", 12, "bold"))
crypto_combobox.pack(pady=10)
crypto_combobox.bind("<<ComboboxSelected>>", update_crypto_label)

# Метка полного названия (зеленая, жирная, с подчеркиванием)
crypto_label = Label(window, text="", font=("Arial", 12, "bold", "underline"), fg="#228B22")
crypto_label.pack(pady=10)

# Кнопка получения цены (Желтая, шрифт крупнее, жирный и курсив)
btn = Button(
    window,
    text="Получить курс",
    command=get_price,
    bg="#FFD700",
    font=("Arial", 12, "bold", "italic"),
    activebackground="#FFEA00"
)
btn.pack(pady=10)

window.mainloop()
