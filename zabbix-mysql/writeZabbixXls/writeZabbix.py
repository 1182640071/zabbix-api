#coding=utf-8

from loadZabbix import LoadZabbixMysql

x = LoadZabbixMysql('1')
y = LoadZabbixMysql('2')
print x == y