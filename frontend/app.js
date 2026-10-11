const API = "http://127.0.0.1:8000/api";

const words = {
    uz: {
        home:"Bosh sahifa", accounts:"Hisoblar", analytics:"Tahlil",
        transactions:"Operatsiyalar", categories:"Kategoriyalar",
        addAccount:"Hisob qo'shish", addTransaction:"Yangi operatsiya",
        income:"Kirim", expense:"Chiqim", name:"Nomi",
        amount:"Summa", date:"Sana", note:"Izoh",
        save:"Saqlash", cancel:"Bekor qilish", delete:"O'chirish",
        account:"Hisob", type:"Turi", balance:"Balans",
        all:"Barchasi", error:"Xatolik", loading:"Yuklanmoqda...",
        totalBalance:"Umumiy balans", totalIncome:"Jami kirim",
        totalExpense:"Jami chiqim", count:"Hisoblar soni",
        chooseAccount:"Hisobni tanlang", success:"Muvaffaqiyatli!"
    },
    ru: {
        home:"Главная", accounts:"Счета", analytics:"Аналитика",
        transactions:"Операции", categories:"Категории",
        addAccount:"Добавить счёт", addTransaction:"Новая операция",
        income:"Доход", expense:"Расход", name:"Название",
        amount:"Сумма", date:"Дата", note:"Примечание",
        save:"Сохранить", cancel:"Отмена", delete:"Удалить",
        account:"Счёт", type:"Тип", balance:"Баланс",
        all:"Все", error:"Ошибка", loading:"Загрузка...",
        totalBalance:"Общий баланс", totalIncome:"Общий доход",
        totalExpense:"Общие расходы", count:"Количество счетов",
        chooseAccount:"Выберите счёт", success:"Успешно!"
    },
    en: {
        home:"Dashboard", accounts:"Accounts", analytics:"Analytics",
        transactions:"Transactions", categories:"Categories",
        addAccount:"Add account", addTransaction:"New transaction",
        income:"Income", expense:"Expense", name:"Name",
        amount:"Amount", date:"Date", note:"Note",
        save:"Save", cancel:"Cancel", delete:"Delete",
        account:"Account", type:"Type", balance:"Balance",
        all:"All", error:"Error", loading:"Loading...",
        totalBalance:"Total balance", totalIncome:"Total income",
        totalExpense:"Total expenses", count:"Accounts",
        chooseAccount:"Choose account", success:"Success!"
    }
};

let language = localStorage.getItem("language") || "uz";
let accounts = [];
let incomes = [];
let expenses = [];

function tr(key) {
    return words[language][key] || key;
}

function money(value) {
    return Number(value || 0).toLocaleString() + " UZS";
}

function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, function (c) {
        return {
            "&":"&amp;", "<":"&lt;", ">":"&gt;",
            '"':"&quot;", "'":"&#39;"
        }[c];
    });
}

async function request(endpoint, method = "GET", body = null) {
    const headers = {};
    const token = localStorage.getItem("token");

    if (token) headers.Authorization = "Token " + token;
    if (body) headers["Content-Type"] = "application/json";

    const response = await fetch(API + "/" + endpoint, {
        method: method,
        headers: headers,
        body: body ? JSON.stringify(body) : null
    });

    if (!response.ok) {
        throw new Error("HTTP " + response.status);
    }

    if (response.status === 204) return null;

    return response.json();
}

function list(data) {
    if (Array.isArray(data)) return data;
    return data && Array.isArray(data.results) ? data.results : [];
}

function translatePage() {
    document.documentElement.lang = language;

    document.querySelectorAll("[data-i18n]").forEach(function (el) {
        el.textContent = tr(el.dataset.i18n);
    });

    document.querySelectorAll("[data-uz][data-ru][data-en]")
        .forEach(function (el) {
            el.textContent = el.getAttribute("data-" + language);
        });

    const selector = document.getElementById("languageSelect");
    if (selector) selector.value = language;
}

async function login(username, password) {
    const message = document.getElementById("loginMessage");

    try {
        const response = await fetch(API + "/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Login yoki parol noto‘g‘ri");
        }

        localStorage.setItem("token", data.token);
        message.textContent = "Kirish muvaffaqiyatli!";
        document.getElementById("loginPanel").style.display = "none";

        await loadData();
    } catch (error) {
        message.textContent = "Xatolik: " + error.message;
    }
}

document.getElementById("loginForm").addEventListener(
    "submit", function (event) {
        event.preventDefault();

        const form = new FormData(event.target);
        login(
            form.get("username"),
            form.get("password")
        );
    }
);

document.getElementById("logoutBtn").addEventListener("click", function () {
    localStorage.removeItem("token");
    location.reload();
});

async function loadData() {
    try {
        const results = await Promise.all([
            request("accounts/"),
            request("incomes/"),
            request("expenses/")
        ]);

accounts = list(results[0]);
        incomes = list(results[1]);
        expenses = list(results[2]);

        render();
        document.getElementById("apiStatus").textContent =
            "Backend ulandi";
    } catch (error) {
        document.getElementById("apiStatus").textContent =
            tr("error") + ": " + error.message;
    }
}

