from roman_map.models import Territorie, Historie, CustomDraw, Quiz, Question, Answer, UserScore, UserAnswer, AncientPlaces, CustomUser
from django.test import TestCase
from django.core.exceptions import ValidationError
import json
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.core.files import File
from django.contrib.auth import get_user_model
from datetime import datetime
from django.utils.timezone import now
from django.utils import timezone
import pytz

class TestCustomUser(TestCase):
    
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(
            username='testuser',
            password='testpass',
            tanulo = False,
            tanar = True,
            first_name = 'test_first_name',
            last_name = "test_last_name"
        )
        self.user_count = User.objects.count()
        self.user_2 = User.objects.create(
            username='testuser_2',
            password='testpass_2',
            tanulo = False,
            tanar = True,
            first_name = 'test_first_name_2',
            last_name = "test_last_name_2"
        )
    def test_user_count(self):
        User = get_user_model()
        self.assertEqual(self.user_count + 1, User.objects.count())
    
    def test_user_2(self):
        self.assertEqual(self.user_2.username, "testuser_2")
        self.assertTrue(self.user_2.is_active)
        self.assertFalse(self.user_2.is_staff)
        self.assertFalse(self.user_2.is_superuser)
        self.assertEqual(self.user_2.tanar, True)

class TestAncientPlaces(TestCase):
    def setUp(self):
        self.ancientplace = AncientPlaces.objects.create(
            modern_name = "test modern name",
            ancient_name = "test ancient name",
            coordinates = "[10, 10]"
        )
    
    def test_ancientplaces_is_valid(self):
        self.ancientplace.full_clean()
    
    def test_ancientplaces_string_representation(self):
        self.assertEqual(str(self.ancientplace), f"{self.ancientplace.id} {self.ancientplace.ancient_name} {self.ancientplace.modern_name}")

    def test_ancientplaces_modern_name(self):
        self.assertEqual(self.ancientplace.modern_name, "test modern name")

    def test_ancientplaces_modern_name_long(self):
        long_text = "a" * 256
        self.ancientplace.modern_name = long_text
        with self.assertRaises(ValidationError):
            self.ancientplace.full_clean()
    
    def test_ancientplaces_ancient_name(self):
        self.assertEqual(self.ancientplace.ancient_name, "test ancient name")

    def test_ancientplaces_ancient_name_long(self):
        long_text = "a" * 256
        self.ancientplace.ancient_name = long_text
        with self.assertRaises(ValidationError):
            self.ancientplace.full_clean()
    
    def test_ancientplaces_coordinates_invalid(self):
        self.ancientplace.coordinates = "[21,]"
        with self.assertRaises(json.JSONDecodeError):
            json.loads(self.ancientplace.coordinates)
    
    def test_ancientplaces_coordinates_valid(self):
        assert json.loads(self.ancientplace.coordinates)


class TestUserAnswer(TestCase):
    def setUp(self):
        self.current_time = datetime.now().replace(second=0, microsecond=0)

        User = get_user_model()
        self.user = User.objects.create(
            username='testuser',
            password='testpass',
            tanulo = False,
            tanar = True,
            first_name = 'test_first_name',
            last_name = "test_last_name"
        )

        self.quiz = Quiz.objects.create(
            title = "test_quiz",
            description = "test_description",
            created_date = self.current_time,
            created_by = self.user
        )
        self.question = Question.objects.create(
            quiz = self.quiz,
            text = "test_text",
            question_type = "mc",
            points = 1
        )
        self.answer = Answer.objects.create(
            question = self.question,
            text = "test text",
            is_correct = True
        )

        self.useranswer = UserAnswer.objects.create(
            user = self.user,
            question = self.question,
            selected_answer = self.answer,
            is_correct = True,
            points_awarded = 1
        )
    
    def test_user_answer_is_valid(self):
        self.useranswer.full_clean()
    
    def test_user_answer_string_representation(self):
        self.assertEqual(str(self.useranswer), f"{self.useranswer.user} - {self.useranswer.question.text}: {'Correct' if self.useranswer.is_correct else 'Incorrect'} ({self.useranswer.points_awarded} points)")

    def test_user_answer_user_foreign_key(self):
        self.assertEqual(self.useranswer.user, self.user)

    def test_user_answer_user_foreing_key_CASCADE(self):
        self.user.delete()
        assert not UserAnswer.objects.exists()
    
    def test_user_answer_user_no_object(self):
        with self.assertRaises(ValueError):
            self.useranswer.user = ''
            self.useranswer.full_clean()
    
    def test_user_answer_question_foreign_key(self):
        self.assertEqual(self.useranswer.question, self.question)

    def test_user_answer_question_foreing_key_CASCADE(self):
        self.question.delete()
        assert not UserAnswer.objects.exists()
    
    def test_user_answer_question_no_object(self):
        with self.assertRaises(ValueError):
            self.useranswer.question = ''
            self.useranswer.full_clean()

    def test_user_answer_selected_answer_foreign_key(self):
        self.assertEqual(self.useranswer.selected_answer, self.answer)

    def test_user_answer_selected_answer_foreing_key_CASCADE(self):
        self.answer.delete()
        assert not UserAnswer.objects.exists()
    
    def test_user_answer_selected_answer_no_object(self):
        with self.assertRaises(ValueError):
            self.useranswer.selected_answer = ''
            self.useranswer.full_clean()
    
    def test_user_answer_is_correct(self):
        self.assertEqual(self.useranswer.is_correct, True)

    def test_user_answer_points_awarded(self):
        self.assertEqual(self.useranswer.points_awarded, 1)

    def test_userscore_total_score_negative(self): 
        with self.assertRaises(ValidationError):
            self.useranswer.points_awarded = -1
            self.useranswer.full_clean()

