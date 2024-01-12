from datetime import datetime
from exceptions import (
  NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError
  )


def data_processing(team_data):
    if team_data["titles"] < 0:
        raise NegativeTitlesError("titles cannot be negative")
    first_cup_str = team_data["first_cup"]
    first_cup_date = datetime.strptime(first_cup_str, "%Y-%m-%d")
    first_cup_year = first_cup_date.year
    if first_cup_year < 1930 or (first_cup_year - 1930) % 4 != 0:
        raise InvalidYearCupError("there was no world cup this year")
    current_date = datetime.now()
    current_year = current_date.year
    period = current_year - first_cup_year + 4
    possible_titles_number = period / 4
    if team_data["titles"] > possible_titles_number:
        raise ImpossibleTitlesError(
            "impossible to have more titles than disputed cups"
        )


# data = {
#     "name": "França",
#     "titles": 7,
#     "top_scorer": "Zidane",
#     "fifa_code": "FRA",
#     "first_cup": "2002-10-18"
# }

# try:
#     data_processing(**data)
# except (
#     NegativeTitlesError,
#     InvalidYearCupError,
#     ImpossibleTitlesError
# ) as error:
#     print(error)
