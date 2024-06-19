# from vedis import Vedis
# import config

# # Пытаемся узнать из базы «состояние» пользователя
# def get_current_state(user_id):
#     with Vedis(config.db_file) as db:
#         try:
#             return db[user_id].decode()
#         except KeyError:  # Если такого ключа почему-то не оказалось
#             return config.States.S_START.value  # значение по умолчанию - начало диалога

# # Сохраняем текущее «состояние» пользователя в нашу базу
# def set_state(user_id, value):
#     with Vedis(config.db_file) as db:
#         try:
#             db[user_id] = value
#             return True
#         except:
#             print("ОШИБКА")# тут желательно как-то обработать ситуацию
#             return False
import redis
import config

# Инициализация соединения с Redis
redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)

# Пытаемся узнать из базы «состояние» пользователя
def get_current_state(user_id):
    try:
        state = redis_client.get(user_id)
        if state is None:
            return config.States.S_START.value  # значение по умолчанию - начало диалога
        return state
    except redis.RedisError as e:
        print(f"Ошибка при получении состояния: {e}")
        return config.States.S_START.value  # значение по умолчанию

# Сохраняем текущее «состояние» пользователя в нашу базу
def set_state(user_id, value):
    try:
        redis_client.set(user_id, value)
        return True
    except redis.RedisError as e:
        print(f"Ошибка при сохранении состояния: {e}")
        return False
