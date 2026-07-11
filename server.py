import os
import sys
import json
import time
import secrets
import mimetypes
import threading
import logging
from functools import wraps
from flask import Flask, request, jsonify, send_from_directory, abort

# ============================================================
# ОТКЛЮЧЕНИЕ ЛОГОВ FLASK
# Отключаем логи Werkzeug, чтобы они не ломали CLI-интерфейс
# ============================================================
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
META_FILE = "_meta.json"
MAX_UPLOAD_MB = 300
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024

DEFAULT_CONFIG = {
    "accounts": [{"username": "admin", "password": "123"}],
    "vault_path": "/storage/emulated/0/server",
}

_login_attempts = {}
_MAX_ATTEMPTS = 8
_WINDOW_SEC = 60

# ============================================================
# ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ СЕРВЕРА
# ============================================================
SERVER_THREAD = None
SERVER_RUNNING = False

# ============================================================
# УТИЛИТЫ И КОНФИГ
# ============================================================
def load_config():
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
        return dict(DEFAULT_CONFIG)
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        cfg.setdefault("accounts", DEFAULT_CONFIG["accounts"])
        cfg.setdefault("vault_path", DEFAULT_CONFIG["vault_path"])
        if not cfg["accounts"]:
            cfg["accounts"] = DEFAULT_CONFIG["accounts"]
        return cfg
    except Exception:
        return dict(DEFAULT_CONFIG)

def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

def hidden_path_for(path):
    path = path.rstrip("/")
    d, b = os.path.split(path)
    if b.startswith("."): return path
    return os.path.join(d, "." + b)

def get_current_vault_path():
    cfg = load_config()
    visible = cfg["vault_path"].rstrip("/")
    hidden = hidden_path_for(visible)
    return hidden if os.path.exists(hidden) else visible

def is_hidden():
    cfg = load_config()
    hidden = hidden_path_for(cfg["vault_path"].rstrip("/"))
    return os.path.exists(hidden)

def init_vault():
    path = get_current_vault_path()
    if not os.path.exists(path):
        try:
            os.makedirs(path, exist_ok=True)
            with open(os.path.join(path, "001_Инструкция.txt"), "w", encoding="utf-8") as f:
                f.write("Добро пожаловать в EDM data base!\nПапка успешно создана.\nВы можете редактировать этот текст.")
        except Exception:
            pass

def valid_tokens():
    cfg = load_config()
    return {f"{a['username']}:{a['password']}" for a in cfg.get("accounts", [])}

def safe_name(name: str) -> str:
    if not name or not isinstance(name, str): abort(400, "Invalid filename")
    name = name.strip()
    if not name or name in (".", ".."): abort(400, "Invalid filename")
    if "/" in name or "\\" in name or "\x00" in name: abort(400, "Invalid filename")
    if name == META_FILE: abort(400, "Reserved filename")
    return name

def resolve_in_vault(name: str) -> str:
    name = safe_name(name)
    vault = os.path.realpath(get_current_vault_path())
    target = os.path.realpath(os.path.join(vault, name))
    if os.path.commonpath([vault, target]) != vault: abort(400, "Invalid path")
    return target

def load_meta():
    path = os.path.join(get_current_vault_path(), META_FILE)
    if not os.path.exists(path): return {}
    try:
        with open(path, "r", encoding="utf-8") as f: return json.load(f)
    except Exception: return {}

def save_meta(meta):
    path = os.path.join(get_current_vault_path(), META_FILE)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

# ============================================================
# АВТОРИЗАЦИЯ И MIDDLEWARE
# ============================================================
def _token_ok(token):
    if not token: return False
    tokens = valid_tokens()
    return any(secrets.compare_digest(token, t) for t in tokens)

def check_auth(req):
    auth_header = req.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "): return False
    return _token_ok(auth_header[len("Bearer "):])

def check_auth_query(req):
    return _token_ok(req.args.get("token", ""))

def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not check_auth(request): return jsonify({"error": "Unauthorized"}), 401
        return fn(*args, **kwargs)
    return wrapper

