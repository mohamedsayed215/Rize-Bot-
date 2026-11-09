import discord
from discord.ext import commands
from discord import app_commands
from google import genai
import json
import os
import random
import secrets
import string
import datetime
import asyncio
import re
import io
import math
import base64
from typing import Optional, List
from PIL import Image, ImageDraw, ImageFont

print("⏳ جاري تشغيل بوت Rize والاتصال بالخادم...")

# ==============================================================================
# ⚙️ 1. الإعدادات والمفاتيح الأساسية
# ==============================================================================
TOKEN = "MTU1NzEwNTM5ODA0NDA0MTM0Ng.Gb5NYf.s_-BlcGLrV6V_J3ljSvrYxVMaxFWq61DKa5cdU"
GEMINI_API_KEY = "AQ.Ab8RN6IH-swfjmnyAzqQees82yphB8sy9SqORd_6ToGKpDP_iw"

PRIMARY_OWNER_ID = 875161402476736603
PREMIUM_PAYMENT_RECEIVER_ID = 875161402476736603
PROBOT_ID = 282859044593598464
ADAMC_BOT_ID = 0  # ضع ID بوت AdamC الحقيقي هنا عند معرفته
SPIN_BOT_ID = 1564749940096368833
SUPPORT_GUILD_ID = 882741940968357908
MAIN_GUILD_ID = 882741940968357908
BLACKLIST_ROLE_ID = 1568202927431225344
LINE_IMAGE_B64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAAiAggDASIAAhEBAxEB/8QAHQAAAQQDAQEAAAAAAAAAAAAAAAIDBAUBBgcICf/EAD0QAAEDAgQDBwEGAwcFAAAAAAEAAgMEEQUSITEGE0EHCCJRYXGBMiMzUpGhsQkU0QoVFkJicsEkQ1Ph8P/EAB0BAAICAwEBAQAAAAAAAAAAAAMEBQYBAgcACAn/xAAzEQABAwMCAwUGBwEBAAAAAAABAAIDBBEhMUEFElEGEzJhcSIzNJGx4RRSgaHB0fBi8f/aAAwDAQACEQMRAD8A+dskMNC0iokjhP8AqNj+Sgy49RwOLW55gOoFh+qonxFzrklzj8p2KmF7OC/WWSscTZoVAZTjc3U92PkH7OIAHa7k0+uqJvEMo+NkmGAMNiLhSoIC4g2sEsXvdqUwyNg0CZEk04vnLbb2ATmSaZwAc+w63UqGlD36DRTYoAxuVo1/dDLCdSnYmZwFXwwSFuVxcfVSYqN8Q8Rdl9VZwwh7PFlBHXyTsQbK7K7Ro0Q5GhouSiVdY2li5iLk6BUb6KaV4cAco81JhwiZozNbey2WipYm/UAWjp5q1w2CEEHID53UNUtackqovrJJHl7xclapSYTK8guY63sna+rZhzcoaHy9G+Xutxq8UpKUiGOJhkP1dMqhGiwypcc1OHPcbl2YkkoVNwYzHvHn2fr9kB1bym3KtCqKmarlLpDdx012A9EuGmyAZhe63xvBmE4iMrTNA/zDg4fkQkydmQsWw1kL/IPBaf8AkKVNCWtsESKdrlpsVPynAt+kqVDSA+IGw3KvZuAK/DXHPFdnQg3B+VFqeHaqJw+xe1u5IF7paSIsyUzJVwQN5nn9Nyq4szP8IubfkswwmY5XGymsw94cGtaR8KU3DjcaaqEqZ3G42UFVcSknPLo3p/agU9KQC1w0Uunw9zDa1wVPpcOMoAc3UaArNXiUWFjIBzZG9BsPlQr+eQ8sYuUlzNblyRFh+Rud9gwaknQBIqOIqen+5HOeNydGhV1VW1GIvJmd9mP8g0aFDFOHONtAis4XbMpv5JaSsvhifxDFJ8Zd43+EbNGgHwomXMcr9CNk605TlaNt7JTmidttnJxrGtFmiyQe8k3csYdiEuF1jZGOLS3QHpbyI6hbXQV0eNQl0YDZGi8kW9vUeY/Zajyi45XaEbFSKKeXD3B7Xlj2G7S06o9PUuiwchI1EIkF91sFXSGE5m6tUJ0JlfmPhAVlg+MR45Hlc0R1A3b/AJZPVvr6fksVdE6V1g2wCk3APHMzIKQEhY7ldqqmaMzP0bcJsk5MmysZIeWMrB7m26YlhErtrPH6pGSI6IzZAcKKIWQts7Unc+S673QOxjDO3fiLiXherwXFMRxCbCHV2G12G1oZU4dJFIwHLTuHLqg/mtBic6N3hGR4do7lBaJRkdoehXuv+zp0cVT/ABF2w1EUc0beFcSflkaHC4kpiDY+RVU7XVslDweorI/FG0uGSMjOo/fYjBuMKU4NTiorI4CfEbddVRcD/wAGx3HEWCUlN2r4DTcQ45iLsMp6OoweZlJLI0kSZKkygcyNwyyUz2MqY3XDogLOd5473Hcx457mnaC3AuMsMdDHWGZ+G4jFG9tLiscUnLe+LOA4Wda7XAOGZvQgn2Zx/wBw/vUYb30+1Wq4V7L6vGuB+PeLa+oq8PxySlfw/jlK+rkfFLPG6YFhDXBzJ2ZJ4t2OadFsv8ZjhPtD427EsN4fxx2FVlT2JTx12KPnxIT1dJR1sQghayrLWNrGudECGyCKtytaXwyi1Q6icK7W1Y4nTwyVcU8UwuQCzmZcC3h/6IbZ2vW5sLLU8Hi/DSyNicxzNLg2dbXXyBOPlYXPy4+9aGkWd+6SbAZSl1AvKMupG6Rn5rbHQgLrZwqe0pqSR0GgF77JogxkOOt/VPPlMYs4XI2TdyWkv26LUuFkZpskPALg/MRZMS5qh7nNFrbJzLm/29U26Qk2ZsFjnTLMJNxUMsdHBNatJY8exTxaJNW/V1CSQJ2ZXaOGy2aU00poHlGx1aUlzTG4EbJZ8MZDjfySWHIPEDlKI3VGaUmGR9PUtqL2Mbg4fC7hwDjLZWxvB8LwHD2Oq4e8GV3kwBb/ANl2Pg0jGBxzQHln26KM4uz2WyDbHzUB2mpe9pw/p/K75wri7sBxKNzTaGXVvoeoXd+EsYoeMOHp8NxKGCtoK6EwVEEzczJWOFi0hecuHahuK4fyXOsTq134T0K3Ds+42lwiq/l5iWSxusWk7KFdFm7cdFziRhqYy0+Nnz8ivOve07rVb3bOKzUUUc9VwlibyaGrPiMR35MhGzh0/EBfzty+gxgM1zGy+nEpwftU4Mq8DxqnjrcNxGIxTRPtpfZzT0cDqD0IXz870Xdgxfu08W5Xl9fw9WuJoMQa2zXt/A+30yDqOu4027Z2L7XfjGiirTaUaH8w6+o3G+o3tbuz3GhVj8JVm0o0P5vutWNRHX05ZK1rmO3BVFjeEOpWl7CXQ+fVvv8A1WKHFC5wsbAKzgrg51tCDv1V54lwaHiEecOGh/2oV1o6iSlf7OR0Wru+0aA7Rw0TTyWeG2pV7i3DrZgZaQa7mO/7KlkJYC1wOZumvRcwr+G1FFJ3c4t0Ox9Fc6OqjnZzRn9NwmA0sd4he6TI0NN76FObNOa3omSNNRolB5KUY5NvjJdcJJ+0A/EP1S3OcDoNAsObn8Td/JFCaYcpp4BOUpp12Gx2UiQ8wAW1SZI/CAdT+yM0puMlMOYWO8wVkR2GYp4MsNb29UCLmAk7I7Uy1w3UcR7kBBj5mikBtvhZMIdZzQitaSjteo3JaDl2PmhSBBzRvr+6EcMNkYO6LY2MEQuRqnWMJZmcLFJigP1O2UmGPmuueiWuVXWtusQC9g74UqLxAAbJMcIeRpa36qRTsANjYLYP6p2GmunIhlaA3UlTILM16qOxoZoDqszSimjFtXu2HktXyhrSSpEsZDGZZMAJ+SqEzsrSBbdSKeTnEDYhV0ERNnD8lZUdPzdR9Sr9XXk5VKqZXVEhkf8A+KwoYnEgE/JTuKcS/wB2s5MNjKdz+D/2oWKYt/dMDWNsah40H4B5lUgqSXeIkk7k6kodDC6Y97Jpt5/ZLvZbAVnFXOa7OCTfU3Klw4nkAcNyqmNwaNDclSacZLF3XorB3pWjKa+oV1T4oZRoTmVnS40RFd9wW7Fa437JvMBsD0T0Lnzvudv2Q5KsMCHWSR0zMZd0/tbnhHFRZZpcbHa/RWrKinrtHxhpd1ZoVpFIc3h2tsrjDqiZht+qipq/NyqlM18jy9xuSthfw81zbQFkpd0cNVEqsIgw1hdPEGn0/oj/ABAMGaATnmOw8vdOQ42MQZmq7SeQO49kCGkdUnmdhv1SU0/c4GSqPGA2sp7RuMDdrdXKmdhBdoQHAdQtuqMGiri58bttQ07qsq8OdcgNs4fqpVtHFGwNYLKPNW5x9orXZcOe99g0hoTE9NrkaPS62AuNuW8fmE1LTwtjOUWd1PRKyUwJW4nN1rz4/wCXFgLlJdESMzRYq4mwxkbM7hmJUSahMbszDdqjpKcjK2EwcoYaKhvk4fqsclx1ds1Sn02cZmaOG4TTi6ZwBsAlHNxle5uiZbPkeCLgDa24Wx4RxQyoaI6wgOOgm6O/3f1/PzVE6NmrbfKbc/kNLBqSsRTviOEKWNsgsVuFXSiD6Rq7rbSyg1NJnaXNFiOgVdg/EkmDRBkgE8X/AIydW+x6e2yvaeWHEmc2lfcWu5p0c33H/Klo5o5vDg9FGuY6N1zp1VZJTZ2ZnNyu8/Ne1f4A3EH+FO/Ji2KuNO0YXwNjFVmnkbHE3J/Lu8b3EBrdNSSAPNeO5KI1BudGhemu5Z21di/d34Tq8bxKPiOp7Upmuhp58SwBuJcP0EJIIDIYquJ8kpc1juZM17WFgyxXAeqh24onz8GnpY2OcZBygNBdrubbDf8AYE4U32fqGxVrJXOADTfJtpsPPovWvAP8UHti7vfb7WYr2udoGDzcJcQYjNTcL8H1WHwNrqynnnLKbEZpYYxJQ0EYc1/NlzyTRtIjieCJBwn+Od2JcRdnHE/DGIQ8RnHODqmeopKmioKMUeE4Njn304hjBdmMsTg4TSvkmdynh0hADRzDtA7Eeyrt846xziN3ee4Wp8Y4krpa6qZxBwfjVCTJK4lwMtpgQL2BLibAeS65279qfFvH3ce4t4CquP8Au08Z8N8M09LWirpccqY8frailAy1dJFKAZZ3tBY5pbYiRwAF1zGk4RBw7ilLXULA04bK0xOibY2aC3mYLubc3N+Z19Q2zRbJq+WppZKad1xq084ebjJvZxwbDyHS+V88JHCnBGheU3KLgO2cpU8HIdmdYuOwUcQkgvOtui7ORhUxrhqmy5r2eLcJl15jro0J90fMbmFrjcJDWcwZSbH0Qw0o4N8hMPBkGVos0JEjhA0NA9z5qRK3KLN36lJMYh0dqT6LzWlGY4KM5mmZl/X0WHNEwuLBwT7ouUbt2KaewDxM+fRFATDXJkQZgXOvYfqkvlDnkEWb0TpcZXD08kjk812XL7FbNvfCO0ph7jE+27SN1b8FYh/duJjpHNpqdz0UGSFsTMg8bvTYJqWcUzgS67wbi3RbTU7ZYnRvOq2mYJozGd13vgjHLBlyt4raV2K0bKumF6uAatH/AHW+XuOi4hwJxIJ4Yng76EeR6rrvBnEAOTxKqw5BY/ULknFKeWln72PUf6y3Ls97QSwsBkOnrZdPxKlwbtc4NqsBx6ljrsNr2ZXxu0LT0ew7tcDqCNlxLHsCdG92KUA/11EQ/V7f+R8q+4F47tk8fsmowQ4EGzhkEfUIckcdUwVNPgj5g/7Qryp3oO6zi/dz4p8HMr+H61xNDXNbo8fgfbRsgG467jTbm1DiOW1vn1X1CE2F9ovC1Tg+M00Vfh1fHy5oJBcOHQg7gg6gjUHZeMO9f3I8R7F5psdwAT4rwvI7MZLXloLnRs1tx5SAWPWx37J2T7ZictpK08sugOzv6d5aHborjwLtK2e1LW4k0B2d91x+OrBsQSClVtBT4tHmeMkwH1tGp9/NUtNVmInNmDm7g7hWEFaC299F0mWCGrj7uVoI6FW9vPE4PjNiqnEsImonXkaCzo4bH+iiPaXkAaBbhDOyrhyutbyIuCqzEuHWvbelIA/ATv7FUHivZKWEmSj9pvTcenX6+qsdBxlriGT4PXb7KgOVp6GyS+Kzsw2KkzUxppCx7S1w3BSeUYz6FVPu3NNnaqzRyA5CjmAPBI39FjkW1IPynywtF2hZMPM9bI7G5TbHnZRsmYa2shsZbcH6SpJYCLW2WHNBAHTRMsATUZJFymQwAWtol8oMALdk62MA7A3TrIwz1v0TLGplpwo7qe9j9JKE+WblyEVGa02V04eIJyLR4QhIDZRMOoUhn1tUlw0b7lCFgqWg2S4dvkpgG8r/AP7yQhI1/u0vx/4Vvr/BUuj+9+Fc4aBce4QhVKpVRbqtfxsl2MT3JPjKQhCs9L7pvoFoNSpNFq9qmt1n+EITA0Kbh1CeqNwOllOo/uR8IQo6q1Kq3Ffinev8KxwwAlyuMM2+ChChZ1G9VUwOL6kFxJJOt/dT5XESCxKEK3xbKvzbqww15D9z+am1oFm6dUIRHbKMl8Sp8VaBK3QahVs2gKEJV+qMzwhDNacg6jKUzTi+YHUaoQk3aLzVFf8Aej5UWp0qTbTZCFFSaJhYqfqCYjH/AFCEJWRZZ4Ul+so90t0roJ4nsc5jwdHNNiEIWGeILDtCuhVrB/KMNhcxgnTdQHtApzYAXuhCsb9lCR6KGzwl1tFDMbZJMzmhzgbgkXIQhJHVOx7qLXD7Q+6iRblCEm5OjwpB0nFvVN1QtJ8IQhIseqZdsU4BenHohC8jhNj6HDookH3yELyajSRpL8p6qGWJltLjX1QhEi8SKFElNnn2UKM5qjXVCFl+ybh0WzdnryHSi5sJBbX0XX+DXnKzU/mhCrEnxT/X+Fz7tR713+2XU+FnEhtyTstWjAg4or2MGRjKhwa1ugAv0CEJh3iCqfZ73k3oPqumcESuJb4nfmut8Kxtq4GxStEsUoyPY8ZmvaRYgg7gjohCxVbJfifjXyr7ZaOHDu0PGIaeKOCKKvmYxkbQ1rGh5sABoAPJUdASR8IQvqWh0HoPoF3Gn9w30VjFoVMg+v4QhSrlh2ij8SRtdhWYtBcHaEjUKhbrDr5IQuX9p/jj6BXDgfw49ViLf4WBpL8oQoJuisUaxIPG5YP1oQis1TkXhSoPqPsnG6vQhMs0TLNEf5vhCEIiYZov/9k="
LINE_IMAGE_FILENAME = "rize_line.jpg"
line_message_counters = {}
ADMIN_IDS = [875161402476736603] 
PER_DEVS = [875161402476736603]

client_ai = genai.Client(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
active_giveaways = {}
active_roulettes = {}

# ==============================================================================
# 💾 2. قاعدة البيانات ودوال النظام
# ==============================================================================
DATA_FILE = "economy.json"
RUNTIME_FILE = "runtime.json"
DEFAULT_INITIAL_BUDGET = 0


def _default_runtime():
    return {"version": 1, "active_giveaways": {}, "active_roulettes": {}, "pending_winner_checks": {}}


def load_runtime():
    data = _default_runtime()
    if os.path.exists(RUNTIME_FILE):
        try:
            with open(RUNTIME_FILE, "r", encoding="utf-8") as file:
                stored = json.load(file)
            if isinstance(stored, dict):
                data.update(stored)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"⚠️ تعذر قراءة {RUNTIME_FILE}: {exc}")
    return data


def save_runtime(data):
    temp = f"{RUNTIME_FILE}.tmp"
    with open(temp, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        file.flush()
        os.fsync(file.fileno())
    os.replace(temp, RUNTIME_FILE)


def set_runtime_giveaway(message_id, payload):
    data = load_runtime()
    data.setdefault("active_giveaways", {})[str(message_id)] = payload
    save_runtime(data)


def remove_runtime_giveaway(message_id):
    data = load_runtime()
    data.setdefault("active_giveaways", {}).pop(str(message_id), None)
    save_runtime(data)


def _default_data():
    return {
        "users": {}, "guilds": {}, "blacklist": {}, "transfers": [],
        "exchanges": {}, "custom_replies": {}, "game_controllers": {},
        "admin_controllers": {}, "per_controllers": {}, "server_branding": {}
    }


def load_data():
    data = _default_data()
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                data.update(loaded)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"⚠️ تعذر قراءة {DATA_FILE}: {exc}")
    return data


def save_data(data):
    """حفظ ذري يقلل احتمال تلف الملف إذا توقفت الاستضافة أثناء الكتابة."""
    temp_file = f"{DATA_FILE}.tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp_file, DATA_FILE)

def log_transfer(sender_id, receiver_id, amount):
    data = load_data()
    if "transfers" not in data:
        data["transfers"] = []
    data["transfers"].append({
        "sender": str(sender_id),
        "receiver": str(receiver_id),
        "amount": amount,
        "date": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    })
    save_data(data)

def get_user_transfers(user_id):
    data = load_data()
    transfers = data.get("transfers", [])
    user_str = str(user_id)
    return [t for t in transfers if t.get("sender") == user_str]

def get_balance(user_id):
    data = load_data()
    return data.get("users", {}).get(str(user_id), {}).get("balance", 0)

def update_balance(user_id, amount):
    data = load_data()
    if "users" not in data: data["users"] = {}
    uid = str(user_id)
    if uid not in data["users"]:
        data["users"][uid] = {"balance": 0}
    new_bal = data["users"][uid]["balance"] + amount
    if new_bal < 0:
        new_bal = 0
    data["users"][uid]["balance"] = new_bal
    save_data(data)

def set_balance(user_id, amount):
    data = load_data()
    if "users" not in data: data["users"] = {}
    uid = str(user_id)
    if uid not in data["users"]:
        data["users"][uid] = {"balance": 0}
    data["users"][uid]["balance"] = max(0, amount)
    save_data(data)

def get_guild_budget(guild_id):
    data = load_data()
    gid = str(guild_id)
    if gid not in data.get("guilds", {}):
        if "guilds" not in data: data["guilds"] = {}
        data["guilds"][gid] = {"budget": DEFAULT_INITIAL_BUDGET, "coin_name": "Rize"}
        save_data(data)
        return DEFAULT_INITIAL_BUDGET
    return data["guilds"][gid].get("budget", DEFAULT_INITIAL_BUDGET)

def update_guild_budget(guild_id, amount):
    data = load_data()
    if "guilds" not in data: data["guilds"] = {}
    gid = str(guild_id)
    if gid not in data["guilds"]:
        data["guilds"][gid] = {"budget": DEFAULT_INITIAL_BUDGET, "coin_name": "Rize"}
    new_b = data["guilds"][gid].get("budget", DEFAULT_INITIAL_BUDGET) + amount
    if new_b < 0:
        new_b = 0
    data["guilds"][gid]["budget"] = new_b
    save_data(data)

def set_guild_budget(guild_id, amount):
    data = load_data()
    if "guilds" not in data: data["guilds"] = {}
    gid = str(guild_id)
    if gid not in data["guilds"]:
        data["guilds"][gid] = {"budget": 0, "coin_name": "Rize"}
    data["guilds"][gid]["budget"] = max(0, amount)
    save_data(data)

def get_guild_coin(guild_id):
    if not guild_id: return "Rize"
    data = load_data()
    return data.get("guilds", {}).get(str(guild_id), {}).get("coin_name", "Rize")

def set_guild_coin(guild_id, coin_name):
    data = load_data()
    gid = str(guild_id)
    if "guilds" not in data: data["guilds"] = {}
    if gid not in data["guilds"]: data["guilds"][gid] = {"budget": 0}
    data["guilds"][gid]["coin_name"] = coin_name
    save_data(data)

def get_exchange_rooms(guild_id):
    data = load_data()
    gid = str(guild_id)
    gdata = data.get("guilds", {}).get(gid, {})
    return gdata.get("exchange_room"), gdata.get("delivery_room")

def set_exchange_room(guild_id, channel_id):
    data = load_data()
    gid = str(guild_id)
    if "guilds" not in data: data["guilds"] = {}
    if gid not in data["guilds"]: data["guilds"][gid] = {"budget": 0, "coin_name": "Rize"}
    data["guilds"][gid]["exchange_room"] = channel_id
    save_data(data)

def set_delivery_room(guild_id, channel_id):
    data = load_data()
    gid = str(guild_id)
    if "guilds" not in data: data["guilds"] = {}
    if gid not in data["guilds"]: data["guilds"][gid] = {"budget": 0, "coin_name": "Rize"}
    data["guilds"][gid]["delivery_room"] = channel_id
    save_data(data)

def _default_global_currencies():
    return {
        "adamc":{"rize_amount":5,"coin_amount":1,"status":True,"min_receive":0,"max_receive":None},
        "robux":{"rize_amount":10,"coin_amount":1,"status":True,"min_receive":0,"max_receive":None},
        "credit":{"rize_amount":1,"coin_amount":1,"status":True,"min_receive":0,"max_receive":None},
    }


def get_custom_currencies(guild_id=None):
    data=load_data()
    currencies=data.get("global_currencies")
    if not isinstance(currencies,dict) or not currencies:
        currencies=_default_global_currencies(); data["global_currencies"]=currencies; save_data(data)
    return currencies


def set_custom_currency(guild_id,currency_name,rize_amount,coin_amount):
    data=load_data(); currencies=data.setdefault("global_currencies",_default_global_currencies())
    name=currency_name.lower().strip(); previous=currencies.get(name,{})
    currencies[name]={"rize_amount":rize_amount,"coin_amount":coin_amount,"status":previous.get("status",True),
                      "min_receive":previous.get("min_receive",0),"max_receive":previous.get("max_receive")}
    save_data(data)


def set_currency_status(guild_id,currency_name,status):
    data=load_data(); currencies=data.setdefault("global_currencies",_default_global_currencies())
    name=currency_name.lower().strip()
    if name not in currencies: return False
    currencies[name]["status"]=bool(status); save_data(data); return True


def set_currency_limits(guild_id,currency_name,min_receive=0,max_receive=None):
    data=load_data(); currencies=data.setdefault("global_currencies",_default_global_currencies())
    name=currency_name.lower().strip()
    if name not in currencies: return False
    currencies[name]["min_receive"]=min_receive; currencies[name]["max_receive"]=max_receive; save_data(data); return True


def exchange_system_enabled():
    return bool(load_data().get("exchange_system_enabled",True))


def set_exchange_system_enabled(enabled):
    data=load_data(); data["exchange_system_enabled"]=bool(enabled); save_data(data)


def save_exchange_request(req_id, req_data):
    data = load_data()
    if "exchanges" not in data: data["exchanges"] = {}
    data["exchanges"][str(req_id)] = req_data
    save_data(data)

def get_exchange_request(req_id):
    data = load_data()
    return data.get("exchanges", {}).get(str(req_id))

def update_exchange_status(req_id, status):
    data = load_data()
    if "exchanges" in data and str(req_id) in data["exchanges"]:
        data["exchanges"][str(req_id)]["status"] = status
        save_data(data)

def get_next_exchange_id():
    data = load_data()
    exchanges = data.get("exchanges", {})
    if not exchanges: return 1
    return max([int(k) for k in exchanges.keys()]) + 1

def blacklist_role_status(user_id):
    guild=bot.get_guild(MAIN_GUILD_ID) if bot.is_ready() else None
    if not guild:
        return "السيرفر الأساسي غير متاح"
    member=guild.get_member(int(user_id))
    if not member:
        return "العضو غير موجود في السيرفر الأساسي"
    return "معه رتبة البلاك ليست" if any(role.id==BLACKLIST_ROLE_ID for role in member.roles) else "بدون رتبة البلاك ليست"


async def sync_blacklist_role(user_id, add=True):
    guild=bot.get_guild(MAIN_GUILD_ID)
    if not guild:
        return False,"السيرفر الأساسي غير متاح"
    member=guild.get_member(int(user_id))
    if not member:
        return False,"العضو غير موجود حالياً في السيرفر الأساسي، وسيأخذ الرتبة فور دخوله"
    role=guild.get_role(BLACKLIST_ROLE_ID)
    if not role:
        return False,"رتبة البلاك ليست غير موجودة أو البوت لا يراها"
    try:
        if add and role not in member.roles: await member.add_roles(role,reason="Rize blacklist sync")
        if not add and role in member.roles: await member.remove_roles(role,reason="Rize blacklist removed")
        return True,"تمت مزامنة الرتبة"
    except Exception as exc:
        return False,f"تعذر تعديل الرتبة: {type(exc).__name__}"


def is_blacklisted(user_id):
    data = load_data()
    bl = data.get("blacklist", {})
    return str(user_id) in bl and bl[str(user_id)].get("active", True)

def member_is_fully_blacklisted(member):
    return bool(member) and (is_blacklisted(member.id) or user_has_blacklist_role(member))


async def blacklist_message_for_guild(guild):
    if guild and guild.id==SUPPORT_GUILD_ID:
        return "🚫 أنت في البلاك ليست. الرجاء التواصل مع الدعم الفني داخل هذا السيرفر."
    invite=await get_support_invite()
    return "🚫 أنت في البلاك ليست. الرجاء التواصل مع سيرفر الدعم" + (f": {invite}" if invite else ".")


def add_to_blacklist(user_id, reason, admin_id):
    data = load_data()
    if "blacklist" not in data: data["blacklist"] = {}
    data["blacklist"][str(user_id)] = {
        "active": True,
        "reason": reason,
        "admin": admin_id,
        "date": str(datetime.date.today())
    }
    save_data(data)

def remove_from_blacklist(user_id, reason, admin_id):
    data = load_data()
    if "blacklist" not in data: data["blacklist"] = {}
    uid = str(user_id)
    if uid in data["blacklist"]:
        data["blacklist"][uid]["active"] = False
        data["blacklist"][uid]["remove_reason"] = reason
        data["blacklist"][uid]["removed_by"] = admin_id
        data.setdefault("role_blacklisted_users", {}).pop(str(user_id), None)
    save_data(data)

def get_blacklist_roles():
    return load_data().get("blacklist_roles", {})


def user_has_blacklist_role(member):
    if not member:
        return False
    data=load_data()
    if str(member.id) in data.get("role_blacklisted_users",{}):
        return True
    blocked_ids={int(role_id) for role_id in data.get("blacklist_roles",{}).keys()}
    matched=next((role for role in getattr(member,"roles",[]) if role.id in blocked_ids),None)
    if matched:
        data.setdefault("role_blacklisted_users",{})[str(member.id)]={
            "role_id":matched.id,"role_name":matched.name,"detected_guild":member.guild.id
        }
        save_data(data)
        return True
    return False


def blacklist_role_reason(member):
    roles=get_blacklist_roles()
    for role in getattr(member,"roles",[]):
        if str(role.id) in roles:
            return roles[str(role.id)].get("reason","رتبة محظورة")
    return None


async def get_support_invite():
    guild=bot.get_guild(SUPPORT_GUILD_ID)
    if not guild:
        return None
    channel=next((ch for ch in guild.text_channels if ch.permissions_for(guild.me).create_instant_invite),None)
    if not channel:
        return None
    try:
        invite=await channel.create_invite(max_age=86400,max_uses=0,unique=False,reason="Rize support link")
        return invite.url
    except Exception:
        return None


async def send_role_blacklist_notice(destination, member):
    invite=await get_support_invite()
    text=(f"🚫 {member.mention} لا يمكنك استخدام البوت لأن لديك رتبة ضمن القائمة السوداء العامة.\n"
          f"السبب: {blacklist_role_reason(member) or 'رتبة محظورة'}\n"
          "رجاء تواصل مع سيرفر الدعم" + (f": {invite}" if invite else "."))
    await destination.send(text)


def _controller_entries(data, key, guild_id):
    value = data.get(key, {}).get(str(guild_id), [])
    if isinstance(value, dict):
        return [value]
    return value if isinstance(value, list) else []


def _matches_controller(user_id, guild, key):
    if not guild:
        return False
    member = guild.get_member(user_id)
    for controller in _controller_entries(load_data(), key, guild.id):
        if controller.get("type") == "user" and controller.get("id") == user_id:
            return True
        if controller.get("type") == "role" and member:
            if any(role.id == controller.get("id") for role in member.roles):
                return True
    return False


def is_owner(user_id):
    if is_blacklisted(user_id):
        return False
    return user_id == PRIMARY_OWNER_ID


def has_native_staff_permission(user_id,guild=None):
    if not guild: return False
    member=guild.get_member(user_id)
    if not member: return False
    perms=member.guild_permissions
    return member.id==guild.owner_id or perms.administrator or perms.manage_guild


def is_per_controller(user_id, guild=None):
    if is_blacklisted(user_id) or (guild and user_has_blacklist_role(guild.get_member(user_id))):
        return False
    return is_owner(user_id) or _matches_controller(user_id, guild, "per_controllers")


def is_admin(user_id, guild=None):
    if is_blacklisted(user_id) or (guild and user_has_blacklist_role(guild.get_member(user_id))):
        return False
    if is_owner(user_id) or user_id in ADMIN_IDS or is_per_controller(user_id,guild) or has_native_staff_permission(user_id,guild):
        return True
    if _matches_controller(user_id, guild, "admin_controllers"):
        return True
    if guild:
        data = load_data()
        admin_role_id = data.get("guilds", {}).get(str(guild.id), {}).get("admin_role")
        member = guild.get_member(user_id)
        if admin_role_id and member and any(role.id == admin_role_id for role in member.roles):
            return True
    return False


def is_games_controller(user_id, guild=None):
    if is_blacklisted(user_id) or (guild and user_has_blacklist_role(guild.get_member(user_id))):
        return False
    if has_native_staff_permission(user_id,guild):
        return True
    return is_admin(user_id, guild) or _matches_controller(user_id, guild, "game_controllers")


def _set_controller(guild_id, key, target_type, target_id, target_name):
    data = load_data()
    controllers = data.setdefault(key, {})
    gid = str(guild_id)
    current = controllers.get(gid, [])
    if isinstance(current, dict):
        current = [current]
    current = [item for item in current if not (
        item.get("type") == target_type and item.get("id") == target_id
    )]
    current.append({"type": target_type, "id": target_id, "name": target_name})
    controllers[gid] = current
    save_data(data)


def _remove_controller(guild_id, key, target_id):
    data = load_data()
    controllers = data.setdefault(key, {})
    gid = str(guild_id)
    current = controllers.get(gid, [])
    if isinstance(current, dict):
        current = [current]
    updated = [item for item in current if item.get("id") != target_id]
    removed = len(updated) != len(current)
    controllers[gid] = updated
    save_data(data)
    return removed

def parse_number(val) -> Optional[int]:
    if isinstance(val, int): return val
    val_str = str(val).lower().strip()
    match = re.match(r"^([\d\.]+)([kmb]?)$", val_str)
    if not match: return None
    num_part, unit = match.groups()
    try: num = float(num_part)
    except ValueError: return None
    if unit == 'k': num *= 1_000
    elif unit == 'm': num *= 1_000_000
    elif unit == 'b': num *= 1_000_000_000
    return int(num)

def parse_decimal_amount(value):
    """مبالغ تدعم الكسور والاختصارات، مثل 0.2 و 1.5k."""
    text = str(value).strip().lower().replace(",", "")
    match = re.fullmatch(r"(\d+(?:\.\d+)?)([kmb]?)", text)
    if not match:
        return None
    number = float(match.group(1))
    unit = match.group(2)
    if unit == "k": number *= 1_000
    elif unit == "m": number *= 1_000_000
    elif unit == "b": number *= 1_000_000_000
    return int(number) if number.is_integer() else round(number, 8)


def format_amount(value):
    if isinstance(value, float) and not value.is_integer():
        return f"{value:,.8f}".rstrip("0").rstrip(".")
    return f"{int(value):,}"



def code_number(value):
    """Only large values (one million or more) are copyable inline code."""
    try:
        numeric=float(value)
    except Exception:
        return str(value)
    text=format_amount(value)
    return f"`{text}`" if abs(numeric)>=1_000_000 else text


def code_id(value):
    """Discord IDs are copyable code with no thousands separators."""
    return f"`{int(value)}`"


def smart_number(value, force_copy=False):
    """Balances and values >= 1,000,000 are easy to copy; smaller numbers stay plain."""
    try:
        numeric=float(value)
    except Exception:
        return str(value)
    text=format_amount(value)
    return f"`{text}`" if force_copy or abs(numeric) >= 1_000_000 else text

def get_spin_multiplier():
    data = load_data()
    until = float(data.get("spin_double_until", 0) or 0)
    now = datetime.datetime.now(datetime.timezone.utc).timestamp()
    return 2 if until > now else 1


def get_spin_double_until():
    return float(load_data().get("spin_double_until", 0) or 0)


def set_spin_double_until(timestamp):
    data = load_data()
    data["spin_double_until"] = float(timestamp)
    save_data(data)


async def finish_double_spin_at(end_timestamp, channel_id=None):
    remaining = float(end_timestamp) - datetime.datetime.now(datetime.timezone.utc).timestamp()
    if remaining > 0:
        await asyncio.sleep(remaining)
    # لا ننهي فترة أحدث تم تشغيلها بعد هذه المهمة.
    if get_spin_double_until() <= float(end_timestamp) + 0.01:
        set_spin_double_until(0)
        channel = bot.get_channel(channel_id) if channel_id else None
        if channel:
            await channel.send("✅ تم انتهاء فترة الدبل الخاصة ببوت الإسبن. رجعت الجوائز للوضع الطبيعي.")


async def handle_spin_bot_reward(message):
    """يقبل فقط !rize @user amount من بوت الإسبن المحدد، ويخصم من ميزانية السيرفر."""
    if message.author.id != SPIN_BOT_ID or not message.guild:
        return False
    match = re.fullmatch(r"!rize\s+<@!?(\d+)>\s+([\d.,]+[kmb]?)", message.content.strip(), re.IGNORECASE)
    if not match:
        return False
    user_id = int(match.group(1))
    amount = parse_decimal_amount(match.group(2))
    if amount is None or amount <= 0:
        await message.channel.send("❌ أمر بوت الإسبن غير صحيح. استخدم: `!rize @user amount`")
        return True
    multiplier = get_spin_multiplier()
    final_amount = amount * multiplier
    budget = get_guild_budget(message.guild.id)
    if budget < final_amount:
        await message.channel.send(
            f"❌ ميزانية السيرفر لا تكفي. المطلوب `{format_amount(final_amount)}` Rize والمتاح `{format_amount(budget)}` Rize."
        )
        return True
    member = message.guild.get_member(user_id)
    if member is None:
        try: member = await message.guild.fetch_member(user_id)
        except Exception:
            await message.channel.send("❌ العضو المحدد غير موجود في السيرفر.")
            return True
    before = get_balance(member.id)
    update_guild_budget(message.guild.id, -final_amount)
    update_balance(member.id, final_amount)
    after = get_balance(member.id)
    note = " (**مضاعفة 2× فعالة!** 🔥)" if multiplier == 2 else ""
    await message.channel.send(
        f"✅ (عجلة الحظ) تمت إضافة `{format_amount(final_amount)}` Rize إلى رصيد {member.mention}.{note}"
    )
    try:
        await member.send(
            f"✅ (عجلة الحظ) تمت إضافة `{format_amount(final_amount)}` Rize إلى رصيدك."
            + (" مضاعفة 2× فعالة! 🔥" if multiplier == 2 else "")
            + f"\nالرصيد قبل: `{format_amount(before)}` Rize"
            + f"\nالرصيد بعد: `{format_amount(after)}` Rize"
        )
    except Exception: pass
    return True


