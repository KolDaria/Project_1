
from src.reports import spending_by_category
from src.services import profitability_analysis_of_categories_with_increased_cashback
from src.utils import transactions_xlsx
from src.views import location_of_the_main_function

all_operators_list_dict = transactions_xlsx.to_dict(orient="records")


views_info = location_of_the_main_function("2019-10-15 05:30:45")
print(views_info)

services_info = profitability_analysis_of_categories_with_increased_cashback(all_operators_list_dict, 2019, 10)
print(services_info)

reports_info = spending_by_category(transactions_xlsx, "Аптека", "2019-10-13")
print(reports_info)
