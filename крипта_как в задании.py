import tkinter as tk
from tkinter import messagebox, ttk
import requests


class CryptoTrackerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Мониторинг Криптовалют")
        self.root.geometry("550x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f6f9")

        # Список из 30 популярных криптовалют (ID в системе CoinGecko)
        self.crypto_ids = {
            "Bitcoin (BTC)": "bitcoin",
            "Ethereum (ETH)": "ethereum",
            "Binance Coin (BNB)": "binancecoin",
            "Solana (SOL)": "solana",
            "Ripple (XRP)": "ripple",
            "Cardano (ADA)": "cardano",
            "Dogecoin (DOGE)": "dogecoin",
            "Shiba Inu (SHIB)": "shiba-inu",
            "Avalanche (AVAX)": "avalanche-2",
            "Polkadot (DOT)": "polkadot",
            "TRON (TRX)": "tron",
            "Chainlink (LINK)": "chainlink",
            "Polygon (POL/MATIC)": "polygon",
            "Uniswap (UNI)": "uniswap",
            "Litecoin (LTC)": "litecoin",
            "NEAR Protocol (NEAR)": "near",
            "Pepe (PEPE)": "pepe",
            "Sui (SUI)": "sui",
            "Aptos (APT)": "aptos",
            "Stellar (XLM)": "stellar",
            "Hedera (HBAR)": "hedera-hashgraph",
            "Kaspa (KAS)": "kaspa",
            "Monero (XMR)": "monero",
            "Ethereum Classic (ETC)": "ethereum-classic",
            "Render (RENDER)": "render-token",
            "Cosmos (ATOM)": "cosmos",
            "Filecoin (FIL)": "filecoin",
            "Injective (INJ)": "injective-protocol",
            "Optimism (OP)": "optimism",
            "Arbitrum (ARB)": "arbitrum",
        }

        self.create_widgets()
        # По умолчанию загружаем данные для выбранной в комбобоксе валюты
        self.fetch_prices()

    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(
            self.root,
            text="Курсы криптовалют к USD",
            font=("Helvetica", 16, "bold"),
            bg="#f4f6f9",
            fg="#2c3e50",
        )
        title_label.pack(pady=15)

        # Фрейм для выбора валюты через Combobox
        select_frame = tk.Frame(self.root, bg="#f4f6f9")
        select_frame.pack(fill=tk.X, padx=20, pady=5)

        select_label = tk.Label(
            select_frame,
            text="Выберите монету для отслеживания:",
            font=("Helvetica", 11),
            bg="#f4f6f9",
            fg="#34495e",
        )
        select_label.pack(side=tk.LEFT, padx=(0, 10))

        # Сортируем названия монет по алфавиту (от А до Я) для комбобокса
        sorted_crypto_names = sorted(list(self.crypto_ids.keys()))

        # Создание выпадающего списка
        self.crypto_combobox = ttk.Combobox(
            select_frame,
            values=["Все монеты разом"] + sorted_crypto_names,
            state="readonly",
            font=("Helvetica", 10),
            width=22,
        )
        self.crypto_combobox.current(0)  # Выбираем первый пункт по умолчанию
        self.crypto_combobox.pack(side=tk.LEFT)
        self.crypto_combobox.bind("<<ComboboxSelected>>", lambda e: self.fetch_prices())

        # Фрейм для таблицы
        self.table_frame = tk.Frame(self.root, bg="#f4f6f9")
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Конфигурация стилей таблицы
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            font=("Helvetica", 11),
            rowheight=30,
            background="#ffffff",
            fieldbackground="#ffffff",
        )
        style.configure(
            "Treeview.Heading", font=("Helvetica", 11, "bold"), background="#e2e8f0"
        )

        # Создание таблицы данных
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=("Name", "Price", "Change"),
            show="headings",
        )
        self.tree.heading("Name", text="Название")
        self.tree.heading("Price", text="Цена (USD)")
        self.tree.heading("Change", text="Изменение (24ч)")

        self.tree.column("Name", width=170, anchor="w")
        self.tree.column("Price", width=160, anchor="e")
        self.tree.column("Change", width=140, anchor="e")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Нижняя панель с кнопкой обновления
        button_frame = tk.Frame(self.root, bg="#f4f6f9")
        button_frame.pack(fill=tk.X, pady=15)

        self.refresh_btn = tk.Button(
            button_frame,
            text="Обновить данные",
            command=self.fetch_prices,
            font=("Helvetica", 11, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5,
        )
        self.refresh_btn.pack()

        # Индикатор статуса
        self.status_label = tk.Label(
            self.root,
            text="Загрузка данных...",
            font=("Helvetica", 9, "italic"),
            bg="#f4f6f9",
            fg="#7f8c8d",
        )
        self.status_label.pack(side=tk.BOTTOM, pady=5)

    def fetch_prices(self):
        self.refresh_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Обновление данных...", fg="#7f8c8d")
        self.root.update_idletasks()

        # Определяем, какие ID запрашивать на основе выбора в Combobox
        selected_item = self.crypto_combobox.get()

        if selected_item == "Все монеты разом":
            target_coins = self.crypto_ids.copy()
        else:
            target_coins = {selected_item: self.crypto_ids[selected_item]}

        # Блок формирования параметров запроса (сохранен без изменений)
        ids_param = ",".join(target_coins.values())
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": ids_param, "vs_currencies": "usd", "include_24hr_change": "true"}

        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 429:
                messagebox.showwarning(
                    "Превышен лимит",
                    "Слишком много запросов! Пожалуйста, подождите минуту перед следующим обновлением.",
                )
                self.status_label.config(
                    text="Превышен лимит запросов.", fg="#e74c3c"
                )
                return

            response.raise_for_status()
            data = response.json()

            # Очищаем таблицу перед выводом новых данных
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Наполнение таблицы отфильтрованными данными
            for display_name, coin_id in target_coins.items():
                if coin_id in data:
                    price = data[coin_id].get("usd", 0.0)
                    change = data[coin_id].get("usd_24h_change", 0.0)

                    # Гибкое форматирование для дешевых мемкоинов
                    if price >= 1.0:
                        price_str = f"${price:,.2f}"
                    elif price > 0.0:
                        price_str = f"${price:.8f}"  # Больше знаков для точности отображения
                    else:
                        price_str = "$0.00"

                    change_str = f"{change:+.2f}%" if change is not None else "0.00%"

                    tag = "up" if (change and change >= 0) else "down"

                    self.tree.insert(
                        "",
                        tk.END,
                        values=(display_name, price_str, change_str),
                        tags=(tag,),
                    )

            self.tree.tag_configure("up", foreground="#27ae60")
            self.tree.tag_configure("down", foreground="#e74c3c")

            self.status_label.config(text="Данные успешно обновлены", fg="#27ae60")

        except requests.exceptions.RequestException as e:
            messagebox.showerror(
                "Ошибка сети", f"Не удалось получить данные:\n{e}"
            )
            self.status_label.config(
                text="Ошибка при обновлении данных.", fg="#e74c3c"
            )

        finally:
            self.refresh_btn.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoTrackerApp(root)
    root.mainloop()