def parse_time(time_str: str) -> int:
    match = re.match(r"^(\d+)([smhdw])$", time_str.lower())
    if not match: return 0
    amount, unit = match.groups()
    amount = int(amount)
    if unit == 's': return amount
    if unit == 'm': return amount * 60
    if unit == 'h': return amount * 3600
    if unit == 'd': return amount * 86400
    if unit == 'w': return amount * 604800
    return 0

def get_line_settings(guild_id):
    data = load_data()
    guild_data = data.get("guilds", {}).get(str(guild_id), {})
    rooms = guild_data.get("line_rooms")
    if isinstance(rooms, dict):
        return rooms
    # ترقية الإعداد القديم ذي الروم الواحدة تلقائياً.
    old = guild_data.get("line_settings", {})
    if old.get("channel_id"):
        return {
            str(old["channel_id"]): {
                "every_messages": int(old.get("every_messages", 1)),
                "enabled": bool(old.get("enabled", True)),
                "current_count": int(old.get("current_count", 0)),
            }
        }
    return {}


def get_line_image_b64(guild_id):
    data = load_data()
    return data.get("guilds", {}).get(str(guild_id), {}).get("line_image_b64")


def set_line_settings(guild_id, channel_ids, every_messages):
    data = load_data()
    guild_data = data.setdefault("guilds", {}).setdefault(
        str(guild_id), {"budget": DEFAULT_INITIAL_BUDGET, "coin_name": "Rize"}
    )
    # نقل الصورة القديمة المخصصة إلى الحقل الجديد إن وجدت.
    old = guild_data.pop("line_settings", {})
    if old.get("image_b64") and not guild_data.get("line_image_b64"):
        guild_data["line_image_b64"] = old["image_b64"]
    rooms = guild_data.setdefault("line_rooms", {})
    for channel_id in channel_ids:
        rooms[str(int(channel_id))] = {
            "every_messages": int(every_messages),
            "enabled": True,
            "current_count": 0,
        }
    save_data(data)


def remove_line_settings(guild_id, channel_id=None):
    data = load_data()
    guild_data = data.setdefault("guilds", {}).setdefault(str(guild_id), {})
    rooms = guild_data.setdefault("line_rooms", {})
    if channel_id is None:
        removed = bool(rooms or guild_data.pop("line_settings", None))
        rooms.clear()
        for key in list(line_message_counters):
            if isinstance(key, tuple) and key[0] == int(guild_id):
                line_message_counters.pop(key, None)
    else:
        removed = rooms.pop(str(int(channel_id)), None) is not None
        line_message_counters.pop((int(guild_id), int(channel_id)), None)
    save_data(data)
    return removed


def build_line_file(guild_id=None):
    custom_b64 = None
    if guild_id:
        custom_b64 = get_line_image_b64(guild_id)
    raw = base64.b64decode(custom_b64 or LINE_IMAGE_B64)
    return discord.File(io.BytesIO(raw), filename=LINE_IMAGE_FILENAME)


async def send_rize_line(channel):
    await channel.send(file=build_line_file(channel.guild.id))


async def process_auto_line_message(message):
    """Count every message, including bot messages, except the Rize line image itself."""
    if not message.guild:
        return
    # Prevent recursion: the line message sent by this bot must not count as a new message.
    if message.author.id == bot.user.id and any(
        attachment.filename == LINE_IMAGE_FILENAME for attachment in message.attachments
    ):
        return

    rooms = get_line_settings(message.guild.id)
    room_settings = rooms.get(str(message.channel.id), {})
    if not room_settings.get("enabled"):
        return

    every_messages = max(1, int(room_settings.get("every_messages", 1)))
    counter_key = (message.guild.id, message.channel.id)
    current_count = line_message_counters.get(
        counter_key,
        int(room_settings.get("current_count", 0) or 0),
    ) + 1

    if current_count >= every_messages:
        try:
            await send_rize_line(message.channel)
            current_count = 0
        except Exception as exc:
            print(f"auto line send error in {message.guild.id}/{message.channel.id}: {exc!r}")

    line_message_counters[counter_key] = current_count
    data = load_data()
    guild_data = data.setdefault("guilds", {}).setdefault(str(message.guild.id), {})
    line_rooms = guild_data.setdefault("line_rooms", {})
    settings = line_rooms.setdefault(str(message.channel.id), {})
    settings.update({
        "enabled": True,
        "every_messages": every_messages,
        "current_count": current_count,
    })
    save_data(data)


def can_manage_premium(member,guild):
    if not member or not guild:
        return False
    return is_owner(member.id) or member.id==guild.owner_id or member.guild_permissions.administrator


def premium_required_message():
    return "💎 هذا السيرفر يحتاج اشتراك Premium فعال لاستخدام هذه الخاصية."


def premium_info(guild_id):
    info=load_data().get("premium_guilds",{}).get(str(guild_id))
    if not info: return None
    if float(info.get("end_timestamp",0))<=datetime.datetime.now(datetime.timezone.utc).timestamp():
        return None
    return info


def is_premium_guild(guild_id): return premium_info(guild_id) is not None


def require_premium_text(): return "💎 هذه الخاصية متاحة لسيرفرات Premium فقط. استخدم `/active_premium` لتفعيل الاشتراك."


def create_premium_code(duration_seconds,creator_id):
    alphabet=string.ascii_uppercase+string.digits
    code=''.join(secrets.choice(alphabet) for _ in range(14))
    data=load_data(); data.setdefault("premium_codes",{})[code]={"duration":int(duration_seconds),"creator":creator_id,"used":False}
    save_data(data); return code


def update_premium_usage(guild_id,**changes):
    data=load_data(); info=data.setdefault("premium_guilds",{}).setdefault(str(guild_id),{})
    usage=info.setdefault("usage",{})
    usage.update(changes); save_data(data)


async def expire_premium_guild(guild_id):
    data=load_data(); info=data.get("premium_guilds",{}).get(str(guild_id))
    if not info or info.get("expired_cleaned"):
        return
    usage=info.get("usage",{})
    guild=bot.get_guild(int(guild_id))
    # Remove premium customizations when the subscription expires.
    if guild:
        try:
            if usage.get("custom_name") and guild.me:
                await guild.me.edit(nick=None,reason="Rize Premium expired")
        except Exception as exc: print(f"premium nickname reset error: {exc!r}")
        try:
            if usage.get("custom_avatar") or usage.get("custom_banner"):
                payload={}
                if usage.get("custom_avatar"): payload["avatar"]=None
                if usage.get("custom_banner"): payload["banner"]=None
                if payload: await modify_current_guild_profile(guild.id,**payload)
        except Exception as exc: print(f"premium profile reset error: {exc!r}")
    if usage.get("custom_currency"):
        set_guild_coin(int(guild_id),"Rize")
    if usage.get("custom_line"):
        data=load_data(); data.setdefault("guilds",{}).setdefault(str(guild_id),{}).pop("line_image_b64",None); save_data(data)
    info["expired_cleaned"]=True; info["usage"]={}; save_data(data)


async def cleanup_expired_premium():
    now=datetime.datetime.now(datetime.timezone.utc).timestamp()
    data=load_data()
    expired=[gid for gid,info in data.get("premium_guilds",{}).items() if float(info.get("end_timestamp",0))<=now and not info.get("expired_cleaned")]
    for gid in expired:
        await expire_premium_guild(int(gid))


# ==============================================================================
# 🔐 نظام صلاحيات الأقسام المحفوظة
# ==============================================================================
async def _set_controller_command(interaction, key, label, member=None, role=None):
    if not is_owner(interaction.user.id):
        return await interaction.response.send_message("❌ هذا الأمر للمالك الرئيسي فقط.", ephemeral=True)
    if bool(member) == bool(role):
        return await interaction.response.send_message("❌ اختر عضواً واحداً أو رتبة واحدة فقط.", ephemeral=True)
    target = member or role
    target_type = "user" if member else "role"
    target_name = member.display_name if member else role.name
    _set_controller(interaction.guild.id, key, target_type, target.id, target_name)
    await interaction.response.send_message(f"✅ تمت إضافة {target.mention} إلى صلاحيات {label}.")


@bot.tree.command(name="set_per", description="إضافة عضو أو رتبة لصلاحيات المالك المساعدة")
async def set_per(interaction: discord.Interaction, member: Optional[discord.Member] = None, role: Optional[discord.Role] = None):
    await _set_controller_command(interaction, "per_controllers", "المالك المساعد", member, role)


@bot.tree.command(name="remove_controller", description="حذف عضو أو رتبة من صلاحيات قسم")
@app_commands.choices(section=[
    app_commands.Choice(name="الألعاب", value="game_controllers"),
    app_commands.Choice(name="الإدارة", value="admin_controllers"),
    app_commands.Choice(name="المالك المساعد", value="per_controllers")
])
async def remove_controller(interaction: discord.Interaction, section: app_commands.Choice[str], target_id: str):
    if not is_owner(interaction.user.id):
        return await interaction.response.send_message("❌ هذا الأمر للمالك الرئيسي فقط.", ephemeral=True)
    try:
        value = int(target_id)
    except ValueError:
        return await interaction.response.send_message("❌ اكتب ID صحيحاً.", ephemeral=True)
    removed = _remove_controller(interaction.guild.id, section.value, value)
    await interaction.response.send_message("✅ تم الحذف." if removed else "❌ لم يتم العثور على هذا العضو أو الرتبة.", ephemeral=True)


@bot.tree.command(name="show_controllers", description="عرض صلاحيات الألعاب والإدارة والمالك في السيرفر")
async def show_controllers(interaction: discord.Interaction):
    if not is_owner(interaction.user.id):
        return await interaction.response.send_message("❌ هذا الأمر للمالك الرئيسي فقط.", ephemeral=True)
    data = load_data()
    sections = [
        ("🎮 الألعاب", "game_controllers"),
        ("🛡️ الإدارة", "admin_controllers"),
        ("👑 المالك المساعد", "per_controllers")
    ]
    embed = discord.Embed(title="🔐 صلاحيات التحكم", color=discord.Color.blurple())
    for title, key in sections:
        entries = _controller_entries(data, key, interaction.guild.id)
        lines = []
        for item in entries:
            mention = f"<@{item['id']}>" if item.get("type") == "user" else f"<@&{item['id']}>"
            lines.append(f"• {mention} • `{item.get('id')}`")
        embed.add_field(name=title, value="\n".join(lines) if lines else "لا يوجد", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)


