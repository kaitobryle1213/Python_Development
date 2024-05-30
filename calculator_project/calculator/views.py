from django.shortcuts import render

def index(request):
    return render(request, 'calculator/index.html')

def calculate(request):
    if request.method == 'POST':
        number1 = float(request.POST.get('number1', 0))
        number2 = float(request.POST.get('number2', 0))
        operation = request.POST.get('operation')

        if operation == 'add':
            result = number1 + number2
        elif operation == 'subtract':
            result = number1 - number2
        elif operation == 'multiply':
            result = number1 * number2
        elif operation == 'divide':
            if number2 != 0:
                result = number1 / number2
            else:
                result = 'Error: Division by zero'
        else:
            result = 'Invalid operation'

        return render(request, 'calculator/index.html', {'result': result})
