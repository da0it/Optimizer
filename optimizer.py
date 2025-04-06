import sympy as sp

class FunctionCounter:
    def __init__(self, func):
        self.func = func
        self.call_count = 0
    
    def __call__(self, *args, **kwargs):
        self.call_count += 1
        return self.func(*args, **kwargs)
def dyhotomy(a, b, e, l, type, f, update_table_callback, result_callback):

    x = sp.symbols('x')

    formula_expr = sp.sympify(f)

    function = sp.lambdify(x, formula_expr)
	
    func = FunctionCounter(function)

    # Сохранение начальных интервалов неопределенности для построения графика
    a_initial = a
    b_initial = b

    func_eval = 0

    # Проверка соответствия e и l установленным ограничениям
    assert 2 * e > 0, 'E слишком мало либо отрицательно'
    assert l > 0 , 'Конечная длина интервала неопределенности не может быть меньше нуля'

    # Инициализация начального этапа
    k = 1

    # Пока длина между двумя точками превышает конечную длину интервала неопределенности
    while (b - a > l):

        # Вычисление значений точек lambda и mu
        lamb = (a + b)/ 2 - e
        mu = (a + b)/ 2 + e

        f_lamb = func(lamb)
        f_mu = func(mu)

        # Выполнение алгоритма 
        if (type == "min"):
            if (f_lamb < f_mu):
                b = mu
            else:
                a = lamb
        elif (type == "max"):
            if (f_lamb > f_mu):
                b = mu
            else:
                a = lamb

        update_table_callback(k, round(a, 4), round(b, 4), round(lamb, 4), round(mu, 4), round(f_lamb, 4), round(f_mu, 4))
        k += 1

    # Вычисление оптимального значения x и значения функции от этого x
    opt_x = (a + b) / 2
    opt_f = func(opt_x)

    func_eval = func.call_count - 1
    result_callback(opt_x, opt_f, a, b, func_eval)


def golden_ratio(a, b, l, type, f, update_table_callback, result_callback):

    x = sp.symbols('x')

    formula_expr = sp.sympify(f)

    function = sp.lambdify(x, formula_expr)

    func = FunctionCounter(function)

    a_initial = a 
    b_initial = b

    func_eval = 0

    # Константа α 
    alph = 0.618

    # Вычисление начальных значений λ и μ
    lamb = a + (1 - alph) * (b - a)
    mu = a + alph* (b - a)

    # Вычисление функции для начальных значений λ и μ
    f_lamb = func(lamb)
    f_mu = func(mu)

    # Выполнение алгоритма 
    if (type == "min"):
        k = 1

        # Пока длина между точками больше длины конечного интервала неопределенности, выполнение цикла
        while (b - a > l):
            # Если f(λ) > f(μ) то шаг 2
            if (f_lamb > f_mu):
                a = lamb
                b = b
                lamb = mu
                mu = a + alph * (b - a)

                f_lamb = f_mu
                f_mu = func(mu)

            # Если f(λ) <= f(μ) то шаг 3
            elif (f_lamb <= f_mu):
                a = a
                b = mu
                mu = lamb
                lamb = a + (1 - alph) * (b - a)

                f_mu = f_lamb
                f_lamb = func(lamb)
            update_table_callback(k, round(a, 4), round(b, 4), round(lamb, 4), round(mu, 4), round(f_lamb, 4), round(f_mu, 4))
            k += 1

    elif (type == "max"):
        k = 1
        while (b - a > l):

            f_lamb = func(lamb)
            f_mu = func(mu)
            if (f_lamb < f_mu):
                a = lamb
                b = b
                lamb = mu
                mu = a + alph * (b - a)

            elif (f_lamb >= f_mu):
                a = a
                b = mu
                mu = lamb
                lamb = a + (1 - alph) * (b - a)
            update_table_callback(k, round(a, 4), round(b, 4), round(lamb, 4), round(mu, 4), round(f_lamb, 4), round(f_mu, 4))
            k += 1
            
    opt_x = (a + b) / 2
    opt_f = func(opt_x)

    func_eval = func.call_count - 1

    result_callback(opt_x, opt_f, a, b, func_eval)

def generate_fibonacci(limit):
    """Генерация последовательности Фибоначчи до достижения limit."""
    fibs = [1, 1]
    while fibs[-1] < limit:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs

def fibonacci_search(f, a1, b1, l, epsilon, extremum_type,  update_table_callback, result_callback):

    x = sp.symbols('x')

    formula_expr = sp.sympify(f)

    func = sp.lambdify(x, formula_expr)

    # Предварительный этап
    fib_limit = (b1 - a1) / l
    fibs = generate_fibonacci(fib_limit)
    n = len(fibs)  # n - номер в последовательности, где F(n) > fib_limit

    # Инициализация
    a_k = a1
    b_k = b1
    lambda_val = a_k + (fibs[n - 3] / fibs[n - 1]) * (b_k - a_k)
    mu_val = a_k + (fibs[n - 2] / fibs[n - 1]) * (b_k - a_k)

    function_eval_count = 0
    f_lambda = func(lambda_val)
    f_mu = func(mu_val)
    k = 1

    # Основной этап: пока k <= n - 2
    while k <= n - 2:
        update_table_callback(k, round(a_k, 4), round(b_k, 4), round(lambda_val, 4), round(mu_val, 4), round(func(lambda_val), 4), round(func(mu_val), 4))

        # Для min: если f(λ_k) > f(μ_k), для max наоборот
        if (extremum_type == "min" and f_lambda > f_mu) or \
           (extremum_type == "max" and f_lambda < f_mu):
            # Шаг 2: сдвигаем левую границу
            a_k = lambda_val
            lambda_val = mu_val
            f_lambda = f_mu
            function_eval_count += 1
            if k == n - 2:
                break
            mu_val = a_k + (fibs[n - k - 2] / fibs[n - k - 1]) * (b_k - a_k)
            f_mu = func(mu_val)
        else:
            # Шаг 3: сдвигаем правую границу
            b_k = mu_val
            mu_val = lambda_val
            f_mu = f_lambda
            function_eval_count += 1
            if k == n - 2:
                break
            lambda_val = a_k + (fibs[n - k - 3] / fibs[n - k - 1]) * (b_k - a_k)
            f_lambda = func(lambda_val)
        k += 1

    # Шаг 5: корректировка конечных точек с учётом epsilon
    lambda_n = min(lambda_val, mu_val) - epsilon
    mu_n = max(lambda_val, mu_val) + epsilon
    f_lambda_n = func(lambda_n)
    f_mu_n = func(mu_n)

    if (extremum_type == "min" and f_lambda_n < f_mu_n) or \
       (extremum_type == "max" and f_lambda_n > f_mu_n):
        a_n = lambda_n
        b_n = b_k
    else:
        a_n = a_k
        b_n = mu_n

    x_opt = (a_n + b_n) / 2
    f_opt = func(x_opt)

    k = k + 1
    function_eval_count += 1
    update_table_callback(k, round(a_k, 4), round(b_k, 4), round(lambda_val, 4), round(mu_val, 4), round(func(lambda_val), 4), round(func(mu_val), 4))

    result_callback(x_opt, f_opt, a_k, b_k, function_eval_count)

