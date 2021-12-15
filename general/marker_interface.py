# Интерфейс-маркер, маркер (англ. marker interface pattern) — это шаблон
# проектирования, применяемый в языках программирования с проверкой типов во
# время выполнения. Шаблон предоставляет возможность связать метаданные
# (интерфейс) с классом даже при отсутствии в языке явной поддержки для
# метаданных.
#
# Чтобы использовать эту модель, класс реализует интерфейс[1]
# («помечается интерфейсом»), а взаимодействующие с классом методы проверяют
# наличие интерфейса. В отличие от обычного интерфейса, который определяет
# функциональность (в виде объявлений методов и свойств), которой должен
# обладать реализуемый класс объектов, важен сам факт обладания класса
# маркером. Маркер лишь является признаком наличия определённого поведения
# у объектов класса, помеченного маркером. Разумеется, возможны и «смешанные»
# интерфейсы, однако при неаккуратном использовании они могут создавать
# путаницу.
#
# Пример применения маркеров-интерфейсов в языке программирования Java
# является интерфейс Serializable. Класс должен реализовать этот интерфейс,
# чтобы показать, что его экземпляры могут быть записаны в ObjectOutputStream.
# Класс ObjectOutputStream имеет публичный метод writeObject(), который
# содержит ряд instanceof проверок возможности записи, одной из которых
# является интерфейс Serializable. Если вся серия проверок оканчивается
# неудачей, метод выбрасывает исключение NotSerializableException.
#
# Другим примером является интерфейс INamingContainer, который определен в
# .NET Framework. INamingContainer определяет элемент управления контейнером,
# который создает новый идентификатор пространства имен в иерархии элементов
# управления объекта Page.[2]. Любой элемент управления, который реализует
# этот интерфейс, создает новое пространство имен, в котором обеспечивается
# уникальность всех идентификаторов атрибутов дочерних элементов управления в
# пределах всего приложения. При разработке шаблонных элементов управления
# необходимо реализовывать этот интерфейс, чтобы избежать конфликтов
# именования на странице.
