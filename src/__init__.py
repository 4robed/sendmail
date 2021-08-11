import logging
import click
from gevent.monkey import patch_all
import os

from config import REDIS
from src.common.utils import log

patch_all()


def execute_command(command):
    import subprocess
    return subprocess.check_call(command)


@click.group()
def cli():
    pass


@cli.command(short_help='Runs a shell in the app context.')
@click.argument('ipython_args', nargs=-1, type=click.UNPROCESSED)
def shell(ipython_args):
    import sys
    import IPython
    from IPython.terminal.ipapp import load_default_config

    from src.databases import Redis

    ip_config = load_default_config()

    redis = Redis(**REDIS, db=1)

    ctx = dict(
        redis=redis,
    )

    banner = 'Python %s on %s\n' % (sys.version, sys.platform)
    if ctx:
        banner += 'Objects created:'
    for k, v in ctx.items():
        banner += '\n    {0}: {1}'.format(k, v)
    ip_config.TerminalInteractiveShell.banner1 = banner
    IPython.start_ipython(argv=ipython_args, user_ns=ctx, config=ip_config)


@cli.command(short_help='db initialization')
def init_db():
    pass


@cli.command(short_help='Run celery worker')
@click.option('--concurrency', default='5')
@click.option('--queue', default='SendMail')
@click.option('--pool', default='gevent')
@click.option('--loglevel', default='info')
def celery(**kwargs):
    concurrency = kwargs['concurrency']
    queue = kwargs['queue']
    pool = kwargs['pool']
    loglevel = kwargs['loglevel']
    command = [
        'celery',
        'worker',
        '--app=src.celery.task_handler',
        f'--loglevel={loglevel}',
        f'--pool={pool}',
        f'--queue={queue}',
        f'--concurrency={concurrency}'
    ]
    return execute_command(command)


@cli.command(short_help='Run an api.')
@click.option('--uwsgi', default='false')
@click.option('--port', default='5000')
@click.option('--processes', default='2')
@click.option('--threads', default='5')
@click.option('--buffer-size', default='65535')
@click.option('--host')
def api(**kwargs):
    ch = logging.StreamHandler()
    ch.setFormatter(
        logging.Formatter("%(asctime)s --  %(levelname)s  -- %(message)s"))
    log.setLevel(logging.DEBUG)
    log.addHandler(ch)

    uwsgi_enabled = False if kwargs['uwsgi'] == 'false' else True
    host = kwargs.get('host')
    if not host:
        host = '0.0.0.0'
    try:
        port = os.getenv('PORT')
        if not port:
            port = kwargs['port']
        port = int(port)
    except Exception as e:
        raise e

    if not uwsgi_enabled:
        from src.api import app

        params = dict(port=port, debug=True)
        if host:
            params['host'] = host
        return app.run(**params)

    wsgi_file = f'src/api/__init__.py'

    command = ['uwsgi', '--wsgi-file=%s' % wsgi_file]

    try:
        processes = int(kwargs['processes'])
        threads = int(kwargs['threads'])
        buffer_size = int(kwargs['buffer_size'])
    except Exception as e:
        raise e

    command.append('--processes=%s' % processes)
    command.append('--gevent=%s' % threads)
    command.append('--buffer-size=%s' % buffer_size)

    if host:
        command.append('--http-socket=%s:%s' % (host, port))
    else:
        command.append('--http-socket=:%s' % port)
    command.extend(['--lazy-apps', '--callable=app', '--enable-threads'])
    return execute_command(command)
