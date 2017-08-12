from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

Base = declarative_base()

class Sniffer(Base):
    __tablename__ = 'sniffers'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    location = relationship('Location', back_populates='sniffers')
    probe_requests = relationship('ProbeRequest')
    name = Column(String, unique=True)
    display_name = Column(String)
    description = Column(String)
    model = Column(String)
    mac = Column(String, unique=True)
    rssi_adjustment = Column(Float, nullable=False, default=0.0)
    updated = Column(DateTime)

    def __str__(self):
        return str(self.name)

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    sniffers = relationship('Sniffer', back_populates='location')
    occupancy_snapshots = relationship('OccupancySnapshot', back_populates='location')
    name = Column(String, unique=True)
    display_name = Column(String, nullable=False)
    description = Column(String)
    capacity = Column(Integer)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return '<Location {} with id {}>'.format(self.name, self.id)

class ProbeRequest(Base):
    __tablename__ = 'probe_requests'
    id = Column(Integer, primary_key=True)
    sniffer_id = Column(Integer, ForeignKey('sniffers.id'))
    sniffer = relationship('Sniffer', back_populates='probe_requests')
    time = Column(DateTime, nullable=False)
    sniffer_mac = Column(String, nullable=False)
    device_mac = Column(String, nullable=False)
    rssi = Column(Float, nullable=False)
    channel = Column(Integer, nullable=False)

class OccupancySnapshot(Base):
    __tablename__ = 'occupancy_snapshots'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    location = relationship('Location')
    time = Column(DateTime, nullable=False)
    estimate = Column(Float, nullable=False)
    error = Column(Float, nullable=False)
    actual = Column(Float)
    degraded = Column(Boolean, default=False, nullable=False)