class TestUserScore(TestCase):
    def setUp(self):
        self.current_time = datetime.now().replace(second=0, microsecond=0)

        User = get_user_model()
        self.user = User.objects.create(
            username='testuser',
            password='testpass',
            tanulo = False,
            tanar = True,
            first_name = 'test_first_name',
            last_name = "test_last_name"
        )

        self.quiz = Quiz.objects.create(
            title = "test_quiz",
            description = "test_description",
            created_date = self.current_time,
            created_by = self.user
        )

        self.userscore = UserScore.objects.create(
            quiz = self.quiz,
            user = self.user,
            total_score = 1
        )
    
    def test_userscore_is_valid(self):
        self.userscore.full_clean()

    def test_userscore_string_representation(self):
        self.assertEqual(str(self.userscore), f"{self.userscore.user} - {self.userscore.quiz.title}: {self.userscore.total_score} points")

    def test_userscore_quiz_foreing_key(self):
        self.assertEqual(self.userscore.quiz, self.quiz)
    
    def test_userscore_quiz_foreing_key_CASCADE(self):
        self.quiz.delete()
        assert not UserScore.objects.exists()
    
    def test_userscore_quiz_no_object(self):
        with self.assertRaises(ValueError):
            self.userscore.quiz = ''
            self.userscore.full_clean()
    
    def test_userscore_user_foreing_key(self):
        self.assertEqual(self.userscore.user, self.user)
    
    def test_userscore_user_foreing_key_CASCADE(self):
        self.user.delete()
        assert not UserScore.objects.exists()

    def test_userscore_quiz_no_object(self):
        with self.assertRaises(ValueError):
            self.userscore.user = ''
            self.userscore.full_clean()
        
    def test_userscore_total_score(self):
        self.assertEqual(self.userscore.total_score, 1)
    
    def test_userscore_total_score_negative(self):
        
        with self.assertRaises(ValidationError):
            self.userscore.total_score = -1
            self.userscore.full_clean()

    


class TestAnswer(TestCase):
    def setUp(self):
        self.current_time = datetime.now().replace(second=0, microsecond=0)

        User = get_user_model()
        self.user = User.objects.create(
            username='testuser',
            password='testpass',
            tanulo = False,
            tanar = True,
            first_name = 'test_first_name',
            last_name = "test_last_name"
        )

        self.quiz = Quiz.objects.create(
            title = "test_quiz",
            description = "test_description",
            created_date = self.current_time,
            created_by = self.user
        )
        self.question = Question.objects.create(
            quiz = self.quiz,
            text = "test_text",
            question_type = "mc",
            points = 1
        )
        self.answer = Answer.objects.create(
            question = self.question,
            text = "test text",
            is_correct = True
        )

    def test_answer_is_valid(self):
        self.answer.full_clean()
    
    def test_answer_string_representation(self):
        self.assertEqual(str(self.answer), f"{self.answer.text} ({'Correct' if self.answer.is_correct else 'Incorrect'})")

    def test_answer_question_foreign_key(self):
        self.assertEqual(self.answer.question, self.question)

    def test_answer_question_foreign_key_CASCADE(self):
        self.question.delete()
        assert not Answer.objects.exists()
    
    def test_answer_text(self):
        self.assertEqual(self.answer.text, "test text")

    def test_answer_text_to_long_text(self):
        long_text = "a" * 256
        self.answer.text = long_text
        with self.assertRaises(ValidationError):
            self.answer.full_clean()
    
    def test_answer_is_correct(self):
        self.assertEqual(self.answer.is_correct, True)


