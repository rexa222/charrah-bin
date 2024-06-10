from typing import Annotated

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Response, HTTPException, Form, BackgroundTasks

import pytz
import uvicorn
from persiantools import digits
from persiantools.jdatetime import JalaliDateTime

from logger import logger
from excel_handler import write_excel, remove_file
from config import VEHICLES_DATA, POSITIONS_DATA, FinalData, generate_report_file_name


app = FastAPI()


# load static files
app.mount('/static', StaticFiles(directory='static'), name='static')
# load templates
templates = Jinja2Templates(directory='templates')


@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException) -> Response:
    """Custom exception handler for 404 Not Found."""
    return templates.TemplateResponse('layouts/not-found.html', {'request': request})


@app.get('/')
async def index(request: Request):
    context = {
        'request': request,
        'positions_data': POSITIONS_DATA,
    }
    logger.info(f'request: {request.url}')
    return templates.TemplateResponse('pages/index.html', context)


@app.post('/report')
async def report(
        request: Request,
        address: Annotated[str, Form()],
        position: Annotated[str, Form()],
):
    logger.info(f'request: {request.url}')
    start_datetime = JalaliDateTime.now(pytz.timezone('Asia/Tehran'))

    context = {
        'request': request,
        'address': address,
        'position': position,
        'start_timestamp': start_datetime.to_gregorian().timestamp(),
        'start_time': start_datetime.strftime('%H:%M'),
        'vehicles_data': VEHICLES_DATA,
    }

    return templates.TemplateResponse('pages/report.html', context)


@app.post('/export')
async def export(
        request: Request,
        data: FinalData,
):
    data = data.model_dump(mode='json')
    start_datetime = JalaliDateTime.fromtimestamp(data['start_timestamp'], pytz.timezone("Asia/Tehran"))

    context = {
        'request': request,
        'data': data,
        'report_file_name': generate_report_file_name(start_datetime),
    }
    return templates.TemplateResponse('pages/export.html', context)


@app.post('/download')
async def download_excel_file(
        request: Request,
        data: FinalData,
        background_tasks: BackgroundTasks
):
    logger.info(f'request: {request.url}')
    logger.info(f'body: {data.model_dump_json(indent=2)}')

    data = data.model_dump(mode='json')
    start_datetime = JalaliDateTime.fromtimestamp(data['start_timestamp'], pytz.timezone("Asia/Tehran"))
    end_datetime = JalaliDateTime.now(pytz.timezone('Asia/Tehran'))

    main_data_rows = [
        [VEHICLES_DATA[vehicle]['alias'], data[vehicle]['right'], data[vehicle]['straight'], data[vehicle]['left']]
        for vehicle in VEHICLES_DATA
    ]

    general_info = [
        data['address'],
        POSITIONS_DATA[data['position']],
        digits.en_to_fa(start_datetime.strftime('%Y/%m/%d')),
        digits.en_to_fa(start_datetime.strftime('%H:%M')),
        digits.en_to_fa(end_datetime.strftime('%H:%M'))
    ]

    path = write_excel(general_info, main_data_rows)

    background_tasks.add_task(remove_file, path)
    return FileResponse(path, filename=generate_report_file_name(start_datetime))


if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=5000, reload=True)
