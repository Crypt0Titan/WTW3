from models import Game, Player
from sqlalchemy import func
from extensions import db
import pytz
from datetime import datetime

def check_answers(questions, submitted_answers):
    score = 0
    for question, answer in zip(questions, submitted_answers):
        if question.answer.lower() == answer.lower():
            score += 1
    return score

def determine_winner(game):
    players = Player.query.filter_by(game_id=game.id).order_by(Player.score.desc()).all()
    if players:
        return players[0]
    return None

def calculate_game_statistics():
    try:
        total_games = Game.query.count()
        total_rewards = db.session.query(func.sum(Game.pot_size)).scalar() or 0
        total_players = Player.query.count()
        completed_games = Game.query.filter_by(is_complete=True)
        completed_games_count = completed_games.count()
        total_time = completed_games.with_entities(func.sum(Game.time_limit)).scalar() or 0
        avg_time_per_game = total_time / completed_games_count if completed_games_count > 0 else 0
        avg_earnings_per_winner = total_rewards / completed_games_count if completed_games_count > 0 else 0

        return {
            'total_games': total_games,
            'total_rewards': total_rewards,
            'total_players': total_players,
            'total_time': total_time,
            'avg_time_per_game': avg_time_per_game,
            'avg_earnings_per_winner': avg_earnings_per_winner
        }
    except Exception as e:
        print(f"Error calculating game statistics: {e}")
        return {
            'total_games': 0,
            'total_rewards': 0,
            'total_players': 0,
            'total_time': 0,
            'avg_time_per_game': 0,
            'avg_earnings_per_winner': 0
        }

def make_aware(dt):
    if dt is None:
        return None
    if dt.tzinfo is None:
        return pytz.utc.localize(dt)
    return dt
