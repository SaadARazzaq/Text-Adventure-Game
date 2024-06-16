'''

Text Adventure Game:
Programming Language: Python
Interface: GUI based

'''

import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class Player:
    def __init__(self, name, player_class):
        self.name = name
        self.player_class = player_class
        self.level = 1
        self.xp = 0
        self.max_health = 100
        self.health = self.max_health
        self.attack = 5
        self.defense = 3
        self.inventory = {"Potion": 3, "Gold": 500}  # Start with 500 gold

    def gain_xp(self, xp):
        self.xp += xp
        if self.xp >= 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_health += 10
        self.attack += 2
        self.defense += 1
        self.health = self.max_health
        self.xp = 0
        messagebox.showinfo("Level Up", f"Congratulations! You've reached Level {self.level}.")

    def heal(self):
        if "Potion" in self.inventory and self.health < self.max_health:
            self.health = min(self.health + 20, self.max_health)
            self.inventory["Potion"] -= 1
            messagebox.showinfo("Healing", "You used a Potion to heal yourself.")
        else:
            messagebox.showwarning("No Potion", "You don't have any Potions left.")

class Monster:
    def __init__(self, name, health, attack, reward_xp, reward_potion):
        self.name = name
        self.health = health
        self.attack = attack
        self.reward_xp = reward_xp
        self.reward_potion = reward_potion

    def is_defeated(self):
        return self.health <= 0

    def take_damage(self, damage):
        self.health -= damage

