# откуда парсим покерные данные ??????

## Форумы с разборами рук (лучший источник)

**Two Plus Two Forums**
`https://forumserver.twoplustwo.com/` 
- Разделы: "Poker Theory", "Beginner's Questions", "Hand Analysis"
- Что брать: Тысячи реальных разборов рук от игроков
- Формат: Текстовые описания раздач + комментарии экспертов

**Reddit Poker**
`https://www.reddit.com/r/poker/`
`https://www.reddit.com/r/learnpoker/`
- Треды: "Hand History Review", "What would you do?"
- Преимущество: Актуальные дискуссии, разные уровни сложности

**PokerStrategy.com Forum**
`https://www.pokerstrategy.com/forum/`
- Контент: Бесплатные разборы, стратегические статьи
- Сообщество: Активные игроки разных лимитов

## Сайты с покерной теорией

**The Poker Bank**
`https://www.thepokerbank.com/`
- Структура: Уроки от базовых до продвинутых
- Примеры: Конкретные раздачи с анализом

**PokerNews**
`https://www.pokernews.com/strategy/`
- Статьи: Стратегические материалы от профессионалов
- Разборы: Анализ известных раздач

## Базы знаний и статьи

**Wikipedia Poker Strategy**
`https://en.wikipedia.org/wiki/Poker_strategy`
- Теория: Фундаментальные концепции
- Примеры: Базовые стратегии

**CardPlayer.com**
`https://www.cardplayer.com/poker-strategy`
- Эксперты: Статьи от известных игроков
- Разборы: Турнирные и кэш-раздачи

## Сайты с статистикой

**PokerSites.com**
`https://www.pokersites.com/poker-strategy/`
- Статьи: Образовательный контент
- Примеры: Стратегические ситуации

**Beat The Fish**
`https://www.beatthefish.com/poker-strategy/`
- Уроки: Пошаговые руководства
- Анализ: Разбор конкретных рук


# Практические рекомендации по парсингу от deepseak

**Легальные сайты для скрапинга:**
```py
SAFE_FOR_SCRAPING = [
    "forumserver.twoplustwo.com",
    "reddit.com/r/poker",
    "thepokerbank.com", 
    "pokerstrategy.com/forum",
    "en.wikipedia.org"
]
```
**Что конкретно парсить:**
- Текстовые описания раздач в формате:
```txt 
Hero: A♠ K♣
Board: Q♥ 9♦ 2♣ 7♥ 3♠
Actions: Preflop - raise, call...
```

- Вопросы и ответы по стратегии

- Комментарии экспертов к раздачам

- Статистические данные из обсуждений

## Технические ограничения:
- Reddit: Используйте официальный API (реддит банят за агрессивный парсинг)
 
- Форумы: Соблюдайте robots.txt, ставьте задержки между запросами

- YouTube: Парсите только публично доступные данные

# Начните с Two Plus Two и Reddit - там максимальная концентрация полезного контента для обучения ИИ.