def rate_limited(ip):
    now = time.time()
    attempts = [t for t in _login_attempts.get(ip, []) if now - t < _WINDOW_SEC]
    _login_attempts[ip] = attempts
    return len(attempts) >= _MAX_ATTEMPTS

def register_attempt(ip):
    _login_attempts.setdefault(ip, []).append(time.time())

# ============================================================
# РОУТЫ СЕРВЕРА
# ============================================================
@app.route("/")
def index():
    init_vault()
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/api/login", methods=["POST"])
def login():
    ip = request.remote_addr or "unknown"
    if rate_limited(ip): return jsonify({"success": False, "error": "Too many attempts, try later"}), 429
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", ""))
    password = str(data.get("password", ""))
    cfg = load_config()
    match = next((acc for acc in cfg.get("accounts", []) if secrets.compare_digest(username, acc["username"]) and secrets.compare_digest(password, acc["password"])), None)
    if match: return jsonify({"success": True, "token": f"{match['username']}:{match['password']}"})
    register_attempt(ip)
    return jsonify({"success": False, "error": "Access Denied"}), 401

@app.route("/api/status", methods=["GET"])
@require_auth
def status():
    vault = get_current_vault_path()
    total = sum(os.path.getsize(os.path.join(vault, f)) for f in os.listdir(vault) if os.path.isfile(os.path.join(vault, f)) and f != META_FILE) if os.path.exists(vault) else 0
    return jsonify({"hidden": is_hidden(), "path": get_current_vault_path(), "total_size": total})

@app.route("/api/toggle_hide", methods=["POST"])
@require_auth
def toggle_hide():
    cfg = load_config()
    visible = cfg["vault_path"].rstrip("/")
    hidden = hidden_path_for(visible)
    try:
        if os.path.exists(hidden):
            os.rename(hidden, visible)
            return jsonify({"success": True, "hidden": False})
        elif os.path.exists(visible):
            os.rename(visible, hidden)
            return jsonify({"success": True, "hidden": True})
        return jsonify({"success": False, "error": "Vault folder not found"}), 404
    except Exception as e: return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/files", methods=["GET"])
@require_auth
def list_files():
    vault, meta, files = get_current_vault_path(), load_meta(), []
    try:
        for f in os.listdir(vault):
            if f == META_FILE: continue
            full_path = os.path.join(vault, f)
            if os.path.isfile(full_path):
                info = meta.get(f, {})
                files.append({"name": f, "size": os.path.getsize(full_path), "mtime": os.path.getmtime(full_path), "tags": info.get("tags", []), "liked": bool(info.get("liked", False)), "favorite": bool(info.get("favorite", False))})
        files.sort(key=lambda x: x["mtime"], reverse=True)
        return jsonify({"files": files, "success": True})
    except Exception as e: return jsonify({"files": [], "success": False, "error": str(e)})

TEXT_EXTENSIONS = {".txt", ".md", ".json", ".py", ".js", ".html", ".css", ".csv", ".log", ".yml", ".yaml", ".xml", ".ini", ".cfg", ".sh"}

@app.route("/api/file/<name>", methods=["GET"])
def get_file(name):
    if not (check_auth(request) or check_auth_query(request)): return jsonify({"error": "Unauthorized"}), 401
    file_path = resolve_in_vault(name)
    ext = os.path.splitext(name)[1].lower()
    if not os.path.exists(file_path): return jsonify({"error": "Not found"}), 404
    if ext in TEXT_EXTENSIONS and request.args.get("raw") != "1":
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return jsonify({"success": True, "content": f.read(), "is_text": True})
    mt = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    return send_from_directory(get_current_vault_path(), os.path.basename(file_path), mimetype=mt, conditional=True)

@app.route("/api/save", methods=["POST"])
@require_auth
def save_file():
    data = request.get_json(silent=True) or {}
    with open(resolve_in_vault(data.get("name")), "w", encoding="utf-8") as f: f.write(data.get("content", ""))
    return jsonify({"success": True})

