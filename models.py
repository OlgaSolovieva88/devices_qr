from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, relationship, backref
from sqlalchemy import  Column, Integer, String, Date, ForeignKey

from consts import DEVTYPE_DEVICE_MAP
from context import Context
from utils import generate_qr
  

c = Context()

class Base(DeclarativeBase): pass
  
class DevTypes(Base):
    """Таблица видов оборудования для мониторинга и измерений. 
    Включает: 
    СИ (средства измерений), 
    Э (эталоны единиц величин), 
    СК (средства контроля),
    И (индикаторы),
    ТУИФ (технические устройства с измерительными функциями),
    ИО (испытательное оборудование)"""
    
    __tablename__ = "dev_types"
  
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, comment='Наименование вида оборудования')

class CTypes(Base):
    """Таблица наименований типов СИ (категория)
    Например: осциллографы цифровые, анализаторы спектра и тд."""
    
    __tablename__ = "c_types"
  
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, comment='Наименование типа СИ')

class Devices(Base):
    """Информация об оборудовании"""
    
    __tablename__ = "devices"
  
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    model = Column(String, comment='модель оборудования')
    modification = Column(String, comment='модификация модели оборудования')
    c_regnum = Column(String, comment='регистрационный номер типа СИ (номер в госреестре)')
    man_id = Column(Integer, comment='заводской номер оборудования')
    c_class = Column(Integer, comment='класс оборудования по виду измерений')
    test_type = Column(String, comment='виды испытаний')
    manufacturer = Column(String, comment='производитель/страна')
    work_start = Column(Integer, comment='год ввода в эксплуатацию')
    pov_per = Column(Integer, comment='межповерочный интервал (в годах)')
    pov_num = Column(String, comment='номер свидетельства о поверке')
    pov_ext = Column(Date, comment='дата окончания действия срока поверки')
    check_per = Column(Integer, comment='межпроверочный интервал (в годах)')
    check_protocol = Column(String, comment='номер протокола по проверке работоспособности')
    check_ext = Column(Date, comment='дата окончания действия срока проверки')
    att_per = Column(Integer, comment='межаттестационный период (в годах)')
    att_protocol = Column(String, comment='номер аттестата/протокола аттестации')
    att_ext = Column(Date, comment='дата окончания действия срока аттестации')

    dev_type_id = Column(Integer, ForeignKey('dev_types.id'))
    dev_type = relationship("DevTypes", backref=backref("devices", uselist=False))
    c_type_id = Column(Integer, ForeignKey('c_types.id'))
    c_type = relationship("CTypes", backref=backref("devices", uselist=False))

    def __setattr__(self, name, value):
        try:
            column_type = getattr(self.__class__, name).type
            if isinstance(column_type, Date) and value:
                object.__setattr__(self, name, datetime.strptime(value, '%Y-%m-%d').date())
            elif isinstance(column_type, Integer) and value:
                object.__setattr__(self, name, int(value))
            elif isinstance(column_type, String):
                object.__setattr__(self, name, str(value))
        except AttributeError:
            if name == 'c_type':
                object.__setattr__(self, name, self._get_c_type_by_id_str(value))
            elif name == 'dev_type':
                object.__setattr__(self, name, self._get_dev_type_by_id_str(value))
            else:
                object.__setattr__(self, name, value)
        except TypeError:
            if name == 'c_type':
                object.__setattr__(self, name, self._get_c_type_by_id_str(value))
            elif name == 'dev_type':
                object.__setattr__(self, name, self._get_dev_type_by_id_str(value))
            else:
                print(f'Unknown type of "{name}" "{value}", type is {type(value)}')
                pass

    def _get_dev_type_by_id_str(self, id_str):
        try:
            return c.session.query(DevTypes).filter_by(id=int(id_str)).first()            
        except TypeError:
            print(f'Wrong value type "{id_str}"{type(id_str)}')

    def _get_c_type_by_id_str(self, id_str):
        try:
            return c.session.query(CTypes).filter_by(id=int(id_str)).first()
        except TypeError:
            print(f'Wrong value type "{id_str}"{type(id_str)}')

    def to_dict(self):
        dev_dict = {}
        for k, v in list(self.__dict__.items()):
            print(f'{k} {v}')
            if k.startswith('_'):
                continue
            # 
            if k not in DEVTYPE_DEVICE_MAP[self.dev_type.name]:
                continue

            dev_dict[k] = v.name if isinstance(v, (DevTypes, CTypes)) else v

        return dev_dict
    
    @property
    def label(self):
        try:
            return f'{self.c_type.name} {self.modification or self.model}'
        except AttributeError:
            return 'Новый прибор'
        if self.modification is None:
            return f'{self.model} {self.manufacturer}'

        return f'{self.modification} {self.manufacturer}'
    
    @property
    def qr(self):
        return generate_qr(int(self.id))

