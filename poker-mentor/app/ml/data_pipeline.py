# app/ml/data_pipeline.py
class DataPipeline:
    def __init__(self):
        self.training_data = []
    
    def record_decision(self, game_state: dict, action: str, result: float):
        """Запись данных для обучения"""
        features = self._extract_features(game_state)
        self.training_data.append({
            'features': features,
            'action': self._action_to_index(action),
            'result': result,
            'timestamp': datetime.now()
        })
    
    def _extract_features(self, game_state: dict) -> list:
        """Извлечение 47 фич для ML"""
        return [
            # Сила руки (0-1)
            game_state.get('hand_strength', 0.5),
            # Позиция (ранняя=0, средняя=0.5, поздняя=1)
            game_state.get('position_value', 0.5),
            # Размер стека относительно блайндов
            game_state.get('stack_ratio', 1.0),
            # Пот оддсы
            game_state.get('pot_odds', 0.0),
            # Количество игроков
            game_state.get('players_remaining', 2),
            # Стадия игры (префлоп=0, флоп=0.33, терн=0.66, ривер=1)
            game_state.get('street_progress', 0.0),
            # Агрессия оппонента
            game_state.get('opponent_aggression', 0.5),
            # ... и 40 других фич
        ]