# ==============================================================================
# 🎨 3. دالة كابتشا احترافية وعصرية (خلفية مظلمة، ألوان زاهية، تداخل وتصميم فخم)
# ==============================================================================
def _captcha_font(size: int):
    """اختيار خط واضح يعمل على استضافات Linux وعلى Windows."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        "arialbd.ttf",
        "arial.ttf",
    ]
    for font_path in candidates:
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def generate_captcha_image(code: str) -> io.BytesIO:
    """كابتشا Rize واضحة، متباعدة، ومتوافقة مع الاستضافة."""
    width, height = 600, 230
    image = Image.new("RGB", (width, height), (10, 14, 24))
    draw = ImageDraw.Draw(image)

    # خلفية متدرجة داكنة.
    for y in range(height):
        ratio = y / max(height - 1, 1)
        color = (
            int(10 + 14 * ratio),
            int(14 + 25 * ratio),
            int(24 + 42 * ratio),
        )
        draw.line((0, y, width, y), fill=color)

    # زخارف خلفية خفيفة لا تغطي الأرقام.
    for _ in range(14):
        x = random.randint(-40, width - 20)
        y = random.randint(-40, height - 20)
        radius = random.randint(18, 55)
        draw.ellipse(
            (x, y, x + radius, y + radius),
            outline=random.choice([(20, 70, 105), (42, 58, 112), (28, 92, 82), (79, 48, 103)]),
            width=random.randint(1, 3),
        )

    font = _captcha_font(122)
    colors = [(74, 218, 255), (75, 235, 170), (204, 132, 255), (255, 201, 91)]

    # مسافة كبيرة وواضحة بين الأرقام الأربعة.
    slot_width = 125
    left = (width - slot_width * len(code)) // 2

    for index, char in enumerate(code):
        char_layer = Image.new("RGBA", (145, 175), (0, 0, 0, 0))
        char_draw = ImageDraw.Draw(char_layer)
        color = colors[index % len(colors)]

        # ظل ثم رقم بحد أبيض خفيف لزيادة الوضوح.
        char_draw.text((22, 7), char, font=font, fill=(0, 0, 0, 150), stroke_width=3)
        char_draw.text(
            (15, 0), char, font=font, fill=color + (255,),
            stroke_width=2, stroke_fill=(240, 248, 255, 225)
        )

        char_layer = char_layer.rotate(
            random.randint(-11, 11),
            resample=Image.Resampling.BICUBIC,
            expand=False,
        )
        image.paste(
            char_layer,
            (left + index * slot_width - 7, random.randint(24, 36)),
            char_layer,
        )

    draw = ImageDraw.Draw(image)

    # خطوط موجية محدودة، لا تحجب الرقم بالكامل.
    for _ in range(2):
        base_y = random.randint(72, 165)
        phase = random.randint(0, 80)
        points = []
        for x in range(-20, width + 21, 20):
            wave_y = base_y + int(11 * math.sin((x + phase) / 38))
            points.append((x, wave_y))
        draw.line(
            points,
            fill=random.choice([(80, 192, 232), (96, 210, 163), (181, 121, 224)]),
            width=2,
        )

    # نقاط خفيفة خارجية لصد القراءة الآلية من دون إزعاج المستخدم.
    for _ in range(170):
        x, y = random.randrange(width), random.randrange(height)
        draw.point((x, y), fill=random.choice([(78, 110, 136), (70, 131, 148), (104, 92, 146)]))

    # إطار Rize احترافي.
    draw.rounded_rectangle((3, 3, width - 4, height - 4), radius=24, outline=(58, 174, 228), width=4)
    draw.rounded_rectangle((12, 12, width - 13, height - 13), radius=18, outline=(39, 65, 92), width=2)

    buffer = io.BytesIO()
    image.save(buffer, format="PNG", optimize=True)
    buffer.seek(0)
    return buffer

# ==============================================================================
# 🎨 4. دالة توليد صورة عجلة الحظ للروليت
# ==============================================================================
def create_wheel_image(players_names: List[str], center_avatar_bytes: bytes = None, selected_name: str = None) -> io.BytesIO:
    size=1080
    image=Image.new("RGBA",(size,size),(0,0,0,0))
    draw=ImageDraw.Draw(image)
    cx=cy=size//2; radius=440
    names=players_names or ["لا يوجد"]
    count=len(names); slice_angle=360/count
    colors=[(164,132,94,255),(101,145,101,255),(150,105,157,255),(151,151,143,255),(91,139,151,255),(157,126,92,255)]
    selected_index=names.index(selected_name) if selected_name in names else 0
    pointer_angle=180
    rotation=pointer_angle-(selected_index*slice_angle+slice_angle/2)
    font=_captcha_font(34 if count<=8 else 29 if count<=14 else 23)
    for index,name in enumerate(names):
        start=rotation+index*slice_angle; end=start+slice_angle
        draw.pieslice((cx-radius,cy-radius,cx+radius,cy+radius),start=start,end=end,fill=colors[index%len(colors)],outline=(255,255,255,255),width=5)
        mid=math.radians(start+slice_angle/2)
        tx=cx+radius*.68*math.cos(mid); ty=cy+radius*.68*math.sin(mid)
        label=name if len(name)<=16 else name[:15]+"…"
        draw.text((tx,ty),label,font=font,fill=(255,255,255,255),anchor="mm",stroke_width=1,stroke_fill=(70,70,70,255))
    center_radius=125
    if center_avatar_bytes:
        try:
            avatar=Image.open(io.BytesIO(center_avatar_bytes)).convert("RGBA").resize((center_radius*2,center_radius*2))
            mask=Image.new("L",avatar.size,0); ImageDraw.Draw(mask).ellipse((0,0,*avatar.size),fill=255)
            image.paste(avatar,(cx-center_radius,cy-center_radius),mask)
        except Exception: pass
    draw.ellipse((cx-center_radius,cy-center_radius,cx+center_radius,cy+center_radius),outline=(255,255,255,255),width=4)
    pa=math.radians(pointer_angle)
    tip=(cx+(radius+5)*math.cos(pa),cy+(radius+5)*math.sin(pa))
    base_x=cx+(radius+62)*math.cos(pa); base_y=cy+(radius+62)*math.sin(pa)
    t=math.radians(pointer_angle+90)
    p2=(base_x+22*math.cos(t),base_y+22*math.sin(t)); p3=(base_x-22*math.cos(t),base_y-22*math.sin(t))
    draw.polygon([tip,p2,p3],fill=(255,255,255,255))
    buffer=io.BytesIO(); image.save(buffer,format="PNG",optimize=True); buffer.seek(0); return buffer

# ==============================================================================
# 🚀 5. أحداث الفحص ومزامنة أوامر السلاش
# ==============================================================================
@bot.before_invoke
async def check_blacklist_before_command(ctx):
    if member_is_fully_blacklisted(ctx.author):
        set_balance(ctx.author.id,0)
        await ctx.send(await blacklist_message_for_guild(ctx.guild))
        raise commands.CommandError("User is blacklisted")

_restore_started = False


async def global_slash_check(interaction:discord.Interaction):
    if interaction.guild and member_is_fully_blacklisted(interaction.user):
        set_balance(interaction.user.id,0)
        if not interaction.response.is_done():
            await interaction.response.send_message(await blacklist_message_for_guild(interaction.guild),ephemeral=True)
        return False
    return True


bot.tree.interaction_check = global_slash_check


@bot.event
async def on_member_join(member):
    if member.guild.id==MAIN_GUILD_ID and is_blacklisted(member.id):
        set_balance(member.id,0)
        await sync_blacklist_role(member.id,True)
    if user_has_blacklist_role(member):
        set_balance(member.id,0)
        try: await member.send("🚫 تم التعرف على حظرك، ولذلك لا يمكنك استخدام بوت Rize.")
        except Exception: pass


@bot.event
async def on_ready():
    global _restore_started, PER_DEVS, ADMIN_IDS
    if not getattr(bot,"_premium_views_added",False):
        bot.add_view(PremiumStartView())
        bot.add_view(PremiumFinishPurchaseView())
        bot._premium_views_added=True
    await cleanup_expired_premium()
    print(f'✅ تم تسجيل الدخول بنجاح باسم البوت: {bot.user.name}')
    try:
        synced = await bot.tree.sync()
        print(f"⚡ تم مزامنة {len(synced)} أمر Slash Commands بنجاح!")
    except Exception as exc:
        print(f"Error syncing commands: {exc}")
    await bot.change_presence(activity=discord.Game(name="Rize • /help"))

    # استعادة المطورين المسجلين بصورة دائمة.
    saved_data = load_data()
    saved_devs = [int(uid) for uid in saved_data.get("per_devs", [])]
    saved_admins = [int(uid) for uid in saved_data.get("admin_ids", [])]
    PER_DEVS = list(dict.fromkeys([PRIMARY_OWNER_ID] + saved_devs))
    ADMIN_IDS = list(dict.fromkeys([PRIMARY_OWNER_ID] + saved_admins + saved_devs))
    for guild in bot.guilds:
        for member in guild.members:
            if user_has_blacklist_role(member):
                set_balance(member.id,0)
    main_guild=bot.get_guild(MAIN_GUILD_ID)
    if main_guild:
        for uid,info in load_data().get("blacklist",{}).items():
            if info.get("active",True):
                await sync_blacklist_role(int(uid),True)

    if not _restore_started:
        _restore_started = True
        await restore_active_giveaways()
        spin_until = get_spin_double_until()
        if spin_until > datetime.datetime.now(datetime.timezone.utc).timestamp():
            asyncio.create_task(finish_double_spin_at(spin_until))

@bot.event
async def on_guild_join(guild):
    blocked=get_server_blacklist().get(str(guild.id))
    if blocked:
        message=f"❌ هذا السيرفر موجود في القائمة السوداء. رجاء تواصل مع المالك <@875161402476736603>."
        channel=next((ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages),None)
        if channel:
            try: await channel.send(message)
            except Exception: pass
        await asyncio.sleep(2)
        try: await guild.leave()
        except Exception: pass
        return
    get_guild_budget(guild.id)
    try: await bot.tree.sync(guild=guild)
    except Exception as exc: print(f"Error syncing guild commands: {exc}")

# ==============================================================================
# 🎨 6. قائمة الهيلب (!help و /help)
# ==============================================================================
HELP_COMMANDS = {'general': [('ai', 'سؤال الذكاء الاصطناعي Gemini'), ('bal', 'معرفة رصيدك أو رصيد عضو آخر'), ('exchange', 'تحويل عملات السيرفر إلى عملة أخرى متاحة'), ('exchange_stats', 'عرض عدد العمليات الناجحة والعملات المتبدلة للسيرفر'), ('help', 'فتح مركز مساعدة Rize المتطور'), ('ping', 'فحص سرعة استجابة البوت • استخدم !ping'), ('see_coins', 'عرض العملات وأسعار الصرف وحدود الاستلام'), ('see_exchange', 'عرض آخر طلبات التبديل الخاصة بك أنت فقط'), ('server_info', 'معرفة معلومات السيرفر الحالي'), ('show_exchange', 'عرض آخر طلبات التبديل في السيرفر'), ('show_transfer', 'عرض العمليات التي تم تحويلها من شخص معين'), ('timer', 'إنشاء مؤقت وينبهك عند انتهائه'), ('transfer', 'تحويل آمن بكابتشا واضحة و3 محاولات خلال 20 ثانية')], 'games': [('box', 'إنشاء صندوق عملات للأسرع'), ('double_spin', 'تشغيل دبل جوائز بوت الإسبن لمدة محددة'), ('giveaway', 'إنشاء سحب منظم مع عدد مشاركين مباشر'), ('remove_games', 'إزالة عضو أو رتبة من صلاحيات الألعاب'), ('roulette', 'بدء لعبة روليت الإقصاء بالشرط (تخصم من ميزانية السيرفر)'), ('show_games', 'عرض أصحاب صلاحيات الألعاب'), ('stop_roulette', 'إيقاف لعبة الروليت الحالية فوراً'), ('stopgiveaway', 'إنهاء السحب فوراً واختيار الفائزين')], 'admin': [('ban', 'حظر عضو من السيرفر • استخدم !ban'), ('come', 'استدعاء عضو للروم عبر الخاص • استخدم !come'), ('del', 'مسح عدد من الرسائل • استخدم !del'), ('exchange_accept', 'قبول طلب تبديل برقم التعامل'), ('exchange_deny', 'رفض طلب تبديل برقم التعامل وإرجاع العملات'), ('hide', 'إخفاء الروم الحالية • استخدم !hide'), ('kick', 'طرد عضو من السيرفر • استخدم !kick'), ('lock', 'قفل الشات الحالي • استخدم !lock'), ('make', 'إعطاء رتبة لعضو • استخدم !make'), ('make_easy', 'إنشاء اختصار أو أمر جديد مخصص'), ('make_line', 'تشغيل الخط التلقائي في عدة رومات'), ('nick', 'تغيير لقب عضو في السيرفر أو إرجاعه لاسمه الأصلي بتركه فارغاً • استخدم !nick'), ('open', 'فتح الشات الحالي • استخدم !open'), ('remove_line', 'إيقاف الخط من روم محددة أو كل الرومات'), ('remove_reply', 'حذف رد تلقائي'), ('rename', 'تغيير اسم الروم الحالية • استخدم !rename'), ('say', 'التحدث باسم البوت مع دعم المرفقات • استخدم !say'), ('set_delivery', 'تعيين روم التسليمات التلقائية للبوت'), ('set_exchange', 'تعيين روم استقبال طلبات التبديل'), ('set_reply', 'إضافة أو تعديل رد تلقائي'), ('set_role', 'تعيين رتبة التحكم الإداري بالبوت في السيرفر'), ('setup', 'عرض وتجهيز رومات نظام Rize'), ('setup_exchange', 'إنشاء واجهة تبديل العملات'), ('show', 'إظهار الروم الحالية • استخدم !show'), ('show_line', 'عرض كل الرومات التي يعمل فيها الخط'), ('show_reply', 'عرض الردود التلقائية في السيرفر'), ('unban', 'فك حظر عضو عبر الـ ID • استخدم !unban'), ('unmake', 'سحب رتبة من عضو • استخدم !unmake')], 'owner': [('blacklist', 'إضافة عضو أو ID للبلاك ليست مع سبب إجباري'), ('blacklist_server', 'حظر سيرفر وإخراج البوت منه'), ('give_per', 'إعطاء صلاحية المطور والأدمن المطلقة لشخص (للمالك فقط)'), ('give_server', 'شحن ميزانية السيرفر بالعملات عن بعد عبر الـ ID'), ('leave_guild', 'إخراج البوت من السيرفر الحالي أو سيرفر معين عبر الـ ID'), ('remove', 'خصم عملات من شخص'), ('remove_admin', 'إزالة عضو أو رتبة من صلاحيات الإدارة'), ('remove_all_per', 'إعادة ضبط جميع المتحكمين والإداريين مع إبقاء المالك فقط'), ('remove_controller', 'حذف عضو أو رتبة من صلاحيات قسم'), ('rize', 'إضافة عملات للشخص (يخصم من ميزانية السيرفر)'), ('see_servers', 'عرض السيرفرات المتواجد بها البوت'), ('server_budget', 'عرض ميزانية السيرفر الحالية'), ('server_join', 'إرسال رابط مؤقت لسيرفر موجود فيه البوت عبر ID'), ('set_per', 'إضافة عضو أو رتبة لصلاحيات المالك المساعدة'), ('set_server_budget', 'تحديد ميزانية السيرفر مباشرة'), ('show_admin', 'عرض قائمة الإداريين والأدمن مع بيان من يملك الصلاحيات المطلقة'), ('show_blacklist', 'عرض البلاك ليست وحالة الرتبة'), ('show_blacklist_servers', 'عرض السيرفرات المحظورة'), ('show_controllers', 'عرض صلاحيات الألعاب والإدارة والمالك في السيرفر'), ('show_per', 'عرض المطورين والأشخاص الحاصلين على give_per والصلاحيات المطلقة'), ('show_permissions', 'عرض جميع صلاحيات البوت في السيرفر'), ('take_server', 'خصم مبلغ من ميزانية سيرفر معين عن بعد عبر الـ ID'), ('takefrom', 'تصفير رصيد العضو'), ('toggle_exchange_system', 'فتح أو إغلاق نظام التبديل عالميًا'), ('unblacklist', 'إزالة عضو أو ID من البلاك ليست'), ('unblacklist_server', 'إزالة سيرفر من القائمة السوداء'), ('ungive_admin', 'إزالة أدمن بالمنشن أو الـ ID'), ('ungive_per', 'سحب صلاحية المطور والأدمن من شخص (للمالك فقط)'), ('back_server', 'إرجاع سيرفر واحد للوضع الافتراضي - مالك البوت فقط'), ('back_all_servers', 'إرجاع جميع السيرفرات للوضع الافتراضي - مالك البوت فقط'), ('see_server_premium', 'عرض جميع السيرفرات التي لديها Premium فعال - مالك البوت فقط'), ('take_premium', 'سحب Premium من السيرفر الحالي فوراً - مالك البوت فقط'), ('setup_premium', 'إنشاء واجهة شراء Premium'), ('set_premium_price', 'تحديد سعر شهر Premium لكل عملة'), ('see_premium', 'البحث عن عملية Premium باستخدام ID'), ('set_channel_premium', 'تحديد روم سجلات جميع معاملات Premium'), ('set_channel_premium_purchers', 'تحديد روم إتمام وفواتير شراء Premium'), ('make_coin', 'إضافة أو ضبط سعر صرف عملة بالنسبة لـ Rize • للمالك الرئيسي فقط'), ('set_coin_limit', 'تحديد حدود العملة؛ اكتب no limit لإلغاء أي حد • للمالك الرئيسي فقط'), ('toggle_currency_status', 'تفعيل أو تعطيل عملة للتحويل • للمالك الرئيسي فقط')], 'premium': [('active_premium', 'تفعيل Premium للسيرفر باستخدام كود'), ('change_banner', 'تغيير بانر البوت في هذا السيرفر فقط'), ('change_name', 'تغيير اسم البوت في هذا السيرفر فقط'), ('change_photo', 'تغيير صورة البوت في هذا السيرفر فقط'), ('edit_server_profile', 'تعديل ملف البوت الكامل في هذا السيرفر فقط'), ('make_premium_code', 'إنشاء كود Premium مكون من 14 حرفًا'), ('premium_stats', 'عرض تفاصيل Premium والخصائص المستخدمة'), ('premium_status', 'عرض حالة Premium في السيرفر'), ('change_coin', 'تغيير اسم عملة السيرفر - يتطلب Premium'), ('back_coin', 'إرجاع اسم عملة السيرفر إلى Rize - يتطلب Premium'), ('change_line', 'تغيير صورة الخط - Premium وصاحب السيرفر أو Administrator فقط'), ('buy_premium', 'فتح روم خاص وشراء Premium')]}

def build_help_page(category, title, intro, color, guild=None):
    commands_list = HELP_COMMANDS[category]
    embed = discord.Embed(title=title, description=intro, color=color)
    chunk, size, part = [], 0, 1
    for name, description in commands_list:
        line = f"`/{name}`\n└ {description}"
        if size + len(line) > 850 and chunk:
            embed.add_field(name=f"◈ القائمة {part}", value="\n\n".join(chunk), inline=False)
            chunk, size, part = [], 0, part + 1
        chunk.append(line); size += len(line) + 2
    if chunk:
        embed.add_field(name=f"◈ القائمة {part}", value="\n\n".join(chunk), inline=False)
    if guild:
        branding = load_data().get("server_branding", {}).get(str(guild.id), {})
        if branding.get("logo"): embed.set_thumbnail(url=branding["logo"])
    embed.set_footer(text=f"Rize Command Center • {len(commands_list)} أمر • استخدم زر الرئيسية للعودة")
    return embed


def build_main_help_embed(guild=None):
    counts = {key: len(value) for key, value in HELP_COMMANDS.items()}
    total = sum(counts.values())
    embed = discord.Embed(
        title="🚀 RIZE COMMAND CENTER",
        description=(
            "مرحباً بك في مركز التحكم المتطور لبوت **Rize**.\n"
            "اختر القسم المطلوب من الأزرار، وستظهر الأوامر مع وصف مباشر لكل وظيفة.\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"🌐 **العامة والاقتصاد**  •  `{counts['general']}` أمر\n"
            f"🎁 **الألعاب والجوائز**  •  `{counts['games']}` أمر\n"
            f"⚙️ **الإدارة والتحكم**  •  `{counts['admin']}` أمر\n"
            f"👑 **المالك والمطورون**  •  `{counts['owner']}` أمر\n"
            f"💎 **Premium**  •  `{counts['premium']}` أمر\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "💾 الجيف أواي يستمر بعد إعادة التشغيل.\n"
            "🔐 الصلاحيات والإعدادات محفوظة.\n"
            "⚡ يدعم البوت أوامر `/` وأوامر `!`."
        ),
        color=discord.Color.from_rgb(88, 101, 242)
    )
    if guild:
        branding = load_data().get("server_branding", {}).get(str(guild.id), {})
        if branding.get("logo"): embed.set_thumbnail(url=branding["logo"])
        elif guild.icon: embed.set_thumbnail(url=guild.icon.url)
        if branding.get("banner"): embed.set_image(url=branding["banner"])
    embed.add_field(name="📊 إجمالي الأوامر", value=f"`{total}` أمر موثق", inline=True)
    embed.add_field(name="🧭 طريقة الاستخدام", value="اختر قسماً من الأزرار", inline=True)
    embed.set_footer(text="Rize Currency System • واجهة المساعدة الاحترافية")
    return embed


class HelpView(discord.ui.View):
    def __init__(self, author_id):
        super().__init__(timeout=240)
        self.author_id = author_id

    async def interaction_check(self, interaction):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("❌ لوحة المساعدة تخص صاحب الأمر فقط.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="العامة", emoji="🌐", style=discord.ButtonStyle.primary, row=0)
    async def general(self, interaction, button):
        await interaction.response.edit_message(embed=build_help_page("general","🌐 العامة والاقتصاد","الأرصدة والتحويلات والتبديل والخدمات الأساسية.",discord.Color.blue(),interaction.guild),view=self)

    @discord.ui.button(label="الألعاب", emoji="🎁", style=discord.ButtonStyle.success, row=0)
    async def games(self, interaction, button):
        await interaction.response.edit_message(embed=build_help_page("games","🎁 الألعاب والجوائز","الروليت والجيف أواي والصناديق وصلاحيات الألعاب.",discord.Color.green(),interaction.guild),view=self)

    @discord.ui.button(label="الإدارة", emoji="⚙️", style=discord.ButtonStyle.danger, row=0)
    async def admin(self, interaction, button):
        await interaction.response.edit_message(embed=build_help_page("admin","⚙️ الإدارة والتحكم","الإشراف والردود والعملات وإدارة السيرفر.",discord.Color.red(),interaction.guild),view=self)

    @discord.ui.button(label="المالك", emoji="👑", style=discord.ButtonStyle.secondary, row=0)
    async def owner(self, interaction, button):
        await interaction.response.edit_message(embed=build_help_page("owner","👑 المالك والمطورون","الصلاحيات العليا والميزانيات والسيرفرات.",discord.Color.gold(),interaction.guild),view=self)

    @discord.ui.button(label="Premium",emoji="💎",style=discord.ButtonStyle.primary,row=1)
    async def premium(self,interaction,button):
        await interaction.response.edit_message(embed=build_help_page("premium","💎 أوامر Premium","التفعيل والحالة وتخصيص هوية البوت داخل السيرفر.",discord.Color.purple(),interaction.guild),view=self)

    @discord.ui.button(label="الرئيسية", emoji="🏠", style=discord.ButtonStyle.secondary, row=1)
    async def home(self, interaction, button):
        await interaction.response.edit_message(embed=build_main_help_embed(interaction.guild),view=self)


@bot.command(name="help")
async def help_cmd(ctx):
    await ctx.send(embed=build_main_help_embed(ctx.guild), view=HelpView(ctx.author.id))


@bot.tree.command(name="help", description="فتح مركز مساعدة Rize المتطور")
async def help_slash(interaction: discord.Interaction):
    if is_blacklisted(interaction.user.id): return
    await interaction.response.send_message(embed=build_main_help_embed(interaction.guild), view=HelpView(interaction.user.id))

# ==============================================================================
# 🌐 7. أوامر إدارة السيرفرات والمعلومات (! و /)
# ==============================================================================
def server_stats():
    guilds=sorted(bot.guilds,key=lambda g:(g.member_count or 0),reverse=True)
    total_members=sum((g.member_count or 0) for g in guilds)
    return guilds,total_members


@bot.command(name="server_count")
async def server_count_cmd(ctx):
    guilds,total=server_stats()
    await ctx.send(f"📊 يتواجد البوت حالياً في {code_number(len(guilds))} سيرفر، ويخدم أكثر من {code_number(total)} عضو.")


@bot.command(name="see_servers")
async def see_servers_cmd(ctx):
    if not is_owner(ctx.author.id): return await ctx.send("❌ للمالك فقط.")
    guilds,total=server_stats(); pages=[guilds[i:i+7] for i in range(0,len(guilds),7)] or [[]]
    for page_index,page in enumerate(pages,1):
        lines=[]
        for index,guild in enumerate(page,(page_index-1)*7+1):
            link_text="غير متاح"
            channel=next((ch for ch in guild.text_channels if ch.permissions_for(guild.me).create_instant_invite),None)
            if channel:
                try:
                    invite=await channel.create_invite(max_age=300,max_uses=1,unique=True)
                    link_text=f"[اضغط هنا للدخول]({invite.url})"
                except Exception: pass
            lines.append(
                f"**#{index} | {guild.name}**\n"
                f"• ID: {code_id(guild.id)}\n"
                f"• الأعضاء: {code_number(guild.member_count or 0)}\n"
                f"• رابط الدعوة: {link_text}"
            )
        embed=discord.Embed(
            title=f"📊 قائمة سيرفرات البوت ({len(guilds)} سيرفر) - صفحة {page_index}/{len(pages)}",
            description=f"👥 إجمالي الأعضاء: {code_number(total)} عضو\n\n"+"\n\n".join(lines),color=discord.Color.blue())
        await ctx.send(embed=embed)


@bot.tree.command(name="see_servers",description="عرض السيرفرات المتواجد بها البوت")
async def see_servers_slash(interaction:discord.Interaction):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ للمالك فقط.",ephemeral=True)
    guilds,total=server_stats()
    lines=[f"**#{i} | {g.name}** • ID {code_id(g.id)} • أعضاء {code_number(g.member_count or 0)}" for i,g in enumerate(guilds[:20],1)]
    embed=discord.Embed(title=f"📊 السيرفرات: {code_number(len(guilds))}",description=f"إجمالي الأعضاء: {code_number(total)}\n\n"+"\n".join(lines),color=discord.Color.blue())
    await interaction.response.send_message(embed=embed,ephemeral=True)


@bot.command(name="leave_guild")
async def leave_guild_cmd(ctx, guild_id: str = None):
    if not is_owner(ctx.author.id): return await ctx.send("❌ مخصص للمطورين فقط!")
    target = bot.get_guild(int(guild_id)) if guild_id else ctx.guild
    if target:
        await ctx.send(f"👋 جاري مغادرة السيرفر: **{target.name}**...")
        await target.leave()

@bot.tree.command(name="leave_guild", description="إخراج البوت من السيرفر الحالي أو سيرفر معين عبر الـ ID")
async def leave_guild_slash(interaction: discord.Interaction, guild_id: Optional[str] = None):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ مخصص للمطورين فقط!", ephemeral=True)
    target = bot.get_guild(int(guild_id)) if guild_id else interaction.guild
    if target:
        await interaction.response.send_message(f"👋 جاري مغادرة السيرفر: **{target.name}**...")
        await target.leave()

@bot.command(name="server_join")
async def server_join_cmd(ctx, guild_id: str):
    if not is_owner(ctx.author.id): return await ctx.send("❌ هذا الأمر للمالك الرئيسي فقط.")
    try: guild = bot.get_guild(int(guild_id))
    except ValueError: guild = None
    if not guild: return await ctx.send("❌ البوت غير موجود في سيرفر بهذا الـ ID.")
    channel = next((ch for ch in guild.text_channels if ch.permissions_for(guild.me).create_instant_invite), None)
    if not channel: return await ctx.send("❌ لا توجد روم يستطيع البوت إنشاء دعوة منها.")
    try:
        invite = await channel.create_invite(max_age=300, max_uses=1, unique=True, reason=f"Requested by owner {ctx.author.id}")
        await ctx.author.send(f"🔗 رابط دخول مؤقت لسيرفر **{guild.name}**:\n{invite.url}\nينتهي خلال 5 دقائق أو بعد استخدام واحد.")
        await ctx.send("✅ أرسلت رابط الدخول في الخاص.")
    except Exception as exc:
        print(f"server_join error: {exc!r}"); await ctx.send("❌ تعذر إنشاء الدعوة. تأكد من صلاحية Create Invite.")


@bot.tree.command(name="server_join", description="إرسال رابط مؤقت لسيرفر موجود فيه البوت عبر ID")
async def server_join_slash(interaction: discord.Interaction, guild_id: str):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ هذا الأمر للمالك الرئيسي فقط.", ephemeral=True)
    try: guild = bot.get_guild(int(guild_id))
    except ValueError: guild = None
    if not guild: return await interaction.response.send_message("❌ البوت غير موجود في سيرفر بهذا الـ ID.", ephemeral=True)
    channel = next((ch for ch in guild.text_channels if ch.permissions_for(guild.me).create_instant_invite), None)
    if not channel: return await interaction.response.send_message("❌ لا توجد روم يستطيع البوت إنشاء دعوة منها.", ephemeral=True)
    try:
        invite = await channel.create_invite(max_age=300, max_uses=1, unique=True, reason=f"Requested by owner {interaction.user.id}")
        embed=discord.Embed(title="🔗 رابط دخول مؤقت", description=f"**السيرفر:** {guild.name}\n**ID:** `{guild.id}`\n[اضغط هنا للدخول]({invite.url})", color=discord.Color.green())
        embed.set_footer(text="صالح 5 دقائق أو لاستخدام واحد")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except Exception as exc:
        print(f"server_join error: {exc!r}"); await interaction.response.send_message("❌ تعذر إنشاء الدعوة. تأكد من صلاحية Create Invite.", ephemeral=True)


@bot.command(name="server_info")
async def server_info_cmd(ctx):
    guild = ctx.guild
    coin = get_guild_coin(guild.id)
    embed = discord.Embed(title=f"🏰 معلومات سيرفر: {guild.name}", color=discord.Color.purple())
    embed.add_field(name="🆔 الـ ID", value=f"`{guild.id}`", inline=True)
    embed.add_field(name="👑 المالك", value=f"{guild.owner.display_name}", inline=True)
    embed.add_field(name="👥 أعداد الأعضاء", value=f"`{guild.member_count}` عضو", inline=True)
    embed.add_field(name="🪙 عملة السيرفر", value=f"`{coin}`", inline=True)
    if guild.icon: embed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=embed)

@bot.tree.command(name="server_info", description="معرفة معلومات السيرفر الحالي")
async def server_info_slash(interaction: discord.Interaction):
    guild = interaction.guild
    coin = get_guild_coin(guild.id)
    embed = discord.Embed(title=f"🏰 معلومات سيرفر: {guild.name}", color=discord.Color.purple())
    embed.add_field(name="🆔 الـ ID", value=f"`{guild.id}`", inline=True)
    embed.add_field(name="👑 المالك", value=f"{guild.owner.display_name}", inline=True)
    embed.add_field(name="👥 أعداد الأعضاء", value=f"`{guild.member_count}` عضو", inline=True)
    embed.add_field(name="🪙 عملة السيرفر", value=f"`{coin}`", inline=True)
    if guild.icon: embed.set_thumbnail(url=guild.icon.url)
    await interaction.response.send_message(embed=embed)

# ==============================================================================
# 💸 8. التحويل مع الكابتشا (4 أرقام - مهلة 20 ثانية كاملة - لا يغلق عند الخطأ)
# ==============================================================================
async def start_transfer_process(ctx_or_interaction, sender: discord.User, receiver: discord.User, amount_str: str):
    if sender.id == receiver.id:
        return "❌ لا يمكنك تحويل العملات إلى نفسك. اختر عضواً آخر."
    if receiver.bot:
        return "❌ لا يمكن تحويل العملات إلى حساب بوت."

    guild = ctx_or_interaction.guild
    guild_id = guild.id if guild else 0
    coin = get_guild_coin(guild_id)
    parsed_amount = parse_decimal_amount(amount_str)

    if parsed_amount is None or parsed_amount <= 0:
        return "❌ المبلغ غير صحيح. استخدم رقماً موجباً مثل `1000` أو `5k` أو `2m`."

    sender_balance = get_balance(sender.id)
    if parsed_amount > sender_balance:
        return (
            f"❌ رصيدك غير كافٍ لإتمام التحويل.\n"
            f"💰 رصيدك الحالي: `{format_amount(sender_balance)}` {coin}\n"
            f"📤 المبلغ المطلوب: `{format_amount(parsed_amount)}` {coin}"
        )

    captcha_code = str(random.randint(1000, 9999))
    captcha_buffer = generate_captcha_image(captcha_code)
    captcha_file = discord.File(captcha_buffer, filename="rize_captcha.png")

    embed = discord.Embed(
        title="🔐 تأكيد عملية التحويل",
        description=(
            f"👤 **المستلم:** {receiver.mention}\n"
            f"📤 **المُرسل:** {sender.mention}\n"
            f"💰 **المبلغ:** `{format_amount(parsed_amount)}` {coin}\n\n"
            "اكتب **الأرقام الأربعة** الظاهرة في الصورة داخل نفس الروم."
        ),
        color=discord.Color.blurple(),
    )
    embed.add_field(name="⏳ المهلة", value="20 ثانية", inline=True)
    embed.add_field(name="🔁 المحاولات", value="3 محاولات", inline=True)
    embed.add_field(name="🛡️ الحماية", value="لن يُخصم الرصيد قبل نجاح التحقق", inline=False)
    embed.set_image(url="attachment://rize_captcha.png")
    embed.set_footer(text="Rize Secure Transfer • لا تشارك رمز التحقق مع أي شخص")

    if isinstance(ctx_or_interaction, commands.Context):
        captcha_message = await ctx_or_interaction.send(embed=embed, file=captcha_file)
        channel = ctx_or_interaction.channel
    else:
        await ctx_or_interaction.response.send_message(embed=embed, file=captcha_file)
        captcha_message = await ctx_or_interaction.original_response()
        channel = ctx_or_interaction.channel

    def check(message):
        return message.author.id == sender.id and message.channel.id == channel.id

    loop = asyncio.get_running_loop()
    deadline = loop.time() + 20.0
    attempts_left = 3
    verified = False
    cancelled_reason = "timeout"

    while attempts_left > 0:
        remaining = deadline - loop.time()
        if remaining <= 0:
            break
        try:
            response_message = await bot.wait_for("message", timeout=remaining, check=check)
        except asyncio.TimeoutError:
            break

        answer = response_message.content.strip()
        try:
            await response_message.delete()
        except Exception:
            pass

        if answer == captcha_code:
            verified = True
            break

        attempts_left -= 1
        cancelled_reason = "attempts"
        if attempts_left > 0:
            warning = await channel.send(
                f"⚠️ {sender.mention} الرمز غير صحيح. متبقي لك **{attempts_left}** "
                f"{'محاولة' if attempts_left == 1 else 'محاولات'} قبل إلغاء التحويل."
            )
            await asyncio.sleep(2.5)
            try:
                await warning.delete()
            except Exception:
                pass

    try:
        await captcha_message.delete()
    except Exception:
        pass

    if not verified:
        if cancelled_reason == "attempts" and attempts_left == 0:
            return await channel.send(
                f"🚫 {sender.mention} تم إلغاء التحويل بسبب إدخال رمز خاطئ **3 مرات**. "
                "لم يتم خصم أي رصيد."
            )
        return await channel.send(
            f"⏰ {sender.mention} انتهت مهلة التحقق بعد **20 ثانية**. "
            "تم إلغاء التحويل ولم يتم خصم أي رصيد."
        )

    # فحص الرصيد مرة أخرى لمنع تعارض تحويلين متزامنين.
    latest_balance = get_balance(sender.id)
    if parsed_amount > latest_balance:
        return await channel.send(
            f"❌ تعذر إتمام التحويل لأن رصيد {sender.mention} تغير أثناء التحقق. "
            f"الرصيد الحالي: `{format_amount(latest_balance)}` {coin}."
        )

    update_balance(sender.id, -parsed_amount)
    update_balance(receiver.id, parsed_amount)
    log_transfer(sender.id, receiver.id, parsed_amount)

    sender_new_balance = get_balance(sender.id)
    receiver_new_balance = get_balance(receiver.id)

    success_embed = discord.Embed(
        title="✅ تم التحويل بنجاح",
        description=(
            f"تم تحويل `{format_amount(parsed_amount)}` {coin} من {sender.mention} إلى {receiver.mention}."
        ),
        color=discord.Color.green(),
        timestamp=datetime.datetime.now(datetime.timezone.utc),
    )
    success_embed.add_field(name="رصيد المُرسل", value=f"`{format_amount(sender_new_balance)}` {coin}", inline=True)
    success_embed.add_field(name="رصيد المستلم", value=f"`{format_amount(receiver_new_balance)}` {coin}", inline=True)
    success_embed.set_footer(text="Rize Secure Transfer")
    await channel.send(embed=success_embed)

    try:
        await sender.send(
            embed=discord.Embed(
                title="📤 إيصال تحويل صادر",
                description=(
                    f"أرسلت `{format_amount(parsed_amount)}` {coin} إلى **{receiver.display_name}**.\n"
                    f"رصيدك الآن: `{format_amount(sender_new_balance)}` {coin}"
                ),
                color=discord.Color.blue(),
                timestamp=datetime.datetime.now(datetime.timezone.utc),
            )
        )
    except Exception:
        pass

    try:
        await receiver.send(
            embed=discord.Embed(
                title="📥 تم استلام عملات",
                description=(
                    f"استلمت `{format_amount(parsed_amount)}` {coin} من **{sender.display_name}**.\n"
                    f"رصيدك الآن: `{format_amount(receiver_new_balance)}` {coin}"
                ),
                color=discord.Color.green(),
                timestamp=datetime.datetime.now(datetime.timezone.utc),
            )
        )
    except Exception:
        pass

@bot.command(name="transfer")
async def transfer_cmd(ctx, member: discord.Member, amount: str):
    purchase=purchase_by_channel(ctx.channel.id)
    parsed=parse_number(amount)
    if (purchase and purchase.get("status")=="awaiting_payment" and purchase.get("payment_method")=="adamc"
        and ctx.author.id==int(purchase.get("buyer_id",0)) and member.id==PREMIUM_PAYMENT_RECEIVER_ID
        and parsed==int(purchase.get("amount",-1))):
        return
    res = await start_transfer_process(ctx, ctx.author, member, amount)
    if res and not isinstance(res, discord.Message):
        await ctx.send(str(res))

@bot.tree.command(name="transfer", description="تحويل آمن بكابتشا واضحة و3 محاولات خلال 20 ثانية")
async def transfer_slash(interaction: discord.Interaction, member: discord.Member, amount: str):
    if is_blacklisted(interaction.user.id): return
    res = await start_transfer_process(interaction, interaction.user, member, amount)
    if res and not isinstance(res, discord.Message):
        if interaction.response.is_done():
            await interaction.followup.send(str(res),ephemeral=True)
        else:
            await interaction.response.send_message(str(res),ephemeral=True)

@bot.command(name="show_transfer")
async def show_transfer_cmd(ctx, member: discord.Member = None):
    target = member or ctx.author
    transfers = get_user_transfers(target.id)
    coin = get_guild_coin(ctx.guild.id)
    
    if not transfers:
        return await ctx.send(f"📜 لا توجد عمليات تحويل مسجلة لـ {target.display_name} حتى الآن.")
    
    history_lines = []
    for t in transfers[-10:]:
        history_lines.append(f"• إلى <@{t['receiver']}>: **{t['amount']:,} {coin}** 🪙 | 🕒 `{t['date']}`")
    
    embed = discord.Embed(
        title=f"📜 **سجل عمليات التحويل الصادرة لـ {target.display_name}**",
        description="\n".join(history_lines),
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.tree.command(name="show_transfer", description="عرض العمليات التي تم تحويلها من شخص معين")
async def show_transfer_slash(interaction: discord.Interaction, member: Optional[discord.Member] = None):
    target = member or interaction.user
    transfers = get_user_transfers(target.id)
    coin = get_guild_coin(interaction.guild.id)
    
    if not transfers:
        return await interaction.response.send_message(f"📜 لا توجد عمليات تحويل مسجلة لـ {target.display_name} حتى الآن.", ephemeral=True)
    
    history_lines = []
    for t in transfers[-10:]:
        history_lines.append(f"• إلى <@{t['receiver']}>: **{t['amount']:,} {coin}** 🪙 | 🕒 `{t['date']}`")
    
    embed = discord.Embed(
        title=f"📜 **سجل عمليات التحويل الصادرة لـ {target.display_name}**",
        description="\n".join(history_lines),
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)

# ==============================================================================
# 🪙 9. أوامر التحكم في العملات وأسعار الصرف للتبديل
# ==============================================================================
@bot.command(name="make_coin")
async def make_coin_cmd(ctx, rize_amount: str, currency_name: str, coin_amount: str):
    if not is_owner(ctx.author.id): return await ctx.send("❌ هذا الأمر للمالك الرئيسي للبوت فقط.")
    parsed_rize = parse_number(rize_amount)
    parsed_coin = parse_number(coin_amount)
    if not parsed_rize or not parsed_coin or parsed_rize <= 0 or parsed_coin <= 0:
        return await ctx.send("❌ أرقام غير صحيحة!")
    
    set_custom_currency(ctx.guild.id, currency_name, parsed_rize, parsed_coin)
    coin = get_guild_coin(ctx.guild.id)
    await ctx.send(f"⚙️ **تم ضبط عملة `{currency_name}` بنجاح!**\nكل `{parsed_rize:,}` {coin} تساوي `{parsed_coin:,}` من عملة `{currency_name}`.")

@bot.tree.command(name="make_coin", description="إضافة أو ضبط سعر صرف عملة بالنسبة لـ Rize")
@app_commands.describe(rize_amount="عدد عملات الرايز", currency_name="اسم العملة المراد إضافتها", coin_amount="المقابل من العملة الجديدة")
async def make_coin_slash(interaction: discord.Interaction, rize_amount: str, currency_name: str, coin_amount: str):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ هذا الأمر للمالك الرئيسي للبوت فقط.", ephemeral=True)
    parsed_rize = parse_number(rize_amount)
    parsed_coin = parse_number(coin_amount)
    if not parsed_rize or not parsed_coin or parsed_rize <= 0 or parsed_coin <= 0:
        return await interaction.response.send_message("❌ أرقام غير صحيحة!", ephemeral=True)
    
    set_custom_currency(interaction.guild.id, currency_name, parsed_rize, parsed_coin)
    coin = get_guild_coin(interaction.guild.id)
    await interaction.response.send_message(f"⚙️ **تم ضبط عملة `{currency_name}` بنجاح!**\nكل `{parsed_rize:,}` {coin} تساوي `{parsed_coin:,}` من عملة `{currency_name}`.")

@bot.command(name="toggle_currency_status")
async def toggle_currency_status_cmd(ctx, currency_name: str, status: str):
    if not is_owner(ctx.author.id): return await ctx.send("❌ هذا الأمر للمالك الرئيسي للبوت فقط.")
    is_true = status.lower() in ["true", "1", "مفعل", "تفعيل", "yes"]
    success = set_currency_status(ctx.guild.id, currency_name, is_true)
    if success:
        st_text = "🟢 **مفعلة**" if is_true else "🔴 **معطلة**"
        await ctx.send(f"⚙️ تم تغيير حالة العملة `{currency_name}` إلى {st_text} بنجاح!")
    else:
        await ctx.send(f"❌ العملة غير متواجدة، انتظرونا!")

@bot.tree.command(name="toggle_currency_status", description="تفعيل أو تعطيل عملة للتحويل")
@app_commands.describe(currency_name="اسم العملة", status="حالة العملة (true لتفعيل / false لتعطيل)")
async def toggle_currency_status_slash(interaction: discord.Interaction, currency_name: str, status: bool):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ هذا الأمر للمالك الرئيسي للبوت فقط.", ephemeral=True)
    success = set_currency_status(interaction.guild.id, currency_name, status)
    if success:
        st_text = "🟢 **مفعلة**" if status else "🔴 **معطلة**"
        await interaction.response.send_message(f"⚙️ تم تغيير حالة العملة `{currency_name}` إلى {st_text} بنجاح!")
    else:
        await interaction.response.send_message(f"❌ العملة غير متواجدة، انتظرونا!", ephemeral=True)

def parse_optional_limit(value: str, *, minimum=False):
    """يدعم no limit / unlimited / غير محدود لإلغاء الحد."""
    clean = str(value).strip().lower().replace("_", " ").replace("-", " ")
    unlimited_words = {
        "no limit", "nolimit", "unlimited", "none", "off", "disable",
        "غير محدود", "بلا حد", "بدون حد", "مفتوح"
    }
    if clean in unlimited_words:
        return 0 if minimum else None
    parsed = parse_number(clean)
    if parsed is None or parsed < 0:
        raise ValueError("invalid limit")
    return parsed


def build_coins_embed(guild_id):
    currencies = get_custom_currencies(guild_id)
    coin = get_guild_coin(guild_id)
    embed = discord.Embed(
        title="🪙 العملات وأسعار الصرف",
        description="الأسعار وحدود الاستلام الحالية لهذا السيرفر.",
        color=discord.Color.gold()
    )
    if not currencies:
        embed.description = "لا توجد عملات مضافة حالياً."
        return embed
    for name, info in currencies.items():
        status = "🟢 متاحة" if info.get("status", True) else "🔴 متوقفة"
        minimum = info.get("min_receive", 0)
        maximum = info.get("max_receive")
        minimum_text = "غير محدود" if minimum in (None, 0) else f"{minimum:,}"
        maximum_text = "غير محدود" if maximum is None else f"{maximum:,}"
        value = (
            f"**سعر الصرف**\n`{info.get('rize_amount', 0):,}` {coin} = "
            f"`{info.get('coin_amount', 0):,}` {name.upper()}\n"
            f"**الحالة:** {status}\n"
            f"**الحد الأدنى:** `{minimum_text}`\n"
            f"**الحد الأقصى:** `{maximum_text}`"
        )
        embed.add_field(name=f"💱 {name.upper()}", value=value, inline=False)
    embed.set_footer(text=f"Rize Currency System • عملة السيرفر: {coin}")
    return embed


@bot.command(name="see_coins")
async def see_coins_cmd(ctx):
    await ctx.send(embed=build_coins_embed(ctx.guild.id))


@bot.tree.command(name="see_coins", description="عرض العملات وأسعار الصرف وحدود الاستلام")
async def see_coins_slash(interaction: discord.Interaction):
    await interaction.response.send_message(embed=build_coins_embed(interaction.guild.id))


@bot.tree.command(name="set_coin_limit", description="تحديد حدود العملة؛ اكتب no limit لإلغاء أي حد")
@app_commands.describe(
    currency_name="اسم العملة",
    minimum="الحد الأدنى أو no limit",
    maximum="الحد الأقصى أو no limit"
)
async def set_coin_limit(interaction: discord.Interaction, currency_name: str, minimum: str, maximum: str):
    if not is_owner(interaction.user.id):
        return await interaction.response.send_message(embed=error_embed("🔒 غير مصرح", "هذا الأمر للمالك الرئيسي للبوت فقط."), ephemeral=True)
    try:
        min_value = parse_optional_limit(minimum, minimum=True)
        max_value = parse_optional_limit(maximum, minimum=False)
    except ValueError:
        return await interaction.response.send_message(
            embed=error_embed("❌ حدود غير صحيحة", "اكتب رقماً مثل `10k` أو اكتب `no limit` لإلغاء الحد."),
            ephemeral=True
        )
    if max_value is not None and min_value > max_value:
        return await interaction.response.send_message(
            embed=error_embed("❌ ترتيب الحدود غير صحيح", "الحد الأدنى لا يمكن أن يكون أكبر من الحد الأقصى."),
            ephemeral=True
        )
    data=load_data(); gid=str(interaction.guild.id)
    currencies=data.setdefault("guilds",{}).setdefault(gid,{}).setdefault("currencies",get_custom_currencies(interaction.guild.id))
    key=currency_name.lower().strip()
    if key not in currencies:
        return await interaction.response.send_message(embed=error_embed("❌ عملة غير موجودة", f"لم يتم العثور على `{key}`."), ephemeral=True)
    currencies[key]["min_receive"]=min_value
    currencies[key]["max_receive"]=max_value
    save_data(data)
    min_text="غير محدود" if min_value == 0 else f"{min_value:,}"
    max_text="غير محدود" if max_value is None else f"{max_value:,}"
    embed=discord.Embed(title="✅ تم تحديث حدود العملة", color=discord.Color.green())
    embed.add_field(name="العملة", value=f"`{key.upper()}`", inline=False)
    embed.add_field(name="الحد الأدنى", value=f"`{min_text}`", inline=True)
    embed.add_field(name="الحد الأقصى", value=f"`{max_text}`", inline=True)
    embed.set_footer(text="Rize Currency System")
    await interaction.response.send_message(embed=embed)

# ==============================================================================
# 🔄 10. نظام التبديل (Exchange System) - مع أمر عرض تبديلاتي الشخصية /see_exchange
# ==============================================================================
async def process_exchange(ctx_or_interaction, user: discord.User, guild: discord.Guild, amount_str: str, target_type: str, notes: str = "لا يوجد"):
    if not exchange_system_enabled():
        return "⛔ نظام التبديل مغلق عالميًا في Rize حاليًا. انتظرونا حتى يتم فتحه."
    coin = get_guild_coin(guild.id)
    parsed_amount = parse_number(amount_str)
    if not parsed_amount or parsed_amount <= 0: return "❌ مبلغ غير صحيح للتبديل!"

    currencies = get_custom_currencies(guild.id)
    target_clean = target_type.lower().strip()
    
    if target_clean not in currencies or not currencies[target_clean].get("status", True):
        return "❌ العملة غير متواجدة، انتظرونا!"

    c_info = currencies[target_clean]
    user_bal = get_balance(user.id)
    if parsed_amount > user_bal: return f"❌ رصيدك غير كافٍ! رصيدك الحالي: `{user_bal:,}` {coin}."

    calculated_received = (parsed_amount / c_info["rize_amount"]) * c_info["coin_amount"]
    min_receive = c_info.get("min_receive", 0)
    max_receive = c_info.get("max_receive")
    if calculated_received < min_receive:
        return f"❌ أقل كمية استلام لهذه العملة هي `{min_receive:,}` {target_clean}."
    if max_receive is not None and calculated_received > max_receive:
        return f"❌ أقصى كمية استلام لهذه العملة هي `{max_receive:,}` {target_clean}."

    exchange_room_id, delivery_room_id = get_exchange_rooms(guild.id)
    if not exchange_room_id:
        return "❌ لم يتم تحديد روم طلبات التبديل بعد بواسطة الإدارة باستخدام `/set_exchange`!"

    exchange_room = guild.get_channel(exchange_room_id)
    if not exchange_room:
        return "❌ روم طلبات التبديل غير موجودة أو تم حذفها!"

    update_balance(user.id, -parsed_amount)
    req_id = get_next_exchange_id()

    req_data = {
        "id": req_id,
        "user_id": user.id,
        "guild_id": guild.id,
        "amount": parsed_amount,
        "received_amount": calculated_received,
        "target_type": target_clean,
        "notes": notes,
        "status": "pending"
    }
    save_exchange_request(req_id, req_data)

    embed = discord.Embed(
        title=f"📥 طلب تبديل جديد #{req_id}",
        color=discord.Color.gold()
    )
    embed.add_field(name="🏛️ السيرفر", value=f"{guild.name}", inline=True)
    delivery_channel_mention = f"<#{delivery_room_id}>" if delivery_room_id else "غير محددة"
    embed.add_field(name="📦 روم التسليمات", value=delivery_channel_mention, inline=True)
    embed.add_field(name="👤 العضو", value=f"{user.mention} (`{user.id}`)", inline=False)
    embed.add_field(name=f"🏛️ مبلغ {coin}", value=f"`{parsed_amount:,}`", inline=True)
    embed.add_field(name=f"💵 المستحق من ({target_clean})", value=f"`{calculated_received:,.1f}`", inline=True)
    embed.add_field(name="📝 الوصف والملاحظات", value=f"```\n{notes}\n```", inline=False)
    embed.set_footer(text=f"للقبول: /exchange_accept {req_id} | للرفض: /exchange_deny {req_id}")

    await exchange_room.send(embed=embed)
    return f"✅ **تم إرسال طلب التبديل بنجاح برقم التعامل #{req_id} وتم خصم `{parsed_amount:,}` {coin} من رصيدك.**"

class ExchangeAmountModal(discord.ui.Modal,title="إرسال طلب تبديل"):
    amount=discord.ui.TextInput(label="المبلغ من رصيدك الأساسي",placeholder="مثال: 10000000 أو 10m",required=True,max_length=30)
    notes=discord.ui.TextInput(label="ملاحظة اختيارية",required=False,style=discord.TextStyle.paragraph,max_length=500)
    def __init__(self,currency): super().__init__(); self.currency=currency
    async def on_submit(self,interaction):
        result=await process_exchange(interaction,interaction.user,interaction.guild,str(self.amount),self.currency,str(self.notes) or "لا يوجد")
        await interaction.response.send_message(result,ephemeral=True)


class ExchangeCurrencySelect(discord.ui.Select):
    def __init__(self,guild_id):
        currencies=get_custom_currencies(guild_id); coin=get_guild_coin(guild_id); options=[]
        for name,info in currencies.items():
            rize_amount=info.get("rize_amount",1)
            coin_amount=info.get("coin_amount",1)
            state="متاحة" if info.get("status",True) else "مغلقة"
            # نفس النسبة المخزنة التي يعرضها see_coins، بدون افتراض مبلغ ثابت.
            ratio=f"{format_amount(rize_amount)} {coin} = {format_amount(coin_amount)} {name.upper()}"
            min_receive=info.get("min_receive",0)
            max_receive=info.get("max_receive")
            limits=[]
            if min_receive: limits.append(f"حد أدنى {format_amount(min_receive)}")
            if max_receive is not None: limits.append(f"حد أقصى {format_amount(max_receive)}")
            description=ratio+f" • {state}"+(" • "+" | ".join(limits) if limits else "")
            options.append(discord.SelectOption(label=name.upper(),value=name,description=description[:100]))
        super().__init__(placeholder="اختر العملة التي تريد استلامها...",options=options[:25])
    async def callback(self,interaction):
        info=get_custom_currencies(interaction.guild.id).get(self.values[0],{})
        if not info.get("status",True):
            return await interaction.response.send_message("⛔ هذه العملة مغلقة حالياً. انتظرونا حتى يتم فتحها.",ephemeral=True)
        await interaction.response.send_modal(ExchangeAmountModal(self.values[0]))


class ExchangePrivateView(discord.ui.View):
    def __init__(self,guild_id): super().__init__(timeout=120); self.add_item(ExchangeCurrencySelect(guild_id))


class ExchangePanel(discord.ui.View):
    def __init__(self,guild_id): super().__init__(timeout=None); self.guild_id=guild_id
    @discord.ui.button(label="تبديل العملات",emoji="💱",style=discord.ButtonStyle.primary,custom_id="rize:exchange:start")
    async def start(self,interaction,button):
        await interaction.response.send_message(
            "اختر العملة التي تريد استلامها. كل عملة ستعرض نفس نسبة التحويل والحدود الموجودة في `/see_coins`:",
            view=ExchangePrivateView(interaction.guild.id),ephemeral=True)


@bot.tree.command(name="setup_exchange",description="إنشاء واجهة تبديل العملات")
async def setup_exchange(interaction:discord.Interaction,channel:Optional[discord.TextChannel]=None):
    if not is_admin(interaction.user.id,interaction.guild): return await interaction.response.send_message("❌ للإدارة فقط.",ephemeral=True)
    target=channel or interaction.channel; coin=get_guild_coin(interaction.guild.id)
    embed=discord.Embed(title="💱 تبديل العملات",description=(
        "اضغط الزر أدناه لاختيار العملة التي تريد استلامها.\n"
        f"سيتم خصم المبلغ من رصيدك {coin} بعد التحقق، ثم يُرسل الطلب إلى الإدارة.\n\n"
        "سيظهر تأكيد الطلب لك بشكل خاص ولن يراه باقي الأعضاء."),color=discord.Color.teal())
    embed.set_footer(text="Rize Currency System • Exchange")
    await target.send(embed=embed,view=ExchangePanel(interaction.guild.id))
    await interaction.response.send_message("✅ تم إنشاء واجهة التبديل.",ephemeral=True)


@bot.command(name="set_exchange")
async def set_exchange_cmd(ctx, channel: discord.TextChannel = None):
    if not is_admin(ctx.author.id, ctx.guild): return await ctx.send("❌ مخصص للإدارة!")
    ch = channel or ctx.channel
    set_exchange_room(ctx.guild.id, ch.id)
    await ctx.send(f"✅ تم تعيين روم طلبات التبديل لتكون: {ch.mention}")

@bot.tree.command(name="set_exchange", description="تعيين روم استقبال طلبات التبديل")
async def set_exchange_slash(interaction: discord.Interaction, channel: discord.TextChannel):
    if not is_admin(interaction.user.id, interaction.guild): return await interaction.response.send_message("❌ مخصص للإدارة!", ephemeral=True)
    set_exchange_room(interaction.guild.id, channel.id)
    await interaction.response.send_message(f"✅ تم تعيين روم طلبات التبديل لتكون: {channel.mention}")

@bot.command(name="set_delivery")
async def set_delivery_cmd(ctx, channel: discord.TextChannel = None):
    if not is_admin(ctx.author.id, ctx.guild): return await ctx.send("❌ مخصص للإدارة!")
    ch = channel or ctx.channel
    set_delivery_room(ctx.guild.id, ch.id)
    await ctx.send(f"✅ تم تعيين روم التسليمات الخاصة بالبوت لتكون: {ch.mention}")

@bot.tree.command(name="set_delivery", description="تعيين روم التسليمات التلقائية للبوت")
async def set_delivery_slash(interaction: discord.Interaction, channel: discord.TextChannel):
    if not is_admin(interaction.user.id, interaction.guild): return await interaction.response.send_message("❌ مخصص للإدارة!", ephemeral=True)
    set_delivery_room(interaction.guild.id, channel.id)
    await interaction.response.send_message(f"✅ تم تعيين روم التسليمات لتكون: {channel.mention}")

@bot.command(name="exchange")
async def exchange_cmd(ctx, amount: str, target: str, *, notes: str = "لا يوجد"):
    res = await process_exchange(ctx, ctx.author, ctx.guild, amount, target, notes)
    await ctx.send(res)

@bot.tree.command(name="exchange", description="تحويل عملات السيرفر إلى عملة أخرى متاحة")
@app_commands.describe(amount="المبلغ المراد تحويله", target="اسم العملة", notes="ملاحظات اضافية")
async def exchange_slash(interaction: discord.Interaction, amount: str, target: str, notes: str = "لا يوجد"):
    if is_blacklisted(interaction.user.id): return
    res = await process_exchange(interaction, interaction.user, interaction.guild, amount, target, notes)
    await interaction.response.send_message(res, ephemeral=True)

@bot.command(name="show_exchange")
async def show_exchange_cmd(ctx):
    data = load_data()
    exchanges = data.get("exchanges", {})
    coin = get_guild_coin(ctx.guild.id)
    
    guild_exchanges = [req for req in exchanges.values() if req.get("guild_id") == ctx.guild.id]
    
    if not guild_exchanges:
        return await ctx.send("📜 لا توجد أي طلبات تبديل مسجلة في هذا السيرفر حتى الآن.")
    
    recent = guild_exchanges[-10:]
    lines = []
    for r in recent:
        status_emoji = "🟢" if r['status'] == "accepted" else ("🔴" if r['status'] == "rejected" else "🟡")
        lines.append(f"{status_emoji} **#{r['id']}** | العضو: <@{r['user_id']}> | المبلغ: `{r['amount']:,}` {coin} 👈 `{r.get('received_amount', 0):,.1f}` {r['target_type']}")
        
    embed = discord.Embed(
        title="📜 **آخر طلبات التبديل في السيرفر**",
        description="\n".join(lines),
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.tree.command(name="show_exchange", description="عرض آخر طلبات التبديل في السيرفر")
async def show_exchange_slash(interaction: discord.Interaction):
    data = load_data()
    exchanges = data.get("exchanges", {})
    coin = get_guild_coin(interaction.guild.id)
    
    guild_exchanges = [req for req in exchanges.values() if req.get("guild_id") == interaction.guild.id]
    
    if not guild_exchanges:
        return await interaction.response.send_message("📜 لا توجد أي طلبات تبديل مسجلة في هذا السيرفر حتى الآن.", ephemeral=True)
    
    recent = guild_exchanges[-10:]
    lines = []
    for r in recent:
        status_emoji = "🟢" if r['status'] == "accepted" else ("🔴" if r['status'] == "rejected" else "🟡")
        lines.append(f"{status_emoji} **#{r['id']}** | العضو: <@{r['user_id']}> | المبلغ: `{r['amount']:,}` {coin} 👈 `{r.get('received_amount', 0):,.1f}` {r['target_type']}")
        
    embed = discord.Embed(
        title="📜 **آخر طلبات التبديل في السيرفر**",
        description="\n".join(lines),
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)

@bot.command(name="see_exchange")
async def see_exchange_cmd(ctx):
    data = load_data()
    exchanges = data.get("exchanges", {})
    coin = get_guild_coin(ctx.guild.id)
    
    user_exchanges = [req for req in exchanges.values() if req.get("guild_id") == ctx.guild.id and req.get("user_id") == ctx.author.id]
    
    if not user_exchanges:
        return await ctx.send(f"📜 {ctx.author.mention}, ليس لديك أي طلبات تبديل مسجلة باسمك في هذا السيرفر.")
    
    recent = user_exchanges[-10:]
    lines = []
    for r in recent:
        status_emoji = "🟢" if r['status'] == "accepted" else ("🔴" if r['status'] == "rejected" else "🟡")
        status_text = "مقبول" if r['status'] == "accepted" else ("مرفوض" if r['status'] == "rejected" else "قيد الانتظار")
        lines.append(f"{status_emoji} **#{r['id']}** | المبلغ: `{r['amount']:,}` {coin} 👈 `{r.get('received_amount', 0):,.1f}` {r['target_type']} | الحالة: **{status_text}**")
        
    embed = discord.Embed(
        title=f"📜 **سجل طلبات التبديل الخاصة بك ({ctx.author.display_name})**",
        description="\n".join(lines),
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.tree.command(name="see_exchange", description="عرض آخر طلبات التبديل الخاصة بك أنت فقط")
async def see_exchange_slash(interaction: discord.Interaction):
    data = load_data()
    exchanges = data.get("exchanges", {})
    coin = get_guild_coin(interaction.guild.id)
    
    user_exchanges = [req for req in exchanges.values() if req.get("guild_id") == interaction.guild.id and req.get("user_id") == interaction.user.id]
    
    if not user_exchanges:
        return await interaction.response.send_message(f"📜 {interaction.user.mention}, ليس لديك أي طلبات تبديل مسجلة باسمك في هذا السيرفر.", ephemeral=True)
    
    recent = user_exchanges[-10:]
    lines = []
    for r in recent:
        status_emoji = "🟢" if r['status'] == "accepted" else ("🔴" if r['status'] == "rejected" else "🟡")
        status_text = "مقبول" if r['status'] == "accepted" else ("مرفوض" if r['status'] == "rejected" else "قيد الانتظار")
        lines.append(f"{status_emoji} **#{r['id']}** | المبلغ: `{r['amount']:,}` {coin} 👈 `{r.get('received_amount', 0):,.1f}` {r['target_type']} | الحالة: **{status_text}**")
        
    embed = discord.Embed(
        title=f"📜 **سجل طلبات التبديل الخاصة بك ({interaction.user.display_name})**",
        description="\n".join(lines),
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.command(name="exchange_stats")
async def exchange_stats_cmd(ctx):
    data = load_data()
    exchanges = data.get("exchanges", {})
    coin = get_guild_coin(ctx.guild.id)
    
    successful_count = 0
    total_coins_exchanged = 0
    
    for req_id, req_info in exchanges.items():
        if req_info.get("guild_id") == ctx.guild.id and req_info.get("status") == "accepted":
            successful_count += 1
            total_coins_exchanged += req_info.get("amount", 0)
            
    embed = discord.Embed(
        title="📊 **إحصائيات التبديلات بالخادم**",
        color=discord.Color.blue()
    )
    embed.add_field(name="✅ عدد العمليات الناجحة", value=f"`{successful_count:,}` عملية", inline=False)
    embed.add_field(name="🪙 إجمالي العملات المتبدلة", value=f"`{total_coins_exchanged:,}` {coin}", inline=False)
    await ctx.send(embed=embed)

@bot.tree.command(name="exchange_stats", description="عرض عدد العمليات الناجحة والعملات المتبدلة للسيرفر")
async def exchange_stats_slash(interaction: discord.Interaction):
    data = load_data()
    exchanges = data.get("exchanges", {})
    coin = get_guild_coin(interaction.guild.id)
    
    successful_count = 0
    total_coins_exchanged = 0
    
    for req_id, req_info in exchanges.items():
        if req_info.get("guild_id") == interaction.guild.id and req_info.get("status") == "accepted":
            successful_count += 1
            total_coins_exchanged += req_info.get("amount", 0)
            
    embed = discord.Embed(
        title="📊 **إحصائيات التبديلات بالخادم**",
        color=discord.Color.blue()
    )
    embed.add_field(name="✅ عدد العمليات الناجحة", value=f"`{successful_count:,}` عملية", inline=False)
    embed.add_field(name="🪙 إجمالي العملات المتبدلة", value=f"`{total_coins_exchanged:,}` {coin}", inline=False)
    await interaction.response.send_message(embed=embed)

async def handle_exchange_action(ctx_or_interaction, req_id: int, action: str, reason: str = "لم يحدد سبب"):
    user = ctx_or_interaction.user if hasattr(ctx_or_interaction, 'user') else ctx_or_interaction.author
    guild = ctx_or_interaction.guild

    if not is_admin(user.id, guild):
        msg = "❌ هذا الأمر مخصص للإدارة فقط!"
        if hasattr(ctx_or_interaction, 'response'): await ctx_or_interaction.response.send_message(msg, ephemeral=True)
        else: await ctx.send(msg)
        return

    req_data = get_exchange_request(req_id)
    if not req_data:
        msg = f"❌ لم يتم العثور على طلب تبديل برقم التعامل #{req_id}!"
        if hasattr(ctx_or_interaction, 'response'): await ctx_or_interaction.response.send_message(msg, ephemeral=True)
        else: await ctx.send(msg)
        return

    if req_data["status"] != "pending":
        msg = f"⚠️ هذا الطلب #{req_id} تمت معالجته مسبقاً ({req_data['status']})!"
        if hasattr(ctx_or_interaction, 'response'): await ctx_or_interaction.response.send_message(msg, ephemeral=True)
        else: await ctx.send(msg)
        return

    target_user_id = req_data["user_id"]
    target_member = guild.get_member(target_user_id) or await bot.fetch_user(target_user_id)
    coin = get_guild_coin(guild.id)
    _, delivery_room_id = get_exchange_rooms(guild.id)

    amount_formatted = f"{req_data['amount']:,}"
    recv_formatted = f"{req_data.get('received_amount', req_data['amount']):,}"
    target_coin = req_data['target_type']

    if action == "accept":
        update_exchange_status(req_id, "accepted")
        response_text = f"✅ **تم قبول طلب التبديل #{req_id} بنجاح بواسطة {user.display_name}!**"
        
        if delivery_room_id:
            delivery_channel = guild.get_channel(delivery_room_id)
            if delivery_channel:
                msg_format = f"🎉 تم بنجاح تبديل `{amount_formatted}` **{coin}** مقابل `{recv_formatted}` من عملة **{target_coin}** لـ {target_member.mention}."
                await delivery_channel.send(msg_format)

        try:
            await target_member.send(f"🎉 **تم قبول طلب التبديل الخاص بك #{req_id} بنجاح!**\n`{amount_formatted}` {coin} مقابل `{recv_formatted}` {target_coin}.")
        except Exception: pass

    else:
        update_exchange_status(req_id, "rejected")
        update_balance(target_user_id, req_data["amount"])
        response_text = f"❌ تم رفض طلب التبديل #{req_id}. السبب: {reason}. وتم إرجاع `{amount_formatted}` {coin}."
        
        if delivery_room_id:
            delivery_channel = guild.get_channel(delivery_room_id)
            if delivery_channel:
                msg_format = f"❌ تم رفض تبديل `{amount_formatted}` **{coin}** مقابل `{recv_formatted}` من عملة **{target_coin}** لـ {target_member.mention}، وتم إرجاع العملات."
                await delivery_channel.send(msg_format)

        try:
            await target_member.send(f"❌ تم رفض طلب التبديل #{req_id}.\nالسبب: {reason}\nتمت إعادة `{amount_formatted}` {coin} إلى رصيدك.")
        except Exception: pass

    if hasattr(ctx_or_interaction, 'response'):
        await ctx_or_interaction.response.send_message(response_text)
    else:
        await ctx.send(response_text)

@bot.command(name="exchange_accept", aliases=["accept_exchange"])
async def exchange_accept_cmd(ctx, req_id: int):
    await handle_exchange_action(ctx, req_id, "accept")

@bot.tree.command(name="exchange_accept", description="قبول طلب تبديل برقم التعامل")
@app_commands.describe(req_id="رقم التعامل")
async def exchange_accept_slash(interaction: discord.Interaction, req_id: int):
    await handle_exchange_action(interaction, req_id, "accept")

@bot.command(name="exchange_deny", aliases=["deny_exchange"])
async def exchange_deny_cmd(ctx, req_id: int, *, reason: str = "لم يحدد سبب"):
    await handle_exchange_action(ctx, req_id, "deny", reason)

@bot.tree.command(name="exchange_deny", description="رفض طلب تبديل برقم التعامل وإرجاع العملات")
@app_commands.describe(req_id="رقم التعامل", reason="سبب الرفض اختياري")
async def exchange_deny_slash(interaction: discord.Interaction, req_id: int, reason: str = "لم يحدد سبب"):
    await handle_exchange_action(interaction, req_id, "deny", reason)

# ==============================================================================
# 🎡 11. لعبة روليت الإقصاء وزر الاعتماد
# ==============================================================================
async def send_game_reward_receipt(member, amount, guild_id, game_name, balance_before, balance_after):
    """إيصال خاص موحد للفائزين في الجيف أواي والروليت."""
    coin = get_guild_coin(guild_id)
    embed = discord.Embed(
        title="🏆 تم استلام جائزتك",
        description=(
            f"مبروك {member.mention}!\n"
            f"تم استلام `{format_amount(amount)}` {coin} لأنك فزت في **{game_name}**."
        ),
        color=discord.Color.gold(),
        timestamp=datetime.datetime.now(datetime.timezone.utc)
    )
    embed.add_field(name="الرصيد قبل", value=f"`{format_amount(balance_before)}` {coin}", inline=True)
    embed.add_field(name="الرصيد بعد", value=f"`{format_amount(balance_after)}` {coin}", inline=True)
    embed.set_footer(text="Rize Rewards • مبروك الفوز")
    try:
        await member.send(embed=embed)
    except Exception:
        pass


class ConditionalRerollView(discord.ui.View):
    def __init__(self, prize, condition, guild_id, winner_number, candidate_ids, excluded_ids):
        super().__init__(timeout=None)
        self.prize=int(prize); self.condition=condition; self.guild_id=int(guild_id)
        self.winner_number=int(winner_number); self.candidate_ids=[int(x) for x in candidate_ids]
        self.excluded_ids={int(x) for x in excluded_ids}; self.used=False

    async def interaction_check(self, interaction):
        if not is_games_controller(interaction.user.id, interaction.guild):
            await interaction.response.send_message("❌ لمسؤولي الألعاب والمالك فقط.",ephemeral=True); return False
        if self.used:
            await interaction.response.send_message("⚠️ تم استخدام إعادة السحب بالفعل.",ephemeral=True); return False
        return True

    @discord.ui.button(label="إعادة السحب",emoji="🎲",style=discord.ButtonStyle.primary,custom_id="rize:conditional_reroll")
    async def reroll(self, interaction, button):
        members=[interaction.guild.get_member(uid) for uid in self.candidate_ids if uid not in self.excluded_ids]
        members=[m for m in members if m and not m.bot]
        if not members:
            self.used=True; button.disabled=True
            return await interaction.response.edit_message(content="❌ لا يوجد مشاركون آخرون متاحون.",embed=None,view=self)
        if get_guild_budget(self.guild_id) < self.prize:
            return await interaction.response.send_message("❌ ميزانية السيرفر لا تكفي لإعادة السحب.",ephemeral=True)
        self.used=True; button.disabled=True
        update_guild_budget(self.guild_id,-self.prize)
        winner=random.choice(members)
        excluded=list(self.excluded_ids|{winner.id})
        await interaction.response.edit_message(content=f"🎲 تمت إعادة السحب. الفائز البديل: {winner.mention}",embed=None,view=self)
        await interaction.channel.send(
            f"تحقق من شرط العضو {winner.mention}\n**الفائز البديل رقم {self.winner_number}:** {winner.mention}\n**الشرط:** {self.condition}\n**الجائزة:** `{self.prize:,}` {get_guild_coin(self.guild_id)}",
            view=SingleWinnerVerifyView(winner,self.prize,self.condition,self.guild_id,self.winner_number,"الجيف أواي",self.candidate_ids,excluded)
        )


class SingleWinnerVerifyView(discord.ui.View):
    def __init__(self,winner,prize,condition,guild_id,winner_number,event_name="المسابقة",candidate_ids=None,excluded_ids=None):
        super().__init__(timeout=None)
        self.winner=winner; self.prize=int(prize); self.condition=condition; self.guild_id=int(guild_id)
        self.winner_number=int(winner_number); self.event_name=event_name
        self.candidate_ids=[int(x) for x in (candidate_ids or [])]; self.excluded_ids={int(x) for x in (excluded_ids or [])}; self.resolved=False

    async def interaction_check(self,interaction):
        if not is_games_controller(interaction.user.id,interaction.guild):
            await interaction.response.send_message("❌ لمسؤولي الألعاب فقط.",ephemeral=True); return False
        if self.resolved:
            await interaction.response.send_message("⚠️ تم اتخاذ القرار بالفعل.",ephemeral=True); return False
        return True

    @discord.ui.button(label="استلام",emoji="✅",style=discord.ButtonStyle.success,custom_id="rize:verify:approve")
    async def approve(self,interaction,button):
        self.resolved=True; before=get_balance(self.winner.id); update_balance(self.winner.id,self.prize); after=get_balance(self.winner.id)
        for x in self.children: x.disabled=True
        coin=get_guild_coin(self.guild_id)
        await interaction.response.edit_message(content=f"✅ تم تسليم `{self.prize:,}` {coin} إلى {self.winner.mention} بواسطة {interaction.user.mention}.",embed=None,view=self)
        await send_game_reward_receipt(self.winner,self.prize,self.guild_id,self.event_name,before,after)

    @discord.ui.button(label="عدم الاستلام",emoji="❌",style=discord.ButtonStyle.danger,custom_id="rize:verify:reject")
    async def reject(self,interaction,button):
        self.resolved=True; update_guild_budget(self.guild_id,self.prize); coin=get_guild_coin(self.guild_id)
        conditional=(self.event_name=="الجيف أواي" and self.condition.strip().lower() not in ["","بدون شرط","لا يوجد شرط","none","no condition"] and self.candidate_ids)
        if conditional:
            view=ConditionalRerollView(self.prize,self.condition,self.guild_id,self.winner_number,self.candidate_ids,list(self.excluded_ids|{self.winner.id}))
            await interaction.response.edit_message(content=f"❌ لم يتم تسليم {self.winner.mention}. تمت إعادة `{self.prize:,}` {coin} للميزانية.\nاضغط 🎲 **إعادة السحب** لو أردت، ولن يحدث سحب تلقائي.",embed=None,view=view)
        else:
            for x in self.children: x.disabled=True
            await interaction.response.edit_message(content=f"❌ لم يتم التسليم إلى {self.winner.mention}. تمت إعادة الجائزة للميزانية.",embed=None,view=self)


async def send_individual_winner_checks(channel,winners,prize,condition,guild_id,event_name,all_candidates=None):
    mentions="، ".join(w.mention for w in winners)
    await channel.send(f"🎊 **الفائزون في {event_name}:** {mentions}!\n⚠️ **الشرط:** {condition}\nفي انتظار مراجعة الإدارة للتسليم.")
    candidates=[m.id for m in (all_candidates or []) if not m.bot]; excluded=[w.id for w in winners]
    for i,winner in enumerate(winners,1):
        await channel.send(
            f"تحقق من شرط العضو {winner.mention}\n**الفائز رقم {i}:** {winner.mention}\n**الشرط:** {condition}\n**الجائزة:** `{prize:,}` {get_guild_coin(guild_id)}",
            view=SingleWinnerVerifyView(winner,prize,condition,guild_id,i,event_name,candidates if event_name=="الجيف أواي" else [],excluded)
        )


class EliminateSelect(discord.ui.Select):
    def __init__(self, current_turn: discord.Member, players: List[discord.Member]):
        self.current_turn = current_turn
        options = [discord.SelectOption(label=p.display_name, value=str(p.id)) for p in players if p.id != current_turn.id]
        super().__init__(placeholder="🎯 اختر عضواً مستهدفاً لإقصائه...", options=options[:25], row=0)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.current_turn.id:
            return await interaction.response.send_message("❌ ليس دورك للاختيار!", ephemeral=True)
        
        target_id = int(self.values[0])
        self.view.chosen_target = interaction.guild.get_member(target_id)
        await interaction.response.send_message(f"🎯 اخترت إقصاء {self.view.chosen_target.mention}!", ephemeral=True)
        self.view.stop()

class EliminateView(discord.ui.View):
    def __init__(self, current_turn: discord.Member, players: List[discord.Member]):
        super().__init__(timeout=25)
        self.current_turn = current_turn
        self.players = players
        self.chosen_target = None
        self.action_type = "target"
        
        self.add_item(EliminateSelect(current_turn, players))

    @discord.ui.button(label="إقصاء عشوائي 🎲", style=discord.ButtonStyle.primary, row=1)
    async def random_eliminate(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.current_turn.id:
            return await interaction.response.send_message("❌ ليس دورك للاختيار!", ephemeral=True)
        
        possible_targets = [p for p in self.players if p.id != self.current_turn.id]
        if possible_targets:
            self.chosen_target = random.choice(possible_targets)
            self.action_type = "random"
            await interaction.response.send_message(f"🎲 تم اختيار إقصاء عشوائي لـ {self.chosen_target.mention}!", ephemeral=True)
        self.stop()

    @discord.ui.button(label="انسحاب فوراً 🚪", style=discord.ButtonStyle.danger, row=1)
    async def self_forfeit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.current_turn.id:
            return await interaction.response.send_message("❌ ليس دورك للانسحاب!", ephemeral=True)
        
        self.chosen_target = self.current_turn
        self.action_type = "forfeit"
        await interaction.response.send_message("🚪 اخترت الانسحاب من اللعبة وإقصاء نفسك!", ephemeral=True)
        self.stop()

class JoinRouletteView(discord.ui.View):
    def __init__(self, host: discord.User, amount: int, condition: str, guild_id: int, msg_to_update: discord.Message = None):
        super().__init__(timeout=45)
        self.host = host
        self.amount = amount
        self.condition = condition
        self.guild_id = guild_id
        self.players: List[discord.Member] = []
        self.msg_to_update = msg_to_update

    @discord.ui.button(label="دخول في الروليت 🎲", style=discord.ButtonStyle.success)
    async def join_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        if member_is_fully_blacklisted(interaction.user):
            set_balance(interaction.user.id,0)
            return await interaction.response.send_message(await blacklist_message_for_guild(interaction.guild),ephemeral=True)
        if interaction.user in self.players:
            return await interaction.response.send_message("⚠️ أنت مشترك بالفعل!", ephemeral=True)
        if len(self.players) >= 50:
            return await interaction.response.send_message("❌ اكتمل العدد الأقصى (50 شخص)!", ephemeral=True)
        
        self.players.append(interaction.user)
        await interaction.response.send_message(f"✅ تم انضمامك للروليت! (العدد الحالي: {len(self.players)}/50)", ephemeral=True)
        await self.update_embed(interaction.guild)

    @discord.ui.button(label="خروج من اللعبة ❌", style=discord.ButtonStyle.danger)
    async def leave_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in self.players:
            return await interaction.response.send_message("⚠️ أنت غير مشترك باللعبة للانسحاب!", ephemeral=True)
        
        self.players.remove(interaction.user)
        await interaction.response.send_message("🚪 تم انسحابك وخروجك من الروليت بنجاح.", ephemeral=True)
        await self.update_embed(interaction.guild)

    async def update_embed(self, guild):
        if self.msg_to_update:
            try:
                coin = get_guild_coin(self.guild_id)
                players_list_str = "\n".join(f"• {p.mention}" for p in self.players) if self.players else "لا يوجد حالياً"
                embed = discord.Embed(
                    title="🎡 **بدء روليت الإقصاء الجماعية!** 🎡",
                    description=(
                        f"💰 **المكافأة النهائية:** `{self.amount:,}` {coin} 🪙 (تُخصم من ميزانية السيرفر)\n"
                        f"📜 **الشرط:** {self.condition}\n"
                        f"⏰ **وقت الدخول:** 45 ثانية\n"
                        f"👥 **عدد المشاركين:** `{len(self.players)}/50` لاعبين\n\n"
                        f"📝 **المشتركين:**\n{players_list_str}\n\n"
                        f"اضغط على الأزرار بالأسفل للدخول أو الخروج!"
                    ),
                    color=discord.Color.purple()
                )
                if guild.icon: embed.set_thumbnail(url=guild.icon.url)
                await self.msg_to_update.edit(embed=embed)
            except Exception: pass

async def start_elimination_roulette(channel,guild,host,prize,condition):
    coin=get_guild_coin(guild.id); budget=get_guild_budget(guild.id)
    if prize>budget: return await channel.send(f"❌ الميزانية لا تكفي. المتاح {code_number(budget)} {coin}.")
    update_guild_budget(guild.id,-prize)
    embed=discord.Embed(title="🎯 Roulette | لعبة الروليت 🎯",description=(
        f"الجائزة للفائز الأخير: {code_number(prize)} {coin}\n"
        f"الحد الأدنى للبدء: {code_number(2)} لاعبين\n"
        f"وقت التسجيل: {code_number(45)} ثانية"),color=discord.Color.red())
    view=JoinRouletteView(host,prize,condition,guild.id)
    msg=await channel.send(embed=embed,view=view); view.msg_to_update=msg
    active_roulettes[guild.id]={"msg":msg,"active":True}
    await asyncio.sleep(45)
    players=list(view.players)
    if len(players)<2:
        update_guild_budget(guild.id,prize); active_roulettes.pop(guild.id,None)
        return await channel.send("❌ تم إلغاء الروليت وإعادة الجائزة لعدم وجود لاعبين كافيين.")
    avatar_bytes=await guild.icon.read() if guild.icon else None
    round_number=1
    while len(players)>2:
        current=random.choice(players)
        wheel=create_wheel_image([p.display_name for p in players],avatar_bytes,current.display_name)
        await channel.send(
            f"🎡 الجولة {code_number(round_number)}: تم تدوير العجلة ووقفت على {current.mention}!",
            file=discord.File(wheel,filename=f"roulette_{round_number}.png"))
        view_action=EliminateView(current,players)
        players_text="\n".join(f"• {p.mention}" for p in players)
        await channel.send(
            f"🎲 {current.mention} معك {code_number(25)} ثانية لاختيار قرارك.\n"
            f"**اللاعبون المتبقون:**\n{players_text}",view=view_action)
        await view_action.wait()
        if view_action.chosen_target:
            eliminated=view_action.chosen_target
            if eliminated in players: players.remove(eliminated)
            action_label={"random":"اختيار عشوائي","forfeit":"انسحاب","target":"اختيار محدد"}.get(view_action.action_type,"اختيار محدد")
            await channel.send(f"🎲 **{action_label}:** تم إقصاء {eliminated.mention}. المتبقون: {code_number(len(players))}")
        else:
            if current in players: players.remove(current)
            await channel.send(f"⏰ لم يتم الاختيار؛ تم إقصاء {current.mention} تلقائياً.")
        round_number+=1
    winner=random.choice(players)
    final=create_wheel_image([p.display_name for p in players],avatar_bytes,winner.display_name)
    await channel.send(f"🏆 العجلة النهائية وقفت على {winner.mention}!",file=discord.File(final,filename="roulette_final.png"))
    clean_condition=condition.strip().lower()
    if clean_condition in ["لا يوجد شرط","بدون شرط","none","no condition",""]:
        before=get_balance(winner.id); update_balance(winner.id,prize); after=get_balance(winner.id)
        await channel.send(
            f"👑 مبروك للفائز بالروليت: {winner.mention}!\n"
            f"تم تسليم {code_number(prize)} {coin} إلى رصيدك تلقائياً."
        )
        await send_game_reward_receipt(winner,prize,guild.id,"الروليت",before,after)
    else:
        await channel.send(
            f"🎊 الفائز بالروليت: {winner.mention}!\n"
            f"⚠️ الشرط: `{condition}`\n"
            "في انتظار مراجعة الإدارة للتسليم."
        )
        await send_individual_winner_checks(
            channel,[winner],prize,condition,guild.id,"الروليت",all_candidates=players
        )
    active_roulettes.pop(guild.id,None)


@bot.command(name="roulette", aliases=["r"])
async def roulette_cmd(ctx, amount: str, *, condition: str = "بدون شرط"):
    if not is_games_controller(ctx.author.id, ctx.guild):
        return await ctx.send("❌ هذا الأمر مخصص للمسؤولين المعتمدين!")
    parsed_prize = parse_number(amount)
    if parsed_prize is None or parsed_prize <= 0: return await ctx.send("❌ مبلغ غير صحيح!")
    await start_elimination_roulette(ctx.channel, ctx.guild, ctx.author, parsed_prize, condition)

@bot.tree.command(name="roulette", description="بدء لعبة روليت الإقصاء بالشرط (تخصم من ميزانية السيرفر)")
async def roulette_slash(interaction: discord.Interaction, amount: str, condition: str = "بدون شرط"):
    if not is_games_controller(interaction.user.id, interaction.guild):
        return await interaction.response.send_message("❌ هذا الأمر مخصص للمسؤولين المعتمدين!", ephemeral=True)
    parsed_prize = parse_number(amount)
    if parsed_prize is None or parsed_prize <= 0: return await interaction.response.send_message("❌ مبلغ غير صحيح!", ephemeral=True)
    await interaction.response.send_message("🎰 جاري تجهيز وبدء الروليت...", ephemeral=True)
    await start_elimination_roulette(interaction.channel, interaction.guild, interaction.user, parsed_prize, condition)

@bot.command(name="stop_roulette")
async def stop_roulette_cmd(ctx):
    if not is_games_controller(ctx.author.id, ctx.guild): return await ctx.send("❌ للإدارة العليا فقط!")
    if ctx.guild.id in active_roulettes:
        active_roulettes[ctx.guild.id]["active"] = False
        active_roulettes.pop(ctx.guild.id, None)
        await ctx.send("🛑 **تم إيقاف الروليت الحالية فوراً بنجاح!**")
    else:
        await ctx.send("❌ لا توجد روليت نشطة حالياً في هذا السيرفر لتوقفها.")

@bot.tree.command(name="stop_roulette", description="إيقاف لعبة الروليت الحالية فوراً")
async def stop_roulette_slash(interaction: discord.Interaction):
    if not is_games_controller(interaction.user.id, interaction.guild): return await interaction.response.send_message("❌ للإدارة العليا فقط!", ephemeral=True)
    if interaction.guild.id in active_roulettes:
        active_roulettes[interaction.guild.id]["active"] = False
        active_roulettes.pop(interaction.guild.id, None)
        await interaction.response.send_message("🛑 **تم إيقاف الروليت الحالية فوراً بنجاح!**")
    else:
        await interaction.response.send_message("❌ لا توجد روليت نشطة حالياً في هذا السيرفر.", ephemeral=True)

# ==============================================================================
# 🎉 12. الجيف أواي والسيطرة والإيقاف الفوري
# ==============================================================================
async def finish_giveaway(msg, prize, winners_count, condition, host_user=None):
    try:
        msg=await msg.channel.fetch_message(msg.id)
    except Exception:
        remove_runtime_giveaway(msg.id); active_giveaways.pop(msg.id,None); return
    coin=get_guild_coin(msg.guild.id)
    users=[]
    for reaction in msg.reactions:
        if str(reaction.emoji)=="🎉":
            async for user in reaction.users():
                if not user.bot and user not in users:
                    member=msg.guild.get_member(user.id)
                    if not member_is_fully_blacklisted(member):
                        users.append(user)
    ended_data={
        "guild_id":msg.guild.id,"prize":prize,"winners":winners_count,
        "condition":condition,"end_timestamp":datetime.datetime.now(datetime.timezone.utc).timestamp()
    }
    if not users:
        refund=prize*winners_count
        update_guild_budget(msg.guild.id,refund)
        ended_embed=build_live_giveaway_embed(ended_data,0,ended=True)
        ended_embed.add_field(name="النتيجة",value=f"لم يشترك أحد. تمت إعادة {code_number(refund)} {coin} لميزانية السيرفر.",inline=False)
        await msg.edit(content=None,embed=ended_embed)
        remove_runtime_giveaway(msg.id); active_giveaways.pop(msg.id,None); return

    winners=random.sample(users,min(len(users),winners_count))
    mentions="، ".join(user.mention for user in winners)
    participant_count=len(users)
    ended_embed=build_live_giveaway_embed(ended_data,participant_count,ended=True)
    ended_embed.add_field(name="🏆 الفائزون",value=mentions,inline=False)
    await msg.edit(content=None,embed=ended_embed)

    clean=condition.strip().lower()
    if clean in ["لا يوجد شرط","بدون شرط","none","no condition",""]:
        for winner in winners:
            before=get_balance(winner.id)
            update_balance(winner.id,prize)
            after=get_balance(winner.id)
            await send_game_reward_receipt(winner,prize,msg.guild.id,"الجيف أواي",before,after)
        await msg.channel.send(
            f"🎊 مبارك للفائزين: {mentions}!\n"
            f"تم تسليم {code_number(prize)} {coin} تلقائياً لكل فائز."
        )
    else:
        await msg.channel.send(
            f"🎊 الفائزون بالقرعة: {mentions}!\n"
            f"⚠️ **الشرط:** `{condition}`\n"
            "في انتظار مراجعة الإدارة للتسليم."
        )
        await send_individual_winner_checks(
            msg.channel,winners,prize,condition,msg.guild.id,"الجيف أواي",all_candidates=users
        )
    remove_runtime_giveaway(msg.id)
    active_giveaways.pop(msg.id,None)


async def giveaway_worker(message_id):
    data = load_runtime().get("active_giveaways", {}).get(str(message_id))
    if not data:
        return
    channel = bot.get_channel(int(data["channel_id"]))
    if channel is None:
        try: channel = await bot.fetch_channel(int(data["channel_id"]))
        except Exception:
            remove_runtime_giveaway(message_id); return
    try: msg = await channel.fetch_message(int(message_id))
    except Exception:
        remove_runtime_giveaway(message_id); return
    remaining = float(data["end_timestamp"]) - datetime.datetime.now(datetime.timezone.utc).timestamp()
    if remaining > 0:
        await asyncio.sleep(remaining)
    latest = load_runtime().get("active_giveaways", {}).get(str(message_id))
    if not latest:
        return
    host = bot.get_user(int(data["host_id"]))
    await finish_giveaway(msg, int(data["prize"]), int(data["winners"]), data["condition"], host)


async def restore_active_giveaways():
    saved = load_runtime().get("active_giveaways", {})
    restored = 0
    for message_id, payload in list(saved.items()):
        task = asyncio.create_task(giveaway_worker(int(message_id)))
        active_giveaways[int(message_id)] = {
            **payload,
            "task": task,
            "restored": True
        }
        restored += 1
    if restored:
        print(f"♻️ تمت استعادة {restored} Giveaway من runtime.json")


async def count_giveaway_participants(message):
    """عدد المشاركين الحقيقي من تفاعل 🎉، مع استبعاد حساب البوت."""
    try:
        fresh_message = await message.channel.fetch_message(message.id)
    except Exception:
        fresh_message = message
    for reaction in fresh_message.reactions:
        if str(reaction.emoji) != "🎉":
            continue
        # reaction.count متاح فوراً حتى لو تعذر جلب قائمة المستخدمين.
        count = int(reaction.count or 0)
        try:
            bot_reacted = await reaction.users().get(id=bot.user.id)
            if bot_reacted:
                count -= 1
        except Exception:
            # البوت يضيف تفاعل الدخول بنفسه، لذلك نخصمه كخيار احتياطي.
            count -= 1
        return max(0, count)
    return 0


def build_live_giveaway_embed(data,participant_count,ended=False):
    coin=get_guild_coin(int(data["guild_id"]))
    timestamp=int(float(data["end_timestamp"]))
    condition=str(data.get("condition") or "لا يوجد شرط")
    status_line="\nالحالة: انتهى السحب" if ended else ""
    embed=discord.Embed(
        title=f"🎉 سحب على {coin}! 🎉",
        description=(
            f"الجائزة لكل فائز: {code_number(int(data['prize']))} {coin}\n"
            f"عدد الفائزين: `{int(data['winners'])}`\n"
            f"المشاركين: `{participant_count}`\n"
            f"الشرط: {condition}\n"
            f"ينتهي: <t:{timestamp}:R>{status_line}\n\n"
            "تفاعل بالرياكشن 🎉 للدخول في السحب!"
        ),color=discord.Color.from_rgb(168,85,247))
    return embed


async def update_giveaway_participants(message_id):
    # تم تعطيل التحديث الدوري لتجنب Discord rate limits.
    # عدد المشاركين يتحدث فقط عند إضافة/إزالة رياكشن 🎉.
    return


async def create_persistent_giveaway(channel, guild, host, prize, winners, seconds, condition):
    coin = get_guild_coin(guild.id)
    total = prize * winners
    budget = get_guild_budget(guild.id)
    if total > budget:
        return None, f"❌ الميزانية لا تكفي. المطلوب `{total:,}` والمتاح `{budget:,}` {coin}."
    update_guild_budget(guild.id, -total)
    end_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=seconds)
    timestamp = int(end_time.timestamp())
    initial_data = {
        "guild_id": guild.id,
        "prize": prize,
        "winners": winners,
        "condition": condition,
        "end_timestamp": end_time.timestamp()
    }
    giveaway_embed = build_live_giveaway_embed(initial_data, 0)
    msg = await channel.send(embed=giveaway_embed)
    await msg.add_reaction("🎉")
    payload = {
        "guild_id": guild.id, "channel_id": channel.id, "message_id": msg.id,
        "host_id": host.id, "prize": prize, "winners": winners,
        "condition": condition, "end_timestamp": end_time.timestamp()
    }
    set_runtime_giveaway(msg.id, payload)
    task = asyncio.create_task(giveaway_worker(msg.id))
    active_giveaways[msg.id] = {
        **payload,
        "task": task
    }
    return msg, None


@bot.command(name="giveaway")
async def giveaway_cmd(ctx, prize: str, winners: int, duration: str, *, condition: str = "لا يوجد شرط"):
    if not is_games_controller(ctx.author.id, ctx.guild): return await ctx.send("❌ مخصص لمسؤولي الألعاب.")
    amount = parse_number(prize); seconds = parse_time(duration)
    if not amount or amount <= 0 or winners <= 0 or seconds <= 0: return await ctx.send("❌ تحقق من الجائزة وعدد الفائزين والمدة.")
    msg, error = await create_persistent_giveaway(ctx.channel, ctx.guild, ctx.author, amount, winners, seconds, condition)
    if error: await ctx.send(error)
    else: await ctx.send(f"✅ تم إنشاء Giveaway دائم. ID: `{msg.id}`")


@bot.tree.command(name="giveaway", description="إنشاء سحب منظم مع عدد مشاركين مباشر")
async def giveaway_slash(interaction: discord.Interaction, prize: str, winners: int, duration: str, condition: str = "لا يوجد شرط"):
    if not is_games_controller(interaction.user.id, interaction.guild): return await interaction.response.send_message("❌ مخصص لمسؤولي الألعاب.", ephemeral=True)
    amount = parse_number(prize); seconds = parse_time(duration)
    if not amount or amount <= 0 or winners <= 0 or seconds <= 0: return await interaction.response.send_message("❌ تحقق من الجائزة وعدد الفائزين والمدة.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    msg, error = await create_persistent_giveaway(interaction.channel, interaction.guild, interaction.user, amount, winners, seconds, condition)
    if error: await interaction.followup.send(error, ephemeral=True)
    else: await interaction.followup.send(f"✅ تم إنشاء Giveaway دائم. ID: `{msg.id}`", ephemeral=True)


async def stop_saved_giveaway(channel, message_id):
    data = load_runtime().get("active_giveaways", {}).get(str(message_id))
    if not data: return False
    running = active_giveaways.pop(message_id, None)
    if running and running.get("task"):
        running["task"].cancel()
    try: msg = await channel.fetch_message(message_id)
    except Exception: return False
    host = bot.get_user(int(data["host_id"]))
    await finish_giveaway(msg, int(data["prize"]), int(data["winners"]), data["condition"], host)
    return True


@bot.command(name="stopgiveaway")
async def stop_giveaway_cmd(ctx, message_id: str):
    if not is_games_controller(ctx.author.id, ctx.guild): return await ctx.send("❌ مخصص لمسؤولي الألعاب.")
    try: success = await stop_saved_giveaway(ctx.channel, int(message_id))
    except ValueError: success = False
    await ctx.send("⏹️ تم إنهاء الجيف أواي." if success else "❌ لم يتم العثور على Giveaway نشط بهذا الرقم.")


@bot.tree.command(name="stopgiveaway", description="إنهاء السحب فوراً واختيار الفائزين")
async def stop_giveaway_slash(interaction: discord.Interaction, message_id: str):
    if not is_games_controller(interaction.user.id, interaction.guild): return await interaction.response.send_message("❌ مخصص لمسؤولي الألعاب.", ephemeral=True)
    try: success = await stop_saved_giveaway(interaction.channel, int(message_id))
    except ValueError: success = False
    await interaction.response.send_message("⏹️ تم إنهاء الجيف أواي." if success else "❌ لم يتم العثور على Giveaway نشط بهذا الرقم.", ephemeral=True)

@bot.tree.command(name="timer", description="إنشاء مؤقت وينبهك عند انتهائه")
@app_commands.describe(duration="مثل 10s أو 5m أو 2h", note="وصف اختياري للمؤقت")
async def timer_slash(interaction: discord.Interaction, duration: str, note: Optional[str] = None):
    seconds=parse_time(duration)
    if seconds <= 0:
        return await interaction.response.send_message("❌ اكتب مدة صحيحة مثل `10s` أو `5m` أو `2h`.", ephemeral=True)
    end_ts=int(datetime.datetime.now(datetime.timezone.utc).timestamp()+seconds)
    await interaction.response.send_message(f"⏳ {interaction.user.mention} المؤقت هيخلص <t:{end_ts}:R>" + (f" • {note}" if note else ""))
    await asyncio.sleep(seconds)
    await interaction.channel.send(f"⏰ {interaction.user.mention} المؤقت خلص!" + (f" • {note}" if note else ""))


def _controller_lines(guild_id, key):
    entries=_controller_entries(load_data(),key,guild_id)
    return "\n".join((f"• <@{x['id']}>" if x.get('type')=='user' else f"• <@&{x['id']}>") for x in entries) or "لا يوجد"


def get_server_blacklist():
    return load_data().get("server_blacklist", {})


@bot.tree.command(name="remove_games", description="إزالة عضو أو رتبة من صلاحيات الألعاب")
async def remove_games(interaction: discord.Interaction, target_id: str):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ للمالك فقط.",ephemeral=True)
    try: removed=_remove_controller(interaction.guild.id,"game_controllers",int(target_id))
    except ValueError: removed=False
    await interaction.response.send_message("✅ تم الحذف." if removed else "❌ غير موجود.",ephemeral=True)


@bot.tree.command(name="remove_admin", description="إزالة عضو أو رتبة من صلاحيات الإدارة")
async def remove_admin(interaction: discord.Interaction, target_id: str):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ للمالك فقط.",ephemeral=True)
    try: removed=_remove_controller(interaction.guild.id,"admin_controllers",int(target_id))
    except ValueError: removed=False
    await interaction.response.send_message("✅ تم الحذف." if removed else "❌ غير موجود.",ephemeral=True)


@bot.tree.command(name="show_games", description="عرض أصحاب صلاحيات الألعاب")
async def show_games(interaction: discord.Interaction):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ للمالك فقط.",ephemeral=True)
    await interaction.response.send_message(f"🎮 **مسؤولو الألعاب:**\n{_controller_lines(interaction.guild.id,'game_controllers')}",ephemeral=True)


@bot.tree.command(name="show_permissions", description="عرض جميع صلاحيات البوت في السيرفر")
async def show_permissions(interaction: discord.Interaction):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ للمالك فقط.",ephemeral=True)
    text=(f"🎮 **الألعاب**\n{_controller_lines(interaction.guild.id,'game_controllers')}\n\n"
          f"🛡️ **الإدارة**\n{_controller_lines(interaction.guild.id,'admin_controllers')}\n\n"
          f"👑 **المالك المساعد**\n{_controller_lines(interaction.guild.id,'per_controllers')}")
    await interaction.response.send_message(text,ephemeral=True)


@bot.tree.command(name="blacklist_server", description="حظر سيرفر وإخراج البوت منه")
async def blacklist_server(interaction: discord.Interaction, server_id: str, reason: Optional[str] = None):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ للمالك فقط.",ephemeral=True)
    try: gid=int(server_id)
    except ValueError: return await interaction.response.send_message("❌ ID غير صحيح.",ephemeral=True)
    data=load_data(); data.setdefault("server_blacklist",{})[str(gid)]={"reason":reason or "بدون سبب","by":interaction.user.id}; save_data(data)
    guild=bot.get_guild(gid)
    await interaction.response.send_message("✅ تم حظر السيرفر وسيخرج البوت منه." if guild else "✅ تم حظر السيرفر.",ephemeral=True)
    if guild:
        try: await guild.leave()
        except Exception: pass


@bot.tree.command(name="unblacklist_server", description="إزالة سيرفر من القائمة السوداء")
async def unblacklist_server(interaction: discord.Interaction, server_id: str):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ للمالك فقط.",ephemeral=True)
    data=load_data(); removed=data.setdefault("server_blacklist",{}).pop(str(server_id),None); save_data(data)
    await interaction.response.send_message("✅ تم فك حظر السيرفر." if removed else "❌ غير موجود بالقائمة.",ephemeral=True)


@bot.tree.command(name="show_blacklist_servers", description="عرض السيرفرات المحظورة")
async def show_blacklist_servers(interaction: discord.Interaction):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ للمالك فقط.",ephemeral=True)
    items=get_server_blacklist()
    text="\n".join(f"• `{gid}` • {info.get('reason','بدون سبب')}" for gid,info in items.items()) or "لا توجد سيرفرات محظورة."
    await interaction.response.send_message(f"🚫 **السيرفرات المحظورة**\n{text}",ephemeral=True)


@bot.tree.command(name="double_spin", description="تشغيل دبل جوائز بوت الإسبن لمدة محددة")
@app_commands.describe(duration="مثل 10m أو 2h أو 1d")
async def double_spin(interaction: discord.Interaction, duration: str):
    if not is_owner(interaction.user.id):
        return await interaction.response.send_message("❌ هذا الأمر للمالك الرئيسي فقط.", ephemeral=True)
    seconds = parse_time(duration)
    if seconds <= 0:
        return await interaction.response.send_message("❌ اكتب مدة صحيحة مثل `10m` أو `2h` أو `1d`.", ephemeral=True)
    end_timestamp = datetime.datetime.now(datetime.timezone.utc).timestamp() + seconds
    set_spin_double_until(end_timestamp)
    end_int = int(end_timestamp)
    await interaction.response.send_message(
        f"🎰 تم تشغيل دبل بوت الإسبن ×2، وينتهي <t:{end_int}:R>."
    )
    asyncio.create_task(finish_double_spin_at(end_timestamp, interaction.channel_id))


@bot.tree.command(name="ungive_admin", description="إزالة أدمن بالمنشن أو الـ ID")
@app_commands.describe(member="العضو المراد إزالة صلاحياته", user_id="أو اكتب ID العضو")
async def ungive_admin(
    interaction: discord.Interaction,
    member: Optional[discord.Member] = None,
    user_id: Optional[str] = None,
):
    global ADMIN_IDS
    if not is_owner(interaction.user.id):
        return await interaction.response.send_message("❌ هذا الأمر للمالك الرئيسي فقط.", ephemeral=True)
    if bool(member) == bool(user_id):
        return await interaction.response.send_message("❌ اختر منشن عضو أو اكتب ID واحد فقط.", ephemeral=True)
    try:
        target_id = member.id if member else int(user_id)
    except (TypeError, ValueError):
        return await interaction.response.send_message("❌ الـ ID غير صحيح.", ephemeral=True)
    if target_id == PRIMARY_OWNER_ID:
        return await interaction.response.send_message("❌ لا يمكن إزالة المالك الرئيسي.", ephemeral=True)
    removed = False
    if target_id in ADMIN_IDS:
        ADMIN_IDS.remove(target_id)
        removed = True
    if _remove_controller(interaction.guild.id, "admin_controllers", target_id):
        removed = True
    data = load_data()
    data["admin_ids"] = [uid for uid in ADMIN_IDS if uid != PRIMARY_OWNER_ID]
    save_data(data)
    await interaction.response.send_message(
        f"✅ تم سحب صلاحيات الإدارة من <@{target_id}>." if removed else "❌ العضو لا يملك صلاحيات إدارة محفوظة.",
        ephemeral=True,
    )


@bot.tree.command(name="remove_all_per", description="إعادة ضبط جميع المتحكمين والإداريين مع إبقاء المالك فقط")
async def remove_all_per(interaction: discord.Interaction):
    global ADMIN_IDS, PER_DEVS
    if not is_owner(interaction.user.id):
        return await interaction.response.send_message("❌ هذا الأمر للمالك الرئيسي فقط.", ephemeral=True)
    data = load_data()
    data["game_controllers"] = {}
    data["admin_controllers"] = {}
    data["per_controllers"] = {}
    data["per_devs"] = []
    data["admin_ids"] = []
    # إزالة رتب الإدارة القديمة المحفوظة من كل السيرفرات.
    for guild_data in data.get("guilds", {}).values():
        if isinstance(guild_data, dict):
            guild_data.pop("admin_role", None)
    save_data(data)
    ADMIN_IDS = [PRIMARY_OWNER_ID]
    PER_DEVS = [PRIMARY_OWNER_ID]
    await interaction.response.send_message(
        "✅ تم تصفير صلاحيات الألعاب والإدارة والمالك المساعد والمطورين. بقي المالك الرئيسي فقط.",
        ephemeral=True,
    )


@bot.tree.command(name="make_line", description="تشغيل الخط التلقائي في عدة رومات")
@app_commands.describe(
    every_messages="إرسال الخط بعد كل كام رسالة",
    channel_1="الروم الأولى",
    channel_2="الروم الثانية اختياري",
    channel_3="الروم الثالثة اختياري",
    channel_4="الروم الرابعة اختياري",
    channel_5="الروم الخامسة اختياري",
)
async def make_line(
    interaction: discord.Interaction,
    every_messages: app_commands.Range[int, 1, 100],
    channel_1: discord.TextChannel,
    channel_2: Optional[discord.TextChannel] = None,
    channel_3: Optional[discord.TextChannel] = None,
    channel_4: Optional[discord.TextChannel] = None,
    channel_5: Optional[discord.TextChannel] = None,
):
    if not is_admin(interaction.user.id, interaction.guild):
        return await interaction.response.send_message("❌ هذا الأمر للإدارة والمالك فقط.", ephemeral=True)
    channels=[]
    for channel in [channel_1,channel_2,channel_3,channel_4,channel_5]:
        if channel and channel.id not in [x.id for x in channels]:
            permissions=channel.permissions_for(interaction.guild.me)
            if not permissions.send_messages or not permissions.attach_files:
                return await interaction.response.send_message(
                    f"❌ البوت يحتاج إرسال الرسائل وإرفاق الملفات في {channel.mention}.",ephemeral=True)
            channels.append(channel)
    set_line_settings(interaction.guild.id,[ch.id for ch in channels],every_messages)
    for channel in channels:
        line_message_counters[(interaction.guild.id,channel.id)]=0
    mentions="، ".join(ch.mention for ch in channels)
    await interaction.response.send_message(
        f"✅ تم تشغيل خط Rize تلقائياً بعد كل `{every_messages}` رسالة في: {mentions}",ephemeral=True)


@bot.tree.command(name="change_line", description="تغيير صورة الخط في هذا السيرفر فقط")
@app_commands.describe(attachment="الصورة الجديدة للخط في السيرفر الحالي")
async def change_line(interaction: discord.Interaction, attachment: discord.Attachment):
    if not can_manage_premium(interaction.user,interaction.guild):
        return await interaction.response.send_message("❌ تغيير الخط متاح لصاحب السيرفر أو Administrator فقط.",ephemeral=True)
    if not is_premium_guild(interaction.guild.id):
        return await interaction.response.send_message(premium_required_message(),ephemeral=True)
    content_type = attachment.content_type or ""
    if not content_type.startswith("image/"):
        return await interaction.response.send_message("❌ ارفع صورة فقط.", ephemeral=True)
    if attachment.size and attachment.size > 8 * 1024 * 1024:
        return await interaction.response.send_message("❌ حجم الصورة كبير. الحد الأقصى 8MB.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    try:
        raw = await attachment.read()
        # الحفاظ على نسبة الصورة الأصلية بدون أي فراغ أسود، مثل خط Rize Support.
        source = Image.open(io.BytesIO(raw)).convert("RGB")
        if source.width > 520:
            target_width = 520
            target_height = max(1, round(source.height * target_width / source.width))
            source = source.resize((target_width, target_height), Image.Resampling.LANCZOS)
        output = io.BytesIO()
        source.save(output, format="JPEG", quality=94, optimize=True)
        image_b64 = base64.b64encode(output.getvalue()).decode("ascii")
    except Exception as exc:
        print(f"change_line image error: {exc!r}")
        return await interaction.followup.send("❌ تعذر معالجة الصورة.", ephemeral=True)
    data=load_data()
    guild_data=data.setdefault("guilds",{}).setdefault(str(interaction.guild.id),{})
    guild_data["line_image_b64"]=image_b64
    save_data(data)
    update_premium_usage(interaction.guild.id,custom_line=True)
    await interaction.followup.send("✅ تم تغيير خط هذا السيرفر فقط مع الحفاظ على النسبة الأصلية بدون فراغات سوداء.", ephemeral=True)


@bot.tree.command(name="remove_line", description="إيقاف الخط من روم محددة أو كل الرومات")
@app_commands.describe(channel="اتركها فارغة لإيقاف الخط من كل الرومات")
async def remove_line(interaction: discord.Interaction, channel: Optional[discord.TextChannel] = None):
    if not is_admin(interaction.user.id,interaction.guild):
        return await interaction.response.send_message("❌ هذا الأمر للإدارة والمالك فقط.",ephemeral=True)
    removed=remove_line_settings(interaction.guild.id,channel.id if channel else None)
    text=(f"✅ تم إيقاف الخط في {channel.mention}." if channel else "✅ تم إيقاف الخط في كل الرومات.")
    await interaction.response.send_message(text if removed else "❌ لا توجد إعدادات مطابقة.",ephemeral=True)


@bot.tree.command(name="show_line", description="عرض كل الرومات التي يعمل فيها الخط")
async def show_line(interaction: discord.Interaction):
    if not is_admin(interaction.user.id,interaction.guild):
        return await interaction.response.send_message("❌ هذا الأمر للإدارة والمالك فقط.",ephemeral=True)
    rooms=get_line_settings(interaction.guild.id)
    if not rooms:
        return await interaction.response.send_message("❌ الخط التلقائي غير مفعل في أي روم.",ephemeral=True)
    lines=[]
    for channel_id,settings in rooms.items():
        lines.append(f"• <#{channel_id}> بعد كل `{settings.get('every_messages',1)}` رسالة")
    await interaction.response.send_message("🖼️ **رومات الخط التلقائي**\n"+"\n".join(lines),ephemeral=True)


@bot.tree.command(name="setup",description="عرض وتجهيز رومات نظام Rize")
@app_commands.describe(exchange_room="روم طلبات التبديل",delivery_room="روم التسليمات",balance_room="روم إشعارات الرصيد اختياري")
async def setup_slash(interaction: discord.Interaction,exchange_room:Optional[discord.TextChannel]=None,delivery_room:Optional[discord.TextChannel]=None,balance_room:Optional[discord.TextChannel]=None):
    if not is_admin(interaction.user.id,interaction.guild): return await interaction.response.send_message("❌ للإدارة والمالك فقط.",ephemeral=True)
    data=load_data(); g=data.setdefault("guilds",{}).setdefault(str(interaction.guild.id),{})
    if exchange_room: g["exchange_room"]=exchange_room.id
    if delivery_room: g["delivery_room"]=delivery_room.id
    if balance_room: g["balance_room"]=balance_room.id
    save_data(data)
    await interaction.response.send_message(
        "🧭 **معالج إعداد Rize**\n\n"
        f"• روم التحويلات: {f'<#{g.get("exchange_room")}>' if g.get('exchange_room') else 'غير محدد — مهم'}\n"
        f"• روم التسليمات: {f'<#{g.get("delivery_room")}>' if g.get('delivery_room') else 'غير محدد — مهم'}\n"
        f"• روم إشعارات الرصيد: {f'<#{g.get("balance_room")}>' if g.get('balance_room') else 'غير محدد — اختياري'}\n"
        f"• رومات الخط التلقائي: `{len(get_line_settings(interaction.guild.id))}` روم\n\n"
        "يمكنك تشغيل الأمر مرة أخرى مع تحديد الرومات المطلوبة.",ephemeral=True)


async def reset_server_to_defaults(guild_id):
    guild=bot.get_guild(int(guild_id))
    errors=[]
    if guild:
        try:
            if guild.me: await guild.me.edit(nick=None,reason="Rize server reset")
        except Exception as exc: errors.append(f"name:{type(exc).__name__}")
        try:
            await modify_current_guild_profile(guild.id,avatar=None,banner=None)
        except Exception as exc: errors.append(f"profile:{type(exc).__name__}")
    data=load_data(); g=data.setdefault("guilds",{}).setdefault(str(guild_id),{})
    g["coin_name"]="Rize"
    g.pop("line_image_b64",None)
    # Clear only server customization systems, not balances or budget.
    g.pop("aliases",None); g.pop("replies",None)
    info=data.setdefault("premium_guilds",{}).get(str(guild_id))
    if info:
        info["usage"]={}; info["expired_cleaned"]=True
        info["end_timestamp"]=0
    save_data(data)
    return errors


@bot.tree.command(name="back_server",description="إرجاع سيرفر محدد للوضع الافتراضي - مالك البوت فقط")
async def back_server(interaction:discord.Interaction,server_id:Optional[str]=None):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ للمالك الرئيسي للبوت فقط.",ephemeral=True)
    try: gid=int(server_id) if server_id else interaction.guild.id
    except ValueError: return await interaction.response.send_message("❌ ID السيرفر غير صحيح.",ephemeral=True)
    errors=await reset_server_to_defaults(gid)
    await interaction.response.send_message(f"✅ تم إرجاع السيرفر {code_id(gid)} للوضع الافتراضي."+(f" ملاحظات: `{', '.join(errors)}`" if errors else ""),ephemeral=True)


@bot.tree.command(name="back_all_servers",description="إرجاع جميع السيرفرات للوضع الافتراضي - مالك البوت فقط")
async def back_all_servers(interaction:discord.Interaction):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ للمالك الرئيسي للبوت فقط.",ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    total=0; failed=0
    for guild in list(bot.guilds):
        errors=await reset_server_to_defaults(guild.id); total+=1
        if errors: failed+=1
    await interaction.followup.send(f"✅ تم إرجاع {total} سيرفر للوضع الافتراضي. السيرفرات ذات الملاحظات: {failed}.",ephemeral=True)


@bot.tree.command(name="see_server_premium",description="عرض السيرفرات التي لديها Premium فعال - مالك البوت فقط")
async def see_server_premium(interaction:discord.Interaction):
    if not is_owner(interaction.user.id):
        return await interaction.response.send_message("❌ هذا الأمر للمالك الرئيسي للبوت فقط.",ephemeral=True)
    await cleanup_expired_premium()
    now=datetime.datetime.now(datetime.timezone.utc).timestamp()
    data=load_data(); rows=[]
    for gid,info in data.get("premium_guilds",{}).items():
        end=float(info.get("end_timestamp",0))
        if end<=now: continue
        guild=bot.get_guild(int(gid)); name=guild.name if guild else "سيرفر غير متاح"
        rows.append((end,name,gid,info))
    rows.sort(key=lambda x:x[0])
    if not rows:
        return await interaction.response.send_message("💎 لا يوجد أي سيرفر لديه Premium فعال حالياً.",ephemeral=True)
    embeds=[]
    for offset in range(0,len(rows),8):
        page=rows[offset:offset+8]; lines=[]
        for i,(end,name,gid,info) in enumerate(page,offset+1):
            lines.append(f"**#{i} | {name}**\n• ID: {code_id(gid)}\n• ينتهي: <t:{int(end)}:F> • <t:{int(end)}:R>")
        embed=discord.Embed(title=f"💎 سيرفرات Premium • {len(rows)}",description="\n\n".join(lines),color=discord.Color.purple())
        embeds.append(embed)
    await interaction.response.send_message(embed=embeds[0],ephemeral=True)
    for embed in embeds[1:]: await interaction.followup.send(embed=embed,ephemeral=True)


@bot.tree.command(name="take_premium",description="سحب Premium من السيرفر الحالي فوراً - مالك البوت فقط")
async def take_premium(interaction:discord.Interaction):
    if not is_owner(interaction.user.id):
        return await interaction.response.send_message("❌ هذا الأمر للمالك الرئيسي للبوت فقط.",ephemeral=True)
    data=load_data(); info=data.get("premium_guilds",{}).get(str(interaction.guild.id))
    if not info or float(info.get("end_timestamp",0))<=datetime.datetime.now(datetime.timezone.utc).timestamp():
        return await interaction.response.send_message("❌ السيرفر الحالي لا يملك Premium فعال.",ephemeral=True)
    # Force expiry then reuse the same cleanup path so every Premium customization is removed.
    info["end_timestamp"]=0; info["expired_cleaned"]=False; save_data(data)
    await expire_premium_guild(interaction.guild.id)
    await interaction.response.send_message("✅ تم سحب Premium من السيرفر الحالي فوراً وإزالة مميزات Premium.",ephemeral=True)


@bot.tree.command(name="toggle_exchange_system",description="فتح أو إغلاق نظام التبديل عالميًا")
async def toggle_exchange_system(interaction:discord.Interaction,enabled:bool):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ للمالك فقط.",ephemeral=True)
    set_exchange_system_enabled(enabled)
    text="✅ تم فتح نظام التبديل عالميًا في Rize." if enabled else "⛔ نظام التبديل مغلق عالميًا في Rize حاليًا."
    await interaction.response.send_message(text)



# ==============================================================================
# Premium shop: ticket, duration, payment, delivery and verification
# ==============================================================================
def premium_shop_data():
    data=load_data()
    shop=data.setdefault("premium_shop",{})
    shop.setdefault("prices",{"credit":0,"adamc":0,"rize":0})
    shop.setdefault("purchases",{})
    shop.setdefault("enabled",True)
    return data,shop


def create_transaction_code():
    alphabet=string.ascii_uppercase+string.digits
    data,shop=premium_shop_data(); transactions=shop.setdefault("transactions",{})
    while True:
        code=''.join(secrets.choice(alphabet) for _ in range(14))
        if code not in transactions:
            return code


def save_transaction_snapshot(p,event,details=""):
    data,shop=premium_shop_data(); code=p.get("transaction_code")
    if not code: return
    tx=shop.setdefault("transactions",{}).setdefault(code,{})
    tx.update({
        "transaction_code":code,"buyer_id":p.get("buyer_id"),"purchase_guild_id":p.get("guild_id"),
        "source_channel_id":p.get("source_channel_id"),"ticket_channel_id":p.get("ticket_channel_id"),
        "payment_method":p.get("payment_method"),"amount":p.get("amount"),"days":p.get("days"),
        "delivery":p.get("delivery"),"target_guild_id":p.get("target_guild_id"),"status":p.get("status"),
        "receipt_message_id":p.get("receipt_message_id"),"premium_code":p.get("code"),
        "last_event":event,"details":details,"updated_at":datetime.datetime.now(datetime.timezone.utc).timestamp(),
        "created_at":p.get("created_at")})
    save_data(data)


def purchase_by_channel(channel_id):
    _,shop=premium_shop_data()
    return shop.get("purchases",{}).get(str(channel_id))


def save_purchase(channel_id,purchase):
    data,shop=premium_shop_data()
    shop.setdefault("purchases",{})[str(channel_id)]=purchase
    save_data(data)


def calculate_premium_price(days,monthly_price):
    return max(1,math.ceil(int(monthly_price)*int(days)/30))


def safe_ticket_name(member):
    clean=re.sub(r"[^a-z0-9-]","-",member.name.lower())[:45].strip("-") or str(member.id)
    return f"{clean}-buy-premium"


async def create_premium_ticket(guild,member,source_channel=None):
    data,shop=premium_shop_data()
    if not shop.get("enabled",True):
        return None,"❌ نظام شراء Premium مغلق حالياً."
    for cid,p in list(shop.get("purchases",{}).items()):
        if int(p.get("buyer_id",0))==member.id and p.get("status") not in ["completed","cancelled"]:
            ch=guild.get_channel(int(cid))
            if ch: return ch,f"✅ عندك عملية شراء مفتوحة بالفعل: {ch.mention}"
    category=discord.utils.get(guild.categories,name="PREMIUM PURCHASES")
    if category is None:
        category=await guild.create_category("PREMIUM PURCHASES",reason="Rize Premium shop")
    overwrites={
        guild.default_role:discord.PermissionOverwrite(view_channel=False),
        member:discord.PermissionOverwrite(view_channel=True,send_messages=True,read_message_history=True,attach_files=True),
        guild.me:discord.PermissionOverwrite(view_channel=True,send_messages=True,manage_channels=True,read_message_history=True),
    }
    for role in guild.roles:
        if role.permissions.administrator and role!=guild.default_role:
            overwrites[role]=discord.PermissionOverwrite(view_channel=True,send_messages=True,read_message_history=True)
    ch=await guild.create_text_channel(safe_ticket_name(member),category=category,overwrites=overwrites,reason="Premium purchase")
    purchase={"buyer_id":member.id,"guild_id":guild.id,"source_channel_id":getattr(source_channel,"id",None),
              "ticket_channel_id":ch.id,"transaction_code":create_transaction_code(),
              "status":"choosing_duration","created_at":datetime.datetime.now(datetime.timezone.utc).timestamp()}
    save_purchase(ch.id,purchase); save_transaction_snapshot(purchase,"تم إنشاء عملية الشراء","تم فتح روم شراء خاص.")
    transaction_notice=(
        "💎 تم إنشاء عملية شراء Premium جديدة.\n"
        f"كود المعاملة الخاص بك: `{purchase['transaction_code']}`\n\n"
        "📌 احتفظ بكود المعاملة، وقدمه للإدارة إذا حدثت أي مشكلة في عملية الشراء حتى يمكن مراجعة العملية بالتحديد."
    )
    try:
        await member.send(transaction_notice)
        purchase["transaction_dm_sent"]=True
    except Exception:
        purchase["transaction_dm_sent"]=False
    save_purchase(ch.id,purchase); save_transaction_snapshot(purchase,"تم إرسال كود المعاملة","تم إرسال كود المعاملة في الخاص." if purchase["transaction_dm_sent"] else "تعذر إرسال كود المعاملة في الخاص؛ الخاص قد يكون مغلقاً.")
    embed=premium_step_embed(
        "💎 Rize Premium • الخطوة 1 من 3",
        f"أهلاً {member.mention}! هذا روم شراء خاص لا يراه إلا المشتري والإدارة.\n\n"
        f"**كود المعاملة:** `{purchase['transaction_code']}`\n"
        "احتفظ بالكود وقدمه للإدارة إذا حدثت مشكلة.\n\n"
        "اختر مدة Premium من الأزرار، أو اختر عدد أيام مخصص.\n"
        "يمكنك إلغاء العملية في أي وقت قبل اكتمال الدفع.",purchase)
    await ch.send(member.mention,embed=embed,view=PremiumDurationView())
    return ch,None


async def set_purchase_days(interaction,days):
    p=purchase_by_channel(interaction.channel_id)
    if not p or int(p.get("buyer_id",0))!=interaction.user.id:
        return await interaction.response.send_message("❌ هذه العملية ليست خاصة بك.",ephemeral=True)
    if p.get("status")!="choosing_duration":
        return await interaction.response.send_message("✅ تم تسجيل مدة Premium بالفعل، ولا يمكن الرجوع للمرحلة السابقة.",ephemeral=True)
    if not 1<=int(days)<=3650:
        return await interaction.response.send_message("❌ المدة يجب أن تكون من يوم إلى 3650 يوم.",ephemeral=True)
    p["days"]=int(days); p["duration_seconds"]=int(days)*86400; p["status"]="choosing_payment"
    save_purchase(interaction.channel_id,p)
    next_embed=premium_step_embed(
        "💳 Rize Premium • الخطوة 2 من 3",
        "تم حفظ المدة. اختر طريقة الدفع المناسبة من الأزرار بالأسفل.",p)
    if interaction.message:
        await interaction.response.edit_message(embed=next_embed,view=PremiumPaymentView())
    else:
        await interaction.response.send_message(embed=next_embed,view=PremiumPaymentView())


def premium_step_embed(title,description,p=None,color=None):
    embed=discord.Embed(title=title,description=description,color=color or discord.Color.purple())
    if p:
        embed.add_field(name="كود المعاملة",value=f"`{p.get('transaction_code','غير متاح')}`",inline=False)
        if p.get("days"): embed.add_field(name="المدة",value=f"`{p['days']}` يوم",inline=True)
        if p.get("amount") is not None: embed.add_field(name="الإجمالي",value=f"`{int(p['amount']):,}`",inline=True)
    embed.set_footer(text="Rize Premium • عملية شراء آمنة وخاصة")
    return embed


async def cancel_premium_purchase(interaction):
    p=purchase_by_channel(interaction.channel_id)
    if not p:
        return await interaction.response.send_message("❌ لا توجد عملية شراء مرتبطة بهذا الروم.",ephemeral=True)
    allowed=interaction.user.id==int(p.get("buyer_id",0)) or is_owner(interaction.user.id) or interaction.user.guild_permissions.administrator
    if not allowed:
        return await interaction.response.send_message("❌ لا يمكنك إلغاء عملية شراء شخص آخر.",ephemeral=True)
    if p.get("status")=="completed":
        return await interaction.response.send_message("❌ العملية مكتملة بالفعل ولا يمكن إلغاؤها.",ephemeral=True)
    p["status"]="cancelled"; p["cancelled_by"]=interaction.user.id; save_purchase(interaction.channel_id,p)
    save_transaction_snapshot(p,"تم إلغاء عملية الشراء",f"أُلغي الطلب بواسطة {interaction.user.id} قبل اكتمال الدفع.")
    await send_premium_transaction_log(p,"تم إلغاء عملية الشراء","تم الإلغاء قبل اكتمال الدفع.")
    await interaction.response.send_message(embed=premium_step_embed("❌ تم إلغاء عملية الشراء","سيتم حذف روم الشراء خلال 5 ثوانٍ.",p,discord.Color.red()))
    await asyncio.sleep(5)
    try: await interaction.channel.delete(reason="Premium purchase cancelled")
    except Exception: pass


class PremiumDaysModal(discord.ui.Modal,title="مدة Premium المخصصة"):
    days=discord.ui.TextInput(label="عدد الأيام",placeholder="مثال: 45",min_length=1,max_length=4)
    async def on_submit(self,interaction):
        try: value=int(str(self.days.value).strip())
        except ValueError: return await interaction.response.send_message("❌ اكتب عدد أيام صحيح.",ephemeral=True)
        await set_purchase_days(interaction,value)


class PremiumDurationView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    async def choose(self,interaction,days): await set_purchase_days(interaction,days)
    @discord.ui.button(label="شهر",emoji="📅",style=discord.ButtonStyle.primary,custom_id="prem_days_30")
    async def d30(self,i,b): await self.choose(i,30)
    @discord.ui.button(label="3 شهور",style=discord.ButtonStyle.primary,custom_id="prem_days_90")
    async def d90(self,i,b): await self.choose(i,90)
    @discord.ui.button(label="6 شهور",style=discord.ButtonStyle.primary,custom_id="prem_days_180")
    async def d180(self,i,b): await self.choose(i,180)
    @discord.ui.button(label="سنة",style=discord.ButtonStyle.success,custom_id="prem_days_365")
    async def d365(self,i,b): await self.choose(i,365)
    @discord.ui.button(label="أيام مخصصة",emoji="✏️",style=discord.ButtonStyle.secondary,custom_id="prem_days_custom")
    async def custom(self,i,b): await i.response.send_modal(PremiumDaysModal())
    @discord.ui.button(label="إلغاء عملية الشراء",emoji="🛑",style=discord.ButtonStyle.danger,row=1,custom_id="premiumdurationview_cancel")
    async def cancel(self,interaction,button): await cancel_premium_purchase(interaction)


async def choose_payment(interaction,method):
    p=purchase_by_channel(interaction.channel_id)
    if not p or int(p.get("buyer_id",0))!=interaction.user.id:
        return await interaction.response.send_message("❌ هذه العملية ليست خاصة بك.",ephemeral=True)
    if p.get("status")!="choosing_payment":
        return await interaction.response.send_message("✅ تم تسجيل طريقة الدفع بالفعل، ولا يمكن الرجوع للمرحلة السابقة.",ephemeral=True)
    data,shop=premium_shop_data(); monthly=int(shop.get("prices",{}).get(method,0))
    if monthly<=0: return await interaction.response.send_message("❌ هذه طريقة الدفع غير متاحة لأن سعرها لم يُحدد.",ephemeral=True)
    p["payment_method"]=method; p["monthly_price"]=monthly
    p["amount"]=calculate_premium_price(p["days"],monthly); p["status"]="choosing_delivery"
    save_purchase(interaction.channel_id,p)
    label={"credit":"Credit","adamc":"Adam C","rize":"Rize"}[method]
    next_embed=premium_step_embed(
        "📦 Rize Premium • الخطوة 3 من 3",
        f"**طريقة الدفع:** {label}\nاختر الآن مكان استلام كود Premium أو السيرفر المطلوب تفعيل Premium عليه.",p)
    await interaction.response.edit_message(embed=next_embed,view=PremiumDeliveryView())


class PremiumPaymentView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Credit",emoji="💳",style=discord.ButtonStyle.primary,custom_id="prem_pay_credit")
    async def credit(self,i,b): await choose_payment(i,"credit")
    @discord.ui.button(label="Adam C",emoji="💰",style=discord.ButtonStyle.primary,custom_id="prem_pay_adamc")
    async def adam(self,i,b): await choose_payment(i,"adamc")
    @discord.ui.button(label="Rize",emoji="🪙",style=discord.ButtonStyle.success,custom_id="prem_pay_rize")
    async def rize(self,i,b): await choose_payment(i,"rize")
    @discord.ui.button(label="إلغاء عملية الشراء",emoji="🛑",style=discord.ButtonStyle.danger,row=1,custom_id="premiumpaymentview_cancel")
    async def cancel(self,interaction,button): await cancel_premium_purchase(interaction)


async def activate_premium_direct(guild_id,duration,user_id):
    guild=bot.get_guild(int(guild_id))
    if not guild: return False,"البوت غير موجود في السيرفر المطلوب."
    data=load_data(); now=datetime.datetime.now(datetime.timezone.utc).timestamp()
    old=data.setdefault("premium_guilds",{}).get(str(guild_id),{})
    old_end=float(old.get("end_timestamp",0)); start=max(now,old_end)
    data["premium_guilds"][str(guild_id)]={"start_timestamp":old.get("start_timestamp",now),
        "end_timestamp":start+int(duration),"activated_by":user_id,"usage":old.get("usage",{}),"expired_cleaned":False}
    save_data(data); return True,data["premium_guilds"][str(guild_id)]["end_timestamp"]


class PremiumFinishPurchaseView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)

    @discord.ui.button(label="إنهاء عملية الشراء",emoji="✅",style=discord.ButtonStyle.success,custom_id="rize_premium_finish_purchase")
    async def finish_purchase(self,interaction:discord.Interaction,button:discord.ui.Button):
        p=purchase_by_channel(interaction.channel_id)
        if not p:
            return await interaction.response.send_message("❌ لا توجد عملية شراء مرتبطة بهذا الروم.",ephemeral=True)
        allowed=(interaction.user.id==int(p.get("buyer_id",0)) or is_owner(interaction.user.id)
                 or interaction.user.guild_permissions.administrator)
        if not allowed:
            return await interaction.response.send_message("❌ هذا الزر خاص بالمشتري أو الإدارة فقط.",ephemeral=True)
        if p.get("status") not in ["code_issued","completed"]:
            return await interaction.response.send_message("❌ لا يمكن إنهاء العملية قبل استلام Premium.",ephemeral=True)
        p["status"]="completed"; p["finished_by"]=interaction.user.id
        p["finished_at"]=datetime.datetime.now(datetime.timezone.utc).timestamp()
        save_purchase(interaction.channel_id,p)
        save_transaction_snapshot(p,"تم إنهاء عملية الشراء","أغلق المشتري أو الإدارة روم الشراء بعد استلام الطلب.")
        await send_premium_transaction_log(p,"تم إنهاء عملية الشراء","تم إغلاق روم الشراء يدوياً بعد الاستلام.")
        for item in self.children: item.disabled=True
        await interaction.response.edit_message(
            embed=premium_step_embed("✅ تم إنهاء عملية الشراء","تم تأكيد استلام الطلب. سيُحذف الروم خلال 5 ثوانٍ.",p,discord.Color.green()),
            view=self)
        await asyncio.sleep(5)
        try: await interaction.channel.delete(reason="Premium purchase finished by buyer")
        except Exception: pass


async def complete_premium_purchase(channel,p):
    if p.get("status")=="completed": return
    user=bot.get_user(int(p["buyer_id"])) or await bot.fetch_user(int(p["buyer_id"]))
    delivery=p.get("delivery","room")
    if delivery in ["current","server_id"]:
        gid=int(p.get("target_guild_id") or p["guild_id"])
        ok,result=await activate_premium_direct(gid,p["duration_seconds"],p["buyer_id"])
        if not ok: return await channel.send(f"❌ تعذر التفعيل المباشر: {result}")
        p["status"]="completed"; save_purchase(channel.id,p)
        await channel.send(f"✅ تم تفعيل Premium للسيرفر `{gid}` حتى <t:{int(result)}:F>. سيتم حذف الروم بعد 10 ثوانٍ.")
        await notify_premium_buyer(p,f"✅ تم تفعيل Premium للسيرفر `{gid}` لمدة `{p['days']}` يوم بنجاح.")
        await send_premium_transaction_log(p,"اكتملت وتم التفعيل",f"السيرفر المستهدف: `{gid}` حتى <t:{int(result)}:F>")
        await send_purchase_completion(p)
        await asyncio.sleep(10); return await channel.delete(reason="Premium purchase completed")
    code=create_premium_code(p["duration_seconds"],p["buyer_id"])
    data=load_data(); rec=data["premium_codes"][code]
    rec.update({"purchase_channel_id":channel.id,"buyer_id":p["buyer_id"],"delivery":delivery,
                "source_channel_id":p.get("source_channel_id"),"purchase_guild_id":p.get("guild_id")}); save_data(data)
    p["status"]="code_issued"; p["code"]=code; save_purchase(channel.id,p)
    secret_text=(f"💎 تم الدفع بنجاح!\nكود Premium لمدة `{p['days']}` يوم:\n`{code}`\n\n"
                 f"فعّله في السيرفر المطلوب بالأمر: `/active_premium {code}`\n"
                 "⚠️ هذا الكود سري، لا تشاركه مع أي شخص.")
    if delivery=="dm":
        try:
            await user.send(secret_text)
            await channel.send(embed=premium_step_embed(
                "✅ تم إرسال كود Premium في الخاص",
                "راجع رسائلك الخاصة. بعد التأكد من استلام الكود اضغط زر **إنهاء عملية الشراء** بالأسفل.",p,discord.Color.green()),
                view=PremiumFinishPurchaseView())
        except discord.Forbidden:
            await channel.send(secret_text)
            await channel.send(embed=premium_step_embed(
                "⚠️ تعذر الإرسال في الخاص",
                "تم عرض الكود داخل روم الشراء الخاص فقط. بعد حفظه اضغط زر **إنهاء عملية الشراء**.",p,discord.Color.orange()),
                view=PremiumFinishPurchaseView())
    else:
        await channel.send(secret_text)
        await channel.send(embed=premium_step_embed(
            "✅ تم تسليم كود Premium",
            "احفظ الكود السري، ثم اضغط زر **إنهاء عملية الشراء** لإغلاق هذا الروم.",p,discord.Color.green()),
            view=PremiumFinishPurchaseView())
    await notify_premium_buyer(p,f"✅ تم إتمام شراء Premium لمدة `{p['days']}` يوم بنجاح. راجع رسالة الاستلام الخاصة بعملية الشراء.")
    await send_premium_transaction_log(p,"تم الشراء وإصدار الكود","تم إصدار كود Premium سري للمشتري بدون عرضه في روم الإتمام العام.")
    await send_purchase_completion(p)


async def finalize_delivery(interaction,delivery,target_guild_id=None):
    p=purchase_by_channel(interaction.channel_id)
    if not p or int(p.get("buyer_id",0))!=interaction.user.id:
        return await interaction.response.send_message("❌ هذه العملية ليست خاصة بك.",ephemeral=True)
    if p.get("status")!="choosing_delivery":
        return await interaction.response.send_message("✅ تم تسجيل طريقة الاستلام بالفعل، ولا يمكن الرجوع للمرحلة السابقة.",ephemeral=True)
    p["delivery"]=delivery
    if target_guild_id: p["target_guild_id"]=int(target_guild_id)
    p["status"]="awaiting_payment"; save_purchase(interaction.channel_id,p)
    if p["payment_method"]=="rize":
        bal=get_balance(interaction.user.id)
        if bal<int(p["amount"]):
            return await interaction.response.send_message(f"❌ رصيدك غير كافٍ. المطلوب `{p['amount']:,}` Rize والمتاح `{bal:,}`.",ephemeral=True)
        update_balance(interaction.user.id,-int(p["amount"])); p["paid"]=True; save_purchase(interaction.channel_id,p)
        await interaction.response.edit_message(embed=premium_step_embed(
            "✅ تم دفع قيمة Premium",
            f"تم خصم `{p['amount']:,}` Rize بنجاح، وجارٍ إتمام عملية الشراء.",p,discord.Color.green()),view=None)
        await send_premium_transaction_log(p,"تم الدفع بـRize",f"تم خصم `{p['amount']:,}` Rize.")
        return await complete_premium_purchase(interaction.channel,p)
    command=(f"#credit {PREMIUM_PAYMENT_RECEIVER_ID} {p['amount']} with tax" if p["payment_method"]=="credit"
             else f"!transfer {PREMIUM_PAYMENT_RECEIVER_ID} {p['amount']}")
    p["payment_command"]=command; save_purchase(interaction.channel_id,p)
    label="Credit" if p["payment_method"]=="credit" else "Adam C"
    payment_embed=premium_step_embed(
        "⏳ في انتظار إتمام الدفع",
        f"**طريقة الدفع:** {label}\nانسخ الأمر التالي وأرسله **في هذا الروم**:\n```\n{command}\n```\n"
        "بعد إرسال الأمر انتظر رسالة تأكيد التحويل. تم قفل المراحل السابقة ولا يمكن اختيارها مرة أخرى.",p,discord.Color.gold())
    if interaction.message:
        await interaction.response.edit_message(embed=payment_embed,view=None)
    else:
        await interaction.response.send_message(embed=payment_embed,view=None)


class PremiumServerIdModal(discord.ui.Modal,title="تفعيل Premium بواسطة Server ID"):
    server_id=discord.ui.TextInput(label="Server ID",placeholder="123456789012345678",min_length=15,max_length=22)
    async def on_submit(self,interaction):
        try: gid=int(str(self.server_id.value).strip())
        except ValueError: return await interaction.response.send_message("❌ Server ID غير صحيح.",ephemeral=True)
        if not bot.get_guild(gid): return await interaction.response.send_message("❌ البوت غير موجود في السيرفر ده.",ephemeral=True)
        await finalize_delivery(interaction,"server_id",gid)


class PremiumDeliveryView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="الكود في الخاص",emoji="📨",style=discord.ButtonStyle.primary,custom_id="prem_delivery_dm")
    async def dm(self,i,b): await finalize_delivery(i,"dm")
    @discord.ui.button(label="الكود في الروم",emoji="💬",style=discord.ButtonStyle.primary,custom_id="prem_delivery_room")
    async def room(self,i,b): await finalize_delivery(i,"room")
    @discord.ui.button(label="السيرفر الحالي",emoji="🏠",style=discord.ButtonStyle.success,custom_id="prem_delivery_current")
    async def current(self,i,b): await finalize_delivery(i,"current",i.guild.id)
    @discord.ui.button(label="Server ID",emoji="🆔",style=discord.ButtonStyle.secondary,custom_id="prem_delivery_id")
    async def sid(self,i,b): await i.response.send_modal(PremiumServerIdModal())
    @discord.ui.button(label="إلغاء عملية الشراء",emoji="🛑",style=discord.ButtonStyle.danger,row=1,custom_id="premiumdeliveryview_cancel")
    async def cancel(self,interaction,button): await cancel_premium_purchase(interaction)


class PremiumStartView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="شراء Premium",emoji="💎",style=discord.ButtonStyle.success,custom_id="rize_buy_premium")
    async def start(self,interaction,button):
        await interaction.response.defer(ephemeral=True)
        try:
            ch,msg=await create_premium_ticket(interaction.guild,interaction.user,interaction.channel)
            await interaction.followup.send(msg or f"✅ تم إنشاء روم الشراء: {ch.mention}",ephemeral=True)
        except Exception as exc:
            await interaction.followup.send(f"❌ تعذر إنشاء الروم: `{type(exc).__name__}`",ephemeral=True)


@bot.tree.command(name="setup_premium",description="إنشاء واجهة شراء Premium")
async def setup_premium(interaction:discord.Interaction):
    if not is_owner(interaction.user.id) and not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ للمالك أو Administrator فقط.",ephemeral=True)
    embed=discord.Embed(
        title="💎 Rize Premium Store",
        description=(
            "**اشترِ Premium بطريقة منظمة وآمنة.**\n\n"
            "🛒 اضغط **شراء Premium** لفتح روم خاص بك.\n"
            "📅 اختر المدة أو اكتب عدد الأيام الذي تريده.\n"
            "💳 اختر طريقة الدفع: Credit أو Adam C أو Rize.\n"
            "📦 اختر استلام الكود أو التفعيل على السيرفر المطلوب.\n\n"
            "🔐 كل عملية لها كود معاملة خاص لمراجعتها مع الإدارة عند الحاجة."
        ),color=discord.Color.from_rgb(114,70,220))
    embed.add_field(name="⚡ سريع",value="خطوات واضحة داخل روم خاص",inline=True)
    embed.add_field(name="🛡️ آمن",value="التحقق من الدفع قبل الإتمام",inline=True)
    embed.add_field(name="🎟️ مرن",value="أيام أو شهور حسب اختيارك",inline=True)
    embed.set_footer(text="Rize Premium • اضغط الزر بالأسفل للبدء")
    await interaction.channel.send(embed=embed,view=PremiumStartView())
    await interaction.response.send_message("✅ تم إنشاء واجهة Premium.",ephemeral=True)


@bot.tree.command(name="buy_premium",description="فتح روم خاص لشراء Premium")
async def buy_premium(interaction:discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    try:
        ch,msg=await create_premium_ticket(interaction.guild,interaction.user,interaction.channel)
        await interaction.followup.send(msg or f"✅ تم إنشاء روم الشراء: {ch.mention}",ephemeral=True)
    except Exception as exc:
        await interaction.followup.send(f"❌ تعذر إنشاء الروم: `{type(exc).__name__}`",ephemeral=True)


@bot.tree.command(name="set_premium_price",description="تحديد سعر شهر Premium")
@app_commands.choices(payment=[app_commands.Choice(name="Credit",value="credit"),app_commands.Choice(name="Adam C",value="adamc"),app_commands.Choice(name="Rize",value="rize")])
async def set_premium_price(interaction:discord.Interaction,payment:app_commands.Choice[str],monthly_price:str):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ للمالك الرئيسي فقط.",ephemeral=True)
    value=parse_number(monthly_price)
    if value is None or value<=0: return await interaction.response.send_message("❌ سعر غير صحيح.",ephemeral=True)
    data,shop=premium_shop_data(); shop["prices"][payment.value]=int(value); save_data(data)
    await interaction.response.send_message(f"✅ سعر شهر {payment.name}: `{int(value):,}`.",ephemeral=True)


@bot.tree.command(name="see_premium",description="عرض تفاصيل عملية شراء Premium بواسطة كود المعاملة")
async def see_premium(interaction:discord.Interaction,transaction_code:str):
    if not is_owner(interaction.user.id):
        return await interaction.response.send_message("❌ للمالك الرئيسي فقط.",ephemeral=True)
    _,shop=premium_shop_data(); code=transaction_code.strip().upper()
    tx=shop.get("transactions",{}).get(code)
    if not tx:
        return await interaction.response.send_message("❌ كود المعاملة غير صحيح أو غير موجود.",ephemeral=True)
    method={"credit":"Credit","adamc":"Adam C","rize":"Rize"}.get(tx.get("payment_method"),"غير محدد")
    delivery={"dm":"كود في الخاص","room":"كود في الروم","current":"السيرفر الحالي","server_id":"Server ID"}.get(tx.get("delivery"),"غير محدد")
    embed=discord.Embed(title="🔎 تفاصيل معاملة Premium",color=discord.Color.blurple())
    embed.add_field(name="كود المعاملة",value=f"`{code}`",inline=False)
    embed.add_field(name="المشتري",value=f"<@{tx.get('buyer_id')}>\n`{tx.get('buyer_id')}`",inline=True)
    embed.add_field(name="الحالة",value=str(tx.get("status","غير محدد")),inline=True)
    embed.add_field(name="آخر حدث",value=str(tx.get("last_event","غير محدد")),inline=False)
    embed.add_field(name="طريقة الدفع",value=method,inline=True)
    embed.add_field(name="المبلغ",value=f"`{int(tx.get('amount') or 0):,}`",inline=True)
    embed.add_field(name="المدة",value=f"`{tx.get('days','?')}` يوم",inline=True)
    embed.add_field(name="طريقة التنفيذ",value=delivery,inline=True)
    if tx.get("target_guild_id"): embed.add_field(name="السيرفر المستهدف",value=f"`{tx.get('target_guild_id')}`",inline=True)
    if tx.get("receipt_message_id"): embed.add_field(name="ID رسالة الدفع",value=f"`{tx.get('receipt_message_id')}`",inline=True)
    if tx.get("premium_code"): embed.add_field(name="كود Premium",value=f"`{tx.get('premium_code')}`",inline=False)
    if tx.get("details"): embed.add_field(name="آخر تفاصيل",value=str(tx.get("details"))[:1024],inline=False)
    await interaction.response.send_message(embed=embed,ephemeral=True)



async def send_premium_transaction_log(p,status,extra=""):
    _,shop=premium_shop_data()
    channel_id=shop.get("log_channel_id")
    channel=bot.get_channel(int(channel_id)) if channel_id else None
    if not channel:
        return
    method={"credit":"Credit","adamc":"Adam C","rize":"Rize"}.get(p.get("payment_method"),"غير محدد")
    delivery={"dm":"كود في الخاص","room":"كود في الروم","current":"السيرفر الحالي","server_id":"Server ID"}.get(p.get("delivery"),"غير محدد")
    embed=discord.Embed(title="💎 سجل معاملة Premium",color=discord.Color.purple())
    embed.add_field(name="كود المعاملة",value=f"`{p.get('transaction_code','غير متاح')}`",inline=False)
    embed.add_field(name="الحالة",value=status,inline=False)
    embed.add_field(name="المشتري",value=f"<@{p.get('buyer_id')}>\n`{p.get('buyer_id')}`",inline=True)
    embed.add_field(name="طريقة الدفع",value=method,inline=True)
    embed.add_field(name="المبلغ",value=f"`{int(p.get('amount',0)):,}`",inline=True)
    embed.add_field(name="المدة",value=f"`{p.get('days','?')}` يوم",inline=True)
    embed.add_field(name="طريقة الاستلام",value=delivery,inline=True)
    purchase_place="شراء من داخل سيرفر" if p.get("source_channel_id") else "شراء من خارج واجهة السيرفر"
    embed.add_field(name="نوع الشراء",value=purchase_place,inline=True)
    embed.add_field(name="سيرفر الشراء",value=f"`{p.get('guild_id')}`",inline=True)
    if p.get("source_channel_id"):
        embed.add_field(name="روم بداية الشراء",value=f"<#{p.get('source_channel_id')}>\n`{p.get('source_channel_id')}`",inline=True)
    if p.get("target_guild_id"):
        embed.add_field(name="السيرفر المستهدف",value=f"`{p.get('target_guild_id')}`",inline=True)
    if p.get("receipt_message_id"):
        embed.add_field(name="ID رسالة الدفع",value=f"`{p.get('receipt_message_id')}`",inline=True)
    if extra:
        embed.add_field(name="تفاصيل",value=extra[:1024],inline=False)
    await channel.send(embed=embed)
    save_transaction_snapshot(p,status,extra)


def build_premium_invoice(p,title="✅ فاتورة شراء Premium",include_secret=False):
    method={"credit":"Credit","adamc":"Adam C","rize":"Rize"}.get(p.get("payment_method"),"غير محدد")
    delivery={"dm":"كود في الخاص","room":"كود في الروم","current":"السيرفر الحالي","server_id":"Server ID"}.get(p.get("delivery"),"غير محدد")
    embed=discord.Embed(title=title,color=discord.Color.green(),timestamp=datetime.datetime.now(datetime.timezone.utc))
    embed.add_field(name="كود المعاملة",value=f"`{p.get('transaction_code')}`",inline=False)
    embed.add_field(name="المشتري",value=f"<@{p.get('buyer_id')}>\n`{p.get('buyer_id')}`",inline=True)
    embed.add_field(name="طريقة الدفع",value=method,inline=True)
    embed.add_field(name="المبلغ المدفوع",value=f"`{int(p.get('amount',0)):,}`",inline=True)
    embed.add_field(name="مدة Premium",value=f"`{p.get('days','?')}` يوم",inline=True)
    embed.add_field(name="طريقة التنفيذ",value=delivery,inline=True)
    if p.get("target_guild_id"): embed.add_field(name="السيرفر المستهدف",value=f"`{p.get('target_guild_id')}`",inline=True)
    # كود Premium سري ولا يظهر في روم الإتمام أو اللوج العام.
    if include_secret and p.get("code"):
        embed.add_field(name="كود Premium السري",value=f"`{p.get('code')}`",inline=False)
    embed.set_footer(text="Rize Premium Purchase Receipt")
    return embed


async def send_purchase_completion(p):
    data,shop=premium_shop_data()
    if not p.get("purchase_number"):
        shop["completed_purchase_count"]=int(shop.get("completed_purchase_count",0))+1
        p["purchase_number"]=shop["completed_purchase_count"]
        if p.get("ticket_channel_id"):
            shop.setdefault("purchases",{})[str(p["ticket_channel_id"])]=p
        save_data(data)
    number=int(p["purchase_number"])
    method={"credit":"Credit","adamc":"Adam C","rize":"Rize"}.get(p.get("payment_method"),"غير محدد")
    delivery={"dm":"كود في الخاص","room":"كود في روم الشراء","current":"السيرفر الحالي","server_id":"سيرفر عن طريق ID"}.get(p.get("delivery"),"غير محدد")
    public_text=(
        f"✅ عملية شراء Premium رقم `{number}`\n"
        f"المشتري: <@{p.get('buyer_id')}>\n"
        f"اشترى لمدة: `{p.get('days','?')}` يوم\n"
        f"استلم عن طريق: **{delivery}**\n"
        f"طريقة الدفع: **{method}**\n"
        f"المبلغ المدفوع: `{int(p.get('amount',0)):,}`"
    )
    channel_id=shop.get("purchase_completion_channel_id")
    channel=bot.get_channel(int(channel_id)) if channel_id else None
    if channel:
        await channel.send(public_text)
    user=bot.get_user(int(p.get("buyer_id",0)))
    if user:
        private_text=(public_text+f"\nكود المعاملة للدعم: `{p.get('transaction_code')}`")
        try: await user.send(private_text)
        except Exception: pass


async def notify_premium_buyer(p,text):
    user=bot.get_user(int(p.get("buyer_id",0)))
    if user:
        try: await user.send(text)
        except Exception: pass


@bot.tree.command(name="set_channel_premium",description="تحديد روم سجلات معاملات Premium")
async def set_channel_premium(interaction:discord.Interaction,channel:discord.TextChannel):
    if not is_owner(interaction.user.id):
        return await interaction.response.send_message("❌ الأمر للمالك الرئيسي للبوت فقط.",ephemeral=True)
    data,shop=premium_shop_data(); shop["log_channel_id"]=channel.id; save_data(data)
    await interaction.response.send_message(f"✅ تم تحديد {channel.mention} كروم سجلات معاملات Premium.",ephemeral=True)
    await channel.send("✅ تم تفعيل سجلات معاملات Premium في هذا الروم.")


@bot.tree.command(name="set_channel_premium_purchers",description="تحديد روم إتمام وفواتير شراء Premium")
async def set_channel_premium_purchers(interaction:discord.Interaction,channel:discord.TextChannel):
    if not is_owner(interaction.user.id):
        return await interaction.response.send_message("❌ الأمر للمالك الرئيسي للبوت فقط.",ephemeral=True)
    data,shop=premium_shop_data(); shop["purchase_completion_channel_id"]=channel.id; save_data(data)
    await interaction.response.send_message(f"✅ تم تحديد {channel.mention} كروم إتمام وفواتير شراء Premium.",ephemeral=True)
    await channel.send("✅ تم تفعيل روم إتمام وفواتير شراء Premium.")


async def handle_premium_payment_receipt(message):
    p=purchase_by_channel(message.channel.id)
    if not p or p.get("status")!="awaiting_payment" or p.get("payment_method") not in ["credit","adamc"]:
        return False
    method=p.get("payment_method")
    author_name=re.sub(r"[^a-z0-9]","",str(message.author.name).lower())
    if method=="credit":
        if message.author.id!=PROBOT_ID:
            return False
    else:
        # ID هو الأفضل. مؤقتاً يقبل اسم AdamC فقط مع رد مباشر على أمر المشتري داخل نفس تذكرة الشراء.
        adam_author_ok=(ADAMC_BOT_ID and message.author.id==ADAMC_BOT_ID) or author_name in {"adamc","adamcbot"}
        if not adam_author_ok:
            return False
    content=message.content or ""
    for emb in message.embeds:
        content+=" "+(emb.title or "")+" "+(emb.description or "")
        for field in emb.fields: content+=f" {field.name} {field.value}"
    normalized=content.replace(",","").replace("$","")
    numbers=[int(x) for x in re.findall(r"\d+",normalized)]
    requested=int(p["amount"])
    if requested not in numbers:
        return False
    if method=="credit":
        if str(PREMIUM_PAYMENT_RECEIVER_ID) not in normalized:
            return False
    else:
        # رسالة AdamC الظاهرة لا تعرض ID المستلم، لذلك نربطها بأمر المشتري الذي رد عليه البوت.
        ref=message.reference
        if not ref or not ref.message_id:
            return False
        try: original=await message.channel.fetch_message(ref.message_id)
        except Exception: return False
        expected=f"!transfer {PREMIUM_PAYMENT_RECEIVER_ID} {requested}"
        if original.author.id!=int(p["buyer_id"]) or original.content.strip()!=expected:
            return False
        if "has transferred" not in normalized.lower():
            return False
    p["paid"]=True; p["status"]="payment_verified"; p["receipt_message_id"]=message.id
    p["verified_amount"]=requested; save_purchase(message.channel.id,p)
    await message.channel.send(embed=premium_step_embed("✅ تم التحقق من الدفع",f"تم تأكيد دفع `{requested:,}` بنجاح، وجارٍ إتمام طلب Premium.",p,discord.Color.green()))
    await send_premium_transaction_log(p,"تم التحقق من الدفع",f"طريقة الدفع: {method} • المبلغ: `{requested:,}`")
    await complete_premium_purchase(message.channel,p)
    return True


@bot.tree.command(name="make_premium_code",description="إنشاء كود Premium مكون من 14 حرفًا")
async def make_premium_code(interaction:discord.Interaction,duration:str):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ للمالك فقط.",ephemeral=True)
    seconds=parse_time(duration)
    if seconds<=0: return await interaction.response.send_message("❌ مدة غير صحيحة، مثل 30d أو 1y غير مدعوم؛ استخدم 365d.",ephemeral=True)
    code=create_premium_code(seconds,interaction.user.id)
    await interaction.response.send_message(f"💎 كود Premium: `{code}`\nالمدة: `{duration}`",ephemeral=True)


@bot.tree.command(name="active_premium",description="تفعيل Premium للسيرفر باستخدام كود")
async def active_premium(interaction:discord.Interaction,code:str):
    if not can_manage_premium(interaction.user,interaction.guild):
        return await interaction.response.send_message("❌ تفعيل Premium متاح لصاحب السيرفر أو Administrator فقط.",ephemeral=True)
    data=load_data(); record=data.get("premium_codes",{}).get(code.upper())
    if not record or record.get("used"): return await interaction.response.send_message("❌ الكود غير صحيح أو مستخدم.",ephemeral=True)
    now=datetime.datetime.now(datetime.timezone.utc).timestamp(); current=premium_info(interaction.guild.id)
    start=max(now,float(current.get("end_timestamp",0))) if current else now; end=start+int(record["duration"])
    old_info=data.setdefault("premium_guilds",{}).get(str(interaction.guild.id),{})
    data["premium_guilds"][str(interaction.guild.id)]={
        "start_timestamp":old_info.get("start_timestamp",now),"end_timestamp":end,
        "activated_by":interaction.user.id,"usage":old_info.get("usage",{}),"expired_cleaned":False
    }
    record["used"]=True; record["used_guild"]=interaction.guild.id; save_data(data)
    await interaction.response.send_message(f"💎 تم تفعيل Premium حتى <t:{int(end)}:F>.")
    ticket_id=record.get("purchase_channel_id")
    if ticket_id:
        purchase=purchase_by_channel(int(ticket_id))
        if purchase:
            purchase["status"]="completed"; purchase["target_guild_id"]=interaction.guild.id; save_purchase(int(ticket_id),purchase)
            await notify_premium_buyer(purchase,f"✅ تم تفعيل Premium في سيرفر **{interaction.guild.name}** (`{interaction.guild.id}`) بنجاح.")
            await send_premium_transaction_log(purchase,"اكتملت وتم تفعيل الكود",f"السيرفر: **{interaction.guild.name}** (`{interaction.guild.id}`)")
        ticket=bot.get_channel(int(ticket_id))
        if ticket:
            await ticket.send(f"✅ تم تفعيل الكود في السيرفر `{interaction.guild.id}`. سيتم حذف الروم بعد 10 ثوانٍ.")
            await asyncio.sleep(10)
            try: await ticket.delete(reason="Premium code activated")
            except Exception: pass


def build_premium_stats_embed(guild,info):
    usage=info.get("usage",{})
    embed=discord.Embed(title=f"💎 تفاصيل اشتراك Premium | {guild.name}",color=discord.Color.purple())
    embed.add_field(name="📅 تاريخ التفعيل",value=f"<t:{int(info['start_timestamp'])}:F>",inline=False)
    embed.add_field(name="⏳ تاريخ الانتهاء",value=f"<t:{int(info['end_timestamp'])}:F>",inline=False)
    embed.add_field(name="⏱️ الوقت المتبقي",value=f"<t:{int(info['end_timestamp'])}:R>",inline=False)
    embed.add_field(name="🎨 الاسم المخصص",value=f"`{usage.get('name_value','غير مستخدم')}`" if usage.get("custom_name") else "❌ غير مستخدم",inline=False)
    embed.add_field(name="🏞️ الصورة المخصصة",value="✅ مفعلة" if usage.get("custom_avatar") else "❌ غير مفعلة",inline=False)
    embed.add_field(name="🚩 البانر المخصص",value="✅ مفعل" if usage.get("custom_banner") else "❌ غير مفعل",inline=False)
    embed.add_field(name="🪙 اسم الرصيد المعروض",value=f"`{get_guild_coin(guild.id)}`" if usage.get("custom_currency") else "`Rize` (الافتراضي)",inline=False)
    embed.add_field(name="➖ صورة الخط المخصصة",value="✅ مفعلة" if usage.get("custom_line") else "❌ غير مفعلة",inline=False)
    return embed


@bot.tree.command(name="premium_stats",description="عرض تفاصيل Premium والخصائص المستخدمة")
async def premium_stats(interaction:discord.Interaction):
    if not can_manage_premium(interaction.user,interaction.guild): return await interaction.response.send_message("❌ لصاحب السيرفر أو Administrator فقط.",ephemeral=True)
    await cleanup_expired_premium(); info=premium_info(interaction.guild.id)
    if not info: return await interaction.response.send_message("❌ السيرفر لا يملك Premium فعال.",ephemeral=True)
    await interaction.response.send_message(embed=build_premium_stats_embed(interaction.guild,info))


@bot.tree.command(name="premium_status",description="عرض حالة Premium في السيرفر")
async def premium_status(interaction:discord.Interaction):
    if not can_manage_premium(interaction.user,interaction.guild): return await interaction.response.send_message("❌ لصاحب السيرفر أو Administrator فقط.",ephemeral=True)
    await cleanup_expired_premium(); info=premium_info(interaction.guild.id)
    if not info: return await interaction.response.send_message("❌ السيرفر لا يملك Premium فعال.",ephemeral=True)
    await interaction.response.send_message(embed=build_premium_stats_embed(interaction.guild,info))


# ==============================================================================
# 🛡️ 13. الأوامر الإدارية والإشرافية (! و /)
# ==============================================================================
@bot.command(name="set_role")
async def set_role_cmd(ctx, role: discord.Role):
    if not is_owner(ctx.author.id) and not is_admin(ctx.author.id, ctx.guild):
        return await ctx.send("❌ للإدارة العليا فقط!")
    data = load_data()
    gid = str(ctx.guild.id)
    if "guilds" not in data: data["guilds"] = {}
    if gid not in data["guilds"]: data["guilds"][gid] = {}
    data["guilds"][gid]["admin_role"] = role.id
    save_data(data)
    await ctx.send(f"🛡️ تم تعيين رتبة التحكم في البوت لتكون: **{role.name}** بنجاح!")

@bot.tree.command(name="set_role", description="تعيين رتبة التحكم الإداري بالبوت في السيرفر")
@app_commands.describe(role="الرتبة المراد منحها صلاحيات البوت")
async def set_role_slash(interaction: discord.Interaction, role: discord.Role):
    if not is_owner(interaction.user.id) and not is_admin(interaction.user.id, interaction.guild):
        return await interaction.response.send_message("❌ للإدارة العليا فقط!", ephemeral=True)
    data = load_data()
    gid = str(interaction.guild.id)
    if "guilds" not in data: data["guilds"] = {}
    if gid not in data["guilds"]: data["guilds"][gid] = {}
    data["guilds"][gid]["admin_role"] = role.id
    save_data(data)
    await interaction.response.send_message(f"🛡️ تم تعيين رتبة التحكم في البوت لتكون: **{role.name}** بنجاح!")

@bot.command(name="nick")
async def nick_cmd(ctx, member: discord.Member, *, new_nick: Optional[str] = None):
    if not is_admin(ctx.author.id, ctx.guild): return await ctx.send("❌ مخصص للمسؤولين فقط!")
    try:
        if not new_nick:
            await member.edit(nick=None)
            await ctx.send(f"🔄 تم إرجاع اسم {member.mention} إلى اسمه الأصلي الأساسي في ديسكورد بنجاح.")
        else:
            await member.edit(nick=new_nick)
            await ctx.send(f"✏️ تم تغيير لقب {member.display_name} إلى **{new_nick}** بنجاح.")
    except Exception as e:
        await ctx.send(f"❌ حدث خطأ (تأكد من صلاحيات البوت): `{e}`")

async def nick_slash(interaction: discord.Interaction, member: discord.Member, new_nick: Optional[str] = None):
    if not is_admin(interaction.user.id, interaction.guild): return await interaction.response.send_message("❌ مخصص للمسؤولين فقط!", ephemeral=True)
    try:
        if not new_nick:
            await member.edit(nick=None)
            await interaction.response.send_message(f"🔄 تم إرجاع اسم {member.mention} إلى اسمه الأصلي الأساسي في ديسكورد بنجاح.")
        else:
            await member.edit(nick=new_nick)
            await interaction.response.send_message(f"✏️ تم تغيير لقب {member.display_name} إلى **{new_nick}** بنجاح.")
    except Exception as e:
        await interaction.response.send_message(f"❌ حدث خطأ: `{e}`", ephemeral=True)

@bot.command(name="change_coin")
async def change_coin_cmd(ctx, *, coin_name: str):
    if not can_manage_premium(ctx.author,ctx.guild): return await ctx.send("❌ مخصص لمسؤولي السيرفر فقط!")
    if not is_premium_guild(ctx.guild.id): return await ctx.send(premium_required_message())
    name=coin_name.strip()
    set_guild_coin(ctx.guild.id,name)
    update_premium_usage(ctx.guild.id,custom_currency=True,currency_value=name)
    await ctx.send(f"🪙 تم تحديث اسم العملة في هذا السيرفر لتصبح: **{name}** بنجاح!")


@bot.tree.command(name="change_coin",description="تغيير اسم العملة في السيرفر - Premium")
@app_commands.describe(coin_name="اسم العملة الجديد")
async def change_coin_slash(interaction:discord.Interaction,coin_name:str):
    if not can_manage_premium(interaction.user,interaction.guild): return await interaction.response.send_message("❌ مخصص لمسؤولي السيرفر فقط!",ephemeral=True)
    if not is_premium_guild(interaction.guild.id): return await interaction.response.send_message(premium_required_message(),ephemeral=True)
    name=coin_name.strip()
    set_guild_coin(interaction.guild.id,name)
    update_premium_usage(interaction.guild.id,custom_currency=True,currency_value=name)
    await interaction.response.send_message(f"🪙 تم تحديث اسم العملة في هذا السيرفر لتصبح: **{name}** بنجاح!")


@bot.command(name="back_coin")
async def back_coin_cmd(ctx):
    if not can_manage_premium(ctx.author,ctx.guild): return await ctx.send("❌ مخصص لمسؤولي السيرفر فقط!")
    if not is_premium_guild(ctx.guild.id): return await ctx.send(premium_required_message())
    set_guild_coin(ctx.guild.id,"Rize")
    update_premium_usage(ctx.guild.id,custom_currency=False,currency_value="Rize")
    await ctx.send("🔄 تم استعادة اسم العملة الأساسي للسيرفر ليصبح: **Rize** بنجاح!")


@bot.tree.command(name="back_coin",description="استعادة اسم العملة Rize - Premium")
async def back_coin_slash(interaction:discord.Interaction):
    if not can_manage_premium(interaction.user,interaction.guild): return await interaction.response.send_message("❌ مخصص لمسؤولي السيرفر فقط!",ephemeral=True)
    if not is_premium_guild(interaction.guild.id): return await interaction.response.send_message(premium_required_message(),ephemeral=True)
    set_guild_coin(interaction.guild.id,"Rize")
    update_premium_usage(interaction.guild.id,custom_currency=False,currency_value="Rize")
    await interaction.response.send_message("🔄 تم استعادة اسم العملة الأساسي للسيرفر ليصبح: **Rize** بنجاح!")


@bot.command(name="make_easy")
async def make_easy_cmd(ctx, alias: str, *, target_cmd: str):
    if not is_admin(ctx.author.id, ctx.guild): return await ctx.send("❌ مخصص للإدارة!")
    data = load_data()
    gid = str(ctx.guild.id)
    if "guilds" not in data: data["guilds"] = {}
    if gid not in data["guilds"]: data["guilds"][gid] = {}
    if "aliases" not in data["guilds"][gid]: data["guilds"][gid]["aliases"] = {}
    
    clean_alias = alias.lstrip("!").lower()
    data["guilds"][gid]["aliases"][clean_alias] = target_cmd.strip()
    save_data(data)
    await ctx.send(f"⚡ تم إنشاء الاختصار `{clean_alias}` (ويمكنك استخدامه مع أو بدون `!`) ليقوم بتنفيذ: `{target_cmd}` بنجاح!")

@bot.tree.command(name="make_easy", description="إنشاء اختصار أو أمر جديد مخصص")
@app_commands.describe(alias="اسم الاختصار", target_cmd="الأمر الأصلي")
async def make_easy_slash(interaction: discord.Interaction, alias: str, target_cmd: str):
    if not is_admin(interaction.user.id, interaction.guild): return await interaction.response.send_message("❌ مخصص للإدارة!", ephemeral=True)
    data = load_data()
    gid = str(interaction.guild.id)
    if "guilds" not in data: data["guilds"] = {}
    if gid not in data["guilds"]: data["guilds"][gid] = {}
    if "aliases" not in data["guilds"][gid]: data["guilds"][gid]["aliases"] = {}
    
    clean_alias = alias.lstrip("!").lower()
    data["guilds"][gid]["aliases"][clean_alias] = target_cmd.strip()
    save_data(data)
    await interaction.response.send_message(f"⚡ تم إنشاء الاختصار `{clean_alias}` (مع أو بدون `!`) ليقوم بتنفيذ: `{target_cmd}` بنجاح!", ephemeral=True)

@bot.command(name="kick")
async def kick_cmd(ctx, member: discord.Member, *, reason: str = "لم يحدد سبب"):
    if not is_admin(ctx.author.id, ctx.guild):
        return await ctx.send("❌ هذا الأمر مخصص للمسؤولين المعتمدين!")
    try: await member.send(f"👢 تم طردك من **{ctx.guild.name}**.\nالسبب: {reason}")
    except Exception: pass
    await member.kick(reason=reason)
    await ctx.send(f"👢 تم طرد {member.mention} | السبب: {reason}")

async def kick_slash(interaction: discord.Interaction, member: discord.Member, reason: str = "لم يحدد سبب"):
    if not is_admin(interaction.user.id, interaction.guild):
        return await interaction.response.send_message("❌ هذا الأمر مخصص للمسؤولين المعتمدين!", ephemeral=True)
    try: await member.send(f"👢 تم طردك من **{interaction.guild.name}**.\nالسبب: {reason}")
    except Exception: pass
    await member.kick(reason=reason)
    await interaction.response.send_message(f"👢 تم طرد {member.mention} | السبب: {reason}")

@bot.command(name="ban")
async def ban_cmd(ctx, member: discord.Member, *, reason: str = "لم يحدد سبب"):
    if not is_admin(ctx.author.id, ctx.guild):
        return await ctx.send("❌ هذا الأمر مخصص للمسؤولين المعتمدين!")
    try: await member.send(f"🔨 تم حظرك من **{ctx.guild.name}**.\nالسبب: {reason}")
    except Exception: pass
    await member.ban(reason=reason)
    await ctx.send(f"🔨 تم حظر {member.mention} | السبب: {reason}")

async def ban_slash(interaction: discord.Interaction, member: discord.Member, reason: str = "لم يحدد سبب"):
    if not is_admin(interaction.user.id, interaction.guild):
        return await interaction.response.send_message("❌ هذا الأمر مخصص للمسؤولين المعتمدين!", ephemeral=True)
    try: await member.send(f"🔨 تم حظرك من **{interaction.guild.name}**.\nالسبب: {reason}")
    except Exception: pass
    await member.ban(reason=reason)
    await interaction.response.send_message(f"🔨 تم حظر {member.mention} | السبب: {reason}")

@bot.command(name="unban")
async def unban_cmd(ctx, user_id: str):
    if not is_admin(ctx.author.id, ctx.guild):
        return await ctx.send("❌ هذا الأمر مخصص للمسؤولين المعتمدين!")
    user = await bot.fetch_user(int(user_id))
    await ctx.guild.unban(user)
    await ctx.send(f"✅ تم فك حظر {user.name} بنجاح.")

async def unban_slash(interaction: discord.Interaction, user_id: str):
    if not is_admin(interaction.user.id, interaction.guild):
        return await interaction.response.send_message("❌ هذا الأمر مخصص للمسؤولين المعتمدين!", ephemeral=True)
    user = await bot.fetch_user(int(user_id))
    await interaction.guild.unban(user)
    await interaction.response.send_message(f"✅ تم فك حظر {user.name} بنجاح.")

@bot.command(name="make")
async def make_cmd(ctx, member: discord.Member, role: discord.Role):
    if not is_admin(ctx.author.id, ctx.guild):
        return await ctx.send("❌ هذا الأمر مخصص للمسؤولين المعتمدين!")
    try:
        await member.add_roles(role)
        await ctx.send(f"✅ تم إعطاء رتبة {role.name} لـ {member.display_name} بنجاح.")
    except discord.Forbidden:
        await ctx.send("❌ البوت لا يمتلك صلاحيات كافية لإعطاء هذه الرتبة.")
    except Exception as e:
        await ctx.send(f"❌ حدث خطأ: `{e}`")

async def make_slash(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    if not is_admin(interaction.user.id, interaction.guild):
        return await interaction.response.send_message("❌ هذا الأمر مخصص للمسؤولين المعتمدين!", ephemeral=True)
    try:
        await member.add_roles(role)
        await interaction.response.send_message(f"✅ تم إعطاء رتبة {role.name} لـ {member.display_name} بنجاح.")
    except discord.Forbidden:
        await interaction.response.send_message("❌ البوت لا يمتلك صلاحيات كافية لإعطاء هذه الرتبة.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ حدث خطأ: `{e}`", ephemeral=True)

@bot.command(name="unmake")
async def unmake_cmd(ctx, member: discord.Member, role: discord.Role):
    if not is_admin(ctx.author.id, ctx.guild):
        return await ctx.send("❌ هذا الأمر مخصص للمسؤولين المعتمدين!")
    try:
        await member.remove_roles(role)
        await ctx.send(f"🔻 تم سحب رتبة {role.name} من {member.display_name} بنجاح.")
    except discord.Forbidden:
        await ctx.send("❌ البوت لا يمتلك صلاحيات كافية لسحب هذه الرتبة.")
    except Exception as e:
        await ctx.send(f"❌ حدث خطأ: `{e}`")

async def unmake_slash(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    if not is_admin(interaction.user.id, interaction.guild):
        return await interaction.response.send_message("❌ هذا الأمر مخصص للمسؤولين المعتمدين!", ephemeral=True)
    try:
        await member.remove_roles(role)
        await interaction.response.send_message(f"🔻 تم سحب رتبة {role.name} من {member.display_name} بنجاح.")
    except discord.Forbidden:
        await interaction.response.send_message("❌ البوت لا يمتلك صلاحيات كافية لسحب هذه الرتبة.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ حدث خطأ: `{e}`", ephemeral=True)

@bot.command(name="come")
async def come_cmd(ctx, member: discord.Member, *, reason: str = "بدون سبب"):
    if not is_admin(ctx.author.id, ctx.guild):
        return await ctx.send("❌ هذا الأمر مخصص للمسؤولين المعتمدين!")
    try:
        embed = discord.Embed(title="📨 **استدعاء إداري**", description=f"أهلاً بك، يرجى التوجه للروم التالية: {ctx.channel.mention}\n📜 السبب: {reason}", color=discord.Color.gold())
        await member.send(embed=embed)
        await ctx.send(f"📩 تم استدعاء {member.display_name} بنجاح بالخاص.")
    except Exception: await ctx.send(f"⚠️ تعذر إرسال الرسالة لـ {member.display_name} في الخاص.")

async def come_slash(interaction: discord.Interaction, member: discord.Member, reason: str = "بدون سبب"):
    if not is_admin(interaction.user.id, interaction.guild):
        return await interaction.response.send_message("❌ هذا الأمر مخصص للمسؤولين المعتمدين!", ephemeral=True)
    try:
        embed = discord.Embed(title="📨 **استدعاء إداري**", description=f"أهلاً بك، يرجى التوجه للروم التالية: {interaction.channel.mention}\n📜 السبب: {reason}", color=discord.Color.gold())
        await member.send(embed=embed)
        await interaction.response.send_message(f"📩 تم استدعاء {member.display_name} بنجاح بالخاص.")
    except Exception: await interaction.response.send_message(f"⚠️ تعذر إرسال الرسالة لـ {member.display_name} في الخاص.", ephemeral=True)

async def attachment_to_data_uri(attachment: discord.Attachment):
    content_type = attachment.content_type or "image/png"
    if not content_type.startswith("image/"):
        raise ValueError("not_image")
    raw = await attachment.read()
    if len(raw) > 10 * 1024 * 1024:
        raise ValueError("too_large")
    return f"data:{content_type};base64,{base64.b64encode(raw).decode('ascii')}"


async def modify_current_guild_profile(guild_id, **fields):
    payload = {key: value for key, value in fields.items() if value is not ...}
    route = discord.http.Route("PATCH", "/guilds/{guild_id}/members/@me", guild_id=guild_id)
    return await bot.http.request(route, json=payload)


def profile_success_embed(title, changed):
    embed = discord.Embed(title=title, description="تم تحديث ملف البوت **لهذا السيرفر فقط**.", color=discord.Color.green())
    embed.add_field(name="التغييرات", value="\n".join(f"• {item}" for item in changed), inline=False)
    embed.set_footer(text="Rize Server Profile • لا يؤثر على باقي السيرفرات")
    return embed


@bot.command(name="change_name")
async def change_name_cmd(ctx, *, new_name: str):
    if not is_premium_guild(ctx.guild.id): return await ctx.send(premium_required_message())
    if not can_manage_premium(ctx.author,ctx.guild):
        return await ctx.send(embed=error_embed("🔒 غير مصرح", "هذا الأمر مخصص لمسؤولي البوت."))
    try:
        await modify_current_guild_profile(ctx.guild.id, nick=new_name[:32])
        update_premium_usage(ctx.guild.id,custom_name=True,name_value=new_name[:32])
        await ctx.send(embed=profile_success_embed("✅ تم تغيير اسم البوت", [f"الاسم: **{new_name[:32]}**"]))
    except Exception as exc:
        print(f"change_name error: {exc!r}")
        await ctx.send(embed=error_embed("❌ تعذر تغيير الاسم", "تأكد من صلاحية تغيير اللقب ورتبة البوت."))


@bot.tree.command(name="change_name", description="تغيير اسم البوت في هذا السيرفر فقط")
async def change_name_slash(interaction: discord.Interaction, new_name: str):
    if not is_premium_guild(interaction.guild.id): return await interaction.response.send_message(premium_required_message(),ephemeral=True)
    if not can_manage_premium(interaction.user,interaction.guild):
        return await interaction.response.send_message(embed=error_embed("🔒 غير مصرح", "هذا الأمر مخصص لمسؤولي البوت."), ephemeral=True)
    try:
        await modify_current_guild_profile(interaction.guild.id, nick=new_name[:32])
        update_premium_usage(interaction.guild.id,custom_name=True,name_value=new_name[:32])
        await interaction.response.send_message(embed=profile_success_embed("✅ تم تغيير اسم البوت", [f"الاسم: **{new_name[:32]}**"]))
    except Exception as exc:
        print(f"change_name error: {exc!r}")
        await interaction.response.send_message(embed=error_embed("❌ تعذر تغيير الاسم", "تأكد من صلاحية تغيير اللقب ورتبة البوت."), ephemeral=True)


@bot.command(name="change_photo", aliases=["set_photo"])
async def change_photo_cmd(ctx):
    if not is_premium_guild(ctx.guild.id): return await ctx.send(premium_required_message())
    if not can_manage_premium(ctx.author,ctx.guild):
        return await ctx.send(embed=error_embed("🔒 غير مصرح", "هذا الأمر مخصص لمسؤولي البوت."))
    if not ctx.message.attachments:
        return await ctx.send(embed=error_embed("🖼️ صورة مطلوبة", "أرفق صورة مع الأمر `!change_photo`."))
    try:
        avatar = await attachment_to_data_uri(ctx.message.attachments[0])
        await modify_current_guild_profile(ctx.guild.id, avatar=avatar)
        update_premium_usage(ctx.guild.id,custom_avatar=True)
        await ctx.send(embed=profile_success_embed("✅ تم تغيير صورة البوت", ["الصورة الخاصة بهذا السيرفر"]))
    except ValueError:
        await ctx.send(embed=error_embed("❌ ملف غير صالح", "أرفق صورة صحيحة وحجمها أقل من 10MB."))
    except Exception as exc:
        print(f"change_photo error: {exc!r}")
        await ctx.send(embed=error_embed("❌ تعذر تغيير الصورة", "هذه الميزة تحتاج دعماً من Discord للحساب وصلاحيات مناسبة."))


@bot.tree.command(name="change_photo", description="تغيير صورة البوت في هذا السيرفر فقط")
async def change_photo_slash(interaction: discord.Interaction, attachment: discord.Attachment):
    if not is_premium_guild(interaction.guild.id): return await interaction.response.send_message(premium_required_message(),ephemeral=True)
    if not can_manage_premium(interaction.user,interaction.guild):
        return await interaction.response.send_message(embed=error_embed("🔒 غير مصرح", "هذا الأمر مخصص لمسؤولي البوت."), ephemeral=True)
    try:
        avatar = await attachment_to_data_uri(attachment)
        await modify_current_guild_profile(interaction.guild.id, avatar=avatar)
        update_premium_usage(interaction.guild.id,custom_avatar=True)
        await interaction.response.send_message(embed=profile_success_embed("✅ تم تغيير صورة البوت", ["الصورة الخاصة بهذا السيرفر"]))
    except ValueError:
        await interaction.response.send_message(embed=error_embed("❌ ملف غير صالح", "أرفق صورة صحيحة وحجمها أقل من 10MB."), ephemeral=True)
    except Exception as exc:
        print(f"change_photo error: {exc!r}")
        await interaction.response.send_message(embed=error_embed("❌ تعذر تغيير الصورة", "هذه الميزة تحتاج دعماً من Discord للحساب وصلاحيات مناسبة."), ephemeral=True)


@bot.command(name="change_banner")
async def change_banner_cmd(ctx):
    if not is_premium_guild(ctx.guild.id): return await ctx.send(premium_required_message())
    if not can_manage_premium(ctx.author,ctx.guild):
        return await ctx.send(embed=error_embed("🔒 غير مصرح", "هذا الأمر مخصص لمسؤولي البوت."))
    if not ctx.message.attachments:
        return await ctx.send(embed=error_embed("🌄 بانر مطلوب", "أرفق صورة مع الأمر `!change_banner`."))
    try:
        banner = await attachment_to_data_uri(ctx.message.attachments[0])
        await modify_current_guild_profile(ctx.guild.id, banner=banner)
        update_premium_usage(ctx.guild.id,custom_banner=True)
        await ctx.send(embed=profile_success_embed("✅ تم تغيير بانر البوت", ["البانر الخاص بهذا السيرفر"]))
    except ValueError:
        await ctx.send(embed=error_embed("❌ ملف غير صالح", "أرفق صورة صحيحة وحجمها أقل من 10MB."))
    except Exception as exc:
        print(f"change_banner error: {exc!r}")
        await ctx.send(embed=error_embed("❌ تعذر تغيير البانر", "هذه الميزة تحتاج دعماً من Discord للحساب وصلاحيات مناسبة."))


@bot.tree.command(name="change_banner", description="تغيير بانر البوت في هذا السيرفر فقط")
async def change_banner_slash(interaction: discord.Interaction, attachment: discord.Attachment):
    if not is_premium_guild(interaction.guild.id): return await interaction.response.send_message(premium_required_message(),ephemeral=True)
    if not can_manage_premium(interaction.user,interaction.guild):
        return await interaction.response.send_message(embed=error_embed("🔒 غير مصرح", "هذا الأمر مخصص لمسؤولي البوت."), ephemeral=True)
    try:
        banner = await attachment_to_data_uri(attachment)
        await modify_current_guild_profile(interaction.guild.id, banner=banner)
        update_premium_usage(interaction.guild.id,custom_banner=True)
        await interaction.response.send_message(embed=profile_success_embed("✅ تم تغيير بانر البوت", ["البانر الخاص بهذا السيرفر"]))
    except ValueError:
        await interaction.response.send_message(embed=error_embed("❌ ملف غير صالح", "أرفق صورة صحيحة وحجمها أقل من 10MB."), ephemeral=True)
    except Exception as exc:
        print(f"change_banner error: {exc!r}")
        await interaction.response.send_message(embed=error_embed("❌ تعذر تغيير البانر", "هذه الميزة تحتاج دعماً من Discord للحساب وصلاحيات مناسبة."), ephemeral=True)


@bot.tree.command(name="edit_server_profile", description="تعديل ملف البوت الكامل في هذا السيرفر فقط")
@app_commands.describe(nickname="اسم السيرفر", bio="نبذة السيرفر", avatar="صورة السيرفر", banner="بانر السيرفر")
async def edit_server_profile(
    interaction: discord.Interaction,
    nickname: Optional[str] = None,
    bio: Optional[str] = None,
    avatar: Optional[discord.Attachment] = None,
    banner: Optional[discord.Attachment] = None,
):
    if not is_premium_guild(interaction.guild.id): return await interaction.response.send_message(premium_required_message(),ephemeral=True)
    if not can_manage_premium(interaction.user,interaction.guild):
        return await interaction.response.send_message(embed=error_embed("🔒 غير مصرح", "هذا الأمر مخصص لمسؤولي البوت."), ephemeral=True)
    if not any((nickname, bio, avatar, banner)):
        return await interaction.response.send_message(embed=error_embed("⚠️ لا توجد تعديلات", "حدد اسماً أو نبذة أو صورة أو بانر على الأقل."), ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    payload = {}
    changed = []
    try:
        if nickname is not None:
            payload["nick"] = nickname[:32]
            changed.append(f"الاسم: **{nickname[:32]}**")
        if bio is not None:
            payload["bio"] = bio[:190]
            changed.append("النبذة")
        if avatar is not None:
            payload["avatar"] = await attachment_to_data_uri(avatar)
            changed.append("الصورة")
        if banner is not None:
            payload["banner"] = await attachment_to_data_uri(banner)
            changed.append("البانر")
        await modify_current_guild_profile(interaction.guild.id, **payload)
        update_premium_usage(interaction.guild.id,
            custom_name=any("الاسم" in item for item in changed) or premium_info(interaction.guild.id).get("usage",{}).get("custom_name",False),
            name_value=name or premium_info(interaction.guild.id).get("usage",{}).get("name_value"),
            custom_avatar=any("الصورة" in item for item in changed) or premium_info(interaction.guild.id).get("usage",{}).get("custom_avatar",False),
            custom_banner=any("البانر" in item for item in changed) or premium_info(interaction.guild.id).get("usage",{}).get("custom_banner",False))
        await interaction.followup.send(embed=profile_success_embed("✅ تم تعديل ملف البوت", changed), ephemeral=True)
    except ValueError:
        await interaction.followup.send(embed=error_embed("❌ ملف غير صالح", "استخدم صوراً صحيحة وحجم كل صورة أقل من 10MB."), ephemeral=True)
    except Exception as exc:
        print(f"edit_server_profile error: {exc!r}")
        await interaction.followup.send(embed=error_embed("❌ تعذر تعديل الملف", "لم يقبل Discord أحد الحقول. جرّب الحقول منفردة وتأكد من الصلاحيات."), ephemeral=True)


@bot.command(name="say")
async def say_cmd(ctx, *, message: str = ""):
    if not is_owner(ctx.author.id) and not is_admin(ctx.author.id, ctx.guild):
        return await ctx.send("❌ مخصص للإدارة!")
    files=[]
    for att in list(ctx.message.attachments):
        try:
            raw=await att.read()
            files.append(discord.File(io.BytesIO(raw),filename=att.filename,spoiler=att.is_spoiler()))
        except Exception as exc:
            print(f"say attachment error: {exc!r}")
    if not message.strip() and not files:
        return await ctx.send("❌ اكتب رسالة أو ارفع صورة/ملف مع أمر `!say`.",delete_after=5)
    try: await ctx.message.delete()
    except Exception: pass
    await ctx.send(content=message if message.strip() else None,files=files)

@bot.command(name="lock")
async def lock_channel_cmd(ctx):
    if not is_admin(ctx.author.id, ctx.guild):
        return await ctx.send("❌ هذا الأمر مخصص للمسؤولين المعتمدين!")
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 **تم قفل الشات بنجاح.**")

async def lock_channel_slash(interaction: discord.Interaction):
    if not is_admin(interaction.user.id, interaction.guild):
        return await interaction.response.send_message("❌ هذا الأمر مخصص للمسؤولين المعتمدين!", ephemeral=True)
    await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
    await interaction.response.send_message("🔒 **تم قفل الشات بنجاح.**")

@bot.command(name="open")
async def open_channel_cmd(ctx):
    if not is_admin(ctx.author.id, ctx.guild):
        return await ctx.send("❌ هذا الأمر مخصص للمسؤولين المعتمدين!")
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 **تم فتح الشات بنجاح.**")

async def open_channel_slash(interaction: discord.Interaction):
    if not is_admin(interaction.user.id, interaction.guild):
        return await interaction.response.send_message("❌ هذا الأمر مخصص للمسؤولين المعتمدين!", ephemeral=True)
    await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
    await interaction.response.send_message("🔓 **تم فتح الشات بنجاح.**")

@bot.command(name="hide")
async def hide_channel_cmd(ctx):
    if not is_admin(ctx.author.id, ctx.guild):
        return await ctx.send("❌ هذا الأمر مخصص للمسؤولين المعتمدين!")
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ctx.send("👻 **تم إخفاء الروم بنجاح.**")

async def hide_channel_slash(interaction: discord.Interaction):
    if not is_admin(interaction.user.id, interaction.guild):
        return await interaction.response.send_message("❌ هذا الأمر مخصص للمسؤولين المعتمدين!", ephemeral=True)
    await interaction.channel.set_permissions(interaction.guild.default_role, view_channel=False)
    await interaction.response.send_message("👻 **تم إخفاء الروم بنجاح.**")

@bot.command(name="show")
async def show_channel_cmd(ctx):
    if not is_admin(ctx.author.id, ctx.guild):
        return await ctx.send("❌ هذا الأمر مخصص للمسؤولين المعتمدين!")
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
    await ctx.send("👁️ **تم إظهار الروم بنجاح.**")

async def show_channel_slash(interaction: discord.Interaction):
    if not is_admin(interaction.user.id, interaction.guild):
        return await interaction.response.send_message("❌ هذا الأمر مخصص للمسؤولين المعتمدين!", ephemeral=True)
    await interaction.channel.set_permissions(interaction.guild.default_role, view_channel=True)
    await interaction.response.send_message("👁️ **تم إظهار الروم بنجاح.**")

@bot.command(name="rename")
async def rename_channel_cmd(ctx, *, new_name: str):
    if not is_admin(ctx.author.id, ctx.guild):
        return await ctx.send("❌ هذا الأمر مخصص للمسؤولين المعتمدين!")
    old_name = ctx.channel.name
    await ctx.channel.edit(name=new_name)
    await ctx.send(f"✏️ تم تغيير اسم الروم من **#{old_name}** إلى **#{new_name}**")

async def rename_channel_slash(interaction: discord.Interaction, new_name: str):
    if not is_admin(interaction.user.id, interaction.guild):
        return await interaction.response.send_message("❌ هذا الأمر مخصص للمسؤولين المعتمدين!", ephemeral=True)
    old_name = interaction.channel.name
    await interaction.channel.edit(name=new_name)
    await interaction.response.send_message(f"✏️ تم تغيير اسم الروم من **#{old_name}** إلى **#{new_name}**")

@bot.command(name="del", aliases=["purge"])
async def delete_messages_cmd(ctx, amount: int = 5):
    if not is_admin(ctx.author.id,ctx.guild):
        return await ctx.send("❌ هذا الأمر مخصص للمسؤولين المعتمدين!")
    amount=max(1,min(int(amount),1000))
    try:
        await ctx.message.delete()
        deleted=await ctx.channel.purge(limit=amount)
        notice=await ctx.send(f"🔹 تم مسح {code_number(len(deleted))} رسالة بنجاح.")
        await asyncio.sleep(3)
        await notice.delete()
    except Exception as exc:
        await ctx.send(f"❌ تعذر مسح الرسائل: `{exc}`")


@bot.command(name="clear")
async def clear_all_messages_cmd(ctx):
    """مسح جميع الرسائل القابلة للمسح في الروم الحالي."""
    if not is_admin(ctx.author.id,ctx.guild):
        return await ctx.send("❌ هذا الأمر مخصص للمسؤولين المعتمدين!")
    try:
        await ctx.message.delete()
    except Exception:
        pass
    total=0
    try:
        while True:
            deleted=await ctx.channel.purge(limit=100)
            count=len(deleted)
            total+=count
            if count<100:
                break
            await asyncio.sleep(1.2)
        notice=await ctx.send(f"🔹 تم مسح جميع رسائل الروم القابلة للمسح. العدد: {code_number(total)}")
        await asyncio.sleep(4)
        await notice.delete()
    except Exception as exc:
        await ctx.send(f"❌ تعذر إكمال المسح: `{exc}`")


async def delete_messages_slash(interaction:discord.Interaction,amount:app_commands.Range[int,1,1000]=5):
    if not is_admin(interaction.user.id,interaction.guild):
        return await interaction.response.send_message("❌ هذا الأمر مخصص للمسؤولين المعتمدين!",ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    try:
        deleted=await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"🔹 تم مسح {code_number(len(deleted))} رسالة بنجاح.",ephemeral=True)
    except Exception as exc:
        await interaction.followup.send(f"❌ تعذر مسح الرسائل: `{exc}`",ephemeral=True)


# ==============================================================================
# 👑 14. إدارة صلاحيات المطورين والأدمن
# ==============================================================================
@bot.command(name="give_per")
async def give_per_cmd(ctx, member: discord.Member):
    if not is_owner(ctx.author.id): return await ctx.send("❌ مخصص للمالك الرئيسي حصراً!")
    
    if member.id not in ADMIN_IDS: ADMIN_IDS.append(member.id)
    if member.id not in PER_DEVS: PER_DEVS.append(member.id)
    data=load_data(); data["per_devs"]=[uid for uid in PER_DEVS if uid != PRIMARY_OWNER_ID]
    data["admin_ids"]=[uid for uid in ADMIN_IDS if uid != PRIMARY_OWNER_ID]
    save_data(data)
        
    await ctx.send(f"👑 **تم منح صلاحيات المطور والأدمن المطلقة لـ {member.display_name} بنجاح!**")

@bot.tree.command(name="give_per", description="إعطاء صلاحية المطور والأدمن المطلقة لشخص (للمالك فقط)")
async def give_per_slash(interaction: discord.Interaction, member: discord.Member):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ مخصص للمالك الرئيسي حصراً!", ephemeral=True)
    
    if member.id not in ADMIN_IDS: ADMIN_IDS.append(member.id)
    if member.id not in PER_DEVS: PER_DEVS.append(member.id)
    data=load_data(); data["per_devs"]=[uid for uid in PER_DEVS if uid != PRIMARY_OWNER_ID]
    data["admin_ids"]=[uid for uid in ADMIN_IDS if uid != PRIMARY_OWNER_ID]
    save_data(data)
        
    await interaction.response.send_message(f"👑 **تم منح صلاحيات المطور والأدمن المطلقة لـ {member.display_name} بنجاح!**", ephemeral=True)

@bot.command(name="ungive_per")
async def ungive_per_cmd(ctx, member: discord.Member):
    if not is_owner(ctx.author.id): return await ctx.send("❌ مخصص للمالك الرئيسي حصراً!")
    if member.id == PRIMARY_OWNER_ID:
        return await ctx.send("❌ لا يمكنك سحب الصلاحيات من المالك الرئيسي للبوت!")
    
    if member.id in ADMIN_IDS: ADMIN_IDS.remove(member.id)
    if member.id in PER_DEVS: PER_DEVS.remove(member.id)
    data=load_data(); data["per_devs"]=[uid for uid in PER_DEVS if uid != PRIMARY_OWNER_ID]
    data["admin_ids"]=[uid for uid in ADMIN_IDS if uid != PRIMARY_OWNER_ID]
    save_data(data)
        
    await ctx.send(f"🔻 **تم إزالة صلاحيات المطور والأدمن المطلقة من {member.display_name} تماماً!**")

@bot.tree.command(name="ungive_per", description="سحب صلاحية المطور والأدمن من شخص (للمالك فقط)")
async def ungive_per_slash(interaction: discord.Interaction, member: discord.Member):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ مخصص للمالك الرئيسي حصراً!", ephemeral=True)
    if member.id == PRIMARY_OWNER_ID:
        return await interaction.response.send_message("❌ لا يمكنك سحب الصلاحيات من المالك الرئيسي للبوت!", ephemeral=True)
    
    if member.id in ADMIN_IDS: ADMIN_IDS.remove(member.id)
    if member.id in PER_DEVS: PER_DEVS.remove(member.id)
    data=load_data(); data["per_devs"]=[uid for uid in PER_DEVS if uid != PRIMARY_OWNER_ID]
    data["admin_ids"]=[uid for uid in ADMIN_IDS if uid != PRIMARY_OWNER_ID]
    save_data(data)
        
    await interaction.response.send_message(f"🔻 **تم إزالة صلاحيات المطور والأدمن المطلقة من {member.display_name} تماماً!**", ephemeral=True)

@bot.command(name="show_per")
async def show_per_cmd(ctx):
    if not is_admin(ctx.author.id, ctx.guild): return await ctx.send("❌ مخصص للإدارة المصرح لها فقط!")
    
    primary_owner = f"👑 **المالك الرئيسي الحصري:** <@{PRIMARY_OWNER_ID}> (`{PRIMARY_OWNER_ID}`) — *(يملك الأوامر المطلقة ⚡)*"
    other_devs = []
    for uid in PER_DEVS:
        if uid != PRIMARY_OWNER_ID:
            other_devs.append(f"• <@{uid}> (`{uid}`) — **[معـه الأوامر المطلقة⚡]**")
            
    devs_text = "\n".join(other_devs) if other_devs else "لا يوجد مطورين آخرين مضافين حالياً."
    
    embed = discord.Embed(
        title="👑 **قائمة المطورين وصلاحيات الـ Per المطلقة**",
        description=f"{primary_owner}\n\n🛠️ **المطورون المضافون عبر give_per:**\n{devs_text}",
        color=discord.Color.gold()
    )
    await ctx.send(embed=embed)

@bot.tree.command(name="show_per", description="عرض المطورين والأشخاص الحاصلين على give_per والصلاحيات المطلقة")
async def show_per_slash(interaction: discord.Interaction):
    if not is_admin(interaction.user.id, interaction.guild): return await interaction.response.send_message("❌ مخصص للإدارة المصرح لها فقط!", ephemeral=True)
    
    primary_owner = f"👑 **المالك الرئيسي الحصري:** <@{PRIMARY_OWNER_ID}> (`{PRIMARY_OWNER_ID}`) — *(يملك الأوامر المطلقة ⚡)*"
    other_devs = []
    for uid in PER_DEVS:
        if uid != PRIMARY_OWNER_ID:
            other_devs.append(f"• <@{uid}> (`{uid}`) — **[معـه الأوامر المطلقة⚡]**")
            
    devs_text = "\n".join(other_devs) if other_devs else "لا يوجد مطورين آخرين مضافين حالياً."
    
    embed = discord.Embed(
        title="👑 **قائمة المطورين وصلاحيات الـ Per المطلقة**",
        description=f"{primary_owner}\n\n🛠️ **المطورون المضافون عبر give_per:**\n{devs_text}",
        color=discord.Color.gold()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.command(name="show_admin")
async def show_admin_cmd(ctx):
    if not is_admin(ctx.author.id, ctx.guild): return await ctx.send("❌ مخصص للإداريين المصرح لهم فقط!")
    
    admin_lines = []
    for uid in ADMIN_IDS:
        if uid in PER_DEVS or uid == PRIMARY_OWNER_ID:
            admin_lines.append(f"• <@{uid}> (`{uid}`) — **[معـه الأوامر المطلقة ⚡]**")
        else:
            admin_lines.append(f"• <@{uid}> (`{uid}`) — (أدمن عادي)")
            
    text = "\n".join(admin_lines) if admin_lines else "لا يوجد إداريين مضافين حالياً."
    
    embed = discord.Embed(
        title="🛡️ **قائمة إداريين البوت والأدمن (Admin List)**",
        description=text,
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@bot.tree.command(name="show_admin", description="عرض قائمة الإداريين والأدمن مع بيان من يملك الصلاحيات المطلقة")
async def show_admin_slash(interaction: discord.Interaction):
    if not is_admin(interaction.user.id, interaction.guild): return await interaction.response.send_message("❌ مخصص للإداريين المصرح لهم فقط!", ephemeral=True)
    
    admin_lines = []
    for uid in ADMIN_IDS:
        if uid in PER_DEVS or uid == PRIMARY_OWNER_ID:
            admin_lines.append(f"• <@{uid}> (`{uid}`) — **[معـه الأوامر المطلقة ⚡]**")
        else:
            admin_lines.append(f"• <@{uid}> (`{uid}`) — (أدمن عادي)")
            
    text = "\n".join(admin_lines) if admin_lines else "لا يوجد إداريين مضافين حالياً."
    
    embed = discord.Embed(
        title="🛡️ **قائمة إداريين البوت والأدمن (Admin List)**",
        description=text,
        color=discord.Color.red()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.command(name="rize", aliases=["zex"])
async def add_bal(ctx, member: discord.Member, amount: str):
    if not is_admin(ctx.author.id, ctx.guild): return await ctx.send("❌ للإدارة العليا فقط!")
    coin = get_guild_coin(ctx.guild.id)
    parsed = parse_number(amount)
    if not parsed or parsed <= 0: return await ctx.send("❌ عدد عملات غير صحيح!")
    budget = get_guild_budget(ctx.guild.id)
    if parsed > budget: return await ctx.send(f"❌ ميزانية السيرفر لا تكفي (الميزانية حالياً: `{budget:,}` {coin})!\n💡 يرجى شحن ميزانية السيرفر أولاً عبر أمر `!give_server`.")
    
    update_guild_budget(ctx.guild.id, -parsed)
    update_balance(member.id, parsed)
    
    try:
        embed_dm = discord.Embed(title="📥 **تم استلام عملات!**", description=f"استلمت **{parsed:,} {coin}** 🪙 من الأدمن **{ctx.author.display_name}**.\n💰 رصيدك: `{get_balance(member.id):,}` {coin}", color=discord.Color.green())
        await member.send(embed=embed_dm)
    except Exception: pass
    await ctx.send(f"✅ تم إضافة **{parsed:,} {coin}** 🪙 لحساب {member.mention}.\n🔻 الميزانية المتبقية للسيرفر: `{get_guild_budget(ctx.guild.id):,}` {coin}.")

@bot.tree.command(name="rize", description="إضافة عملات للشخص (يخصم من ميزانية السيرفر)")
async def add_bal_slash(interaction: discord.Interaction, member: discord.Member, amount: str):
    if not is_admin(interaction.user.id, interaction.guild): return await interaction.response.send_message("❌ للإدارة العليا فقط!", ephemeral=True)
    coin = get_guild_coin(interaction.guild.id)
    parsed = parse_number(amount)
    if not parsed or parsed <= 0: return await interaction.response.send_message("❌ عدد عملات غير صحيح!", ephemeral=True)
    budget = get_guild_budget(interaction.guild.id)
    if parsed > budget: return await interaction.response.send_message(f"❌ ميزانية السيرفر لا تكفي (الميزانية حالياً: `{budget:,}` {coin})!\n💡 يرجى شحن ميزانية السيرفر أولاً عبر `/give_server`.", ephemeral=True)
    
    update_guild_budget(interaction.guild.id, -parsed)
    update_balance(member.id, parsed)
    
    try:
        embed_dm = discord.Embed(title="📥 **تم استلام عملات!**", description=f"استلمت **{parsed:,} {coin}** 🪙 من الأدمن **{interaction.user.display_name}**.\n💰 رصيدك: `{get_balance(member.id):,}` {coin}", color=discord.Color.green())
        await member.send(embed=embed_dm)
    except Exception: pass
    await interaction.response.send_message(f"✅ تم إضافة **{parsed:,} {coin}** 🪙 لحساب {member.mention}.\n🔻 الميزانية المتبقية للسيرفر: `{get_guild_budget(interaction.guild.id):,}` {coin}.")

@bot.command(name="remove")
async def remove_bal(ctx, member: discord.Member, amount: str):
    if not is_admin(ctx.author.id, ctx.guild): return await ctx.send("❌ للإدارة العليا فقط!")
    coin = get_guild_coin(ctx.guild.id)
    parsed = parse_number(amount)
    if not parsed or parsed <= 0: return await ctx.send("❌ عدد عملات غير صحيح!")
    update_balance(member.id, -parsed)
    try:
        embed_dm = discord.Embed(title="🔻 **تم خصم عملات!**", description=f"تم خصم **{parsed:,} {coin}** 🪙 بواسطة الأدمن **{ctx.author.display_name}**.\n💰 رصيدك: `{get_balance(member.id):,}` {coin}", color=discord.Color.red())
        await member.send(embed=embed_dm)
    except Exception: pass
    await ctx.send(f"🗑️ تم خصم **{parsed:,} {coin}** 🪙 من حساب {member.mention}.")

@bot.tree.command(name="remove", description="خصم عملات من شخص")
async def remove_bal_slash(interaction: discord.Interaction, member: discord.Member, amount: str):
    if not is_admin(interaction.user.id, interaction.guild): return await interaction.response.send_message("❌ للإدارة العليا فقط!", ephemeral=True)
    coin = get_guild_coin(interaction.guild.id)
    parsed = parse_number(amount)
    if not parsed or parsed <= 0: return await interaction.response.send_message("❌ عدد عملات غير صحيح!", ephemeral=True)
    update_balance(member.id, -parsed)
    try:
        embed_dm = discord.Embed(title="🔻 **تم خصم عملات!**", description=f"تم خصم **{parsed:,} {coin}** 🪙 بواسطة الأدمن **{interaction.user.display_name}**.\n💰 رصيدك: `{get_balance(member.id):,}` {coin}", color=discord.Color.red())
        await member.send(embed=embed_dm)
    except Exception: pass
    await interaction.response.send_message(f"🗑️ تم خصم **{parsed:,} {coin}** 🪙 من حساب {member.mention}.")

@bot.command(name="give_server")
async def give_server_cmd(ctx, amount: str, server_id: str = None):
    if not is_admin(ctx.author.id, ctx.guild): return await ctx.send("❌ للإدارة العليا فقط!")
    coin = get_guild_coin(ctx.guild.id)
    parsed = parse_number(amount)
    if not parsed or parsed <= 0: return await ctx.send("❌ مبلغ غير صحيح!")
    
    if server_id:
        try: target_guild_id = int(server_id.strip())
        except ValueError: return await ctx.send("❌ يرجى إدخال ID سيرفر صحيح (أرقام فقط)!")
    else: target_guild_id = ctx.guild.id

    update_guild_budget(target_guild_id, parsed)
    current_b = get_guild_budget(target_guild_id)
    target_guild = bot.get_guild(target_guild_id)
    server_name = f"**{target_guild.name}** (`{target_guild_id}`)" if target_guild else f"`{target_guild_id}`"
    
    await ctx.send(f"💳 تم إضافة **{parsed:,} {coin}** 🪙 لميزانية السيرفر {server_name} بنجاح!\n🏛️ **الميزانية الكلية الآن:** `{current_b:,}` {coin}")

@bot.tree.command(name="give_server", description="شحن ميزانية السيرفر بالعملات عن بعد عبر الـ ID")
@app_commands.describe(amount="المبلغ المراد إضافته", server_id="رقم الـ ID الخاص بالسيرفر")
async def give_server_slash(interaction: discord.Interaction, amount: str, server_id: Optional[str] = None):
    if not is_admin(interaction.user.id, interaction.guild): return await interaction.response.send_message("❌ للإدارة العليا فقط!", ephemeral=True)
    coin = get_guild_coin(interaction.guild.id)
    parsed = parse_number(amount)
    if not parsed or parsed <= 0: return await interaction.response.send_message("❌ مبلغ غير صحيح!", ephemeral=True)
    
    if server_id:
        try: target_guild_id = int(server_id.strip())
        except ValueError: return await interaction.response.send_message("❌ يرجى إدخال ID سيرفر صحيح (أرقام فقط)!", ephemeral=True)
    else: target_guild_id = interaction.guild.id

    update_guild_budget(target_guild_id, parsed)
    current_b = get_guild_budget(target_guild_id)
    target_guild = bot.get_guild(target_guild_id)
    server_name = f"**{target_guild.name}** (`{target_guild_id}`)" if target_guild else f"`{target_guild_id}`"
    
    await interaction.response.send_message(f"💳 تم إضافة **{parsed:,} {coin}** 🪙 لميزانية السيرفر {server_name} بنجاح!\n🏛️ **الميزانية الكلية الآن:** `{current_b:,}` {coin}")

@bot.command(name="take_server")
async def take_server_cmd(ctx, amount: str, server_id: str = None):
    if not is_admin(ctx.author.id, ctx.guild): return await ctx.send("❌ للإدارة العليا فقط!")
    coin = get_guild_coin(ctx.guild.id)
    parsed = parse_number(amount)
    if not parsed or parsed <= 0: return await ctx.send("❌ مبلغ غير صحيح!")
    
    if server_id:
        try: target_guild_id = int(server_id.strip())
        except ValueError: return await ctx.send("❌ يرجى إدخال ID سيرفر صحيح (أرقام فقط)!")
    else: target_guild_id = ctx.guild.id

    update_guild_budget(target_guild_id, -parsed)
    new_b = get_guild_budget(target_guild_id)
    target_guild = bot.get_guild(target_guild_id)
    server_name = f"**{target_guild.name}** (`{target_guild_id}`)" if target_guild else f"`{target_guild_id}`"
    
    await ctx.send(f"📉 تم خصم **{parsed:,} {coin}** 🪙 من ميزانية السيرفر {server_name} بنجاح!\n🏛️ **الميزانية الكلية الآن:** `{new_b:,}` {coin}")

@bot.tree.command(name="take_server", description="خصم مبلغ من ميزانية سيرفر معين عن بعد عبر الـ ID")
@app_commands.describe(amount="المبلغ المراد خصمه", server_id="رقم الـ ID الخاص بالسيرفر")
async def take_server_slash(interaction: discord.Interaction, amount: str, server_id: Optional[str] = None):
    if not is_admin(interaction.user.id, interaction.guild): return await interaction.response.send_message("❌ للإدارة العليا فقط!", ephemeral=True)
    coin = get_guild_coin(interaction.guild.id)
    parsed = parse_number(amount)
    if not parsed or parsed <= 0: return await interaction.response.send_message("❌ مبلغ غير صحيح!", ephemeral=True)
    
    if server_id:
        try: target_guild_id = int(server_id.strip())
        except ValueError: return await interaction.response.send_message("❌ يرجى إدخال ID سيرفر صحيح (أرقام فقط)!", ephemeral=True)
    else: target_guild_id = interaction.guild.id

    update_guild_budget(target_guild_id, -parsed)
    new_b = get_guild_budget(target_guild_id)
    target_guild = bot.get_guild(target_guild_id)
    server_name = f"**{target_guild.name}** (`{target_guild_id}`)" if target_guild else f"`{target_guild_id}`"
    
    await interaction.response.send_message(f"📉 تم خصم **{parsed:,} {coin}** 🪙 من ميزانية السيرفر {server_name} بنجاح!\n🏛️ **الميزانية الكلية الآن:** `{new_b:,}` {coin}")

@bot.command(name="set_budget")
async def set_budget_owner_only(ctx, amount: str, server_id: str = None):
    if not is_owner(ctx.author.id):
        return await ctx.send("❌ `!set_budget` للمالك الرئيسي للبوت فقط.")
    parsed=parse_number(amount)
    if parsed is None or parsed<0:
        return await ctx.send("❌ مبلغ غير صحيح.")
    target_id=ctx.guild.id
    if server_id:
        try: target_id=int(server_id)
        except ValueError: return await ctx.send("❌ ID السيرفر غير صحيح.")
    set_guild_budget(target_id,parsed)
    await ctx.send(f"✅ تم تعيين ميزانية السيرفر {code_id(target_id)} إلى {smart_number(parsed,force_copy=True)} {get_guild_coin(target_id)}.")


@bot.command(name="server_budget")
async def server_budget_cmd(ctx):
    if not is_admin(ctx.author.id, ctx.guild): return await ctx.send("❌ الأمر للإدارة والمالك فقط.")
    coin = get_guild_coin(ctx.guild.id)
    budget = get_guild_budget(ctx.guild.id)
    embed = discord.Embed(title="🏛️ **ميزانية السيرفر الحالية**", description=f"الميزانية المتوفرة للفعاليات والتحويلات بالسيرفر:\n💰 **`{budget:,}` {coin}** 🪙", color=discord.Color.gold())
    await ctx.send(embed=embed)

@bot.tree.command(name="server_budget", description="عرض ميزانية السيرفر الحالية")
async def server_budget_slash(interaction: discord.Interaction):
    if not is_admin(interaction.user.id, interaction.guild): return await interaction.response.send_message("❌ الأمر للإدارة والمالك فقط.",ephemeral=True)
    coin = get_guild_coin(interaction.guild.id)
    budget = get_guild_budget(interaction.guild.id)
    embed = discord.Embed(title="🏛️ **ميزانية السيرفر الحالية**", description=f"الميزانية المتوفرة للفعاليات والتحويلات بالسيرفر:\n💰 **`{budget:,}` {coin}** 🪙", color=discord.Color.gold())
    await interaction.response.send_message(embed=embed)

@bot.command(name="set_server_budget")
async def set_server_budget_cmd(ctx, amount: str, server_id: str = None):
    if not is_owner(ctx.author.id): return await ctx.send("❌ أمر تعيين الميزانية للمالك الرئيسي للبوت فقط.")
    coin = get_guild_coin(ctx.guild.id)
    parsed = parse_number(amount)
    if parsed is None or parsed < 0: return await ctx.send("❌ مبلغ غير صحيح!")
    
    if server_id:
        try: target_guild_id = int(server_id.strip())
        except ValueError: return await ctx.send("❌ يرجى إدخال ID سيرفر صحيح (أرقام فقط)!")
    else: target_guild_id = ctx.guild.id

    set_guild_budget(target_guild_id, parsed)
    await ctx.send(f"⚙️ تم تعيين ميزانية السيرفر (`{target_guild_id}`) لتصبح: **{parsed:,} {coin}** 🪙 بنجاح!")

@bot.tree.command(name="set_server_budget", description="تحديد ميزانية السيرفر مباشرة")
@app_commands.describe(amount="المبلغ الجديد", server_id="رقم الـ ID الخاص بالسيرفر")
async def set_server_budget_slash(interaction: discord.Interaction, amount: str, server_id: Optional[str] = None):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ أمر تعيين الميزانية للمالك الرئيسي للبوت فقط.", ephemeral=True)
    coin = get_guild_coin(interaction.guild.id)
    parsed = parse_number(amount)
    if parsed is None or parsed < 0: return await interaction.response.send_message("❌ مبلغ غير صحيح!", ephemeral=True)
    
    if server_id:
        try: target_guild_id = int(server_id.strip())
        except ValueError: return await interaction.response.send_message("❌ يرجى إدخال ID سيرفر صحيح (أرقام فقط)!", ephemeral=True)
    else: target_guild_id = interaction.guild.id

    set_guild_budget(target_guild_id, parsed)
    await interaction.response.send_message(f"⚙️ تم تعيين ميزانية السيرفر (`{target_guild_id}`) لتصبح: **{parsed:,} {coin}** 🪙 بنجاح!")

class ClaimBoxView(discord.ui.View):
    def __init__(self, amount: int, coin: str):
        super().__init__(timeout=60)
        self.amount = amount
        self.coin = coin
        self.claimed = False

    @discord.ui.button(label="فتح الصندوق 🎁", style=discord.ButtonStyle.success)
    async def claim_box(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.claimed: return await interaction.response.send_message("❌ تم فتح الصندوق بالفعل!", ephemeral=True)
        self.claimed = True
        update_balance(interaction.user.id, self.amount)
        for item in self.children: item.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.channel.send(f"🎉 **تهانينا!** {interaction.user.display_name} كان الأسرع وفتح الصندوق وحصل على **{self.amount:,} {self.coin}** 🪙!")

@bot.command(name="box")
async def box_cmd(ctx, amount: str):
    if not is_admin(ctx.author.id, ctx.guild):
        return await ctx.send("❌ هذا الأمر مخصص للمسؤولين المعتمدين!")
    coin = get_guild_coin(ctx.guild.id)
    parsed = parse_number(amount)
    if not parsed or parsed <= 0: return await ctx.send("❌ مبلغ غير صحيح!")
    
    budget = get_guild_budget(ctx.guild.id)
    if parsed > budget: return await ctx.send(f"❌ ميزانية السيرفر لا تكفي لإنشاء الصندوق! المتبقي: `{budget:,}` {coin}.")

    update_guild_budget(ctx.guild.id, -parsed)
    embed = discord.Embed(title="🎁 **صندوق العملات السريع!**", description=f"يحتوي الصندوق على **{parsed:,} {coin}** 🪙!\nالأسرع بالضغط على الزر أدناه يأخذ الجائزة!", color=discord.Color.gold())
    await ctx.send(embed=embed, view=ClaimBoxView(parsed, coin))

@bot.tree.command(name="box", description="إنشاء صندوق عملات للأسرع")
async def box_slash(interaction: discord.Interaction, amount: str):
    if not is_admin(interaction.user.id, interaction.guild):
        return await interaction.response.send_message("❌ هذا الأمر مخصص للمسؤولين المعتمدين!", ephemeral=True)
    coin = get_guild_coin(interaction.guild.id)
    parsed = parse_number(amount)
    if not parsed or parsed <= 0: return await interaction.response.send_message("❌ مبلغ غير صحيح!", ephemeral=True)
    
    budget = get_guild_budget(interaction.guild.id)
    if parsed > budget: return await interaction.response.send_message(f"❌ ميزانية السيرفر لا تكفي لإنشاء الصندوق! المتبقي: `{budget:,}` {coin}.", ephemeral=True)

    update_guild_budget(interaction.guild.id, -parsed)
    embed = discord.Embed(title="🎁 **صندوق العملات السريع!**", description=f"يحتوي الصندوق على **{parsed:,} {coin}** 🪙!\nالأسرع بالضغط على الزر أدناه يأخذ الجائزة!", color=discord.Color.gold())
    await interaction.response.send_message(embed=embed, view=ClaimBoxView(parsed, coin))

@bot.command(name="takefrom")
async def takefrom_cmd(ctx, member: discord.Member):
    if not is_admin(ctx.author.id, ctx.guild): return await ctx.send("❌ للإدارة العليا فقط!")
    set_balance(member.id, 0)
    await ctx.send(f"🧹 تم تصفير رصيد {member.display_name} بالكامل.")

@bot.tree.command(name="takefrom", description="تصفير رصيد العضو")
async def takefrom_slash(interaction: discord.Interaction, member: discord.Member):
    if not is_admin(interaction.user.id, interaction.guild): return await interaction.response.send_message("❌ للإدارة العليا فقط!", ephemeral=True)
    set_balance(member.id, 0)
    await interaction.response.send_message(f"🧹 تم تصفير رصيد {member.display_name} بالكامل.")

@bot.command(name="blacklist_role")
async def blacklist_role_cmd(ctx,role:discord.Role,*,reason="رتبة محظورة"):
    if not is_owner(ctx.author.id): return await ctx.send("❌ للمالك فقط.")
    data=load_data(); data.setdefault("blacklist_roles",{})[str(role.id)]={"name":role.name,"guild_id":ctx.guild.id,"reason":reason}; save_data(data)
    affected=0
    for guild in bot.guilds:
        for member in guild.members:
            if user_has_blacklist_role(member):
                set_balance(member.id,0); affected+=1
    await ctx.send(f"🚫 تم حظر رتبة {role.mention} عالمياً وتصفير أرصدة {code_number(affected)} عضو مطابق.")


@bot.command(name="unblacklist_role_user")
async def unblacklist_role_user_cmd(ctx,user_id:str):
    if not is_owner(ctx.author.id): return await ctx.send("❌ للمالك فقط.")
    data=load_data(); removed=data.setdefault("role_blacklisted_users",{}).pop(str(user_id),None); save_data(data)
    await ctx.send("✅ تم فك الحظر العام عن المستخدم." if removed else "❌ المستخدم غير موجود في حظر الرتب.")


@bot.command(name="unblacklist_role")
async def unblacklist_role_cmd(ctx,role_id:str):
    if not is_owner(ctx.author.id): return await ctx.send("❌ للمالك فقط.")
    data=load_data(); removed=data.setdefault("blacklist_roles",{}).pop(str(role_id),None); save_data(data)
    await ctx.send("✅ تم فك حظر الرتبة." if removed else "❌ الرتبة غير موجودة.")


@bot.command(name="blacklist")
async def blacklist_cmd(ctx,target:str,*,reason:str=None):
    if not is_owner(ctx.author.id): return await ctx.send("❌ مخصص للمالك فقط.")
    if not reason or not reason.strip(): return await ctx.send("❌ لازم تكتب السبب. مثال: `!blacklist 123456789 السبب هنا`")
    match=re.search(r"(\d{15,22})",target)
    if not match: return await ctx.send("❌ اكتب منشن أو ID صحيح.")
    user_id=int(match.group(1)); add_to_blacklist(user_id,reason.strip(),ctx.author.id); set_balance(user_id,0)
    ok,status=await sync_blacklist_role(user_id,True)
    await ctx.send(f"⛔ تم وضع <@{user_id}> في البلاك ليست.\nالسبب: {reason.strip()}\nحالة الرتبة: {status}")


@bot.tree.command(name="blacklist",description="إضافة عضو أو ID للبلاك ليست مع سبب إجباري")
async def blacklist_slash(interaction:discord.Interaction,user_id:str,reason:str):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ للمالك فقط.",ephemeral=True)
    if not reason.strip(): return await interaction.response.send_message("❌ السبب إجباري.",ephemeral=True)
    match=re.search(r"(\d{15,22})",user_id)
    if not match: return await interaction.response.send_message("❌ اكتب ID صحيح.",ephemeral=True)
    uid=int(match.group(1)); add_to_blacklist(uid,reason.strip(),interaction.user.id); set_balance(uid,0)
    ok,status=await sync_blacklist_role(uid,True)
    await interaction.response.send_message(f"⛔ تم وضع <@{uid}> في البلاك ليست.\nالسبب: {reason.strip()}\nحالة الرتبة: {status}",ephemeral=True)


@bot.command(name="unblacklist")
async def unblacklist_cmd(ctx,target:str,*,reason:str=None):
    if not is_owner(ctx.author.id): return await ctx.send("❌ للمالك فقط.")
    match=re.search(r"(\d{15,22})",target)
    if not match: return await ctx.send("❌ اكتب منشن أو ID صحيح.")
    uid=int(match.group(1)); remove_from_blacklist(uid,reason or "فك الحظر",ctx.author.id)
    ok,status=await sync_blacklist_role(uid,False)
    await ctx.send(f"✅ تم فك البلاك ليست عن <@{uid}>.\nحالة الرتبة: {status}")


@bot.tree.command(name="unblacklist",description="إزالة عضو أو ID من البلاك ليست")
async def unblacklist_slash(interaction:discord.Interaction,user_id:str,reason:str="فك الحظر"):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ للمالك فقط.",ephemeral=True)
    match=re.search(r"(\d{15,22})",user_id)
    if not match: return await interaction.response.send_message("❌ اكتب ID صحيح.",ephemeral=True)
    uid=int(match.group(1)); remove_from_blacklist(uid,reason,interaction.user.id)
    ok,status=await sync_blacklist_role(uid,False)
    await interaction.response.send_message(f"✅ تم فك البلاك ليست عن <@{uid}>.\nحالة الرتبة: {status}",ephemeral=True)


def build_blacklist_embed():
    data=load_data(); active={uid:info for uid,info in data.get("blacklist",{}).items() if info.get("active",True)}
    with_role=[]; without_role=[]
    for uid,info in active.items():
        line=f"• <@{uid}> • ID: {code_id(uid)}\n  السبب: {info.get('reason','بدون سبب')}"
        status=blacklist_role_status(uid)
        if status=="معه رتبة البلاك ليست": with_role.append(line)
        else: without_role.append(line+f"\n  الحالة: {status}")
    embed=discord.Embed(title=f"🖤 البلاك ليست • الإجمالي {smart_number(len(active))}",color=discord.Color.dark_grey())
    embed.add_field(name=f"✅ معهم الرتبة ({len(with_role)})",value="\n\n".join(with_role) or "لا يوجد",inline=False)
    embed.add_field(name=f"⚠️ بدون الرتبة ({len(without_role)})",value="\n\n".join(without_role) or "لا يوجد",inline=False)
    embed.set_footer(text=f"Main Guild: {MAIN_GUILD_ID} • Blacklist Role: {BLACKLIST_ROLE_ID}")
    return embed


@bot.command(name="show_blacklist")
async def show_blacklist_cmd(ctx):
    if not is_owner(ctx.author.id): return await ctx.send("❌ للمالك فقط.")
    await ctx.send(embed=build_blacklist_embed())


@bot.tree.command(name="show_blacklist",description="عرض البلاك ليست وحالة الرتبة")
async def show_blacklist_slash(interaction:discord.Interaction):
    if not is_owner(interaction.user.id): return await interaction.response.send_message("❌ للمالك فقط.",ephemeral=True)
    await interaction.response.send_message(embed=build_blacklist_embed(),ephemeral=True)


@bot.command(name="bal", aliases=["balance"])
async def check_balance(ctx, member: discord.Member = None):
    target = member or ctx.author
    coin = get_guild_coin(ctx.guild.id)
    bal = get_balance(target.id)
    await ctx.send(f"🪙 رصيد **{target.display_name}** هو: {smart_number(bal, force_copy=True)} {coin}")

@bot.tree.command(name="bal", description="معرفة رصيدك أو رصيد عضو آخر")
async def check_balance_slash(interaction: discord.Interaction, member: Optional[discord.Member] = None):
    target = member or interaction.user
    coin = get_guild_coin(interaction.guild.id)
    bal = get_balance(target.id)
    await interaction.response.send_message(f"🪙 رصيد **{target.display_name}** هو: {smart_number(bal, force_copy=True)} {coin}")

@bot.command(name="ping")
async def ping_cmd(ctx):
    await ctx.send(f"🏓 Pong! **{round(bot.latency * 1000)}ms**")

async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message(f"🏓 Pong! **{round(bot.latency * 1000)}ms**")

@bot.command(name="ai")
async def ai_cmd(ctx, *, question: str):
    async with ctx.typing():
        try:
            res = client_ai.models.generate_content(model='gemini-2.5-flash', contents=question).text
            await ctx.reply(res[:1900])
        except Exception as e: await ctx.send(f"❌ خطأ: `{e}`")

@bot.tree.command(name="ai", description="سؤال الذكاء الاصطناعي Gemini")
async def ai_slash(interaction: discord.Interaction, question: str):
    await interaction.response.defer()
    try:
        res = client_ai.models.generate_content(model='gemini-2.5-flash', contents=question).text
        await interaction.followup.send(res[:1900])
    except Exception as e: await interaction.followup.send(f"❌ خطأ: `{e}`")

# ==============================================================================
# 💬 الردود التلقائية وهوية السيرفر
# ==============================================================================
@bot.tree.command(name="set_reply", description="إضافة أو تعديل رد تلقائي")
async def set_reply(interaction: discord.Interaction, trigger: str, reply: str):
    if not is_admin(interaction.user.id, interaction.guild):
        return await interaction.response.send_message("❌ مخصص للإدارة.", ephemeral=True)
    trigger = trigger.strip().lower()
    if not trigger or len(trigger) > 100 or len(reply) > 1900:
        return await interaction.response.send_message("❌ تأكد أن الكلمة لا تتجاوز 100 حرف والرد لا يتجاوز 1900 حرف.", ephemeral=True)
    data = load_data()
    replies = data.setdefault("custom_replies", {}).setdefault(str(interaction.guild.id), {})
    replies[trigger] = reply
    save_data(data)
    await interaction.response.send_message(f"✅ تم حفظ الرد على: `{trigger}`", ephemeral=True)


@bot.tree.command(name="remove_reply", description="حذف رد تلقائي")
async def remove_reply(interaction: discord.Interaction, trigger: str):
    if not is_admin(interaction.user.id, interaction.guild):
        return await interaction.response.send_message("❌ مخصص للإدارة.", ephemeral=True)
    data = load_data()
    replies = data.setdefault("custom_replies", {}).setdefault(str(interaction.guild.id), {})
    key = trigger.strip().lower()
    if key not in replies:
        return await interaction.response.send_message("❌ الرد غير موجود.", ephemeral=True)
    del replies[key]
    save_data(data)
    await interaction.response.send_message(f"✅ تم حذف الرد: `{key}`", ephemeral=True)


@bot.tree.command(name="show_reply", description="عرض الردود التلقائية في السيرفر")
async def show_reply(interaction: discord.Interaction):
    replies = load_data().get("custom_replies", {}).get(str(interaction.guild.id), {})
    if not replies:
        return await interaction.response.send_message("لا توجد ردود تلقائية.", ephemeral=True)
    lines = [f"• `{key}` ← {value[:100]}" for key, value in list(replies.items())[:25]]
    embed = discord.Embed(title="💬 الردود التلقائية", description="\n".join(lines), color=discord.Color.teal())
    await interaction.response.send_message(embed=embed, ephemeral=True)


async def _convert_prefix_arg(ctx, annotation, raw):
    text=raw.strip()
    origin=getattr(annotation,"__origin__",None)
    args=getattr(annotation,"__args__",())
    choices=[a for a in args if a is not type(None)] if args else [annotation]
    target=choices[0] if choices else str
    if target is discord.Member:
        match=re.search(r"(\d{15,22})",text); return ctx.guild.get_member(int(match.group(1))) if match else None
    if target is discord.TextChannel:
        match=re.search(r"(\d{15,22})",text); return ctx.guild.get_channel(int(match.group(1))) if match else None
    if target is discord.Role:
        match=re.search(r"(\d{15,22})",text); return ctx.guild.get_role(int(match.group(1))) if match else None
    if target in (int,app_commands.Range):
        try: return int(text)
        except: return 0
    if target is bool: return text.lower() in ("true","1","yes","on","صح","نعم")
    return text


async def invoke_slash_from_prefix(ctx, slash_name, arg_text=""):
    command=bot.tree.get_command(slash_name)
    if not command:
        return await ctx.send(f"❌ الأمر `!{slash_name}` غير موجود.")
    callback=command.callback
    import inspect
    params=list(inspect.signature(callback).parameters.values())[1:]  # interaction
    tokens=arg_text.split() if arg_text else []
    kwargs={}; pos=0
    for i,param in enumerate(params):
        optional=param.default is not inspect.Parameter.empty
        if pos>=len(tokens):
            if optional: continue
            return await ctx.send(f"❌ ناقص `{param.name}`. استخدم `/help` لمعرفة تفاصيل الأمر.")
        # Last string-like parameter receives the remaining text.
        raw=" ".join(tokens[pos:]) if i==len(params)-1 else tokens[pos]
        pos=len(tokens) if i==len(params)-1 else pos+1
        kwargs[param.name]=await _convert_prefix_arg(ctx,param.annotation,raw)
    class PrefixInteractionAdapter:
        def __init__(self,ctx):
            self.user=ctx.author; self.guild=ctx.guild; self.channel=ctx.channel; self.channel_id=ctx.channel.id
            self.response=self; self.followup=self
        async def send_message(self,content=None,**kw): return await ctx.send(content,embed=kw.get("embed"),view=kw.get("view"))
        async def defer(self,**kw): return None
        async def send(self,content=None,**kw): return await ctx.send(content,embed=kw.get("embed"),view=kw.get("view"))
        def is_done(self): return False
    try:
        return await callback(PrefixInteractionAdapter(ctx),**kwargs)
    except Exception as exc:
        await ctx.send(f"❌ تعذر تنفيذ `!{slash_name}`: `{type(exc).__name__}`")


# ==============================================================================
# 🔀 نظام معالجة الاختصارات والأوامر المخصصة (make_easy)
# ==============================================================================
@bot.event
async def on_message(message):
    if not message.guild:
        return

    # Premium payment receipts are checked before other bot-message handling.
    if message.author.bot and await handle_premium_payment_receipt(message):
        return

    # Bot messages count too. The designated spin bot is handled first.
    if message.author.bot:
        if message.author.id == SPIN_BOT_ID:
            await handle_spin_bot_reward(message)
        await process_auto_line_message(message)
        return

    raw_content = message.content.strip()
    data = load_data()
    gid = str(message.guild.id)

    # كتابة كلمة "خط" بواسطة أدمن تحذف الكلمة وترسل صورة الخط مباشرة.
    if raw_content == "خط" and is_admin(message.author.id, message.guild):
        try:
            await message.delete()
        except Exception:
            pass
        await send_rize_line(message.channel)
        line_message_counters[(message.guild.id, message.channel.id)] = 0
        return

    # الرسائل البشرية تدخل في نفس عداد الخط المستخدم لرسائل البوتات.
    await process_auto_line_message(message)

    # الردود التلقائية تعمل عند تطابق الرسالة كاملة، ولا تعطل الأوامر.
    if not raw_content.startswith("!"):
        replies = data.get("custom_replies", {}).get(gid, {})
        reply_text = replies.get(raw_content.lower())
        if reply_text:
            await message.reply(str(reply_text), mention_author=False)

    content_without_prefix = raw_content[1:].strip() if raw_content.startswith("!") else raw_content
    if content_without_prefix:
        parts = content_without_prefix.split(" ", 1)
        cmd_alias = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        aliases = data.get("guilds", {}).get(gid, {}).get("aliases", {})
        if cmd_alias in aliases:
            target = aliases[cmd_alias].strip()
            message.content = (target if target.startswith("!") else f"!{target}") + (f" {args}" if args else "")
            await bot.process_commands(message)
            return

    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload:discord.RawReactionActionEvent):
    if not bot.user or payload.user_id==bot.user.id or str(payload.emoji)!="🎉":
        return
    data=load_runtime().get("active_giveaways",{}).get(str(payload.message_id))
    if not data:
        return
    guild=bot.get_guild(payload.guild_id) if payload.guild_id else None
    member=guild.get_member(payload.user_id) if guild else None
    channel=bot.get_channel(payload.channel_id)
    if member_is_fully_blacklisted(member):
        set_balance(payload.user_id,0)
        if channel and member:
            try:
                message=await channel.fetch_message(payload.message_id)
                await message.remove_reaction(payload.emoji,member)
            except Exception: pass
            try: await member.send(await blacklist_message_for_guild(guild))
            except Exception: pass
        return
    if channel:
        try:
            message=await channel.fetch_message(payload.message_id)
            participant_count=await count_giveaway_participants(message)
            await message.edit(content=None,embed=build_live_giveaway_embed(data,participant_count))
        except Exception: pass


@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    if not bot.user or payload.user_id == bot.user.id or str(payload.emoji) != "🎉":
        return
    data = load_runtime().get("active_giveaways", {}).get(str(payload.message_id))
    if not data:
        return
    channel = bot.get_channel(payload.channel_id)
    if channel:
        try:
            message = await channel.fetch_message(payload.message_id)
            participant_count = await count_giveaway_participants(message)
            await message.edit(content=None, embed=build_live_giveaway_embed(data, participant_count))
        except Exception:
            pass


# ==============================================================================
# ✨ رسائل الأخطاء الموحدة
# ==============================================================================
def error_embed(title, description, color=discord.Color.red()):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text="Rize Currency System")
    return embed


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=error_embed("⚠️ بيانات ناقصة", "لم تُدخل جميع البيانات المطلوبة. استخدم `!help` لمعرفة طريقة كتابة الأمر."))
    elif isinstance(error, commands.BadArgument):
        await ctx.send(embed=error_embed("❌ قيمة غير صحيحة", "تأكد من المنشن أو الرقم أو التنسيق، ثم حاول مرة أخرى."))
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=error_embed("🔒 صلاحية غير متاحة", "لا تملك الصلاحية المطلوبة لاستخدام هذا الأمر."))
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send(embed=error_embed("🛡️ صلاحيات البوت ناقصة", "ارفع رتبة البوت وامنحه الصلاحيات المطلوبة ثم حاول مجدداً."))
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=error_embed("⏳ تمهل قليلاً", f"يمكنك استخدام الأمر مجدداً بعد `{error.retry_after:.1f}` ثانية.", discord.Color.orange()))
    else:
        print(f"Prefix command error: {repr(error)}")
        await ctx.send(embed=error_embed("⚠️ تعذر تنفيذ الأمر", "حدث خطأ غير متوقع. راجع صلاحيات البوت وحاول مرة أخرى."))


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    original = getattr(error, "original", error)
    if isinstance(error, app_commands.CommandOnCooldown):
        embed = error_embed("⏳ تمهل قليلاً", f"يمكنك استخدام الأمر مجدداً بعد `{error.retry_after:.1f}` ثانية.", discord.Color.orange())
    elif isinstance(original, discord.Forbidden):
        embed = error_embed("🛡️ صلاحيات البوت ناقصة", "لا يستطيع البوت تنفيذ الإجراء. ارفع رتبة البوت وتأكد من صلاحياته.")
    else:
        print(f"Slash command error: {repr(error)}")
        embed = error_embed("⚠️ تعذر تنفيذ الأمر", "تحقق من البيانات والصلاحيات ثم حاول مرة أخرى.")
    if interaction.response.is_done():
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed, ephemeral=True)


# ==============================================================================
# ⚡ 15. تشغيل البوت
# ==============================================================================
# تسجيل نسخة ! تلقائية لكل أمر Slash لا يملك أمر Prefix بنفس الاسم.
async def _register_prefix_bridges():
    existing={cmd.name for cmd in bot.commands}
    for app_cmd in bot.tree.get_commands():
        name=app_cmd.name
        if name in existing:
            continue
        async def bridge_cmd(ctx, *, args="", _name=name):
            await invoke_slash_from_prefix(ctx,_name,args)
        bridge_cmd.__name__=f"prefix_bridge_{name}"
        bot.add_command(commands.Command(bridge_cmd,name=name))


asyncio.run(_register_prefix_bridges())
bot.run(TOKEN)