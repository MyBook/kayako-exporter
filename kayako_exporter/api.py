# coding: utf-8
import logging

import requests
import xmltodict
from prometheus_client import Summary

__all__ = ['get_session_id', 'get_tickes_count']


logger = logging.getLogger(__name__)

# metrics
fetches = Summary('kayako_api_seconds', 'Time spent, fetching data', ['endpoint'])
track_session_id = fetches.labels({'endpoint': 'get_session_id'}).time()
track_tickets_count = fetches.labels({'endpoint': 'get_tickets_count'}).time()


@track_session_id
def get_session_id(base_url, login, password):
    response = requests.post(base_url + '/staffapi/index.php?/Core/Default/Login',
                             {'username': login, 'password': password})
    response.raise_for_status()
    try:
        session_id = xmltodict.parse(response.content)['kayako_staffapi']['sessionid']
    except Exception as e:
        logger.error('Unable to log in: %s', e)
    else:
        return session_id


@track_tickets_count
def get_tickes_count(base_url, session_id):
    response = requests.post(base_url + '/staffapi/index.php?/Core/Default/GetInfo',
                             {'sessionid': session_id, 'wantmacros': 0})
    response.raise_for_status()
    response_dict = xmltodict.parse(response.content, force_list=('department', 'ticketstatus',))['kayako_staffapi']
    departments = {item['@id']: item['@title'] for item in response_dict['department']}
    statuses = {item['@id']: item['@title'] for item in response_dict['ticketstatus']}
    statuses['0'] = 'Total'
    for item in response_dict['ticketcount']:
        yield {
            'name': statuses[item['@statusid']],
            'count': int(item['@ticketcount']),
            'department': departments[item['@departmentid']],
            'department_id': item['@departmentid'],
        }