function render() {
    const balance = accounts.reduce(
        (sum, item) => sum + Number(item.balance || 0), 0
    );
    const income = incomes.reduce(
        (sum, item) => sum + Number(item.amount || 0), 0
    );
    const expense = expenses.reduce(
        (sum, item) => sum + Number(item.amount || 0), 0
    );

    document.getElementById("totalBalance").textContent = money(balance);
    document.getElementById("totalIncome").textContent = money(income);
    document.getElementById("totalExpense").textContent = money(expense);
    document.getElementById("totalAccounts").textContent = accounts.length;

    document.getElementById("accountsList").innerHTML =
        accounts.map(function (a) {
            return '<article class="stat-card"><h3>' +
                escapeHTML(a.name) + '</h3><p>' +
                escapeHTML(a.type) + '</p><strong>' +
                money(a.balance) +
                '</strong><button data-delete="account" data-id="' +
                a.id + '">' + tr("delete") + '</button></article>';
        }).join("");

    const transactions = incomes.map(function (x) {
        return {...x, kind:"income", label:tr("income")};
    }).concat(expenses.map(function (x) {
        return {...x, kind:"expense", label:tr("expense")};
    }));

    transactions.sort(function (a, b) {
        return new Date(b.date) - new Date(a.date);
    });

    document.getElementById("transactionsTable").innerHTML =
        transactions.map(function (x) {
            return "<tr><td>" + escapeHTML(x.note || x.label) +
                "</td><td>" + escapeHTML(x.type_name || "-") +
                "</td><td>" + escapeHTML(x.account_name || x.account || "-") + +
                "</td><td>" + escapeHTML(x.date || "-") +
                "</td><td>" + money(x.amount) +
                '</td><td><button data-delete="' + x.kind +
                '" data-id="' + x.id + '">' + tr("delete") +
                "</button></td></tr>";
        }).join("");

    translatePage();
}

function openForm(kind) {
    const root = document.getElementById("modalRoot");
    const isAccount = kind === "account";
    const options = accounts.map(function (a) {
        return '<option value="' + a.id + '">' +
            escapeHTML(a.name) + '</option>';
    }).join("");

    root.innerHTML = '<div class="panel"><form id="dataForm">' +
        (isAccount
            ? '<label>' + tr("name") +
              '<input name="name" required></label>' +
              '<label>' + tr("type") +
              '<select name="type"><option value="cash">Cash</option>' +
              '<option value="card">Card</option><option value="bank">Bank</option>' +
              '</select></label><label>' + tr("balance") +
              '<input name="balance" type="number" step="0.01" value="0" required></label>'
            : '<label>' + tr("type") +
              '<select name="kind"><option value="incomes">' + tr("income") +
              '</option><option value="expenses">' + tr("expense") +
              '</option></select></label><label>' + tr("account") +
              '<select name="account" required>' + options +
              '</select></label><label>' + tr("amount") +
              '<input name="amount" type="number" min="0.01" step="0.01" required></label>' +
              '<label>' + tr("date") +
              '<input name="date" type="date" required></label><label>' +
              tr("note") + '<input name="note"></label>') +
        '<button type="submit">' + tr("save") + '</button>' +
        '<button type="button" id="closeForm">' + tr("cancel") +
        '</button></form></div>';

    document.getElementById("closeForm").onclick = function () {
        root.innerHTML = "";
    };

document.getElementById("dataForm").onsubmit = async function (event) {
        event.preventDefault();
        const form = new FormData(event.target);
        const data = Object.fromEntries(form.entries());

        try {
            if (isAccount) {
                data.balance = Number(data.balance);
                await request("accounts/", "POST", data);
            } else {
                const endpoint = data.kind;
                delete data.kind;
                data.account = Number(data.account);
                data.amount = Number(data.amount);
                await request(endpoint + "/", "POST", data);
            }

            root.innerHTML = "";
            await loadData();
        } catch (error) {
            alert(tr("error") + ": " + error.message);
        }
    };
}

document.getElementById("languageSelect").addEventListener(
    "change", function (event) {
        language = event.target.value;
        localStorage.setItem("language", language);
        translatePage();
        render();
    }
);

document.getElementById("refreshBtn").onclick = loadData;
document.getElementById("addAccountBtn").onclick = function () {
    openForm("account");
};
document.getElementById("addTransactionBtn").onclick = function () {
    openForm("transaction");
};

document.addEventListener("click", async function (event) {
    const button = event.target.closest("[data-delete]");
    if (!button) return;

    if (!confirm(tr("delete") + "?")) return;

    const kind = button.dataset.delete;
    const endpoint = kind === "account" ? "accounts/" :
        kind === "income" ? "incomes/" : "expenses/";

    try {
        await request(endpoint + button.dataset.id + "/", "DELETE");
        await loadData();
    } catch (error) {
        alert(tr("error") + ": " + error.message);
    }
});

translatePage();

if (localStorage.getItem("token")) {
    document.getElementById("loginPanel").style.display = "none";
    loadData();
}

