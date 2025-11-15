import random
from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import User, Question, Answer, Tag, QuestionLike, AnswerLike

class Command(BaseCommand):
    help = 'Fill database with test data'
    
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio for data generation')
    
    def handle(self, *args, **options):
        ratio = options['ratio']
        
        self.stdout.write(f'Generating data with ratio {ratio}...')
        
        with transaction.atomic():

            users = []
            for i in range(ratio):
                user = User.objects.create_user(
                    username=f'user_{i}',
                    email=f'user_{i}@example.com',
                    password='password123'
                )
                users.append(user)
            

            tags = []
            for i in range(ratio):
                tag = Tag.objects.create(
                    title=f'tag_{i}',
                    is_active=True
                )
                tags.append(tag)
            

            questions = []
            for i in range(ratio * 10):
                question = Question.objects.create(
                    title=f'Question #{i} - Important topic discussion',
                    detailed='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
                    author=random.choice(users),
                    rating=random.randint(-10, 50),
                    votes_count=random.randint(0, 100),
                    answers_count=random.randint(0, 20),
                    is_active=True
                )

                question_tags = random.sample(tags, min(3, len(tags)))
                question.tags.set(question_tags)
                questions.append(question)
            

            answers = []
            for i in range(ratio * 100):
                answer = Answer.objects.create(
                    question=random.choice(questions),
                    author=random.choice(users),
                    answer_text='This is a detailed answer to the question. It provides useful information and solutions to the problem described in the question.',
                    rating=random.randint(-5, 25),
                    is_correct=random.choice([True, False]) if i % 5 == 0 else False,
                    is_active=True
                )
                answers.append(answer)
            

            question_likes_created = 0
            for i in range(ratio * 200):
                user = random.choice(users)
                question = random.choice(questions)
                
                if not QuestionLike.objects.filter(user=user, question=question).exists():
                    QuestionLike.objects.create(
                        user=user,
                        question=question,
                        value=random.choice([-1, 1])
                    )
                    question_likes_created += 1
            

            answer_likes_created = 0
            for i in range(ratio * 200):
                user = random.choice(users)
                answer = random.choice(answers)
                
                if not AnswerLike.objects.filter(user=user, answer=answer).exists():
                    AnswerLike.objects.create(
                        user=user,
                        answer=answer,
                        value=random.choice([-1, 1])
                    )
                    answer_likes_created += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created:\n'
                f'- Users: {len(users)}\n'
                f'- Tags: {len(tags)}\n'
                f'- Questions: {len(questions)}\n'
                f'- Answers: {len(answers)}\n'
                f'- Question likes: {question_likes_created}\n'
                f'- Answer likes: {answer_likes_created}'
            )
        )