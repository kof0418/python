def new_decorator(original_func):
    def wrap_func():
        print("Here is some codes before the original function.")
        original_func()
        print("Here is some codes after the original function.")
    return wrap_func


@new_decorator
def func_needs_decorator():
    print("I am a function that needs decorator.")


func_needs_decorator()
