import logging
from openai import OpenAI

logging.basicConfig(
                    level=logging.INFO, 
                    format='[%(asctime)s] %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S'
                )

log = logging.getLogger(__name__)

openai = OpenAI()


def create_quiz_prompt(topic, num_of_questions, num_of_possible_answers):
    prompt = f"Create a multiple choice quize on the topic of {topic} consisting of {num_of_questions} questions. "\
            +f"Each question should have {num_of_possible_answers} options. "\
            +f"Also include the correct answer for each question using the starting string 'Correct Answer:' "

    return prompt


def create_quiz(topic='OpenAI', num_of_questions=4, num_of_possible_answers=4):
    prompt = create_quiz_prompt(topic, num_of_questions, num_of_possible_answers)
    response = openai.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.3
    )

    return response


def extract_questions(quiz, num_of_questions):
    questions = {1: ''}
    question_number = 1
    
    for line in quiz.split('\n'):
        if not line.startswith('Correct Answer:'):
            questions[question_number] += line + '\n'
        else:
            if question_number < num_of_questions:
                question_number += 1
                questions[question_number] = ''

    return questions


def extract_answers(quiz, num_of_questions):
    answers = {1: ''}
    question_number = 1
    
    for line in quiz.split('\n'):
        if line.startswith('Correct Answer:'):
            answers[question_number] += line + '\n'
            
            if question_number < num_of_questions:
                question_number += 1
                answers[question_number] = ''

    return answers


def create_student_view(questions):
    for question in questions.values():
        print(question)


def take_quiz(questions):
    student_answers = {}
    for question_num, question  in questions.items():
        print(question)
        answer = input('Enter your answer: ')
        student_answers[question_num] = answer

    return student_answers


def grade(student_answers, correct_answers):
    correct = 0
    for question, answer in student_answers.items():
        if answer == correct_answers[question][16]:
            correct += 1

    grade = int(100 * correct / num_of_questions)

    if grade < 60:
        passed = "NO PASS"
    else:
        passed = "PASS!"

    return f"{correct}/{num_of_questions} answers are correct! You got a {grade} grade, {passed}"


if __name__ == '__main__':
    
    log.info("We'll walk you through some quick questions before we generate a quiz for you\n")
    
    topic = input("Enter the topic you want to generate quiz for: ")
    num_of_questions = int(input("How many questions should your quiz have as a total? "))
    num_of_possible_answers = int(input("How many possible answers each question should have? "))

    response = create_quiz(topic, num_of_questions, num_of_possible_answers)
    quiz = response.choices[0].message.content.strip()

    questions = extract_questions(quiz, num_of_questions)
    create_student_view(questions)

    correct_answers = extract_answers(quiz, num_of_questions)
    student_answers = take_quiz(questions)

    grade = grade(student_answers, correct_answers)

    print(grade)
