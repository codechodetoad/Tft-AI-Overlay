from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Champion(Base):
    """Champion data model"""
    __tablename__ = 'champions'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    cost = Column(Integer, nullable=False)
    traits = Column(JSON)  # List of trait names
    stats = Column(JSON)   # HP, mana, armor, mr, damage
    patch_version = Column(String)
    icon_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    templates = relationship("ChampionTemplate", back_populates="champion")

class Item(Base):
    """Item data model"""
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    components = Column(JSON)  # List of component item names
    stats = Column(JSON)       # Stats provided by item
    description = Column(String)
    priority_score = Column(Float, default=5.0)  # 1-10 scale
    recommended_for = Column(JSON)  # List of champion names
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Augment(Base):
    """Augment/Trait data model"""
    __tablename__ = 'augments'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    tier = Column(String)  # Silver/Gold/Prismatic
    tier_list_rank = Column(String)  # S/A/B/C/D
    win_rate = Column(Float)
    pick_rate = Column(Float)
    description = Column(String)
    synergies = Column(JSON)  # Works well with these traits
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Composition(Base):
    """Meta composition data model"""
    __tablename__ = 'compositions'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    champions = Column(JSON)  # List of champion names
    positioning = Column(JSON)  # Dict of champion: (x, y) hex coordinates
    items_priority = Column(JSON)  # Priority items for each carry
    traits = Column(JSON)  # Active traits
    tier = Column(String)  # S/A/B/C/D
    win_rate = Column(Float)
    avg_placement = Column(Float)
    patch = Column(String)
    play_style = Column(String)  # "Reroll", "Fast 8", "Slow roll", etc
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ChampionTemplate(Base):
    """Champion portrait templates for CV recognition"""
    __tablename__ = 'champion_templates'

    id = Column(Integer, primary_key=True)
    champion_id = Column(Integer, ForeignKey('champions.id'))
    star_level = Column(Integer, default=1)  # 1, 2, or 3
    template_path = Column(String)
    histogram_data = Column(JSON)  # Precomputed histogram for matching
    created_at = Column(DateTime, default=datetime.utcnow)

    champion = relationship("Champion", back_populates="templates")

class MatchHistory(Base):
    """Player match history"""
    __tablename__ = 'match_history'

    id = Column(Integer, primary_key=True)
    placement = Column(Integer)  # 1-8
    composition_used = Column(String)
    final_board = Column(JSON)
    augments = Column(JSON)
    final_level = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    patch = Column(String)

class Trait(Base):
    """Trait/Synergy definitions"""
    __tablename__ = 'traits'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    breakpoints = Column(JSON)  # {2: "Bronze", 4: "Silver", 6: "Gold"}
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
