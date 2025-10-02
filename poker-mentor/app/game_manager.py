import logging
from app.poker_engine import PokerGame, Action
from app.ai_opponents import AIFactory

logger = logging.getLogger(__name__)

class GameManager:
    """Управление игровыми сессиями"""
    
    def __init__(self):
        self.active_games = {}
    
    def create_game(self, user_id: str, ai_type: str = "fish") -> PokerGame:
        """Создать новую игру"""
        ai_opponent = AIFactory.create_ai(ai_type)
        
        game = PokerGame([f"user_{user_id}", ai_opponent.name])
        game.ai_opponent = ai_opponent
        game.start_hand()
        game.post_blinds()
        
        self.active_games[user_id] = game
        logger.info(f"Создана новая игра для пользователя {user_id} с AI {ai_type}")
        
        return game
    
    def get_game(self, user_id: str) -> PokerGame:
        """Получить активную игру пользователя"""
        return self.active_games.get(user_id)
    
    def end_game(self, user_id: str):
        """Завершить игру"""
        if user_id in self.active_games:
            del self.active_games[user_id]
            logger.info(f"Игра пользователя {user_id} завершена")
    
    def process_player_action(self, user_id: str, action: str, amount: int = 0) -> dict:
        """Обработать действие игрока"""
        game = self.get_game(user_id)
        if not game:
            return {"error": "Игра не найдена"}
        
        player = f"user_{user_id}"
        result = {
            "player_action": action,
            "player_amount": amount,
            "ai_action": None,
            "ai_amount": 0,
            "pot": game.pot,
            "player_stack": game.player_stacks[player],
            "community_cards": game.community_cards.copy(),
            "game_continues": True
        }
        
        # Обрабатываем действие игрока
        if action == "fold":
            game.player_stacks[player] -= 0
            result["game_continues"] = False
            result["message"] = "❌ Вы сбросили карты."
            
        elif action == "call":
            call_amount = game.current_bet
            game.player_stacks[player] -= call_amount
            game.pot += call_amount
            result["player_amount"] = call_amount
            result["message"] = f"📥 Вы поставили {call_amount} BB"
            
        elif action == "check":
            game.player_stacks[player] -= 0
            result["message"] = "⚖️ Вы пропустили ход"
            
        elif action == "raise":
            game.player_stacks[player] -= amount
            game.pot += amount
            game.current_bet = amount
            result["message"] = f"📤 Вы поставили рейз {amount} BB"
        
        # Ход AI
        if result["game_continues"]:
            ai_action, ai_amount = self._process_ai_turn(game)
            result["ai_action"] = ai_action
            result["ai_amount"] = ai_amount
            result["ai_message"] = self._get_ai_action_text(ai_action, ai_amount)
            
            # Обновляем состояние после хода AI
            result["pot"] = game.pot
            result["player_stack"] = game.player_stacks[player]
        
        # Проверяем продолжение игры
        if result["game_continues"]:
            result["game_continues"] = self._advance_game_street(game)
            if not result["game_continues"]:
                # Шоудаун
                winners = game.get_winner()
                result["winner"] = "Вы" if 'user' in winners[0] else "AI"
                result["winning_hand"] = game.evaluate_showdown()[winners[0]][0].name
        
        return result
    
    def _process_ai_turn(self, game: PokerGame) -> tuple:
        """Обработать ход AI"""
        ai_action, ai_amount = game.ai_opponent.decide_action(game, game.ai_opponent.name)
        
        if ai_action == Action.FOLD:
            game.player_stacks[game.ai_opponent.name] -= 0
        elif ai_action == Action.CHECK:
            game.player_stacks[game.ai_opponent.name] -= 0
        elif ai_action == Action.CALL:
            game.player_stacks[game.ai_opponent.name] -= ai_amount
            game.pot += ai_amount
        elif ai_action == Action.RAISE:
            game.player_stacks[game.ai_opponent.name] -= ai_amount
            game.pot += ai_amount
            game.current_bet = ai_amount
        
        return ai_action.value, ai_amount
    
    def _get_ai_action_text(self, ai_action: str, ai_amount: int) -> str:
        """Получить текстовое описание действия AI"""
        actions = {
            "fold": "🤖 AI: фолд",
            "check": "🤖 AI: чек", 
            "call": f"🤖 AI: колл {ai_amount} BB",
            "raise": f"🤖 AI: рейз {ai_amount} BB"
        }
        return actions.get(ai_action, "🤖 AI: неизвестное действие")
    
    def _advance_game_street(self, game: PokerGame) -> bool:
        """Перейти на следующую улицу игры"""
        if len(game.community_cards) == 0:
            game.deal_flop()
            return True
        elif len(game.community_cards) == 3:
            game.deal_turn()
            return True
        elif len(game.community_cards) == 4:
            game.deal_river()
            return True
        else:
            # Игра завершена
            return False
    
    def get_game_state(self, user_id: str) -> dict:
        """Получить текущее состояние игры"""
        game = self.get_game(user_id)
        if not game:
            return None
        
        player = f"user_{user_id}"
        return {
            "user_cards": game.player_cards[player],
            "user_stack": game.player_stacks[player],
            "pot": game.pot,
            "current_bet": game.current_bet,
            "community_cards": game.community_cards,
            "ai_name": game.ai_opponent.name if hasattr(game, 'ai_opponent') else "AI"
        }