from sqlalchemy.orm import DeclarativeBase, relationship, backref
from sqlalchemy import  Column, Integer, String, Date, ForeignKey
  
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
    """Таблица наименований типов СИ.
    Например: осциллографы цифровые, анализаторы спектра и тд."""
    
    __tablename__ = "с_types"
  
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
    с_type_id = Column(Integer, ForeignKey('с_types.id'))
    с_type = relationship("CTypes", backref=backref("devices", uselist=False))