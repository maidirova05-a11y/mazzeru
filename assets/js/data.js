/* ==========================================================
   ДАННЫЕ САЙТА — проекты, команда, цены, FAQ, контакты.

   Тексты на трёх языках записываются так:
     tx("Русский", "Қазақша", "English")
   Если текст одинаковый на всех языках — можно просто строку: "Astana Tech Cup"

   Как добавить проект: скопируйте любой блок { ... } в projects:
     cat     — "ai" | "mobile" | "web"
     status  — метка на карточке
     title   — название
     desc    — короткое описание
     image   — обложка ("assets/img/projects/файл.webp" или ссылка)
     video   — видео ("assets/video/файл.mp4") — откроется по клику
     link    — ссылка на сайт (необязательно)
     meta    — доп. строки: [ m(подпись, значение), ... ]
   Если картинка не загрузилась, покажется красивая заглушка.

   Тексты страниц (заголовки, кнопки) лежат в assets/js/i18n.js
   ========================================================== */

const tx = (ru, kz, en) => ({ ru, kz, en });
const m = (k, v) => ({ k, v });

/* Повторяющиеся подписи */
const L = {
  duration: tx("Длительность", "Ұзақтығы", "Duration"),
  time: tx("Срок", "Мерзімі", "Timeline"),
  videos: tx("Роликов", "Ролик", "Videos"),
  shots: tx("Кадров", "Кадр", "Shots"),
  client: tx("Клиент", "Клиент", "Client"),
  field: tx("Сфера", "Сала", "Field"),
  langs: tx("Языки", "Тілдер", "Languages"),
  custom: tx("сделали на заказ", "тапсырыспен жасадық", "custom order"),
  days: (n, kzN = n) => tx(`${n} ${n % 10 === 1 && n !== 11 ? "день" : n % 10 >= 2 && n % 10 <= 4 && (n < 10 || n > 20) ? "дня" : "дней"}`, `${kzN} күн`, `${n} days`),
};