@app.route("/api/create", methods=["POST"])
@require_auth
def create_file():
    data = request.get_json(silent=True) or {}
    file_path = resolve_in_vault(data.get("name"))
    if os.path.exists(file_path): return jsonify({"success": False, "error": "Already exists"}), 409
    with open(file_path, "w", encoding="utf-8") as f: f.write(data.get("content", ""))
    return jsonify({"success": True})

@app.route("/api/upload", methods=["POST"])
@require_auth
def upload_file():
    if "file" not in request.files: return jsonify({"error": "No file"}), 400
    file = request.files["file"]
    if file.filename == "": return jsonify({"error": "Empty filename"}), 400
    name = safe_name(os.path.basename(file.filename))
    file.save(resolve_in_vault(name))
    return jsonify({"success": True, "name": name})

@app.route("/api/delete", methods=["POST"])
@require_auth
def delete_file():
    name = (request.get_json(silent=True) or {}).get("name")
    file_path = resolve_in_vault(name)
    if os.path.exists(file_path):
        os.remove(file_path)
        meta = load_meta()
        meta.pop(name, None)
        save_meta(meta)
        return jsonify({"success": True})
    return jsonify({"error": "Not found"}), 404

@app.route("/api/rename", methods=["POST"])
@require_auth
def rename_file():
    data = request.get_json(silent=True) or {}
    old_name, new_name = data.get("old_name"), data.get("new_name")
    old_path, new_path = resolve_in_vault(old_name), resolve_in_vault(new_name)
    if not os.path.exists(old_path): return jsonify({"error": "Not found"}), 404
    if os.path.exists(new_path): return jsonify({"error": "Target already exists"}), 409
    os.rename(old_path, new_path)
    meta = load_meta()
    if old_name in meta:
        meta[new_name] = meta.pop(old_name)
        save_meta(meta)
    return jsonify({"success": True})

@app.route("/api/meta", methods=["POST"])
@require_auth
def set_meta():
    data = request.get_json(silent=True) or {}
    name = safe_name(data.get("name"))
    if not os.path.exists(resolve_in_vault(name)): return jsonify({"error": "Not found"}), 404
    meta = load_meta()
    entry = meta.setdefault(name, {})
    if "tags" in data: entry["tags"] = [str(t).strip()[:30] for t in data["tags"] if str(t).strip()][:15]
    if "liked" in data: entry["liked"] = bool(data["liked"])
    if "favorite" in data: entry["favorite"] = bool(data["favorite"])
    save_meta(meta)
    return jsonify({"success": True, "meta": entry})

def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)


# ============================================================
# ТЕРМИНАЛЬНЫЙ ИНТЕРФЕЙС (CLI ADMIN UI)
# ============================================================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("\n|\\~ [ ENTER ] ДЛЯ ПРОДОЛЖЕНИЯ... ")

