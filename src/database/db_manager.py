from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
import os
from .models import Base, Champion, Item, Augment, Composition, ChampionTemplate, MatchHistory, Trait

class DatabaseManager:
    """Central database manager with session handling"""

    def __init__(self, db_path='data/tft_overlay.db'):
        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        self.Session = scoped_session(sessionmaker(bind=self.engine))

        # Create all tables
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope for database operations"""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    # Champion operations
    def upsert_champion(self, champ_data):
        """Insert or update champion"""
        with self.session_scope() as session:
            champ = session.query(Champion).filter_by(name=champ_data['name']).first()
            if champ:
                for key, value in champ_data.items():
                    setattr(champ, key, value)
            else:
                champ = Champion(**champ_data)
                session.add(champ)
            return champ.id

    def get_champion(self, name):
        """Get champion by name"""
        with self.session_scope() as session:
            champ = session.query(Champion).filter_by(name=name).first()
            if champ:
                return {
                    'id': champ.id,
                    'name': champ.name,
                    'cost': champ.cost,
                    'traits': champ.traits,
                    'stats': champ.stats
                }
            return None

    def get_all_champions(self):
        """Get all champions"""
        with self.session_scope() as session:
            return [{'id': c.id, 'name': c.name, 'cost': c.cost, 'traits': c.traits}
                    for c in session.query(Champion).all()]

    # Item operations
    def upsert_item(self, item_data):
        """Insert or update item"""
        with self.session_scope() as session:
            item = session.query(Item).filter_by(name=item_data['name']).first()
            if item:
                for key, value in item_data.items():
                    setattr(item, key, value)
            else:
                item = Item(**item_data)
                session.add(item)
            return item.id

    def get_item(self, name):
        """Get item by name"""
        with self.session_scope() as session:
            item = session.query(Item).filter_by(name=name).first()
            if item:
                return {
                    'name': item.name,
                    'components': item.components,
                    'priority_score': item.priority_score,
                    'recommended_for': item.recommended_for
                }
            return None

    def get_top_items(self, limit=10):
        """Get highest priority items"""
        with self.session_scope() as session:
            items = session.query(Item).order_by(Item.priority_score.desc()).limit(limit).all()
            return [{'name': i.name, 'priority_score': i.priority_score} for i in items]

    # Augment operations
    def upsert_augment(self, aug_data):
        """Insert or update augment"""
        with self.session_scope() as session:
            aug = session.query(Augment).filter_by(name=aug_data['name']).first()
            if aug:
                for key, value in aug_data.items():
                    setattr(aug, key, value)
            else:
                aug = Augment(**aug_data)
                session.add(aug)
            return aug.id

    def get_augment(self, name):
        """Get augment by name"""
        with self.session_scope() as session:
            aug = session.query(Augment).filter_by(name=name).first()
            if aug:
                return {
                    'name': aug.name,
                    'tier': aug.tier,
                    'tier_list_rank': aug.tier_list_rank,
                    'win_rate': aug.win_rate
                }
            return None

    def get_augments_by_tier(self, tier_rank):
        """Get augments by tier rank (S/A/B/C/D)"""
        with self.session_scope() as session:
            augs = session.query(Augment).filter_by(tier_list_rank=tier_rank).all()
            return [{'name': a.name, 'tier': a.tier, 'win_rate': a.win_rate} for a in augs]

    # Composition operations
    def upsert_composition(self, comp_data):
        """Insert or update composition"""
        with self.session_scope() as session:
            comp = session.query(Composition).filter_by(
                name=comp_data['name'],
                patch=comp_data.get('patch', 'current')
            ).first()

            if comp:
                for key, value in comp_data.items():
                    setattr(comp, key, value)
            else:
                comp = Composition(**comp_data)
                session.add(comp)
            return comp.id

    def get_composition(self, name):
        """Get composition by name"""
        with self.session_scope() as session:
            comp = session.query(Composition).filter_by(name=name).first()
            if comp:
                return {
                    'name': comp.name,
                    'champions': comp.champions,
                    'positioning': comp.positioning,
                    'items_priority': comp.items_priority,
                    'tier': comp.tier,
                    'win_rate': comp.win_rate
                }
            return None

    def get_top_comps(self, limit=10):
        """Get top meta compositions"""
        with self.session_scope() as session:
            comps = session.query(Composition).order_by(
                Composition.tier,
                Composition.win_rate.desc()
            ).limit(limit).all()

            return [{
                'name': c.name,
                'champions': c.champions,
                'tier': c.tier,
                'win_rate': c.win_rate,
                'avg_placement': c.avg_placement
            } for c in comps]

    # Match history operations
    def save_match(self, match_data):
        """Save match to history"""
        with self.session_scope() as session:
            match = MatchHistory(**match_data)
            session.add(match)
            return match.id

    def get_match_stats(self, limit=20):
        """Get statistics from recent matches"""
        with self.session_scope() as session:
            matches = session.query(MatchHistory).order_by(
                MatchHistory.timestamp.desc()
            ).limit(limit).all()

            if not matches:
                return {'total_games': 0}

            placements = [m.placement for m in matches]
            return {
                'total_games': len(matches),
                'avg_placement': sum(placements) / len(placements),
                'top_4_rate': len([p for p in placements if p <= 4]) / len(placements) * 100,
                'win_rate': len([p for p in placements if p == 1]) / len(placements) * 100
            }

    # Utility
    def clear_old_data(self, patch):
        """Clear data from old patches"""
        with self.session_scope() as session:
            session.query(Composition).filter(Composition.patch != patch).delete()
            session.commit()