class TestQuestion(TestCase):
    QUESTION_TYPES = [
        ('mc', 'Több válasz'),
        ('tf', 'Igaz/Hamis')
    ]
    def setUp(self):
        self.current_time = datetime.now().replace(second=0, microsecond=0)

        User = get_user_model()
        self.user = User.objects.create(
            username='testuser',
            password='testpass',
            tanulo = False,
            tanar = True,
            first_name = 'test_first_name',
            last_name = "test_last_name"
        )

        self.quiz = Quiz.objects.create(
            title = "test_quiz",
            description = "test_description",
            created_date = self.current_time,
            created_by = self.user
        )
        self.question = Question.objects.create(
            quiz = self.quiz,
            text = "test_text",
            question_type = "mc",
            points = 1
        )
    
    def test_question_is_valid(self):
        self.question.full_clean()
    
    def test_question_string_representation(self):
        self.assertEqual(str(self.question), f"{self.question.text}")

    def test_question_text(self):
        self.assertEqual(self.question.text, "test_text")

    def test_question_to_long_text(self):
        long_text = "a" * 256
        self.question.text = long_text
        with self.assertRaises(ValidationError):
            self.question.full_clean()

    def test_question_quiz_foreign_key(self):
        self.assertEqual(self.question.quiz, self.quiz)

    def test_question_quiz_foreign_key_SET_NULL(self):
        self.quiz.delete()
        self.question.refresh_from_db()
        self.assertIsNone(self.question.quiz)
    
    def test_question_question_type(self):
        self.assertIn(self.question.question_type, [c[0] for c in self.QUESTION_TYPES])

    def test_question_points(self):
        self.assertEqual(self.question.points, 1)
    
    def test_question_points_negative(self):
        
        with self.assertRaises(ValidationError):
            self.question.points = -1
            self.question.full_clean()

class TestQuiz(TestCase):
    def setUp(self):

        #self.current_time = datetime.now().replace(second=0, microsecond=0)
        self.current_time = timezone.now()

        User = get_user_model()
        self.user = User.objects.create(
            username='testuser',
            password='testpass',
            tanulo = False,
            tanar = True,
            first_name = 'test_first_name',
            last_name = "test_last_name"
        )

        self.quiz = Quiz.objects.create(
            title = "test_quiz",
            description = "test_description",
            created_by = self.user
        )
    
    def test_quiz_is_valid(self):
        self.quiz.full_clean()
    
    def test_quiz_string_representation(self):
        self.assertEqual(str(self.quiz), f"{self.quiz.title}")
    
    def test_quiz_title(self):
        self.assertEqual(self.quiz.title, "test_quiz")
    
    def test_quiz_to_long_title(self):
        long_title = "a" * 256
        self.quiz.title = long_title
        with self.assertRaises(ValidationError):
            self.quiz.full_clean()
    
    def test_quiz_description(self):
        self.assertEqual(self.quiz.description, "test_description")
    
    def test_quiz_created_date(self):
        self.assertEqual(self.quiz.created_date.replace(second=0, microsecond=0), self.current_time.replace(second=0, microsecond=0))
    
    def test_quiz_created_by_foreign_key(self):
        self.assertEqual(self.quiz.created_by, self.user)

    def test_draw_created_by_foreign_key_CASCADE(self):
        self.user.delete()
        assert not Quiz.objects.exists()
    
    def test_quiz_created_by_no_object(self):
        with self.assertRaises(ValueError):
            self.quiz.created_by = ''
            self.quiz.full_clean()


class TestCustomDraw(TestCase):
    TYPE_CHOICHES = [
        ("point","Point"),
        ("linestring", "LineString"),
        ("polygon", "Polygon"), 
    ]
    def setUp(self):

        User = get_user_model()
        self.user = User.objects.create(
            username='testuser',
            password='testpass',
            tanulo = False,
            tanar = True,
            first_name = 'test_first_name',
            last_name = "test_last_name"
        )
        self.customdraw = CustomDraw.objects.create(
            name = "test_draw",
            description = "test_description",
            coordinates = "[27, 11]",
            type = "point",
            created_by = self.user
        )
    def test_draw_is_valid(self):
        self.customdraw.full_clean()

    def test_draw_string_representation(self):
        self.assertEqual(str(self.customdraw), f"{self.customdraw.id} {self.customdraw.name} {self.customdraw.created_by.last_name} {self.customdraw.created_by.first_name}")

    def test_draw_name(self):
        self.assertEqual(self.customdraw.name, "test_draw")

    def test_draw_to_long_name(self):
        long_name = "a" * 256
        self.customdraw.name = long_name
        with self.assertRaises(ValidationError):
            self.customdraw.full_clean()

    def test_draw_description(self):
        self.assertEqual(self.customdraw.description, "test_description")
    
    def test_draw_coordinates_valid(self):
        assert json.loads(self.customdraw.coordinates)
    
    def test_draw_coordinates_invalid(self):
        self.customdraw.coordinates = "[21, 33"
        with self.assertRaises(json.JSONDecodeError):
            json.loads(self.customdraw.coordinates)
    
    def test_draw_type(self):
        self.assertIn(self.customdraw.type, [c[0] for c in self.TYPE_CHOICHES])
    
    def test_draw_created_by_foreign_key(self):
        self.assertEqual(self.customdraw.created_by, self.user)

    def test_draw_created_by_foreign_key_CASCADE(self):
        self.user.delete()
        assert not CustomDraw.objects.exists()
    
    def test_draw_created_by_no_object(self):
        with self.assertRaises(ValueError):
            self.customdraw.created_by = ''
            self.customdraw.full_clean()