window.SITE = {
  brand: "mazzeru",

  contacts: {
    phone: "+7 707 172 3752",
    whatsapp: "77071723752",          // номер без + и пробелов
    telegram: "aldeke7122",              // username без @
    instagram: "mazzeru.studio",
    email: "mazzeru.studio@gmail.com",
    city: tx("Казахстан, Астана", "Қазақстан, Астана", "Astana, Kazakhstan"),
  },

  categories: {
    ai:     { name: tx("ИИ контент", "ИИ контент", "AI content"),       page: "ai-content.html" },
    mobile: { name: tx("Мобилография", "Мобилография", "Mobilography"), page: "mobilography.html" },
    web:    { name: tx("Сайты", "Сайттар", "Websites"),                 page: "websites.html" },
  },

  projects: [
    /* ---------- Сайты (проекты AZ Group) ---------- */
    { cat: "web", status: L.custom, image: "assets/img/projects/astanatechcup.webp?v=2", link: "https://astanatechcup.kz",
      title: "Astana Tech Cup",
      desc: tx("Сайт республиканского чемпионата по робототехнике и дронам: дисциплины, категории участников, таймер до конца приёма заявок и регистрация команд.",
               "Робототехника мен дрондар бойынша республикалық чемпионат сайты: пәндер, қатысушы санаттары, өтінім қабылдау аяқталғанша таймер және командаларды тіркеу.",
               "Website for a national robotics and drone championship: disciplines, participant categories, an application countdown and team registration."),
      meta: [m(L.client, "AZ Group"), m(L.field, tx("Робототехника", "Робототехника", "Robotics"))] },
    { cat: "web", status: L.custom, image: "assets/img/projects/itecx.webp?v=2", link: "https://itecx.kz",
      title: "ITECX",
      desc: tx("Сайт международного научного конгресса (Астана — Рим): форматы участия, этапы, критерии и регистрация. Интерактивный 3D-глобус, три языка.",
               "Халықаралық ғылыми конгресс сайты (Астана — Рим): қатысу форматтары, кезеңдер, критерийлер және тіркеу. Интерактивті 3D-глобус, үш тіл.",
               "Website for an international science congress (Astana — Rome): participation formats, stages, criteria and registration. Interactive 3D globe, three languages."),
      meta: [m(L.client, "AZ Group"), m(L.field, tx("Наука", "Ғылым", "Science"))] },
    { cat: "web", status: L.custom, image: "assets/img/projects/smarthub.webp?v=2", link: "https://smarthub-kz.com",
      title: "SmartHub",
      desc: tx("Сайт детской академии робототехники и дронов: направления, преподаватели и запись на пробный урок.",
               "Балаларға арналған робототехника және дрон академиясының сайты: бағыттар, оқытушылар және сынақ сабағына жазылу.",
               "Website for a kids’ robotics and drone academy: programs, teachers and trial lesson sign-up."),
      meta: [m(L.client, "AZ Group"), m(L.field, tx("Робототехника", "Робототехника", "Robotics"))] },
    { cat: "web", status: L.custom, image: "assets/img/projects/ascora.webp?v=2", link: "https://www.ascora.education",
      title: "Ascora Education",
      desc: tx("Сайт агентства по обучению за рубежом: программы в 40+ странах, летние лагеря, новости и заявка на консультацию.",
               "Шетелде оқыту агенттігінің сайты: 40+ елдегі бағдарламалар, жазғы лагерьлер, жаңалықтар және кеңеске өтінім.",
               "Website for a study-abroad agency: programs in 40+ countries, summer camps, news and consultation requests."),
      meta: [m(L.client, "AZ Group"), m(L.field, tx("Образование", "Білім", "Education"))] },
    { cat: "web", status: L.custom, image: "assets/img/projects/onerlab.webp?v=2", link: "https://onerlab.kz",
      title: "OnerLab",
      desc: tx("Сайт детской академии живописи в Астане: видео-интро, галерея работ учеников и запись в группы.",
               "Астанадағы балаларға арналған кескіндеме академиясының сайты: бейне-интро, оқушылар жұмыстарының галереясы және топтарға жазылу.",
               "Website for a children’s painting academy in Astana: video intro, student gallery and group enrollment."),
      meta: [m(L.client, "AZ Group"), m(L.field, tx("Творчество", "Шығармашылық", "Arts"))] },
    { cat: "web", status: L.custom, image: "assets/img/projects/fibonacci.webp?v=2", link: "https://fibonacci-olympiads.kz",
      title: "Fibonacci Olympiad",
      desc: tx("Сайт международной олимпиады по математике для 3–12 классов: категории, календарь двух этапов, призы и регистрация. Анимированная заставка, спираль Фибоначчи, три языка.",
               "3–12 сыныптарға арналған халықаралық математика олимпиадасының сайты: санаттар, екі кезең күнтізбесі, жүлделер және тіркеу. Анимациялық заставка, Фибоначчи спиралі, үш тіл.",
               "Website for an international maths olympiad for grades 3–12: categories, a two-stage calendar, prizes and registration. Animated intro, Fibonacci spiral, three languages."),
      meta: [m(L.client, "AZ Group"), m(L.field, tx("Образование", "Білім", "Education"))] },
    { cat: "web", status: L.custom, image: "assets/img/projects/atlantia.webp?v=2", link: "https://atlantia-olympiads.kz",
      title: "Atlantia STEM Olympiads",
      desc: tx("Сайт международных STEM-олимпиад по пяти предметам: этапы, положение, призы, оплата и регистрация. Подводная стилистика, предметы на орбите логотипа, три языка.",
               "Бес пән бойынша халықаралық STEM-олимпиадалар сайты: кезеңдер, ереже, жүлделер, төлем және тіркеу. Су асты стилистикасы, логотип орбитасындағы пәндер, үш тіл.",
               "Website for international STEM olympiads in five subjects: stages, rules, prizes, payment and registration. Underwater styling, subjects orbiting the logo, three languages."),
      meta: [m(L.client, "AZ Group"), m(L.field, tx("Образование", "Білім", "Education"))] },
    { cat: "web", status: L.custom, image: "assets/img/projects/uralmashservice.webp?v=2", link: "https://uralmashservice.kz",
      title: "Uralmashservice",
      desc: tx("Сайт уральского поставщика промышленного оборудования и MRO-материалов: каталог, партнёры-производители, проекты и форма заявки. Три языка.",
               "Оралдағы өнеркәсіптік жабдық пен MRO-материалдар жеткізушісінің сайты: каталог, өндіруші-серіктестер, жобалар және өтінім формасы. Үш тіл.",
               "Website for an Uralsk-based industrial equipment and MRO supplier: catalog, manufacturer partners, projects and a request form. Three languages."),
      meta: [m(L.client, tx("Уралмашсервис", "Уралмашсервис", "Uralmashservice")), m(L.field, tx("Промышленность", "Өнеркәсіп", "Industry"))] },

  ],

  /* Основатели. photo — путь к фото, instagram — ник без @.
     Чтобы добавить ещё участника, скопируйте блок { ... }. */
  team: [
    { name: "Maidyrov Aldiyar Asanuly", instagram: "aldeke7122", photo: "assets/img/team/aldiyar.webp", tag: "web", color: "web",
      role: tx("Frontend-разработчик", "Frontend-әзірлеуші", "Frontend Developer"),
      bio: tx("Отвечает за то, что видит посетитель сайта: вёрстку, адаптив под телефоны и плавные анимации. Следит, чтобы страницы быстро загружались и были удобны на любом экране.",
              "Сайтқа кірген адам көретін бөлікке жауап береді: беттерді құрастыру, телефонға бейімдеу және жатық анимациялар. Беттердің жылдам жүктелуін және кез келген экранда ыңғайлы болуын қадағалайды.",
              "Owns everything a visitor sees: layout, mobile responsiveness and smooth animations. Makes sure pages load fast and feel right on any screen."),
      skills: [tx("Вёрстка", "Беттерді құрастыру", "Layout"), tx("Адаптив", "Бейімделу", "Responsive design"), tx("Анимации", "Анимациялар", "Animations"), tx("Скорость загрузки", "Жүктелу жылдамдығы", "Page speed")] },
    { name: "Kuandyk Amir Raiymbekuly", instagram: "amqx.r", photo: "assets/img/team/amir.webp", tag: "ai", color: "ai",
      role: tx("ИИ-креатор", "ИИ-креатор", "AI Creator"),
      bio: tx("Превращает обычные фотографии в ИИ-видео: подбирает сцену, свет и движение камеры под историю клиента. Работает над love story и памятными роликами.",
              "Қарапайым фотосуреттерді ИИ-видеоға айналдырады: клиенттің оқиғасына сай сахнаны, жарықты және камера қозғалысын таңдайды. Love story және естелік роликтермен жұмыс істейді.",
              "Turns ordinary photos into AI videos, choosing the scene, light and camera movement to fit the client’s story. Works on love stories and keepsake videos."),
      skills: [tx("ИИ-видео", "ИИ-видео", "AI video"), tx("Love story", "Love story", "Love stories"), tx("Сценарий сцены", "Сахна сценарийі", "Scene scripting"), tx("Работа с фото", "Фотомен жұмыс", "Photo prep")] },
    { name: "Turlygazy Beksultan Zhandosuly", instagram: "bekkss____", photo: "assets/img/team/beksultan.webp", tag: "ai", color: "ai",
      role: tx("ИИ-креатор", "ИИ-креатор", "AI Creator"),
      bio: tx("Создаёт ИИ-контент для брендов: рекламные ролики и визуалы для соцсетей. Подбирает стиль под задачу и доводит генерацию до чистого результата.",
              "Брендтерге арналған ИИ-контент жасайды: жарнамалық роликтер мен әлеуметтік желілерге визуалдар. Стильді міндетке сай таңдап, генерацияны таза нәтижеге дейін жеткізеді.",
              "Creates AI content for brands: promo videos and social media visuals. Picks the style for each task and refines generations to a clean result."),
      skills: [tx("ИИ-реклама", "ИИ-жарнама", "AI ads"), tx("Визуалы для соцсетей", "Әлеуметтік желі визуалдары", "Social visuals"), tx("Промпты", "Промпттар", "Prompting"), tx("Доработка кадра", "Кадрды өңдеу", "Frame retouching")] },
    { name: "Zhumakhan Beibarys Dulatuly", instagram: "b_d_no_", photo: "assets/img/team/beibarys.webp", tag: "mobile", color: "mobile",
      role: tx("Мобилограф · ИИ-креатор", "Мобилограф · ИИ-креатор", "Mobilographer · AI Creator"),
      bio: tx("Снимает Reels на телефон и сам их монтирует, а при необходимости дополняет живую съёмку ИИ-сценами. Соединяет два направления студии в одном ролике.",
              "Телефонға Reels түсіріп, өзі монтаждайды, қажет болса тірі түсірілімді ИИ-сахналармен толықтырады. Студияның екі бағытын бір роликте біріктіреді.",
              "Shoots and edits Reels on mobile and, when needed, blends live footage with AI scenes, bringing both of the studio’s directions into one video."),
      skills: [tx("Мобильная съёмка", "Мобильді түсірілім", "Mobile shooting"), tx("Монтаж Reels", "Reels монтажы", "Reels editing"), tx("ИИ-сцены", "ИИ-сахналар", "AI scenes"), tx("Сторис", "Сторис", "Stories")] },
    { name: "Dzhambul Serik Olzhasuly", instagram: "serik_dzhambul", photo: "assets/img/team/dzhambul.webp", tag: "ai", color: "ai",
      role: tx("ИИ-креатор", "ИИ-креатор", "AI Creator"),
      bio: tx("Отвечает за постпродакшн ИИ-роликов: монтаж, ритм, музыку и цвет. Собирает сгенерированные сцены в цельное видео, готовое к публикации.",
              "ИИ-роликтердің постпродакшнына жауап береді: монтаж, ырғақ, музыка және түс. Генерацияланған сахналарды жариялауға дайын тұтас видеоға жинайды.",
              "Handles post-production of AI videos: editing, pacing, music and colour. Assembles generated scenes into a finished video ready to publish."),
      skills: [tx("Монтаж", "Монтаж", "Editing"), tx("Звук и музыка", "Дыбыс және музыка", "Sound & music"), tx("Цвет", "Түс", "Colour"), tx("ИИ-генерация", "ИИ-генерация", "AI generation")] },
    { name: "Amantaev Maksat Sabitovich", instagram: "amantaevms", photo: "assets/img/team/maksat.webp", tag: "web", color: "web",
      role: tx("Backend-разработчик", "Backend-әзірлеуші", "Backend Developer"),
      bio: tx("Отвечает за серверную часть сайтов: формы и заявки, базы данных, интеграции и размещение на хостинге. Делает так, чтобы всё за кадром работало стабильно.",
              "Сайттардың серверлік бөлігіне жауап береді: формалар мен өтінімдер, деректер базасы, интеграциялар және хостингке орналастыру. Сахна артындағы бәрінің тұрақты жұмыс істеуін қамтамасыз етеді.",
              "Owns the server side of our websites: forms and requests, databases, integrations and hosting. Keeps everything behind the scenes running reliably."),
      skills: [tx("Серверная логика", "Серверлік логика", "Server logic"), tx("Базы данных", "Деректер базасы", "Databases"), tx("Интеграции", "Интеграциялар", "Integrations"), tx("Деплой", "Деплой", "Deployment")] },
  ],

  packages: {
    ai: [
      { name: tx("Мини", "Мини", "Mini"), price: tx("от 25 000 ₸", "25 000 ₸-ден", "from 25,000 ₸"), note: tx("ролик до 30 сек", "30 сек-қа дейінгі ролик", "video up to 30 sec"),
        items: [tx("Сценарий по вашей истории", "Сіздің тарихыңыз бойынша сценарий", "Script based on your story"), tx("Сцены по вашим фото", "Фотоларыңыз бойынша сахналар", "Scenes from your photos"), tx("Музыка и титры", "Музыка және титрлер", "Music and titles"), tx("1 круг правок", "1 рет түзету", "1 round of revisions")] },
      { name: "Love Story", price: tx("от 60 000 ₸", "60 000 ₸-ден", "from 60,000 ₸"), note: tx("фильм до 3 мин", "3 минутқа дейінгі фильм", "film up to 3 min"), hot: true,
        items: [tx("Интервью и сценарий", "Сұхбат және сценарий", "Interview and script"), tx("Герои, похожие на вас", "Өзіңізге ұқсас кейіпкерлер", "Characters who look like you"), tx("Озвучка и голос за кадром", "Дыбыстау және кадр сыртындағы дауыс", "Voice-over and narration"), tx("Цветокор и саунд-дизайн", "Түс түзету және саунд-дизайн", "Color grading and sound design"), tx("3 круга правок", "3 рет түзету", "3 rounds of revisions")] },
      { name: tx("Бизнес", "Бизнес", "Business"), price: tx("от 120 000 ₸", "120 000 ₸-ден", "from 120,000 ₸"), note: tx("реклама / аватар", "жарнама / аватар", "ads / avatar"),
        items: [tx("Креативная концепция", "Креативті концепция", "Creative concept"), tx("ИИ-аватар или ИИ-сцены", "ИИ-аватар немесе ИИ-сахналар", "AI avatar or AI scenes"), tx("Версии под Reels, YouTube, TV", "Reels, YouTube, TV нұсқалары", "Versions for Reels, YouTube, TV"), tx("Субтитры KZ / RU / EN", "KZ / RU / EN субтитрлері", "Subtitles KZ / RU / EN")] },
    ],
    mobile: [
      { name: tx("Старт", "Старт", "Start"), price: tx("от 30 000 ₸", "30 000 ₸-ден", "from 30,000 ₸"), note: tx("3 ролика", "3 ролик", "3 videos"),
        items: [tx("Сценарии роликов", "Ролик сценарийлері", "Video scripts"), tx("Съёмка до 2 часов", "2 сағатқа дейін түсірілім", "Up to 2 hours of shooting"), tx("Монтаж и цветокор", "Монтаж және түс түзету", "Editing and color grading"), tx("Трендовая музыка", "Трендтегі музыка", "Trending music")] },
      { name: tx("Контент-месяц", "Контент-ай", "Content month"), price: tx("от 150 000 ₸", "150 000 ₸-ден", "from 150,000 ₸"), note: tx("12 роликов", "12 ролик", "12 videos"), hot: true,
        items: [tx("Контент-план на месяц", "Бір айлық контент-жоспар", "Monthly content plan"), tx("2 съёмочных дня", "2 түсірілім күні", "2 shooting days"), tx("Монтаж и цветокор", "Монтаж және түс түзету", "Editing and color grading"), tx("Обложки для Reels", "Reels мұқабалары", "Reels covers"), tx("Консультация по SMM", "SMM бойынша кеңес", "SMM consultation")] },
      { name: tx("Событие", "Іс-шара", "Event"), price: tx("от 50 000 ₸", "50 000 ₸-ден", "from 50,000 ₸"), note: tx("свадьба / мероприятие", "той / іс-шара", "wedding / event"),
        items: [tx("Съёмка до 6 часов", "6 сағатқа дейін түсірілім", "Up to 6 hours of shooting"), tx("Тизер в день события", "Іс-шара күні дайын тизер", "Teaser on the event day"), tx("Полный ролик за 5 дней", "Толық ролик 5 күнде", "Full video in 5 days"), tx("Бэкстейдж-фото", "Бэкстейдж-фото", "Behind-the-scenes photos")] },
    ],
    web: [
      { name: tx("Лендинг", "Лендинг", "Landing page"), price: tx("от 150 000 ₸", "150 000 ₸-ден", "from 150,000 ₸"), note: tx("1 страница", "1 бет", "1 page"),
        items: [tx("Прототип и дизайн", "Прототип және дизайн", "Prototype and design"), tx("Адаптив под телефоны", "Телефонға арналған адаптив", "Mobile-friendly layout"), tx("Форма заявки и WhatsApp", "Өтінім формасы және WhatsApp", "Lead form and WhatsApp"), tx("Подключение аналитики", "Аналитиканы қосу", "Analytics setup")] },
      { name: tx("Корпоративный сайт", "Корпоративтік сайт", "Corporate website"), price: tx("от 350 000 ₸", "350 000 ₸-ден", "from 350,000 ₸"), note: tx("до 10 страниц", "10 бетке дейін", "up to 10 pages"), hot: true,
        items: [tx("Дизайн с нуля", "Нөлден жасалған дизайн", "Custom design"), tx("Анимации и интерактив", "Анимациялар мен интерактив", "Animations and interactivity"), tx("Три языка: KZ / RU / EN", "Үш тіл: KZ / RU / EN", "Three languages: KZ / RU / EN"), tx("Админ-панель для контента", "Контентке арналған админ-панель", "Content admin panel"), tx("Хостинг и домен", "Хостинг және домен", "Hosting and domain")] },
      { name: tx("Магазин / сервис", "Дүкен / сервис", "Store / web app"), price: tx("от 700 000 ₸", "700 000 ₸-ден", "from 700,000 ₸"), note: tx("под задачу", "міндетке сай", "custom scope"),
        items: [tx("Каталог, корзина, оплата", "Каталог, себет, төлем", "Catalog, cart, payments"), tx("Интеграции Kaspi / 1С / CRM", "Kaspi / 1С / CRM интеграциялары", "Kaspi / 1C / CRM integrations"), tx("Личный кабинет", "Жеке кабинет", "User account"), tx("Поддержка после запуска", "Іске қосқаннан кейінгі қолдау", "Post-launch support")] },
    ],
  },

  faq: {
    home: [
      { q: tx("С какими клиентами вы работаете?", "Қандай клиенттермен жұмыс істейсіздер?", "What clients do you work with?"),
        a: tx("С частными клиентами — love story, семейные истории, свадьбы — и с бизнесом: от образовательных проектов и технологических мероприятий до промышленных компаний.",
              "Жеке клиенттермен — love story, отбасылық оқиғалар, тойлар — және бизнеспен: білім беру жобалары мен технологиялық іс-шаралардан бастап өнеркәсіптік компанияларға дейін.",
              "Private clients — love stories, family stories, weddings — and businesses, from educational projects and tech events to industrial companies.") },
      { q: tx("Можно заказать сразу несколько услуг?", "Бірнеше қызметке бірден тапсырыс беруге бола ма?", "Can I order several services at once?"),
        a: tx("Да, так даже удобнее: например, снимем Reels, сделаем ИИ-ролик и лендинг к запуску в едином стиле. Стоимость комплекса рассчитываем под задачу.",
              "Иә, бұл тіпті ыңғайлырақ: мысалы, Reels түсіріп, ИИ-ролик пен іске қосуға арналған лендингті бірыңғай стильде жасаймыз. Кешеннің құнын міндетке қарай есептейміз.",
              "Yes, and it’s more convenient: for example, we shoot Reels, make an AI video and a launch landing page in one style. Bundle pricing is calculated for your task.") },
      { q: tx("Работаете не только в Астане?", "Тек Астанада ғана жұмыс істейсіздер ме?", "Do you work outside Astana?"),
        a: tx("ИИ-контент и сайты делаем удалённо — для любого города и страны. Мобилография — в Астане, выезды в другие города по договорённости.",
              "ИИ-контент пен сайттарды қашықтан жасаймыз — кез келген қала мен ел үшін. Мобилография — Астанада, басқа қалаларға келісім бойынша барамыз.",
              "AI content and websites are done remotely — for any city or country. Mobile filming is in Astana, with travel to other cities by arrangement.") },
      { q: tx("Как происходит оплата?", "Төлем қалай жүргізіледі?", "How does payment work?"),
        a: tx("Как правило, 50% — предоплата, 50% — после сдачи проекта. Работаем по договору, в том числе с ТОО и ИП.",
              "Әдетте 50% — алдын ала төлем, 50% — жобаны тапсырғаннан кейін. Келісімшарт бойынша жұмыс істейміз, соның ішінде ЖШС және ЖК-мен.",
              "Usually 50% upfront and 50% on delivery. We work under contract, including with LLPs and sole proprietors.") },
    ],
    ai: [
      { q: tx("Что нужно от нас для Love Story?", "Love Story үшін бізден не қажет?", "What do you need from us for a Love Story?"),
        a: tx("10–30 фотографий пары с разных ракурсов, короткий рассказ о вашей истории (можно голосовым) и пожелания по настроению. Сценарий, сцены и монтаж — на нас.",
              "Жұптың әр қырынан түскен 10–30 фотосуреті, тарихыңыз туралы қысқаша әңгіме (дауыстық хабарлама да болады) және көңіл-күй бойынша тілектер. Сценарий, сахналар мен монтаж — бізден.",
              "10–30 photos of the couple from different angles, a short account of your story (a voice message is fine) and your wishes for the mood. Script, scenes and edit are on us.") },
      { q: tx("Будем ли мы похожи на себя?", "Біз өзімізге ұқсаймыз ба?", "Will we look like ourselves?"),
        a: tx("Да. Модель учится на ваших фото, чтобы герои были узнаваемы. До финального рендера показываем ключевые кадры — если сходство не устраивает, дорабатываем.",
              "Иә. Модель сіздің фотоларыңыз бойынша оқиды, сондықтан кейіпкерлерді оңай танисыз. Соңғы рендерге дейін негізгі кадрларды көрсетеміз — ұқсастық көңіліңізден шықпаса, жетілдіреміз.",
              "Yes. The model learns from your photos so the characters are recognizable. We show you key frames before the final render — if the likeness isn’t right, we refine it.") },
      { q: tx("Сколько времени занимает?", "Қанша уақыт кетеді?", "How long does it take?"),
        a: tx("Зависит от длины ролика, числа сцен и правок. Точный срок называем после брифа и фиксируем до старта. Если ролик нужен к дате — скажите сразу.",
              "Ролик ұзақтығына, сахналар мен түзетулер санына байланысты. Нақты мерзімді брифтен кейін айтып, жұмыс басталғанға дейін бекітеміз. Ролик белгілі бір күнге керек болса — бірден айтыңыз.",
              "It depends on the video length, number of scenes and revisions. We name the exact timeline after the brief and lock it in before we start. If you need it by a certain date, tell us upfront.") },
      { q: tx("Можно ли использовать ролик в рекламе?", "Роликті жарнамада қолдануға бола ма?", "Can the video be used in ads?"),
        a: tx("Да, передаём права на итоговое видео. Музыку и ИИ-сервисы подбираем с правом коммерческого использования.",
              "Иә, дайын видеоға құқықтарды береміз. Музыка мен ИИ-сервистерді коммерциялық қолдануға рұқсаты барларынан таңдаймыз.",
              "Yes, we transfer the rights to the final video. We choose music and AI services cleared for commercial use.") },
    ],
    mobile: [
      { q: tx("Почему iPhone, а не камера?", "Неге камера емес, iPhone?", "Why an iPhone, not a camera?"),
        a: tx("iPhone снимает в 4K при 60 кадрах в секунду, а со светом, стабилизацией и цветокором даёт кинематографичную картинку. При этом съёмка быстрее, мобильнее и дешевле.",
              "iPhone 4K форматында секундына 60 кадрмен түсіреді, ал жарық, тұрақтандыру және түс түзетумен кинодағыдай сурет береді. Әрі түсірілім жылдамырақ, ұтқырырақ және арзанырақ.",
              "An iPhone shoots 4K at 60 fps, and with proper lighting, stabilization and color grading it delivers a cinematic look. The shoot is also faster, more mobile and more affordable.") },
      { q: tx("Вы пишете сценарии?", "Сценарийді өздеріңіз жазасыздар ма?", "Do you write the scripts?"),
        a: tx("Да. До съёмки готовим сценарии и раскадровку под вашу цель — продажи, охваты или имидж.",
              "Иә. Түсірілімге дейін мақсатыңызға сай сценарий мен раскадровка дайындаймыз — сату, қамту немесе имидж.",
              "Yes. Before the shoot we prepare scripts and a storyboard for your goal — sales, reach or brand image.") },
      { q: tx("Когда будет готово?", "Қашан дайын болады?", "When will it be ready?"),
        a: tx("Первые ролики — через 2–3 дня после съёмки. Тизер с мероприятия — в тот же день, полный ролик — до 5 дней.",
              "Алғашқы роликтер — түсірілімнен кейін 2–3 күнде. Іс-шара тизері — сол күні, толық ролик — 5 күнге дейін.",
              "First videos arrive 2–3 days after the shoot. An event teaser — the same day, the full video — within 5 days.") },
      { q: tx("Сколько правок включено?", "Қанша түзету кіреді?", "How many revisions are included?"),
        a: tx("Две бесплатные правки на каждый ролик.", "Әр роликке екі тегін түзету.", "Two free revisions per video.") },
    ],
    web: [
      { q: tx("Сколько стоит и сколько делается сайт?", "Сайт қанша тұрады және қанша уақытта жасалады?", "How much does a website cost and how long does it take?"),
        a: tx("Стартовые цены — в пакетах выше. Срок зависит от числа страниц, анимаций и интеграций: точную смету и график фиксируем после брифа.",
              "Бастапқы бағалар — жоғарыдағы пакеттерде. Мерзім беттер санына, анимациялар мен интеграцияларға байланысты: нақты смета мен кестені брифтен кейін бекітеміз.",
              "Starting prices are in the packages above. Timing depends on pages, animations and integrations — we fix the exact quote and schedule after the brief.") },
      { q: tx("Сделаете сайт на трёх языках?", "Сайтты үш тілде жасайсыздар ма?", "Can you build a site in three languages?"),
        a: tx("Да: казахский, русский и английский — как у ITECX, Fibonacci Olympiad и Atlantia из нашего портфолио.",
              "Иә: қазақ, орыс және ағылшын тілдерінде — портфолиомыздағы ITECX, Fibonacci Olympiad және Atlantia сайттарындағыдай.",
              "Yes: Kazakh, Russian and English — like ITECX, Fibonacci Olympiad and Atlantia in our portfolio.") },
      { q: tx("Смогу ли я сам менять тексты и фото?", "Мәтіндер мен фотоларды өзім өзгерте аламын ба?", "Can I edit texts and photos myself?"),
        a: tx("Да. Подключаем админ-панель и показываем, как обновлять контент без разработчика.",
              "Иә. Админ-панель қосып, контентті әзірлеушісіз қалай жаңартуды көрсетеміз.",
              "Yes. We set up an admin panel and show you how to update content without a developer.") },
      { q: tx("Что после запуска?", "Іске қосқаннан кейін не болады?", "What happens after launch?"),
        a: tx("Первый месяц поддерживаем сайт бесплатно, дальше — ежемесячное сопровождение по желанию.",
              "Алғашқы айда сайтты тегін қолдаймыз, кейін — қаласаңыз, ай сайынғы сүйемелдеу.",
              "We support the site free for the first month, then offer optional monthly maintenance.") },
    ],
  },
};
