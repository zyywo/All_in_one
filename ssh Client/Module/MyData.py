"""
TODO:
    3. 判断是否天 [大于|小于|等于] 一个数
    4. 能够使用正则表达式
"""


class MyData:
    def __init__(self, _list: list, **kwargs):
        """
        :param _list: list 一维列表类型，不能内嵌列表
        :param g_type: 如果一个MyData实例是由MyData类型的数据创建的，必须设置该值为True
        """
        self.raw = _list[:]
        try:
            _ = kwargs['g_type']
            self.data = _list
        except KeyError:
            self.data = [i.split() for i in map(str, _list)]

        self.met_reversed = kwargs.get('reversed')  # 矩阵是否翻转标记
        self.maxrow = len(self.data)
        self.maxcolumn = max(len(i) for i in self.data)

    def __repr__(self):
        return '{}'.format(self.data)

    def __getitem__(self, item):
        if isinstance(item, slice):
            return MyData(self.data[item.start: item.stop: item.step], g_type=True)

        else:
            # 因为self.data[item]是str类型
            # 而MyData的参数应是一维列表，所以有了[self.data[item]]=['x x x x']
            return MyData([self.data[item]], g_type=True)

    def __contains__(self, item):
        # 只有行列没翻转时，才需要把每行组合

        # if self.met_reversed:
        #     for value in self.data:
        #         if item in value:
        #             return True
        # else:
        for row in self.data:
            if item in ' '.join(row):
                return True

            for value in row:
                if item == value:
                    return True
        return False

    def column(self, start: int = None, **kwargs):
        """
        :param start:
        :return:
        """
        _nv = [['' for _ in range(self.maxrow)] for _ in range(self.maxcolumn)]

        for row, _rowvlaue in enumerate(self.data):
            for column, value in enumerate(_rowvlaue):
                _nv[column][row] = value

        if start is None:
            return MyData(_nv, g_type=True, reversed=True)

        if kwargs == {}:
            return MyData([_nv[start]], g_type=True, reversed=True)
        else:
            return MyData(_nv[start:kwargs.get('stop'):kwargs.get('step')], g_type=True, reversed=True)

    def to_str(self, append_lf=True):
        _str = []

        for row in self.data:
            _str.append(' '.join(row))

        if append_lf:
            return '\n'.join(_str)
        else:
            return ' '.join(_str)


if __name__ == '__main__':
    # d = MyData(['row0 1: ha ha',
    #             'row1 2: ho ho',
    #             'row2 3: maw maw'])
    d = MyData(['总用量 216\n',
                'drwxr-xr-x 7 zyy zyy   4096 9月  13 20:09 Arduino\n',
                '-rw-r--r-- 1 zyy zyy 156542 12月 20 20:01 autoproxy.pac\n',
                '-rw-r--r-- 1 zyy zyy     90 12月 20 20:01 autoproxy-user-rule\n',
                'drwxr-xr-x 4 zyy zyy   4096 9月  13 20:09 Codes\n',
                'drwxr-xr-x 2 zyy zyy   4096 12月 29 20:06 Desktop\n',
                'drwxr-xr-x 3 zyy zyy   4096 12月 29 21:49 Documents\n',
                'drwxr-xr-x 6 zyy zyy   4096 12月 23 21:19 Downloads\n',
                'drwxr-xr-x 6 zyy zyy   4096 12月 28 21:36 Games\n',
                '-rwxr-xr-x 1 zyy zyy     36 9月  13 20:21 get_file_from_xiaomi_router.sh\n',
                'drwxr-xr-x 7 zyy zyy   4096 11月 15 21:36 GNS3\n',
                'drwxr-xr-x 2 zyy zyy   4096 12月 29 21:36 Image\n',
                'drwxr-xr-x 3 zyy zyy   4096 12月 19 20:36 Music\n',
                'drwxr-xr-x 3 zyy zyy   4096 9月  15 20:18 Public\n',
                'drwxr-xr-x 2 zyy zyy   4096 9月  13 20:23 Video\n',
                'drwxr-xr-x 7 zyy zyy   4096 9月  13 20:29 VirtualBox VMs\n',
                'drwxr-xr-x 2 zyy zyy   4096 9月  13 20:06 模板\n'])

    c = d.column(-3)
    print(c)
    print('Code' in c)
