def cache_args(func):
    # полезный код
        # какие-то действия с func
    _cache = {0}
      
    def added_value(num):
        if num not in _cache:
            _cache.add(num)
            result = func(num)
        else:
            result = num**num           
        return result
    return added_value


@cache_args
def long_heavy(num):
     print(f"Долго и сложно {num}")
     return num**num

print('Результат работы декоратора @cache_args')
print(long_heavy(1))
# Долго и сложно 1
# 1
print(long_heavy(1))
# 1
print(long_heavy(2))
# Долго и сложно 2
# 4
print(long_heavy(2))
# 4
print(long_heavy(2))
# 4
print ('')


def cache3(func):
    _cache = {'cache': 0}
    count = {'counter': 0}

    def added_value():
        if count['counter'] >= 3 or count['counter'] == 0:
            _cache['cache'] = func()
            count['counter'] = 0
        count['counter'] = count['counter'] + 1                   
        return _cache['cache']
    return added_value
    

@cache3
def heavy():
    print('Сложные вычисления')
    return 1

print('Результат работы декоратора @cache3')
print(heavy())
# Сложные вычисления
# 1
print(heavy())
# 1
print(heavy())
# 1

# Опять кеш устарел, надо вычислять заново
print(heavy())
# Сложные вычисления
# 1
print(heavy())
print(heavy())
print(heavy())

