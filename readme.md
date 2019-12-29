# Словарь сленга функционального программирования <!-- omit in TOC -->

## От переводчика <!-- omit in TOC -->

This is a Russian translation of [Functional Programming Jargon][en] with some additional editing and content and examples in Haskell. Many code examples are drawn from a [Haskell- Turkish version][tr].

Эта статья - перевод и переработка публикации [Functional Programming Jargon][en] c
с примерами на Нaskell, в том числе из [турецкой версии][tr] перевода. Оригинальная статья использует примеры на JavaScript - она переведена на русский [здесь](https://habr.com/ru/post/310172/).

[en]: https://github.com/hemanth/functional-programming-jargon
[tr]: https://github.com/mrtkp9993/functional-programming-jargon

Что поменялось в переводе по сравнению с исходной статьей?

- статьи сгруппированы по секциям
- все примеры на языке Haskell
- добавлены раздел ссылки с русскоязычными и аннглийским ресурсами
- изменения в отдельных статьях
- про морфизмы - убрали в отдельный файл, и не переводили
- не проверяется соответствие [Fantasy Land spec](https://github.com/fantasyland/fantasy-land)

Стиль изложения и требования к содержанию изложены в [contributing.md](contributing.md). 
Этот короткий чеклист по требования к изложению технического материала может быть полезен и в других проектах.


## Введение <!-- omit in TOC -->

Functional programming (FP) provides many advantages, and its popularity has been increasing as a result. However, each programming paradigm comes with its own unique jargon and FP is no exception. By providing a glossary, we hope to make learning FP easier.

__Содержание__

- https://www.haskell.org/tutorial/functions.html
- https://wiki.haskell.org/Function

- [1. Функции](#1-Функции)
  - [Функция](#Функция)
  - [Частичная функция](#Частичная-функция)
  - [Функция высшего порядка (ФВП)](#Функция-высшего-порядка-ФВП)
  - [Closure](#closure)
  - [Partial Application](#partial-application)
  - [Currying](#currying)
  - [Auto Currying](#auto-currying)
  - [Function Composition](#function-composition)
  - [Arity](#arity)
  - [Continuation](#continuation)
  - [Purity](#purity)
  - [Point-Free Style](#point-free-style)
  - [Lambda](#lambda)
  - [Lambda Calculus](#lambda-calculus)
  - [Type Signatures](#type-signatures)
- [2. Общие понятия](#2-Общие-понятия)
  - [Referential Transparency](#referential-transparency)
  - [Equational Reasoning](#equational-reasoning)
  - [Side effects](#side-effects)
  - [Idempotent](#idempotent)
  - [Predicate](#predicate)
  - [Contracts](#contracts)
  - [Category](#category)
  - [Value](#value)
  - [Constant](#constant)
  - [Lazy evaluation](#lazy-evaluation)
- [3. Типы](#3-Типы)
  - [Алгебраический тип данных](#Алгебраический-тип-данных)
    - [Тип-сумма (sum type)](#Тип-сумма-sum-type)
    - [Тип-произведение (product type)](#Тип-произведение-product-type)
  - [Functor](#functor)
  - [Pointed Functor](#pointed-functor)
  - [Lift](#lift)
  - [Monoid](#monoid)
  - [Monad](#monad)
  - [Comonad](#comonad)
  - [Applicative Functor](#applicative-functor)
  - [Setoid](#setoid)
  - [Semigroup](#semigroup)
  - [Foldable](#foldable)
  - [Lens](#lens)

# 1. Функции

## Функция

Функция  `f :: X -> Y` каждому элементу `x` типа `X` сопоставляет элемент `f x` типа `Y`. 
`x` называется аргументом функции, а `f x` - значением функции. 

Функции, которые соответствуют данному определению, являются: 

- тотальными (каждому возможному аргументу сопоставлено значение функции), 
- детерминированными (каждому аргументу всегда соответствует одно и то же значение функции)
- чистыми (вычисляют значение функции по аргументу и не производят никаких скрытых операций, приводящих к побочным эффектам).

Результат функции полностью зависит только от аргумента, что делает функции независимыми от контекста, в котором они исполняются. Это делает функции удобными для работы и переиспользования.

В обыденном понимании функцией может называться и та последовательность операций, которая  приводит к побочным эффектам (записи на диск, проведению ввода-вывода, изменению глобальных переменных). Такие операции правильнее называть процедурами, а не функциями.


## Частичная функция 

Partial function

Частичная функция - это функция, для которой нарушается свойство тотальности. Частичная 
функция недоопределена: существуют значения аргумента, для которых частичная функция не может вычислить результат или не закончит свое исполнение.

Частичные функции запутывают анализ программы и могут приводить к ошибкам ее исполнения.

Пример (о нем заранее предупреждается в документации):

```haskell
[1,2,3] !! 5
```

Для устранения частичных функций могут применяться следующие приемы:

- автоматическая проверка на частичные функции на уровне компилятора - в этом случае программа не будет запущена пока частичные функции не будут устранены;
- добавить в область значений функции дополнительное значение, которое выдается, когда 
  аргумент не может быть обработан исходной функцией;
- различные проверки допустимости исходных значений.

(Подробнее см. например [здесь](https://wiki.haskell.org/Avoiding_partial_functions))


<!--

Partial functions add cognitive overhead, they are harder to reason about and can lead to runtime errors. Some examples:
```js
// example 1: sum of the list
// sum :: [Number] -> Number
const sum = arr => arr.reduce((a, b) => a + b)
sum([1, 2, 3]) // 6
sum([]) // TypeError: Reduce of empty array with no initial value

// example 2: get the first item in list
// first :: [A] -> A
const first = a => a[0]
first([42]) // 42
first([]) // undefined
//or even worse:
first([[42]])[0] // 42
first([])[0] // Uncaught TypeError: Cannot read property '0' of undefined

// example 3: repeat function N times
// times :: Number -> (Number -> Number) -> Number
const times = n => fn => n && (fn(n), times(n - 1)(fn))
times(3)(console.log)
// 3
// 2
// 1
times(-1)(console.log)
// RangeError: Maximum call stack size exceeded
```

### Dealing with partial functions
Partial functions are dangerous as they need to be treated with great caution. You might get an unexpected (wrong) result or run into runtime errors. Sometimes a partial function might not return at all. Being aware of and treating all these edge cases accordingly can become very tedious.
Fortunately a partial function can be converted to a regular (or total) one. We can provide default values or use guards to deal with inputs for which the (previously) partial function is undefined. Utilizing the [`Option`](#Option) type, we can yield either `Some(value)` or `None` where we would otherwise have behaved unexpectedly:
```js
// example 1: sum of the list
// we can provide default value so it will always return result
// sum :: [Number] -> Number
const sum = arr => arr.reduce((a, b) => a + b, 0)
sum([1, 2, 3]) // 6
sum([]) // 0

// example 2: get the first item in list
// change result to Option
// first :: [A] -> Option A
const first = a => a.length ? Some(a[0]) : None()
first([42]).map(a => console.log(a)) // 42
first([]).map(a => console.log(a)) // console.log won't execute at all
//our previous worst case
first([[42]]).map(a => console.log(a[0])) // 42
first([]).map(a => console.log(a[0])) // won't execte, so we won't have error here
// more of that, you will know by function return type (Option)
// that you should use `.map` method to access the data and you will never forget
// to check your input because such check become built-in into the function

// example 3: repeat function N times
// we should make function always terminate by changing conditions:
// times :: Number -> (Number -> Number) -> Number
const times = n => fn => n > 0 && (fn(n), times(n - 1)(fn))
times(3)(console.log)
// 3
// 2
// 1
times(-1)(console.log)
// won't execute anything
```
Making your partial functions total ones, these kinds of runtime errors can be prevented. Always returning a value will also make for code that is both easier to maintain as well as to reason about.
-->

## Функция высшего порядка (ФВП)

Higher-Order Function (HOF)

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

## Closure

A closure is a way of accessing a variable outside its scope.
Formally, a closure is a technique for implementing lexically scoped named binding. It is a way of storing a function with an environment.

A closure is a scope which captures local variables of a function for access even after the execution has moved out of the block in which it is defined.
ie. they allow referencing a scope after the block in which the variables were declared has finished executing.


```js
const addTo = x => y => x + y;
var addToFive = addTo(5);
addToFive(3); //returns 8
```
The function ```addTo()``` returns a function(internally called ```add()```), lets store it in a variable called ```addToFive``` with a curried call having parameter 5.

Ideally, when the function ```addTo``` finishes execution, its scope, with local variables add, x, y should not be accessible. But, it returns 8 on calling ```addToFive()```. This means that the state of the function ```addTo``` is saved even after the block of code has finished executing, otherwise there is no way of knowing that ```addTo``` was called as ```addTo(5)``` and the value of x was set to 5.

Lexical scoping is the reason why it is able to find the values of x and add - the private variables of the parent which has finished executing. This value is called a Closure.

The stack along with the lexical scope of the function is stored in form of reference to the parent. This prevents the closure and the underlying variables from being garbage collected(since there is at least one live reference to it).

Lambda Vs Closure: A lambda is essentially a function that is defined inline rather than the standard method of declaring functions. Lambdas can frequently be passed around as objects.

A closure is a function that encloses its surrounding state by referencing fields external to its body. The enclosed state remains across invocations of the closure.

__Further reading/Sources__
* [Lambda Vs Closure](http://stackoverflow.com/questions/220658/what-is-the-difference-between-a-closure-and-a-lambda)
* [JavaScript Closures highly voted discussion](http://stackoverflow.com/questions/111102/how-do-javascript-closures-work)

## Partial Application

Partially applying a function means creating a new function by pre-filling some of the arguments to the original function.


```js
// Helper to create partially applied functions
// Takes a function and some arguments
const partial = (f, ...args) =>
  // returns a function that takes the rest of the arguments
  (...moreArgs) =>
    // and calls the original function with all of them
    f(...args, ...moreArgs)

// Something to apply
const add3 = (a, b, c) => a + b + c

// Partially applying `2` and `3` to `add3` gives you a one-argument function
const fivePlus = partial(add3, 2, 3) // (c) => 2 + 3 + c

fivePlus(4) // 9
```

You can also use `Function.prototype.bind` to partially apply a function in JS:

```js
const add1More = add3.bind(null, 2, 3) // (c) => 2 + 3 + c
```

Partial application helps create simpler functions from more complex ones by baking in data when you have it. [Curried](#currying) functions are automatically partially applied.


## Currying

The process of converting a function that takes multiple arguments into a function that takes them one at a time.

Each time the function is called it only accepts one argument and returns a function that takes one argument until all arguments are passed.

```js
const sum = (a, b) => a + b

const curriedSum = (a) => (b) => a + b

curriedSum(40)(2) // 42.

const add2 = curriedSum(2) // (b) => 2 + b

add2(10) // 12

```

## Auto Currying
Transforming a function that takes multiple arguments into one that if given less than its correct number of arguments returns a function that takes the rest. When the function gets the correct number of arguments it is then evaluated.

lodash & Ramda have a `curry` function that works this way.

```js
const add = (x, y) => x + y

const curriedAdd = _.curry(add)
curriedAdd(1, 2) // 3
curriedAdd(1) // (y) => 1 + y
curriedAdd(1)(2) // 3
```

__Further reading__
* [Favoring Curry](http://fr.umio.us/favoring-curry/)
* [Hey Underscore, You're Doing It Wrong!](https://www.youtube.com/watch?v=m3svKOdZijA)

## Function Composition

The act of putting two functions together to form a third function where the output of one function is the input of the other.

```js
const compose = (f, g) => (a) => f(g(a)) // Definition
const floorAndToString = compose((val) => val.toString(), Math.floor) // Usage
floorAndToString(121.212121) // '121'
```

## Arity

The number of arguments a function takes. From words like unary, binary, ternary, etc. This word has the distinction of being composed of two suffixes, "-ary" and "-ity." Addition, for example, takes two arguments, and so it is defined as a binary function or a function with an arity of two. Such a function may sometimes be called "dyadic" by people who prefer Greek roots to Latin. Likewise, a function that takes a variable number of arguments is called "variadic," whereas a binary function must be given two and only two arguments, currying and partial application notwithstanding (see below).

```js
const sum = (a, b) => a + b

const arity = sum.length
console.log(arity) // 2

// The arity of sum is 2
```


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

## Purity

A function is pure if the return value is only determined by its
input values, and does not produce side effects.

```js
const greet = (name) => `Hi, ${name}`

greet('Brianne') // 'Hi, Brianne'
```

As opposed to each of the following:

```js
window.name = 'Brianne'

const greet = () => `Hi, ${window.name}`

greet() // "Hi, Brianne"
```

The above example's output is based on data stored outside of the function...

```js
let greeting

const greet = (name) => {
  greeting = `Hi, ${name}`
}

greet('Brianne')
greeting // "Hi, Brianne"
```

... and this one modifies state outside of the function.

## Point-Free Style

Writing functions where the definition does not explicitly identify the arguments used. This style usually requires [currying](#currying) or other [Higher-Order functions](#higher-order-functions-hof). A.K.A Tacit programming.

```js
// Given
const map = (fn) => (list) => list.map(fn)
const add = (a) => (b) => a + b

// Then

// Not points-free - `numbers` is an explicit argument
const incrementAll = (numbers) => map(add(1))(numbers)

// Points-free - The list is an implicit argument
const incrementAll2 = map(add(1))
```

`incrementAll` identifies and uses the parameter `numbers`, so it is not points-free.  `incrementAll2` is written just by combining functions and values, making no mention of its arguments.  It __is__ points-free.

Points-free function definitions look just like normal assignments without `function` or `=>`.


## Lambda

An anonymous function that can be treated like a value.

```js
;(function (a) {
  return a + 1
})

;(a) => a + 1
```
Lambdas are often passed as arguments to Higher-Order functions.

```js
;[1, 2].map((a) => a + 1) // [2, 3]
```

You can assign a lambda to a variable.

```js
const add1 = (a) => a + 1
```

## Lambda Calculus
A branch of mathematics that uses functions to create a [universal model of computation](https://en.wikipedia.org/wiki/Lambda_calculus).


## Type Signatures

Often functions in JavaScript will include comments that indicate the types of their arguments and return values.

There's quite a bit of variance across the community but they often follow the following patterns:

```js
// functionName :: firstArgType -> secondArgType -> returnType

// add :: Number -> Number -> Number
const add = (x) => (y) => x + y

// increment :: Number -> Number
const increment = (x) => x + 1
```

If a function accepts another function as an argument it is wrapped in parentheses.

```js
// call :: (a -> b) -> a -> b
const call = (f) => (x) => f(x)
```

The letters `a`, `b`, `c`, `d` are used to signify that the argument can be of any type. The following version of `map` takes a function that transforms a value of some type `a` into another type `b`, an array of values of type `a`, and returns an array of values of type `b`.

```js
// map :: (a -> b) -> [a] -> [b]
const map = (f) => (list) => list.map(f)
```

__Further reading__
* [Ramda's type signatures](https://github.com/ramda/ramda/wiki/Type-Signatures)
* [Mostly Adequate Guide](https://drboolean.gitbooks.io/mostly-adequate-guide/content/ch7.html#whats-your-type)
* [What is Hindley-Milner?](http://stackoverflow.com/a/399392/22425) on Stack Overflow

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


## Side effects

A function or expression is said to have a side effect if apart from returning a value, it interacts with (reads from or writes to) external mutable state.

```js
const differentEveryTime = new Date()
```

```js
console.log('IO is a side effect!')
```

## Idempotent

A function is idempotent if reapplying it to its result does not produce a different result.

```
f(f(x)) ≍ f(x)
```

```js
Math.abs(Math.abs(10))
```

```js
sort(sort(sort([2, 1])))
```


## Predicate
A predicate is a function that returns true or false for a given value. A common use of a predicate is as the callback for array filter.

```js
const predicate = (a) => a > 2

;[1, 2, 3, 4].filter(predicate) // [3, 4]
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


# 3. Типы


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

### Дополнения <!-- omit in TOC -->

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

## Lift

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



__Ссылки__

- <http://degoes.net/articles/fp-glossary>
- <http://fprog.ru/2009/issue3/eugene-kirpichov-elements-of-functional-languages/>
- <https://anton-k.github.io/ru-haskell-book/book/home.html>
- <https://www.ibm.com/developerworks/ru/library/l-haskell2/index.html>
- ohaskell
- ruhaskell.org