class TestTerritorie(TestCase):
    
    def setUp(self):

        self.territorie = Territorie.objects.create(
            name = "test_territorie",
            start_date = 100,
            end_date = 1000,
            color = "#fa0202",
            coordinates = '[[[ 21.7433365440549, 15.921404199368197],[21.56656476090123, 15.921404199368197],[21.56656476090123, 12.28978570046047],[21.7433365440549,12.28978570046047],[21.7433365440549,15.921404199368197]]]'
        )
    
    def test_territorie_is_valid(self):
        self.territorie.full_clean()

    def test_territorie_name(self):
        self.assertEqual(self.territorie.name, "test_territorie")
    
    def test_territorie_to_long_name(self):
        long_name = "a" * 256
        self.territorie.name = long_name
        with self.assertRaises(ValidationError):
            self.territorie.full_clean()

    def test_territorie_string_representation(self):
        self.assertEqual(str(self.territorie), f"{self.territorie.id} {self.territorie.name} {self.territorie.start_date} {self.territorie.end_date}")

    def test_territorie_start_date(self):
        self.assertEqual(self.territorie.start_date, 100)

    def test_territorie_end_date(self):
        self.assertEqual(self.territorie.end_date, 1000)

    def test_territorie__start_date_end_date_valid(self):
        assert not self.territorie.save()
    
    def test_territorie_start_date_end_date_invalid(self):
        self.territorie.start_date = self.territorie.end_date + 1
        with self.assertRaises(ValidationError):
            self.territorie.save()

    def test_territorie_color(self):
        self.assertEqual(self.territorie.color, "#fa0202")

    def test_territorie_coordinates_valid(self):
        assert json.loads(self.territorie.coordinates)
    
    def test_territorie_coordinates_invalid(self):
        self.territorie.coordinates = "[[21, 33] [33, 44]"
        with self.assertRaises(json.JSONDecodeError):
            json.loads(self.territorie.coordinates)


class TestHistorie(TestCase):
    HISTORIE_TYPE_CHOICHES = [
        ('csata','csata'),
        ('esemeny', 'esemény'),
        ]
    def setUp(self):

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.TEST_IMAGE_PATH = os.path.join(BASE_DIR, "test_images", "test_image.png")
        assert os.path.exists(self.TEST_IMAGE_PATH), f"Hiba: A fájl nem létezik: {self.TEST_IMAGE_PATH}"

        self.historie = Historie.objects.create(
            name = "test_historie",
            description = "test description",
            coordinates = "[27.31644987181261, 11.17533692739704]",
            historie_type = "esemeny",
            image = self.TEST_IMAGE_PATH,
            date = 100
        )
        
    def test_historie_is_valid(self):
        self.historie.full_clean()

    def test_historie_image_is_saved(self):
        self.assertTrue(self.historie.image)
        self.assertTrue(os.path.exists(self.TEST_IMAGE_PATH))

    def test_historie_image_name(self):
        self.assertEqual(self.historie.image, self.TEST_IMAGE_PATH)
    
    def test_historie_date(self):
        self.assertEqual(self.historie.date, 100)

    def test_historie_historie_type(self):
        self.assertIn(self.historie.historie_type, [c[0] for c in self.HISTORIE_TYPE_CHOICHES])
    
    def test_historie_coordinates_invalid(self):
        self.historie.coordinates = "[21,]"
        with self.assertRaises(json.JSONDecodeError):
            json.loads(self.historie.coordinates)
    
    def test_historie_coordinates_valid(self):
        assert json.loads(self.historie.coordinates)

    def test_historie_description(self):
        self.assertEqual(self.historie.description, "test description")

    def test_historie_string_representation(self):
        self.assertEqual(str(self.historie), f"{self.historie.id} {self.historie.name} {self.historie.historie_type}")

    def test_historie_name(self):
        self.assertEqual(self.historie.name, "test_historie")
    
    def test_historie_to_long_name(self):
        long_name = "a" * 256
        self.historie.name = long_name
        with self.assertRaises(ValidationError):
            self.historie.full_clean()
    
    

    

    