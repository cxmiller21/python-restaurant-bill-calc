from csv import DictReader
from typing import List


class Bill:
    def __init__(self, drink_total, food_total, tip) -> None:
        self.drink_total: int = drink_total
        self.food_total: int = food_total
        self.tip: int = tip

        self.drink_group_income: int = 0
        self.food_group_income: int = 0

    def get_weighted_percent(self, bi_weekly_income: int, type: str) -> int:
        if type == "food":
            return round((bi_weekly_income / self.food_group_income) * 100)
        if type == "drink":
            return round((bi_weekly_income / self.drink_group_income) * 100)

    def get_bill(self, weighted_percent: int, type: str) -> int:
        if type == "food":
            return (weighted_percent * self.food_total) / 100.0
        if type == "drink":
            return (weighted_percent * self.drink_total) / 100.0

    def get_total(self) -> int:
        return self.drink_total + self.food_total + self.tip

    def __repr__(self) -> str:
        return (
            f"Food: ${self.food_total}, Drinks: ${self.drink_total}, Tip: ${self.tip}\n"
            f"Total Cost: ${self.get_total()}"
        )


class Person:
    def __init__(self, name, bi_weekly_income, had_drinks, had_food) -> None:
        self.name: str = name
        self.bi_weekly_income: int = bi_weekly_income
        self.had_drinks: bool = had_drinks
        self.had_food: bool = had_food

        self.drink_bill: int = 0
        self.weighted_drink_percent: int = 0
        self.food_bill: int = 0
        self.weighted_food_percent: int = 0

    def get_total_bill(self) -> int:
        return self.drink_bill + self.food_bill

    def __repr__(self) -> str:
        return (
            f"{self.name}, Bi-weekly income: ${self.bi_weekly_income}, Had food: {self.had_food}, Had drinks: {self.had_drinks}\n"
            f"Food: ${self.food_bill} ({self.weighted_food_percent}% of total food cost)\n"
            f"Drinks ${self.drink_bill} ({self.weighted_drink_percent}% of total drink cost)\n"
            f"Total: ${self.get_total_bill()}\n"
            "----------------------------------------------------------------------------------------------------------------------------\n"
        )


def get_people(csv_file_name: str) -> List:
    reader = DictReader(open(csv_file_name))
    people = []
    for row in reader:
        had_drinks = True if row["had_drinks"] == "True" else False
        had_food = True if row["had_food"] == "True" else False
        people.append(
            Person(
                name=row["name"],
                bi_weekly_income=int(row["bi_weekly_income"]),
                had_drinks=had_drinks,
                had_food=had_food,
            )
        )
    return people


def main():

    csv_file_name = "people.csv"
    people = get_people(csv_file_name)

    # Get bill inputs
    food_total = int(input("Total Food Cost: $"))
    drink_total = int(input("Total Drink Cost: $"))
    tip_total = int(input("Total Tip Cost: $"))

    restaurant_bill = Bill(food_total=food_total, drink_total=drink_total, tip=tip_total)
    setattr(restaurant_bill, "food_group_income", sum([p.bi_weekly_income for p in people if p.had_food]))
    setattr(restaurant_bill, "drink_group_income", sum([p.bi_weekly_income for p in people if p.had_drinks]))

    for person in people:
        bi_weekly_income = person.bi_weekly_income
        
        if person.had_food:
            weighted_fp = restaurant_bill.get_weighted_percent(bi_weekly_income, "food")
            setattr(person, "weighted_food_percent", weighted_fp)

            food_bill = restaurant_bill.get_bill(weighted_fp, "food")
            setattr(person, "food_bill", food_bill)
        
        if person.had_drinks:
            weighted_dp = restaurant_bill.get_weighted_percent(bi_weekly_income, "drink")
            setattr(person, "weighted_drink_percent", weighted_dp)

            drink_bill = restaurant_bill.get_bill(weighted_dp, "drink")
            setattr(person, "drink_bill", drink_bill)

        print(person)

    print(restaurant_bill)


if __name__ == "__main__":
    main()
