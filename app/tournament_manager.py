import logging
from typing import List, Dict
from app.poker_engine import PokerGame
from app.ai_opponents import AIFactory
import random

logger = logging.getLogger(__name__)

class Tournament:
    def __init__(self, name: str, buyin: int, players: int):
        self.name = name
        self.buyin = buyin
        self.max_players = players
        self.players = []
        self.status = "registering"  # registering, running, finished
        self.current_round = 0
        
    def add_player(self, user_id: str):
        """Добавить игрока в турнир"""
        if len(self.players) < self.max_players:
            self.players.append({
                'user_id': user_id,
                'stack': 1500,  # стартовый стек
                'position': len(self.players),
                'active': True
            })
            return True
        return False
    
    def start_tournament(self):
        """Начать турнир"""
        if len(self.players) >= 2:
            self.status = "running"
            self.current_round = 1
            return True
        return False

class TournamentManager:
    def __init__(self):
        self.active_tournaments = {}
        self.tournament_counter = 0
    
    def create_tournament(self, name: str, buyin: int = 100, players: int = 6) -> str:
        """Создать новый турнир"""
        self.tournament_counter += 1
        tournament_id = f"tournament_{self.tournament_counter}"
        
        self.active_tournaments[tournament_id] = Tournament(name, buyin, players)
        logger.info(f"Created tournament: {name} (ID: {tournament_id})")
        
        return tournament_id
    
    def join_tournament(self, tournament_id: str, user_id: str) -> bool:
        """Присоединиться к турниру"""
        tournament = self.active_tournaments.get(tournament_id)
        if tournament and tournament.status == "registering":
            return tournament.add_player(user_id)
        return False
    
    def get_tournament_info(self, tournament_id: str) -> Dict:
        """Информация о турнире"""
        tournament = self.active_tournaments.get(tournament_id)
        if tournament:
            return {
                'name': tournament.name,
                'players': f"{len(tournament.players)}/{tournament.max_players}",
                'status': tournament.status,
                'buyin': tournament.buyin
            }
        return {}

# Глобальный экземпляр
tournament_manager = TournamentManager()