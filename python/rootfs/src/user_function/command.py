import asyncio
import random
import re
import os

from .lotto import check_winner
from src.coin.coin import add_coin
from src.db_function import check_exist, retrieve
from src.timefn.timestamp import get_timestamp
from .raffle import raffle_save, raffle_winner


# init variable
player_lotto_list = []
shooter_cooldown = 0
lotto_stats = False


# mod function
async def call_to_hell(usernames, exclude_list, timeout):
    print(f"[HELL] [{get_timestamp()}] Wanna go to hell?")
    callhell_timeout = 180
    casualtie = 0
    usernames = [username for username in usernames if username not in exclude_list]
    number_user = int(len(usernames) / 2)
    random.shuffle(usernames)
    poor_users = usernames[:number_user]
    if os.environ.get("env", "") == "dev":
        callhell_timeout = 60
        poor_users += ["sirju001"]
    for username in poor_users:
        casualtie += 1
        print(f"[HELL] [{get_timestamp()}] Timeout: {username} Duration: {callhell_timeout} Reason: โดนสนิฟดีดนิ้ว")
        await timeout(username, callhell_timeout, "โดนสนิฟดีดนิ้ว")
        await asyncio.sleep(1)
    data = {
        "casualtie": casualtie,
        "poor_users": poor_users
    }
    return data


async def shooter(employer, target, vip_list, dev_list, send_message, timeout):
    global shooter_cooldown
    dodge_rate = 10
    payrate = 5
    shooter_timeout = random.randint(15, 60)
    clean_target = target.split("@")
    if len(clean_target) > 1:
        target = clean_target[1]
    if target == "me":
        await timeout(employer, shooter_timeout, f"อยากไปเยือนยมโลกหรอ สนิฟจัดให้ {shooter_timeout} วินาที")
        await send_message(f"@{employer} แวะไปเยือนยมโลก {shooter_timeout} วินาที sniffsAH")
        print(f"[SHOT] [{get_timestamp()}] Shooter: {employer} suicide by sniffsbot for {shooter_timeout} sec")
        return
    exclude_target = vip_list + dev_list
    cooldown = 1200
    if shooter_cooldown == 0:
        available = True
    else:
        now = get_timestamp()
        diff = (now - shooter_cooldown).total_seconds()
        if diff > cooldown:
            available = True
        else:
            available = False
    if available:
        shooter_cooldown = get_timestamp()
        if check_exist(employer):
            userdata = retrieve(employer)
            if userdata["coin"] >= payrate:
                add_coin(employer, -payrate)
                if check_exist(target):
                    submonth = retrieve(target)["submonth"]
                    dodge_rate += min(submonth, 6)
                if target in exclude_target:
                    await timeout(employer, shooter_timeout, f"บังอาจเหิมเกริมหรอ นั่งพักไปก่อน {shooter_timeout} วินาที")
                    await send_message(f"@{employer} บังอาจนักนะ sniffsAngry บินไปเองซะ {shooter_timeout} วินาที")
                    print(f"[SHOT] [{get_timestamp()}] Shooter: {employer} hit by sniffsbot for {shooter_timeout} sec")
                else:
                    if random.random() > (dodge_rate / 100):
                        await timeout(target, shooter_timeout, f"{employer} จ้างมือปืนสนิฟยิงปิ้วๆ {shooter_timeout} วินาที")
                        await send_message(f"@{employer} จ้างมือปืนสนิฟยิง @{target} {shooter_timeout} วินาที sniffsAH")
                        print(f"[SHOT] [{get_timestamp()}] Shooter: {employer} request sniffsbot to shoot {target} for {shooter_timeout} sec")
                    else:
                        shooter_cooldown = 0
                        await send_message(f"@{target} หลบมือปืนสนิฟได้ sniffsHeart @{employer} เสียใจด้วยนะ (Dodge = {int(dodge_rate)}%)")
            else:
                if target in exclude_target:
                    await timeout(employer, int(shooter_timeout * 2), f"ไม่มีเงินจ้างแล้วยังเหิมเกริมอีก รับโทษ 2 เท่า ({shooter_timeout} วินาที)")
                    await send_message(f"@{employer} ไม่มีเงินจ้างมือปืน ยังจะเหิมเกริม sniffsAngry บินไปซะ {int(shooter_timeout * 2)} วินาที")
                    print(f"[SHOT] [{get_timestamp()}] Shooter: {employer} hit by sniffsbot for {int(shooter_timeout * 2)} sec")
                else:
                    await timeout(employer, shooter_timeout, f"ไม่มีเงินจ้างมือปืนงั้นรึ โดนยิงเองซะ {shooter_timeout} วินาที")
                    await send_message(f"@{employer} ไม่มีเงินจ้างมือปืน sniffsAngry โดนมือปืนยิงตาย {shooter_timeout} วินาที")
                    print(f"[SHOT] [{get_timestamp()}] Shooter: {employer} hit by sniffsbot for {shooter_timeout} sec")
        else:
            if target in exclude_target:
                await timeout(employer, int(shooter_timeout * 2), f"ไม่มีเงินจ้างแล้วยังเหิมเกริมอีก รับโทษ 2 เท่า ({shooter_timeout} วินาที)")
                await send_message(f"@{employer} ไม่มีเงินจ้างมือปืน ยังจะเหิมเกริม sniffsAngry บินไปซะ {int(shooter_timeout * 2)} วินาที")
                print(f"[SHOT] [{get_timestamp()}] Shooter: {employer} hit by sniffsbot for {int(shooter_timeout * 2)} sec")
            else:
                await timeout(employer, shooter_timeout, f"ไม่มีเงินจ้างมือปืนงั้นรึ โดนยิงเองซะ {shooter_timeout} วินาที")
                await send_message(f"@{employer} ไม่มีเงินจ้างมือปืน sniffsAngry โดนมือปืนยิงตาย {shooter_timeout} วินาที")
                print(f"[SHOT] [{get_timestamp()}] Shooter: {employer} hit by sniffsbot for {shooter_timeout} sec")


