# CHAR_TYPE = ['SWZ', 'ZY ', 'ZE', 'GR', 'RW', 'SRRB', 'YW', 'RZ', 'YZ', 'WZ', 'QT']


class CheCi(object):

    def __init__(self, **kwargs):
        self._checi = kwargs.get('checi')
        self._SWZ = kwargs.get('SWZ')
        self._ZY = kwargs.get('ZY')
        self._ZE = kwargs.get('ZE')
        self._GR = kwargs.get('GR')
        self._RW = kwargs.get('RW')
        self._SRRB = kwargs.get('SRRB')
        self._YW = kwargs.get('YW')
        self._RZ = kwargs.get('RZ')
        self._YZ = kwargs.get('YZ')
        self._WZ = kwargs.get('WZ')
        self._QT = kwargs.get('QT')

    def __repr__(self):

        return '车次：{}，商务座：{}，一等座：{}，二等座：{}，高级软卧：{}，软卧：{}，动卧：{}，硬卧：{}，软座：{}，硬座：{}，无座：{}，其他：{}'.format(self._checi, self._SWZ, self._ZY, self._ZE, self._GR, self._RW, self._SRRB, self._YW, self._RZ,
                         self._YZ, self._WZ, self._QT)