class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Magic Land Adventure")
        self.geometry("600x400")
        self.resizable(False, False)

        self.player = None
        self.current_location = "Home"
        self.places_to_travel = {
            "Home": ["Oodragoth", "CastleVania", "MilkTown"],
            "Oodragoth": ["CastleVania", "Home"],
            "CastleVania": ["Oodragoth", "Home"],
            "MilkTown": ["Home"]
        }

        self.create_widgets()

    def create_widgets(self):
        self.lbl_info = tk.Label(self, text="Welcome to Magic Land Adventure!")
        self.lbl_info.pack()

        self.btn_start = tk.Button(self, text="Start Adventure", command=self.start_adventure)
        self.btn_start.pack()

    def start_adventure(self):
        self.clear_widgets()
        self.create_player()

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def create_player(self):
        self.lbl_class = tk.Label(self, text="Choose your class:")
        self.lbl_class.pack()

        class_types = ["Mage", "Barbarian", "Archer"]
        for cls in class_types:
            btn_class = tk.Button(self, text=cls, command=lambda c=cls: self.select_class(c))
            btn_class.pack()

    def select_class(self, player_class):
        player_name = simpledialog.askstring("Player Name", "Enter your name:")
        if player_name:
            self.player = Player(player_name, player_class)
            self.show_stats()

    def show_stats(self):
        self.clear_widgets()
        stats_text = f"Player: {self.player.name}\nClass: {self.player.player_class}\nLevel: {self.player.level}\nXP: {self.player.xp}/100\nHealth: {self.player.health}/{self.player.max_health}\nAttack: {self.player.attack}\nDefense: {self.player.defense}\n\nInventory:\n"
        for item, quantity in self.player.inventory.items():
            stats_text += f"{item}: {quantity}\n"
        stats_text += f"\nCurrent Location: {self.current_location}"
        self.lbl_stats = tk.Label(self, text=stats_text)
        self.lbl_stats.pack()

        self.btn_activity = tk.Button(self, text="Choose Activity", command=self.choose_activity)
        self.btn_activity.pack()

    def choose_activity(self):
        self.clear_widgets()
        self.lbl_activity = tk.Label(self, text="Choose an activity:")
        self.lbl_activity.pack()

        activities = ["View Stats", "Travel", "Shop", "Quest"]
        for activity in activities:
            btn_activity = tk.Button(self, text=activity, command=lambda a=activity: self.handle_activity(a))
            btn_activity.pack()

        lbl_location = tk.Label(self, text=f"Monster in Oodragoth, Current Location: {self.current_location}")
        lbl_location.pack()

    def handle_activity(self, activity):
        if activity == "View Stats":
            self.show_stats()
        elif activity == "Travel":
            self.travel()
        elif activity == "Shop":
            self.shop()
        elif activity == "Quest":
            self.quest()

    def travel(self):
        self.clear_widgets()
        self.lbl_travel = tk.Label(self, text="Choose a destination:")
        self.lbl_travel.pack()

        locations = self.places_to_travel[self.current_location]
        for location in locations:
            btn_location = tk.Button(self, text=location, command=lambda l=location: self.travel_to_location(l))
            btn_location.pack()

    def travel_to_location(self, location):
        self.current_location = location
        messagebox.showinfo("Travel", f"You have traveled to {location}!")
        self.choose_activity()

    def shop(self):
        self.clear_widgets()
        self.lbl_shop = tk.Label(self, text="Welcome to the Shop!")
        self.lbl_shop.pack()

        self.lbl_money = tk.Label(self, text=f"Money: ${self.player.inventory.get('Gold', 0)}")
        self.lbl_money.pack()

        self.btn_buy = tk.Button(self, text="Buy Potion ($10)", command=self.buy_potion)
        self.btn_buy.pack()

        self.btn_sell = tk.Button(self, text="Sell Potion ($5)", command=self.sell_potion)
        self.btn_sell.pack()

        self.btn_back = tk.Button(self, text="Back to Activities", command=self.choose_activity)
        self.btn_back.pack()

    def buy_potion(self):
        if self.player.inventory.get("Gold", 0) >= 10:
            self.player.inventory["Gold"] -= 10
            if "Potion" in self.player.inventory:
                self.player.inventory["Potion"] += 1
            else:
                self.player.inventory["Potion"] = 1
            self.lbl_money.config(text=f"Money: ${self.player.inventory.get('Gold', 0)}")
            messagebox.showinfo("Purchase", "You bought a Potion.")
        else:
            messagebox.showwarning("Not Enough Money", "You don't have enough money.")

    def sell_potion(self):
        if "Potion" in self.player.inventory and self.player.inventory["Potion"] > 0:
            self.player.inventory["Gold"] = self.player.inventory.get("Gold", 0) + 5
            self.player.inventory["Potion"] -= 1
            self.lbl_money.config(text=f"Money: ${self.player.inventory.get('Gold', 0)}")
            messagebox.showinfo("Sale", "You sold a Potion.")
        else:
            messagebox.showwarning("No Potion", "You don't have any Potions to sell.")

    def quest(self):
        quest_text = "You encounter a quest-giver!\n\nQuest:\nDefeat 3 enemies in Oodragoth.\nRewards: 50 XP, 50 Gold."
        if self.current_location == "Oodragoth":
            response = messagebox.askyesno("Quest", quest_text)
            if response:
                self.start_quest()
        else:
            messagebox.showinfo("Quest", "No quests available here.")

    def start_quest(self):
        quest_text = "You encounter a quest-giver!\n\nQuest:\nDefeat 3 enemies in Oodragoth.\nRewards: 50 XP, 50 Gold."
        if self.current_location == "Oodragoth":
            response = messagebox.askyesno("Quest", quest_text)
            if response:
                if self.player.health <= 0:
                    if "Potion" in self.player.inventory and self.player.inventory["Potion"] > 0:
                        self.player.heal()
                        messagebox.showinfo("Health Restored", f"Your health has been restored to {self.player.health} HP.")
                    else:
                        messagebox.showinfo("No Health", f"You don't have enough health ({self.player.health} HP) to start the quest.")
                        return
                monsters_defeated = 0
                battle_log = ""
                while monsters_defeated < 3:
                    monster = Monster("Goblin", random.randint(50, 80), random.randint(8, 12), 50, 1)
                    battle_result, battle_log, message = self.battle(monster)
                    battle_log += message + "\n"

                    if battle_result == "Victory":
                        monsters_defeated += 1
                        self.player.gain_xp(monster.reward_xp)
                        self.player.inventory["Gold"] += monster.reward_potion
                        messagebox.showinfo("Victory", message)
                    else:
                        messagebox.showinfo("Defeat", message)
                        break

                if monsters_defeated == 3:
                    messagebox.showinfo("Quest Complete", "You completed the quest!")
                    messagebox.showinfo("Battle Log", battle_log)
                self.choose_activity()
            else:
                messagebox.showinfo("Quest", "You declined the quest.")
        else:
            messagebox.showinfo("Quest", "No quests available here.")

    def battle(self, monster):
        battle_log = ""
        while self.player.health > 0 and not monster.is_defeated():
            player_damage = random.randint(self.player.attack - 2, self.player.attack + 2)
            monster.take_damage(player_damage)
            battle_log += f"You dealt {player_damage} damage to {monster.name}.\n"

            if not monster.is_defeated():
                enemy_damage = random.randint(monster.attack - 2, monster.attack + 2)
                self.player.health -= max(0, enemy_damage - self.player.defense)
                battle_log += f"{monster.name} dealt {enemy_damage} damage to you.\n"

        if self.player.health <= 0:
            battle_log += "You were defeated in battle."
            return "Defeat", battle_log, "Work hard next time, goblin defeated you"
        else:
            battle_log += "You defeated the monster!"
            return "Victory", battle_log, "You trained well for this quest, You defeated the goblin"

if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
