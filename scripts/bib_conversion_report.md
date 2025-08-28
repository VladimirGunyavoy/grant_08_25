# Отчет о преобразовании именования библиографических записей

## Описание изменений

Преобразован формат именования библиографических записей с формата "фамилия год" на формат, основанный на начале заголовка статьи.

## Примеры преобразований

| Старый ключ | Новый ключ | Заголовок |
|-------------|------------|-----------|
| Osinenko2015 | a_method_of_optimal_2015 | A method of optimal traction control for farm tractors with feedback of drive torque |
| Osinenko2017 | optimal_traction_control_for_2017 | Optimal traction control for heavy-duty vehicles |
| Osinenko2022 | reinforcement_learning_with_guarantees_2022 | Reinforcement learning with guarantees: a review |
| Ibrahim2024 | comprehensive_overview_of_reward_2024 | Comprehensive Overview of Reward Engineering and Shaping in Advancing Reinforcement Learning Applications |
| Beckenbach2020 | a_qlearning_predictive_control_2020 | A Q-learning predictive control scheme with guaranteed stability |
| Osinenko2019 | practical_stability_analysis_of_2019 | Practical stability analysis of sliding‐mode control with explicit computation of sampling time |
| Dobriborsci2023 | predictive_reinforcement_learning_mapless_2023 | Predictive reinforcement learning: map-less navigation method for mobile robot |
| Beckenbach2024 | a_stabilizing_reinforcement_learning_2024 | A stabilizing reinforcement learning approach for sampled systems with partially unknown models |
| Pandey2024 | finite_and_fixedtime_stabilization_2024 | Finite and fixed‐time stabilization of discrete‐time systems using passivity‐based control |

## Алгоритм преобразования

1. **Извлечение заголовка**: Извлекается поле `title` из каждой записи
2. **Очистка заголовка**: Удаляются специальные символы, приводится к нижнему регистру
3. **Создание ключа**: Берется первые 3-4 слова заголовка, разделенные подчеркиваниями
4. **Добавление года**: К ключу добавляется год публикации для уникальности

## Файлы

- **Исходный файл**: `central uni grant/articles_list/my_bib.bib`
- **Резервная копия**: `central uni grant/articles_list/my_bib_backup.bib`
- **Скрипт преобразования**: `scripts/convert_bib_naming_fixed.py`

## Преимущества нового формата

1. **Семантическая ясность**: Ключи отражают содержание статьи
2. **Легкость поиска**: Проще найти нужную статью по содержанию
3. **Уникальность**: Год в ключе предотвращает конфликты
4. **Читаемость**: Ключи более информативны для человека

## Статистика

- Всего преобразовано записей: 70+
- Типы записей: @article, @phdthesis, @inproceedings
- Период публикаций: 2011-2025

## Последнее обновление

**Дата**: 28 августа 2024
**Действие**: Преобразование новых добавленных записей
**Результат**: Все записи в файле теперь используют семантическое именование
