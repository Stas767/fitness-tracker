from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    MESSAGE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        # магия какая-то.До конца не понял как это сдеалал.
        # Изначально хотел создать переменную в классе
        # и через функцию asdict преобразовать даные в словарь
        # и затем их подставить. Но нашел более изящный метод.
        # Как я понял, все это автоматом происходит
        # после написания **asdict(self)

        text = self.MESSAGE.format(**asdict(self))
        return text


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65  # метров
    M_IN_KM = 1000  # метров
    MINUTES_IN_HOUR = 60  # минут

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        dist_km = self.action * self.LEN_STEP / self.M_IN_KM
        return dist_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        average_speed = self.get_distance() / self.duration
        return average_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Нужно переопределить функцию!')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=type(self).__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    coeff_calorie_1 = 18
    coeff_calorie_2 = 20

    def get_spent_calories(self) -> float:
        callories = ((self.coeff_calorie_1 * self.get_mean_speed()
                      - self.coeff_calorie_2)
                     * self.weight / self.M_IN_KM * self.duration
                     * self.MINUTES_IN_HOUR)
        return callories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float
    coeff_calorie_1 = 0.035
    coeff_calorie_2 = 0.029
    coeff_calorie_3 = 2

    def get_spent_calories(self) -> float:
        callories = ((self.coeff_calorie_1 * self.weight
                      + (self.get_mean_speed() ** self.coeff_calorie_3
                         // self.height) * self.coeff_calorie_2
                      * self.weight) * self.duration * self.MINUTES_IN_HOUR)
        return callories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38  # метров

    length_pool: float
    count_pool: float
    coeff_calorie_1 = 1.1
    coeff_calorie_2 = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        average_speed = (self.length_pool * self.count_pool
                         / self.M_IN_KM / self.duration)
        return average_speed

    def get_spent_calories(self) -> float:
        callories = ((Swimming.get_mean_speed(self)
                     + self.coeff_calorie_1) * self.coeff_calorie_2
                     * self.weight)
        return callories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_tren: type[str] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    # обработал иссключение,
    # если вдруг в входных данных не будет нужного ключа к тренировке
    if workout_type not in dict_tren.keys():
        raise TypeError('Нет такой тренировки! Доступные: "SWM", "RUN", "WLK"')
    else:
        tren_class = dict_tren.get(workout_type)(*data)
        return tren_class


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
