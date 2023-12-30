from googletrans import Translator


def text_on_eng(username):
    text = f"""
                    🌟 Welcome {username} 🌈
    
                    Hello there! I'm PsychBot, your friendly companion for all things psychology. Whether you're looking for advice on managing stress, understanding emotions, or enhancing your well-being, I'm here to help.
    
                    🧠 Explore the realms of the mind with PsychBot:
                    🔍 Type "/advice" for personalized psychological tips.
                    📚 Ask me about specific topics like anxiety, relationships, or self-esteem.
    
                    Remember, I'm not a substitute for professional help, but I can offer guidance and support. Let's embark on a journey of self-discovery and mental well-being together!
    
                    🌐 Connect with us:
                    👥 Join our community: t.me/PsychBotCommunity
                    📢 Updates and announcements: t.me/PsychBotUpdates
    
                    Ready to dive into the fascinating world of psychology? Type "/start" to begin!
    
                    🌈 Let the journey to a healthier mind begin! 🌟
                    """
    return text


def text_on_rus(username):
    text = f"""
                    🌟 Добро пожаловать {username} 🌈

                    Привет! Я PsychBot, ваш дружелюбный компаньон по всем вопросам психологии. Ищете ли вы совет по управлению стрессом, пониманию эмоций или улучшению своего самочувствия, я здесь, чтобы помочь.
                    
                     🧠 Исследуйте сферы разума с PsychBot:
                     🔍 Введите "/совет" для получения персонализированных психологических советов.
                     📚 Спрашивайте меня о конкретных темах, таких как тревога, отношения или самооценка.
                    
                    Помните, я не заменяю профессиональную помощь, но могу предложить руководство и поддержку. Давайте отправимся в путешествие самопознания и психического благополучия вместе!
                    
                     🌐 Свяжитесь с нами:
                     👥 Присоединяйтесь к нашему сообществу: t.me/PsychBotCommunity
                     📢 Обновления и анонсы: t.me/PsychBotUpdates
                    
                    Готовы погрузиться в увлекательный мир психологии? Введите "/start", чтобы начать!
                    
                     🌈 Пусть начнется путешествие к здоровому разуму! 🌟
    """
    return text


def get_all_themes():
    return [
        "Social Psychology",
        "Developmental Psychology",
        "Positive Psychology",
        "Abnormal Psychology",
        "Neuropsychology",
        "Forensic Psychology"
    ]


def get_subtopics_for_theme(theme):
    subtopics_dict = {
        "Social Psychology": ["Social Influence", "Social Cognition", "Interpersonal Relationships"],
        "Developmental Psychology": ["Child Development", "Adolescent Development", "Adult Development"],
        "Positive Psychology": ["Happiness", "Gratitude", "Mindfulness"],
        "Abnormal Psychology": ["Mood Disorders", "Anxiety Disorders", "Psychotic Disorders"],
        "Neuropsychology": ["Cognitive Neuroscience", "Brain Imaging", "Neurological Disorders"],
        "Forensic Psychology": ["Criminal Profiling", "Legal Psychology", "Eyewitness Testimony"],
    }

    subtopics = subtopics_dict.get(theme, [])

    return subtopics


def translate_text(text):
    translator = Translator()
    translation = translator.translate(text, src="en", dest="ru")
    return translation.text
