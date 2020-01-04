> This is a Russian translation of [Functional Programming Jargon][en] with some additional editing and examples in Haskell.

[en]: https://github.com/hemanth/functional-programming-jargon
[tr]: https://github.com/mrtkp9993/functional-programming-jargon


> Эта статья - перевод и переработка публикации [Functional Programming Jargon][en] c
с примерами на Нaskell. Комментарии переводчика приведены [тут](translation.md). В оригинальной статье примеры на JavaScript, она переведена на русский [здесь](https://habr.com/ru/post/310172).

# Словарь сленга функционального программирования

У функционального программирования (ФП) есть много преимуществ, и как результат, его популярность растет. При этом у любой парадигмы программирования
есть своя терминология и жаргон, и ФП - не исключение. С помощью этого словаря 
мы надеемся упростить задачу изучения ФП. 

__Содержание__
* [1. Функции](#1-функции)
  * [Определение функции](#определение-функции)
  * [Аннотация типа](#аннотация-типа)
  * [Делаем с функциями, что хотим](#делаем-с-функциями-что-хотим)
    * [Композиция функций](#композиция-функций)
    * [Point-free стиль записи](#point-free-стиль-записи)
    * [Лямбда-функция](#лямбда-функция)
    * [Функция высшего порядка (ФВП)](#функция-высшего-порядка-фвп)
  * [Не совсем "правильные" функции](#не-совсем-правильные-функции)
    * [Частичная функция](#частичная-функция)
    * [Чистота и побочные эффекты](#чистота-и-побочные-эффекты)
      * [Чистота](#чистота)
      * [Side effects](#side-effects)
  * [Аргументы функции и их обработка](#аргументы-функции-и-их-обработка)
    * [Арность функции](#арность-функции)
    * [Каррирование](#каррирование)
    * [Частичное применение](#частичное-применение)
  * [Свойства и виды функций](#свойства-и-виды-функций)
    * [Индемпотентность](#индемпотентность)
    * [Предикат](#предикат)
    * [Замыкание](#замыкание)
* [2. Общие понятия](#2-общие-понятия)
  * [Referential Transparency](#referential-transparency)
  * [Equational Reasoning](#equational-reasoning)
  * [Continuation](#continuation)
  * [Contracts](#contracts)
  * [Category](#category)
  * [Value](#value)
  * [Constant](#constant)
  * [Lazy evaluation](#lazy-evaluation)
  * [Lambda Calculus](#lambda-calculus)
* [3. Типы](#3-типы)
  * [Тип (данных)](#тип-данных)
  * [Алгебраический тип данных](#алгебраический-тип-данных)
    * [Тип-сумма (sum type)](#тип-сумма-sum-type)
    * [Тип-произведение (product type)](#тип-произведение-product-type)
    * [Дополнения <!-- omit in TOC -->](#дополнения----omit-in-toc-)
  * [Functor](#functor)
  * [Pointed Functor](#pointed-functor)
  * [Lifting](#lifting)
  * [Monoid](#monoid)
  * [Monad](#monad)
  * [Comonad](#comonad)
  * [Applicative Functor](#applicative-functor)
  * [Setoid](#setoid)
  * [Semigroup](#semigroup)
  * [Foldable](#foldable)
  * [Lens](#lens)

# 1. Функции

<!--
- https://www.haskell.org/tutorial/functions.html
- https://wiki.haskell.org/Function
-->

## Определение функции

*Function*

Функция  `f :: X -> Y` каждому элементу `x` типа `X` сопоставляет элемент `f x` типа `Y`. 

`x` называется аргументом функции, а `f x` - значением функции. 

Функции, которые соответствуют данному определению, являются: 

- *тотальными* - каждому возможному аргументу сопоставлено значение функции, 
- *детерминированными* - каждому аргументу всегда соответствует одно и то же значение функции,
- *чистыми* - вычисляют значение по аргументу и не производят никаких скрытых операций, приводящих к побочным эффектам.

Результат функции полностью зависит только от аргумента, что делает функции независимыми от контекста, в котором они исполняются. Это делает функции удобными для тестирования и переиспользования.

*Примечание:* в программировании функцией может называться и та последовательность операций, которая приводит к побочным эффектам (записи на диск, проведению ввода-вывода, изменению глобальных переменных). Чтобы отличить их от функций в данном определении, такие операции можно называть процедурами. 

## Аннотация типа

*Type signatures*

Подпись, или аннотация, типа - это строка, которая показывает тип какой-либо переменной. 

В Haskell подпись типа может задаваться напрямую в коде, например, таким образом:

```
inc :: Int -> Int
```

В этом случае компилятор будет ожидать, что под имя `inc` соответствует
функции, которая принимает значение типа `Int` и выдает результат
также типа `Int`. В отсутствие подписи типа компилятор сам выводит 
наболее общий вид типа, исходя из того как переменная используется в программе: 

```haskell
Prelude> inc x = x + 1
Prelude> :t inc
inc :: Num a => a -> a
```

`inc :: Num a => a -> a` - это подпись, выведенная компилятором, говорит о том, 
что имя `inc` - это функция, которая принимает значение типа `а` и 
выдает значение типа `a`, при этом сам тип `а` - принадлежит классу 
типов `Num`, который объединяет типы, выражающие числа.

В других языках программирования аннотации типов могут 
иметь справочную функцию, и не проверяться компилятором. 

## Делаем с функциями, что хотим 

### Композиция функций

Создание из двух функций `f(x)` и `g(x)` третьей функции `h`, результатом
которой является применение функции `f` к `g(x)`: `h(x) = f(g(x))`.

В Haskell композиция функций производится оператором `.` (точка). Такая запись 
в point-free форме более лаконична, чем запись с аргументом:

```haskell
-- Предположим, у нас определены две функции 
-- со следующими подписями
even :: Int -> Bool
not :: Bool -> Bool

-- Давайте сдлаем новую функцию, которая проверяет 
-- является ли значение нечетным
myOdd :: Int -> Bool
myOdd x = not (even x)

-- ... или сделаем то же самое с использованием оператора .
myOdd :: Int -> Bool
myOdd = not . even
```

[пример полностью](https://stackoverflow.com/questions/1475896/haskell-function-composition)


```haskell
-- Функция desort создается путем комбинации 
-- сортировки и перечисления списка в обратном порядке
desort = reverse . sort
```

[пример](https://wiki.haskell.org/Function_composition)

### Point-free стиль записи

*Point-free style*

Способ описать функции таким образом, чтобы не использовать 
в явном виде аргументы функции. Например, многие функции могут 
быть представлены как комбинация других функций. 

Сравните, например:

```haskell
sum = foldr (+) 0
```

и

```haskell
sum' xs = foldr (+) 0 xs
```

Обе фукнции выполняют одно и то же действие суммирования, однако 
запись в point-free стиле считается более лаконичной и может содержать 
меньше ошибок. Однако запись более сложных функций в point-free стиле
затрудняет их восприятие и понимание логики вычислений.

*Ссылки:*

- [Point-free](https://wiki.haskell.org/Pointfree)

### Лямбда-функция

*Lambda*

Функция без имени, анонимная фукнция.

```haskell
\x -> x + 1
```

Анонимные функции часто используются с функциями более высокого порядка. 

```haskell
Prelude> map (\x -> x + 1) [1..4]
[2,3,4,5]
```

### Функция высшего порядка (ФВП)

*Higher-Order Function (HOF)*

Функция, которая принимает другую функцию как аргумент и/или возвращает функцию как результат.

```haskell
Prelude> let add3 a = a + 3
Prelude> map add3 [1..4]
[4,5,6,7]
```

```haskell
Prelude> filter (<4) [1..10]
[1,2,3]
```

## Не совсем "правильные" функции 

### Частичная функция 

*Partial function*

Частичная функция - это функция, для которой нарушается свойство тотальности. Частичная 
функция недоопределена: существуют значения аргумента, для которых частичная функция не может вычислить результат или не закончит свое исполнение.

Частичные функции запутывают анализ программы и могут приводить к ошибкам ее исполнения.

Пример запроса несуществующего элемента списка:

```haskell
[1,2,3] !! 5
```

Для устранения частичных функций могут применяться следующие приемы:

- автоматическая проверка на частичные функции на уровне компилятора - в этом случае программа не будет запущена, выведется сообщение об ошибке;
- добавить в область значений функции дополнительное значение, которое выдается функцией, когда аргумент не может быть обработан;
- различные проверки допустимости исходных значений.

Подробнее см. например [здесь](https://wiki.haskell.org/Avoiding_partial_functions).

### Чистота и побочные эффекты

#### Чистота 

*Purity*

Функция является чистой, если ее значение определяется только 
значением аргумента и если она не производит побочных эффектов.

Все функции в языке Haskell являются чистыми. Настолько чистыми, что для того, 
чтобы получить побочный эффект в виде записи на диск или вывода на экран надо 
еще постараться.

#### Side effects

A function or expression is said to have a side effect if apart from returning a value, it interacts with (reads from or writes to) external mutable state.

```js
const differentEveryTime = new Date()
```

```js
console.log('IO is a side effect!')
```

## Аргументы функции и их обработка

### Арность функции

*Arity (function)*

Количество аргументов, которое принимает функция (унарная, бинарная и т.д.)

```
Prelude> let sum a b = a + b
Prelude> :t sum
sum :: Num a => a -> a -> a

-- Арность функции sum равна 2 
```

### Каррирование

*Currying*

Преобразование функции, которая принимает несколько аргументов, в функцию,
которая принимает один аргумент и возвращает функцию, которая далее применяентя 
к последующим аргументам.

В отличие от других языков программирования функции многих аргументов в Haskell каррированы по умолчанию. Это значит, что частичное применение (см. ниже) доступно для всех функций многих аргументов и не требует специальных действий. 

В примере ниже функция `sum` обрабатывает кортеж из двух значений `(a, b)`. Функция 
`curry` преобразует функцию `sum` в `curriedSum`, которая последовательно принимает 
два аргумента `a` и `b`. 

```haskell
Prelude> let sum (a, b) = a + b
Prelude> let curriedSum = curry sum
Prelude> curriedSum 40 2
42
```

Ссылки:

- [Currying](https://wiki.haskell.org/Currying)
- [What is the difference between currying and partial application?](https://stackoverflow.com/questions/218025/what-is-the-difference-between-currying-and-partial-application)


### Частичное применение

*Partial Application*

Вызов функции с меньшим количеством аргументов, чем необходимо для ее завершения. В этом случае создается новая функция, которая будет обрабатывать оставшиеся аргументы. 

Частичное применение позволяет из более общих или сложных функций получать более простые функции с необходимым специфическим поведением. 

```haskell
-- Создаем функцию сложения двух элементов
Prelude> let add x y = x + y

-- Создадим функцию для увеличения аргумента на единицу.
-- Частично применим функцию add к значению 1.
-- В результате получилась новая функция,
-- которой мы присвоили имя inc
Prelude> let inc = add 1
Prelude> inc 8
Prelude> 9 
```

*Предупреждение.* Частичное применение не следует путать с частичной функцией - это похожие названия, означающие разные вещи.

Ссылки:

- [Partial application](https://wiki.haskell.org/Partial_application)



## Свойства и виды функций

*Прим. переводчика:* термины, которые собраны в этом разделе, не показались мне фундаментальными или интересными. Здесь вы найдете их краткое определение, но 
заучивать или сильно вникать в них, на мой взгляд, не нужно.

### Индемпотентность

*Indepotent*

Функция является идемпотентной, если ее повторное применение не влияет на 
исходный результат:

```
f(f(x)) ≍ f(x)
```

```haskell
Prelude> abs (abs (-1))
1
```

```haskell
Prelude Data.List> sort (sort [1,4,3,1,5])
[1,1,3,4,5]
```

### Предикат

Функция, возвращающая значение правда или ложь. Обычно используется для фильтрации 
последовательности значений по какому-либо признаку.

```haskell
Prelude> let predThree a = a < 3
Prelude> filter predThree [1..10]
[1,2]
```

### Замыкание 

*Closure*

Использование доступных для функции переменных, помимо непосредственно переданных ей аргументов.

> Замыкание — это особый вид функции. Она определена в теле другой функции и создаётся каждый раз во время её выполнения. Синтаксически это выглядит как функция, находящаяся целиком в теле другой функции. При этом вложенная внутренняя функция содержит ссылки на локальные переменные внешней функции. Каждый раз при выполнении внешней функции происходит создание нового экземпляра внутренней функции, с новыми ссылками на переменные внешней функции. 

[Источник](https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%BC%D1%8B%D0%BA%D0%B0%D0%BD%D0%B8%D0%B5_(%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5))

В других языках программирования замыкания играют важную роль, например,
в функциях-конструктуорах, которые используют собственные параметры для создания других функций.

Поскольку Haskell основан на лямбда-исчислении (см.)
замыкания используются в нем естественным образом и [не являются 
чем-то особенным](https://stackoverflow.com/questions/9088295/closures-in-haskell).

```haskell
-- Вымученный пример замыкания на Haskell
-- Переменная x не является аргументом лямбда-функции, 
-- но доступна внутри тела функции f
f x = (\y -> x + y)

-- привычная запись на Haskell
f x y = x + y
```

*Примечание:* Функция-[комбинатор](https://wiki.haskell.org/Combinator), в отличие от замыкания, использует только переданные ей аргументы.


# 2. Общие понятия

## Referential Transparency

An expression that can be replaced with its value without changing the
behavior of the program is said to be referentially transparent.

Say we have function greet:

```js
const greet = () => 'Hello World!'
```

Any invocation of `greet()` can be replaced with `Hello World!` hence greet is
referentially transparent.

##  Equational Reasoning

When an application is composed of expressions and devoid of side effects, truths about the system can be derived from the parts.


## Continuation

At any given point in a program, the part of the code that's yet to be executed is known as a continuation.

```js
const printAsString = (num) => console.log(`Given ${num}`)

const addOneAndContinue = (num, cc) => {
  const result = num + 1
  cc(result)
}

addOneAndContinue(2, printAsString) // 'Given 3'
```

Continuations are often seen in asynchronous programming when the program needs to wait to receive data before it can continue. The response is often passed off to the rest of the program, which is the continuation, once it's been received.

```js
const continueProgramWith = (data) => {
  // Continues program with data
}

readFileAsync('path/to/file', (err, response) => {
  if (err) {
    // handle error
    return
  }
  continueProgramWith(response)
})
```

## Contracts

A contract specifies the obligations and guarantees of the behavior from a function or expression at runtime. This acts as a set of rules that are expected from the input and output of a function or expression, and errors are generally reported whenever a contract is violated.

```js
// Define our contract : int -> boolean
const contract = (input) => {
  if (typeof input === 'number') return true
  throw new Error('Contract violated: expected int -> boolean')
}

const addOne = (num) => contract(num) && num + 1

addOne(2) // 3
addOne('some string') // Contract violated: expected int -> boolean
```

## Category

A category in category theory is a collection of objects and morphisms between them. In programming, typically types
act as the objects and functions as morphisms.

To be a valid category 3 rules must be met:

1. There must be an identity morphism that maps an object to itself.
    Where `a` is an object in some category,
    there must be a function from `a -> a`.
2. Morphisms must compose.
    Where `a`, `b`, and `c` are objects in some category,
    and `f` is a morphism from `a -> b`, and `g` is a morphism from `b -> c`;
    `g(f(x))` must be equivalent to `(g • f)(x)`.
3. Composition must be associative
    `f • (g • h)` is the same as `(f • g) • h`

Since these rules govern composition at very abstract level, category theory is great at uncovering new ways of composing things.

__Further reading__

* [Category Theory for Programmers](https://bartoszmilewski.com/2014/10/28/category-theory-for-programmers-the-preface/)

## Value

<!-- Term -->

Anything that can be assigned to a variable.

```js
5
Object.freeze({name: 'John', age: 30}) // The `freeze` function enforces immutability.
;(a) => a
;[1]
undefined
```

## Constant

A variable that cannot be reassigned once defined.

```js
const five = 5
const john = Object.freeze({name: 'John', age: 30})
```

Constants are [referentially transparent](#referential-transparency). That is, they can be replaced with the values that they represent without affecting the result.

With the above two constants the following expression will always return `true`.

```js
john.age + five === ({name: 'John', age: 30}).age + (5)
```

## Lazy evaluation

Lazy evaluation is a call-by-need evaluation mechanism that delays the evaluation of an expression until its value is needed. In functional languages, this allows for structures like infinite lists, which would not normally be available in an imperative language where the sequencing of commands is significant.

```js
const rand = function*() {
  while (1 < 2) {
    yield Math.random()
  }
}
```

```js
const randIter = rand()
randIter.next() // Each execution gives a random value, expression is evaluated on need.
```

## Lambda Calculus
A branch of mathematics that uses functions to create a [universal model of computation](https://en.wikipedia.org/wiki/Lambda_calculus).

# 3. Типы

## Тип (данных)

Тип представляет собой набор возможных значений. Например, у типа `Bool` есть 
два значения `True` и `False`. Тип `Int` включает в себя все целочисленные значения.

Типы бывают простые и составные. Например, мы можем создать новый составной тип данных  
`Point` объвив, что он состоит из двух значений типа `Float`. 

```haskell 
data Point = Point Float Float
```

Термины _тип_ и _тип данных_ взаимозаменяемы. 

В функциональном программировании типы позволяют точно описывать с какими значениями
работают функции. Использование типов дает повышенные гарантии корректности программ. 
Например, получив значение непредусмотренного для функции типа компилятор 
выдаст сообщение об ошибке. 

Цитата:

> ... why we should care about types at all: what are they even for? At the lowest level, a computer is concerned with bytes, with barely any additional structure. What a type system gives us is abstraction. A type adds meaning to plain bytes: it lets us say “these bytes are text”, “those bytes are an airline reservation”, and so on. Usually, a type system goes beyond this to prevent us from accidentally mixing types up: for example, a type system usually won't let us treat a hotel reservation as a car rental receipt.

[источник](http://book.realworldhaskell.org/read/types-and-functions.html)


Ссылки:
- https://stackoverflow.com/questions/51509949/what-do-haskell-data-constructors-construct
- [What is Hindley-Milner?](http://stackoverflow.com/a/399392/22425) on Stack Overflow


## Алгебраический тип данных

Составной тип, который получается путем из соединения нескольких других типов. Соединение типов называется *алгеброй*, что повлияло на название термина. Чаще всего рассматриваются тип-сумма и тип-произведение.

### Тип-сумма (sum type)

Тип-сумма - это комбинация двух и более типов в новый тип таким образом, что число возможных значений в новом типе будет соответствовать сумме входящих элементов.

Булевский тип данных "правда-ложь" является самым простым типом-суммой:

```haskell
data Bool = False | True
```

Три цвета светофора также тип-сумма:

```haskell
data TrafficLight = Red | Yellow | Green
```

В примерах выше тип-сумма построен из простейших элементов, но эти элементы могут быть и более сложными.
Тип `Move` описывает движение робота по прямой с целочисленными шагами вперед, назад или с остановкой. 

```haskell
data Move = Stop | Ahead Int | Back Int
```

Шаги робота теперь можно описать с помощью списка типа `[Move]`, например, `[Ahead 1, Stop, Stop, Back -2]` (шаг вперед, два назад).

Типы `Maybe` и `Either`,  использующиеся в языке Хаскелл для управлениями ситуациями с нежелательными результатами вычислений, также являются типами-суммой. В некоторых других функциональных языках программирования - это тип `Option`.

### Тип-произведение (product type)

Тип-произведение объединяет элементы таким образом, что количество новых значений представляет собой произведение возможных количеств входящих значений. 

В большинстве языков программирования есть тип кортеж (tuple), который является самым простым типом-произведением. Например, кортеж из трех булевых значений типа `(Bool, Bool, Bool)` имеет  2\*2\*2 = 8 значений.

Привычные структры данных, например, записи с полями значений, также являются типами-произведением.

```haskell
data Person = Person {name:String , age::Int}
Person "LittleBaby" 2
```

Место точки на плоскости соcтоит их двух координат, которые можно выразить типом-произведением двух значений типа `Float`:

```haskell
data Position = Position Float Float
Position 1.5 2.8
```

__Дополнения__:

- [Теория множеств](https://ru.wikipedia.org/wiki/%D0%A2%D0%B5%D0%BE%D1%80%D0%B8%D1%8F_%D0%BC%D0%BD%D0%BE%D0%B6%D0%B5%D1%81%D1%82%D0%B2).
- [Бывают ли алгебраические типы данных вне типа-суммы и произведения?](https://stackoverflow.com/questions/59509294/are-there-algebraic-data-types-outside-of-sum-and-product)


## Functor

An object that implements a `map` function which, while running over each value in the object to produce a new object, adheres to two rules:

__Preserves identity__
```
object.map(x => x) ≍ object
```

__Composable__

```
object.map(compose(f, g)) ≍ object.map(g).map(f)
```

(`f`, `g` are arbitrary functions)

A common functor in JavaScript is `Array` since it abides to the two functor rules:

```js
;[1, 2, 3].map(x => x) // = [1, 2, 3]
```

and

```js
const f = x => x + 1
const g = x => x * 2

;[1, 2, 3].map(x => f(g(x))) // = [3, 5, 7]
;[1, 2, 3].map(g).map(f)     // = [3, 5, 7]
```

## Pointed Functor
An object with an `of` function that puts _any_ single value into it.

ES2015 adds `Array.of` making arrays a pointed functor.

```js
Array.of(1) // [1]
```

## Lifting

Lifting is when you take a value and put it into an object like a [functor](#pointed-functor). If you lift a function into an [Applicative Functor](#applicative-functor) then you can make it work on values that are also in that functor.

Some implementations have a function called `lift`, or `liftA2` to make it easier to run functions on functors.

```js
const liftA2 = (f) => (a, b) => a.map(f).ap(b) // note it's `ap` and not `map`.

const mult = a => b => a * b

const liftedMult = liftA2(mult) // this function now works on functors like array

liftedMult([1, 2], [3]) // [3, 6]
liftA2(a => b => a + b)([1, 2], [3, 4]) // [4, 5, 5, 6]
```

Lifting a one-argument function and applying it does the same thing as `map`.

```js
const increment = (x) => x + 1

lift(increment)([2]) // [3]
;[2].map(increment) // [3]
```

## Monoid

An object with a function that "combines" that object with another of the same type.

One simple monoid is the addition of numbers:

```js
1 + 1 // 2
```
In this case number is the object and `+` is the function.

An "identity" value must also exist that when combined with a value doesn't change it.

The identity value for addition is `0`.
```js
1 + 0 // 1
```

It's also required that the grouping of operations will not affect the result (associativity):

```js
1 + (2 + 3) === (1 + 2) + 3 // true
```

Array concatenation also forms a monoid:

```js
;[1, 2].concat([3, 4]) // [1, 2, 3, 4]
```

The identity value is empty array `[]`

```js
;[1, 2].concat([]) // [1, 2]
```

If identity and compose functions are provided, functions themselves form a monoid:

```js
const identity = (a) => a
const compose = (f, g) => (x) => f(g(x))
```
`foo` is any function that takes one argument.
```
compose(foo, identity) ≍ compose(identity, foo) ≍ foo
```

## Monad

A monad is an object with [`of`](#pointed-functor) and `chain` functions. `chain` is like [`map`](#functor) except it un-nests the resulting nested object.

```js
// Implementation
Array.prototype.chain = function (f) {
  return this.reduce((acc, it) => acc.concat(f(it)), [])
}

// Usage
Array.of('cat,dog', 'fish,bird').chain((a) => a.split(',')) // ['cat', 'dog', 'fish', 'bird']

// Contrast to map
Array.of('cat,dog', 'fish,bird').map((a) => a.split(',')) // [['cat', 'dog'], ['fish', 'bird']]
```

`of` is also known as `return` in other functional languages.
`chain` is also known as `flatmap` and `bind` in other languages.

## Comonad

An object that has `extract` and `extend` functions.

```js
const CoIdentity = (v) => ({
  val: v,
  extract () {
    return this.val
  },
  extend (f) {
    return CoIdentity(f(this))
  }
})
```

Extract takes a value out of a functor.

```js
CoIdentity(1).extract() // 1
```

Extend runs a function on the comonad. The function should return the same type as the comonad.

```js
CoIdentity(1).extend((co) => co.extract() + 1) // CoIdentity(2)
```

## Applicative Functor

An applicative functor is an object with an `ap` function. `ap` applies a function in the object to a value in another object of the same type.

```js
// Implementation
Array.prototype.ap = function (xs) {
  return this.reduce((acc, f) => acc.concat(xs.map(f)), [])
}

// Example usage
;[(a) => a + 1].ap([1]) // [2]
```

This is useful if you have two objects and you want to apply a binary function to their contents.

```js
// Arrays that you want to combine
const arg1 = [1, 3]
const arg2 = [4, 5]

// combining function - must be curried for this to work
const add = (x) => (y) => x + y

const partiallyAppliedAdds = [add].ap(arg1) // [(y) => 1 + y, (y) => 3 + y]
```

This gives you an array of functions that you can call `ap` on to get the result:

```js
partiallyAppliedAdds.ap(arg2) // [5, 6, 7, 8]
```

## Setoid

An object that has an `equals` function which can be used to compare other objects of the same type.

Make array a setoid:

```js
Array.prototype.equals = function (arr) {
  const len = this.length
  if (len !== arr.length) {
    return false
  }
  for (let i = 0; i < len; i++) {
    if (this[i] !== arr[i]) {
      return false
    }
  }
  return true
}

;[1, 2].equals([1, 2]) // true
;[1, 2].equals([0]) // false
```

## Semigroup

An object that has a `concat` function that combines it with another object of the same type.

```js
;[1].concat([2]) // [1, 2]
```

## Foldable

An object that has a `reduce` function that applies a function against an accumulator and each element in the array (from left to right) to reduce it to a single value.

```js
const sum = (list) => list.reduce((acc, val) => acc + val, 0)
sum([1, 2, 3]) // 6
```

## Lens ##
A lens is a structure (often an object or function) that pairs a getter and a non-mutating setter for some other data
structure.

```js
// Using [Ramda's lens](http://ramdajs.com/docs/#lens)
const nameLens = R.lens(
  // getter for name property on an object
  (obj) => obj.name,
  // setter for name property
  (val, obj) => Object.assign({}, obj, {name: val})
)
```

Having the pair of get and set for a given data structure enables a few key features.

```js
const person = {name: 'Gertrude Blanch'}

// invoke the getter
R.view(nameLens, person) // 'Gertrude Blanch'

// invoke the setter
R.set(nameLens, 'Shafi Goldwasser', person) // {name: 'Shafi Goldwasser'}

// run a function on the value in the structure
R.over(nameLens, uppercase, person) // {name: 'GERTRUDE BLANCH'}
```

Lenses are also composable. This allows easy immutable updates to deeply nested data.

```js
// This lens focuses on the first item in a non-empty array
const firstLens = R.lens(
  // get first item in array
  xs => xs[0],
  // non-mutating setter for first item in array
  (val, [__, ...xs]) => [val, ...xs]
)

const people = [{name: 'Gertrude Blanch'}, {name: 'Shafi Goldwasser'}]

// Despite what you may assume, lenses compose left-to-right.
R.over(compose(firstLens, nameLens), uppercase, people) // [{'name': 'GERTRUDE BLANCH'}, {'name': 'Shafi Goldwasser'}]
```

Other implementations:
* [partial.lenses](https://github.com/calmm-js/partial.lenses) - Tasty syntax sugar and a lot of powerful features
* [nanoscope](http://www.kovach.me/nanoscope/) - Fluent-interface

<!--

# Добавить

## Мощность множества

Cardinality (set)

Количество элементов конечного множества. 

https://ru.wikipedia.org/wiki/%D0%9C%D0%BE%D1%89%D0%BD%D0%BE%D1%81%D1%82%D1%8C_%D0%BC%D0%BD%D0%BE%D0%B6%D0%B5%D1%81%D1%82%D0%B2%D0%B0

Применительно к типам - см. Isomorphisms and Cardinalities в Thinking with Types: Type-Level Programming in Haskell by Sandy Maguire https://thinkingwithtypes.com/ 

-->

# Ссылки <!-- omit in TOC -->

- <http://degoes.net/articles/fp-glossary>
- <http://fprog.ru/2009/issue3/eugene-kirpichov-elements-of-functional-languages/>
- <https://anton-k.github.io/ru-haskell-book/book/home.html>
- <https://www.ibm.com/developerworks/ru/library/l-haskell2/index.html>
- ohaskell
- ruhaskell.org

[hg]: https://wiki.haskell.org/Category:Glossary


__Развитие словаря__

Что можно сделать в этом словаре лучше? Конечно, это решать читателям. 
Вы можете дать комментарий в [issues этого проекта](https://github.com/epogrebnyak/functional-programming-jargon/issues), или [написать переводчику](https://epogrebnyak.github.io/#contact).