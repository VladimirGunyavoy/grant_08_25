import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Данные для круговой диаграммы
labels = ['Продажа оборудования', 'Сервисное обслуживание', 'Дополнительные услуги']
sizes = [70, 25, 5]
colors = ['#4CAF50', '#2196F3', '#FF9800']
explode = (0.05, 0, 0)  # выделяем самый большой сегмент

# Создание фигуры и оси
fig, ax = plt.subplots(figsize=(10, 8))

# Создание круговой диаграммы
wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                  autopct='%1.0f%%', shadow=True, startangle=90,
                                  textprops={'fontsize': 12, 'fontweight': 'bold'})

# Настройка заголовка
ax.set_title('Структура доходов проекта AIDA-T', fontsize=16, fontweight='bold', pad=20)

# Добавление легенды
ax.legend(wedges, [f'{label}: {size}%' for label, size in zip(labels, sizes)],
          title="Структура доходов",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

# Обеспечение круглой формы диаграммы
ax.axis('equal')

# Улучшение внешнего вида
plt.tight_layout()

# Сохранение в PNG
plt.savefig('grant_08_25/структура_доходов_AIDA-T.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')

print("Диаграмма сохранена как 'структура_доходов_AIDA-T.png'")

# Показать диаграмму (опционально)
# plt.show()