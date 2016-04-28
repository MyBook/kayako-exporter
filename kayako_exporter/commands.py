# coding: utf-8
import logging

import click
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, REGISTRY
from prometheus_client.core import GaugeMetricFamily

import kayako_exporter
from kayako_exporter.api import get_session_id, get_tickes_count
from .compat import HTTPServer, BaseHTTPRequestHandler


logger = logging.getLogger(__name__)


class KayakoCollector(object):

    def __init__(self, base_url, login, password, department_ids=None):
        self.base_url = base_url
        self.login = login
        self.password = password
        self.session_id = None
        if not department_ids:
            class AllDeps(object):
                def __contains__(self, item):
                    return True
            department_ids = AllDeps()
        self.department_ids = department_ids

    def collect(self):
        logger.debug('Polling...')
        if not self.session_id:
            self.session_id = get_session_id(self.base_url, self.login, self.password)
        tickets_count = get_tickes_count(self.base_url, self.session_id)
        support_tickets_total = GaugeMetricFamily(
            'support_tickets_total', 'Number of tickets', labels=['project', 'status'])
        for status_data in tickets_count:
            if status_data['department_id'] in self.department_ids:
                support_tickets_total.add_metric([
                    status_data['department'], status_data['name']], status_data['count'])
        yield support_tickets_total


class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            response = generate_latest(REGISTRY)
            status = 200
        except Exception:
            logger.exception('Fetch failed')
            response = ''
            status = 500
        self.send_response(status)
        self.send_header('Content-Type', CONTENT_TYPE_LATEST)
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, format, *args):
        return


@click.command()
@click.option('--port', default=9223, help='Port to serve prometheus stats [default: 9223]')
@click.option('--url', help='HTTP URL for Kayako instance')
@click.option('--login', help='Kayako username')
@click.option('--password', help='Kayako password')
@click.option('--department-id', multiple=True, help='Kayako department to monitor [default: all available]')
@click.option('--verbose', is_flag=True)
@click.option('--version', is_flag=True)
def cli(**settings):
    """Kayako metrics exporter for Prometheus"""
    if settings['version']:
        click.echo('Version %s' % kayako_exporter.__version__)
        return

    if not settings['url']:
        click.echo('Please provide Kayako API URL')
        return
    if not settings['login']:
        click.echo('Please provide Kayako username')
        return
    if not settings['password']:
        click.echo('Please provide Kayako account password')
        return

    if settings['verbose']:
        handler = logging.StreamHandler()
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s', "%Y-%m-%d %H:%M:%S"))

    click.echo('Exporter for {base_url}, user: {login}, password: ***'.format(
        base_url=settings['url'].rstrip('/'),
        login=settings['login'],
        password=settings['password']
    ))

    REGISTRY.register(KayakoCollector(
        base_url=settings['url'].rstrip('/'),
        login=settings['login'],
        password=settings['password'],
        department_ids=settings['department_id'],
    ))
    httpd = HTTPServer(('', int(settings['port'])), MetricsHandler)
    click.echo('Exporting Kayako metrics on http://0.0.0.0:{}'.format(settings['port']))
    httpd.serve_forever()
