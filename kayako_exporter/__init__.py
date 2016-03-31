# coding: utf-8
__author__ = 'MyBook'
__email__ = 'dev@mybook.ru'
__version__ = '0.1.0'

envvar_prefix = 'KAYAKO'


def main():
    from .commands import cli
    return cli(auto_envvar_prefix=envvar_prefix)


if __name__ == '__main__':
    main()
