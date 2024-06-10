from pydantic import BaseModel, create_model
from persiantools.jdatetime import JalaliDateTime


VEHICLES_DATA = {
    'car': {'alias': 'سواری', 'fontawesome': 'car'},
    'taxi': {'alias': 'تاکسی', 'fontawesome': 'taxi'},
    'bus': {'alias': 'اتوبوس', 'fontawesome': 'bus-simple'},
    'motorcycle': {'alias': 'موتور سیکلت', 'fontawesome': 'motorcycle'},
    'truck': {'alias': 'ماشین سنگین', 'fontawesome': 'truck'},
}

POSITIONS_DATA = {
    'n': 'ضلع شمالی',
    'e': 'ضلع شرقی',
    's': 'ضلع جنوبی',
    'w': 'ضلع غربی',
}


GENERAL_INFO_TITLES = ['نام چهارراه', 'محل قرارگیری در چهارراه', 'تاریخ گزارش', 'زمان شروع', 'زمان پایان']
MAIN_DATA_TITLE_ROW = ['نوع وسیله نقلیه', 'گردش به راست', 'طی مسیر مستقیم', 'گردش به چپ']


class VehicleDirections(BaseModel):
    left: int
    straight: int
    right: int


FinalData = create_model(
    'FinalData',
    address=(str, ...),
    position=(str, ...),
    start_timestamp=(float, ...),
    **{vehicle: (VehicleDirections, ...) for vehicle in VEHICLES_DATA.keys()},
)


def generate_report_file_name(jdatetime: JalaliDateTime) -> str:
    return f'4way-report_{jdatetime.strftime("%Y-%m-%d")}.xlsx'
