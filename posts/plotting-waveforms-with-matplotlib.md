In this tutorial, we will learn how to plot waveforms using Matplotlib, a powerful library for data visualization in Python. A waveform is a graphical representation of a varying quantity over time, and can be used to visualize a wide range of phenomena such as sound, light, and electromagnetism. In order to fully understand and analyze waveforms, it is important to understand its basic properties, including the period, frequency, and amplitude. 

We'll start by defining the key terms of waveforms: a wave is a repeating pattern of oscillation; the period of a wave is the time it takes for one complete oscillation to occur; the frequency of a wave is the number of oscillations that occur in a given period of time; and the amplitude of a wave is the maximum displacement of the oscillation from its equilibrium position

Once we have a good understanding of these concepts, we can move on to using Matplotlib to plot waveforms. We will begin by plotting a single period wave, and then use a function decorator to make it periodic. 

There are many different types of waveforms, each with its own unique characteristics and applications. In this tutorial we will be plotting four of the most common shapes: Square, Triangular, Sawtooth and Sine

## Square Wave
The function \(S_p: [0, 1]\longrightarrow [0, 1]\) that describes a single period of a square wave is given by:
\begin{equation}
    S_p(x)=
    \begin{cases}
        1, \quad \text{if } x < 0.5 \\
        0, \quad \text{if } x > 0.5
    \end{cases}
\end{equation}




## Sawtooth Wave
The function $W_p: [0, 1]\longrightarrow [0, 1]$ that describes a single period of a sawtooth wave is given by:
\begin{equation}
    W_p(x)= x
\end{equation}




## Triangle Wave
The function $T_p: [0, 1]\longrightarrow [0, 1]$ that describes a single period of a triangle wave is given by:
\begin{align}
    T_p(x)=
    \begin{cases}
        2x,  &\text{if } x < 0.5 \\
        -2x + 2,  &\text{if } x > 0.5
    \end{cases}
\end{align}

## Decorators
What are decorators? Decorators are functions that takes another function as argument and modify its behavior without explicity changing it.
This definition might be a little cryptic so let's build an example to ilustrate it

We will start by defining a very simple function that takes no argument and prints a string:

```
def my_func():
    print "function to be decorated"
```

the output for this function is:
```
$ my_func()

#"function to be decorated"
```

Then we will create a function my_decorator that takes another function as argument and  simply prints a string before the argument function is called:

```
def my_func():
    print "function to be decorated"

def my_decorator(func):
    def wrapper():
        print "this function is now decorated"
        func()
    return wrapper
```

After that we will assign the decorator function to the main function, passing the main function as the argument:

```
def my_func():
    print "function to be decorated"

def my_decorator(func):
    def wrapper():
        print "this function is now decorated"
        func()
    return wrapper

my_func = my_decorator(my_func)
```

When called, the output for my_func should be:
```
$ my_func()

#"this function is now decorated"
#"function to be decorated"
```

As you can see the decorator changed the functionality of the function by wrapping it in another function.


You might have noticed that the way we decorated our function is a little clunky, verbose, and it kind of hides the decoration below the definition of the function. Thankfuly Python provides a more elegant way of declaring decorators using the @ symbol.
```
def my_decorator(func)
    def wrapper():
        print "this function is now decorated"
        func()
    return wrapper

@my_decorator
def my_func():
    print "function to be decorated"

```

The code above does exactly the same thing we did when we declared *my_func = my_decorator(my_func)*.

Now that you have a basic understandig of what decorators do and how to use them, we can make it a little more interesting:

Suppose we want to create a function, decorate it in a way that any given number is multiplied by 2 and then display the result

First we will define a function that takes an int as argument and simply return its value:

```
def return_a_number(x):
    return x
```

It is possible to pass arguments to the decorator itself, but to use its values we need do add another wrapper function that will receive and pass the function the same way the decorator did before. Let's see how it works:

```
def multiplier_decorator(number):
  def outer_wrapper(function_to_be_multiplied):
    def wrapper(function_to_be_multiplied_argument):
      result = my_func(function_to_be_multiplied_argument * number)
      print(result)
    return wrapper
  return outer_wrapper
```

Now that our decorator is ready and our function is defined, lets decorate it. In this case, the argument we will be passing to the decorator is the number we want the x value to multiplicated by, namely 2

```
def multiplier_decorator(number):
  def outer_wrapper(function_to_be_multiplied):
    def wrapper(function_to_be_multiplied_argument):
      result = my_func(function_to_be_multiplied_argument * number)
      print(result)
    return wrapper
  return outer_wrapper

@multiplier_decorator(2)
def return_a_number(x):
    return x
```
<br>

```
$ return_a_number(5)

#10
```


![alt text for screen readers](http://2.bp.blogspot.com/-0_YLrLJbPng/UwtcsI38nVI/AAAAAAAABVE/MXbY4pY-pRg/s1600/c%C3%A3o-basset-uma-coisa-puxa-outra.jpg "Text to show on mouseover")




