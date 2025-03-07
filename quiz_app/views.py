from django.shortcuts import render, redirect
from .models import Quiz, Question, Answer
from .forms import QuestionForm, AnswerForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import QuizForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from .forms import LoginForm

def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # або будь-яка інша сторінка після входу
            else:
                form.add_error(None, 'Невірне ім’я користувача або пароль.')
    else:
        form = LoginForm()
    return render(request, 'custom_login.html', {'form': form})

def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    answers = request.session.get('quiz_answers', {})

    correct_answers = sum(1 for answer in answers.values() if answer)
    total_questions = quiz.questions.count()

    return render(request, 'quiz_app/quiz_results.html', {
        'quiz': quiz,
        'correct_answers': correct_answers,
        'total_questions': total_questions
    })


def play_quiz(request, quiz_id, question_number):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if question_number > len(questions):
        return redirect('quiz_results', quiz_id=quiz.id)  # Перехід до результатів

    current_question = questions[question_number - 1]
    answers = current_question.answers.all()

    if request.method == "POST":
        selected_answer_id = request.POST.get("answer")
        selected_answer = Answer.objects.get(id=selected_answer_id)

        # Збереження вибору користувача в сесії
        if 'quiz_answers' not in request.session:
            request.session['quiz_answers'] = {}
        request.session['quiz_answers'][str(question_number)] = selected_answer.is_correct
        request.session.modified = True

        return redirect('play_quiz', quiz_id=quiz.id, question_number=question_number + 1)

    return render(request, 'quiz_app/play_quiz.html', {
        'quiz': quiz,
        'current_question': current_question,
        'answers': answers,
        'question_number': question_number,
        'total_questions': len(questions),
    })

    

def add_question(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.quiz = quiz
            new_question.save()
            Answer.objects.create(question = new_question, text = form.cleaned_data['answer1'], is_correct = form.cleaned_data['correct1'])
            Answer.objects.create(question = new_question, text = form.cleaned_data['answer2'], is_correct = form.cleaned_data['correct2'])
            Answer.objects.create(question = new_question, text = form.cleaned_data['answer3'], is_correct = form.cleaned_data['correct3'])
            Answer.objects.create(question = new_question, text = form.cleaned_data['answer4'], is_correct = form.cleaned_data['correct4'])

            
            return redirect('quiz_detail', quiz_id=quiz.id)  
    else:
        form = QuestionForm(initial= {'quiz': quiz})

    return render(request, 'quiz_app/add_question.html', {'form': form, 'quiz': quiz})

def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()
            return redirect('home')  # Перенаправлення на головну сторінку
    else:
        form = QuizForm()
    return render(request, 'create_quiz.html', {'form': form})

# Головна сторінка
def home(request):
    # Перевірка, чи користувач авторизований
    quizzes = Quiz.objects.all()  # Отримуємо всі вікторини
    return render(request, 'home.html', {'quizzes': quizzes})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматичний вхід після реєстрації
            return redirect('home')  # Після реєстрації перенаправляє на домашню сторінку
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_app/quiz_list.html', {'quizzes': quizzes})

@login_required
def quiz_create(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = request.user  # Встановлюємо поточного користувача
            quiz.save()
            return redirect('quiz_list')  # після успішного створення переходимо до списку вікторин
    else:
        form = QuizForm()
    return render(request, 'quiz_app/quiz_create.html', {'form': form})

def question_create(request):
    if request.method == 'POST':
        # логіка для додавання питання
        pass
    return render(request, 'quiz_app/question_form.html')

def answer_create(request):
    if request.method == 'POST':
        # логіка для додавання відповіді
        pass
    return render(request, 'quiz_app/answer_form.html')

def quiz_detail(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.questions.all()
    return render(request, 'quiz_app/quiz_detail.html', {'quiz': quiz, 'questions': questions})

def results(request):
    return render(request, 'quiz_app/results.html')