# lotto system
async def buy_lotto(username, lotto, send_message):
    global player_lotto_list
    lotto_cost = 5
    if (re.match(r"[0-9]{2}", lotto) is not None) and (len(lotto) == 2):
        if check_exist(username):
            userstat = retrieve(username)
            if userstat["coin"] >= lotto_cost:
                lotto_int = int(lotto)
                # if player_lotto_list != []:
                #     for player_lotto in player_lotto_list:
                #         if lotto_int in player_lotto:
                #             await send_message(f"@{username} ไม่สามารถซื้อเลขซ้ำได้")
                #             print(f"[LOTO] [{get_timestamp()}] {username} Duplicate Lotto: {lotto}")
                #             return False
                add_coin(username, -lotto_cost)
                player_lotto_list += [[username, lotto_int]]
                await send_message(f"@{username} ซื้อ SniffsLotto หมายเลข {lotto} สำเร็จ sniffsHeart sniffsHeart sniffsHeart")
                print(f"[LOTO] [{get_timestamp()}] {username} buy {lotto} successfully")
                return True
            else:
                await send_message(f"@{username} ไม่มีเงินแล้วยังจะซื้ออีก sniffsAngry sniffsAngry sniffsAngry")
                print(f"[LOTO] [{get_timestamp()}] {username} coin insufficient")
                return False


async def draw_lotto(send_message):
    global player_lotto_list
    if player_lotto_list != []:
        print(f"[LOTO] [{get_timestamp()}] All player list : {player_lotto_list}")
        win_number, lotto_winners = check_winner(player_lotto_list)
        win_number_string = f"{win_number:02d}"
        count_winners = len(lotto_winners)
        payout = sum(lotto_winners.values())
        for username, prize in lotto_winners.items():
            add_coin(username, int(prize))
        await send_message(f"ประกาศผลรางวัล SniffsLotto เลขที่ออก {win_number_string} sniffsShock มีผู้ชนะทั้งหมด {count_winners} คน ได้รับรางวัลรวม {payout} sniffscoin sniffsHeart")
        if count_winners <= 5:
            await send_message(f"ผู้โชคดีได้แก่ {'@'+', @'.join(lotto_winners.keys())} คร่า sniffsHeart sniffsHeart sniffsHeart")
        print(f"[LOTO] [{get_timestamp()}] LOTTO draw: {win_number_string} | winners: {count_winners} users | payout: {payout} coin")
        player_lotto_list = []


async def update_lotto(status):
    global lotto_stats
    lotto_stats = status


async def send_lotto_msg(send_message):
    while True:
        if lotto_stats:
            await send_message("sniffsHi เร่เข้ามาเร่เข้ามา SniffsLotto ใบละ 5 coins !lotto ตามด้วยเลข 2 หลัก ประกาศรางวัลตอนปิดไลฟ์จ้า sniffsAH")
        await asyncio.sleep(1800)


async def check_message(username, message, vip_list, dev_list, send_message, timeout):
    restricted_message = ["บอทกาก", "บอทกๅก"]
    exclude_list = vip_list + dev_list
    if username not in exclude_list:
        for res_msg in restricted_message:
            result = re.search(res_msg, message)
            if result:
                await timeout(username, 30, f"@{username} ไหน ใครกาก")
                await send_message(f"@{username} บังอาจนักนะ sniffsAngry sniffsAngry")
                print(f"[_MOD] [{get_timestamp()}] Kill: {username} for 30 secs")


async def buy_raffle(username, count, send_message, timeout):
    raffle_cost = 1
    if check_exist(username):
        userstat = retrieve(username)
        total_raffle = min(int(userstat["coin"] / raffle_cost), count)
        if total_raffle > 0:
            success = raffle_save(username, total_raffle)
            if success:
                await send_message(f"@{username} ซื้อตั๋วสำเร็จ {total_raffle} ใบ sniffsHeart")
                print(f"[RAFL] [{get_timestamp()}] {username} buy {total_raffle} tickets")
                return True
    else:
        await timeout(username, 60, "ไม่มีเงินจ่ายค่าตั๋ว")
        print(f"[RAFL] [{get_timestamp()}] {username} Timeout 60 sec Reason: no money")
        return False


async def draw_raffle(send_message):
    winner = raffle_winner()
    print(f"[RAFL] [{get_timestamp()}] Winner: {winner}")
    await send_message(f"ผู้โชคดีได้แก่ {winner} ค่าาาาา sniffsHeart")