def boot_animation():
    icons = ["·", "✻", "✽", "✶", "✳", "✢"]
    phrases = ["ЗАПУСК ЯДРА", "ЧТЕНИЕ КОНФИГА", "ПРОВЕРКА ХРАНИЛИЩА", "СТАРТ FLASK СЕРВЕРА"]
    start_time = time.time()
    idx = 0
    while time.time() - start_time < 4.0:
        icon = icons[idx % len(icons)]
        phrase = phrases[(idx // 5) % len(phrases)]
        sys.stdout.write(f"\r|\\~ [ {icon} ] {phrase}... ")
        sys.stdout.flush()
        time.sleep(0.15)
        idx += 1
    sys.stdout.write("\r|\\~ [ ✻ ] СИСТЕМА УСПЕШНО ЗАПУЩЕНА!                 \n")
    time.sleep(0.8)

def draw_header(title="ГЛАВНОЕ МЕНЮ"):
    clear()
    cfg = load_config()
    users_count = len(cfg.get("accounts", []))
    v_path = cfg.get("vault_path", "")
    
    short_path = v_path if len(v_path) <= 16 else f"...{v_path[-13:]}"
    status_text = "ОНЛАЙН" if SERVER_RUNNING else "ОФФЛАЙН"
    
    art = [
        r"  _____  _____  __  __   ",
        r" |  ___||  _  \|  \/  |  ",
        r" | |__  | | | || \  / |  ",
        r" |  __| | | | || |\/| |  ",
        r" | |___ | |_| || |  | |  ",
        r" |_____||_____/|_|  |_|  "
    ]
    
    status_box = [
        r"/---------------------------\ ",
        f"| СТАТУС : [{status_text:<9}]  |",
        f"| ПОРТ   : 5000             |",
        f"| АДМИНЫ : {users_count:<16} |",
        f"| ПАПКА  : {short_path:<16} |",
        r"\---------------------------/ "
    ]
    
    print("/" + "-" * 58 + "\\")
    for i in range(6):
        left = art[i] if i < len(art) else " " * 25
        right = status_box[i] if i < len(status_box) else " " * 30
        print(f"| {left:<27} {right:<29} |")
    print("\\" + "-" * 58 + "/")
    print(f"|\\~ /_> {title}")
    print("-" * 60)

def menu_main():
    global SERVER_THREAD, SERVER_RUNNING
    while True:
        cfg = load_config()
        draw_header("ГЛАВНОЕ МЕНЮ")
        
        if not SERVER_RUNNING:
            print("|_ [ 1 ] ЗАПУСТИТЬ СЕРВЕР")
        else:
            print("|_ [ 1 ] СЕРВЕР УЖЕ РАБОТАЕТ (ПОРТ 5000)")
            
        print("|_ [ 2 ] УЧЁТНЫЕ ЗАПИСИ")
        print("|_ [ 3 ] НАСТРОЙКИ ХРАНИЛИЩА (VAULT)")
        print("|_ [ 4 ] ИНФО / СТАТИСТИКА")
        print("|_ [ 0 ] ВЫХОД")
        print("-" * 60)
        
        choice = input("|\\~ ВВОД: ").strip()
        
        if choice == "1":
            if not SERVER_RUNNING:
                boot_animation()
                SERVER_THREAD = threading.Thread(target=run_flask, daemon=True)
                SERVER_THREAD.start()
                SERVER_RUNNING = True
            else:
                print("|\\~ Сервер уже активен. Открой http://127.0.0.1:5000 в браузере.")
                pause()
        elif choice == "2":
            menu_accounts(cfg)
        elif choice == "3":
            menu_vault(cfg)
        elif choice == "4":
            menu_status(cfg)
        elif choice == "0":
            clear()
            print("|\\~ ВЫКЛЮЧЕНИЕ СИСТЕМЫ...")
            sys.exit(0)
        else:
            print("|\\~ ОШИБКА: НЕВЕРНЫЙ ВВОД")
            pause()

def menu_accounts(cfg):
    while True:
        draw_header("УЧЁТНЫЕ ЗАПИСИ")
        for i, a in enumerate(cfg["accounts"], 1):
            print(f"|_ [ {i} ] {a['username']} (Пароль: {'*' * len(a['password'])})")
        print("-" * 60)
        print("|_ [ A ] ДОБАВИТЬ АККАУНТ")
        print("|_ [ D ] УДАЛИТЬ АККАУНТ")
        print("|_ [ P ] СМЕНИТЬ ПАРОЛЬ")
        print("|_ [ L ] СМЕНИТЬ ЛОГИН")
        print("|_ [ 0 ] НАЗАД")
        print("-" * 60)
        
        choice = input("|\\~ ВВОД: ").strip().lower()

        if choice == "a":
            u = input("|\\~ НОВЫЙ ЛОГИН: ").strip()
            if not u: continue
            if any(a["username"] == u for a in cfg["accounts"]):
                print("|\\~ ТАКОЙ ЛОГИН УЖЕ СУЩЕСТВУЕТ")
                pause()
                continue
            p = input("|\\~ НОВЫЙ ПАРОЛЬ: ").strip()
            if not p: continue
            cfg["accounts"].append({"username": u, "password": p})
            save_config(cfg)
            print("|\\~ АККАУНТ ДОБАВЛЕН")
            pause()
        elif choice == "d":
            idx = input("|\\~ НОМЕР АККАУНТА ДЛЯ УДАЛЕНИЯ: ").strip()
            if idx.isdigit() and 1 <= int(idx) <= len(cfg["accounts"]):
                if len(cfg["accounts"]) == 1:
                    print("|\\~ ОШИБКА: НЕЛЬЗЯ УДАЛИТЬ ПОСЛЕДНИЙ АККАУНТ")
                    pause()
                    continue
                removed = cfg["accounts"].pop(int(idx) - 1)
                save_config(cfg)
                print(f"|\\~ УДАЛЕНО: {removed['username']}")
                pause()
        elif choice == "p":
            idx = input("|\\~ НОМЕР АККАУНТА: ").strip()
            if idx.isdigit() and 1 <= int(idx) <= len(cfg["accounts"]):
                newp = input("|\\~ НОВЫЙ ПАРОЛЬ: ").strip()
                if newp:
                    cfg["accounts"][int(idx) - 1]["password"] = newp
                    save_config(cfg)
                    print("|\\~ ПАРОЛЬ ОБНОВЛЕН")
                pause()
        elif choice == "l":
            idx = input("|\\~ НОМЕР АККАУНТА: ").strip()
            if idx.isdigit() and 1 <= int(idx) <= len(cfg["accounts"]):
                newu = input("|\\~ НОВЫЙ ЛОГИН: ").strip()
                if newu and not any(a["username"] == newu for a in cfg["accounts"]):
                    cfg["accounts"][int(idx) - 1]["username"] = newu
                    save_config(cfg)
                    print("|\\~ ЛОГИН ОБНОВЛЕН")
                else:
                    print("|\\~ ОШИБКА: ЛОГИН ЗАНЯТ ИЛИ ПУСТ")
                pause()
        elif choice == "0":
            return

def menu_vault(cfg):
    draw_header("РАСПОЛОЖЕНИЕ VAULT")
    print(f"|_ ТЕКУЩИЙ ПУТЬ : {cfg['vault_path']}")
    print(f"|_ СКРЫТЫЙ ВИД  : {hidden_path_for(cfg['vault_path'])}")
    print("-" * 60)
    print("|\\~ Введи новый абсолютный путь (или Enter для отмены).")
    print("|\\~ Пример: /storage/emulated/0/Documents/MyVault")
    newp = input("\n|\\~ ПУТЬ: ").strip()
    if newp:
        try:
            os.makedirs(newp, exist_ok=True)
            cfg["vault_path"] = newp.rstrip("/")
            save_config(cfg)
            print("|\\~ ПУТЬ УСПЕШНО ОБНОВЛЕН")
        except Exception as e:
            print(f"|\\~ ОШИБКА: {e}")
    pause()

def menu_status(cfg):
    draw_header("СТАТУС ИНФО")
    visible = cfg["vault_path"].rstrip("/")
    hidden = hidden_path_for(visible)
    active = hidden if os.path.exists(hidden) else visible
    
    print(f"|_ АКТИВНЫЙ ПУТЬ : {active}")
    print(f"|_ СОСТОЯНИЕ     : {'[ СКРЫТ ]' if active == hidden else '[ ВИДИМ ]'}")
    
    if os.path.exists(active):
        try:
            files = [f for f in os.listdir(active) if os.path.isfile(os.path.join(active, f)) and f != "_meta.json"]
            total = sum(os.path.getsize(os.path.join(active, f)) for f in files)
            print(f"|_ ВСЕГО ФАЙЛОВ  : {len(files)}")
            print(f"|_ ОБЩИЙ ВЕС     : {total/1024:.1f} KB")
        except Exception as e:
            print(f"|\\~ ОШИБКА ЧТЕНИЯ: {e}")
    else:
        print("|\\~ ПАПКА ЕЩЕ НЕ СОЗДАНА (СИСТЕМА СОЗДАСТ ЕЁ САМА)")
    print("-" * 60)
    pause()

if __name__ == "__main__":
    init_vault()
    menu_main()
