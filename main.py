#!/usr/bin/env python3
"""Точка входа в приложение ValutaTrade Hub."""

from valutatrade_hub.cli.interface import main

if __name__ == '__main__':
    main()

# poetry run project 
# help
# register --username alice --password 1234
# login --username alice --password 1234
# show-portfolio
# buy --currency BTC --amount 0.05
# buy --currency USD --amount 1000
# sell --currency BTC --amount 0.0001
# sell --currency USD --amount 100
# get-rate --from USD --to BTC