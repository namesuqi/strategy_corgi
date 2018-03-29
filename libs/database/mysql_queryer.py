# coding=utf-8
# description: get attribute according to special column from mysql
# author='myn'


from libs.database.mysql_orm import *
# from libs.module.onlines import *

orm = MysqlORM()


def get_attribute_by_peer_id(table_name, peer_id, a):
    results = orm.session.query(table_name).filter_by(peer_id=peer_id).first()
    attribute = getattr(results, a)

    orm.session.close()
    # info.append(var)

    # print attribute
    return attribute


if __name__ == '__main__':
    # get_attribute_by_peer_id(Online, "00000004B9894E617F8DDDCD75058E20", 'sdk_version')
    pass
