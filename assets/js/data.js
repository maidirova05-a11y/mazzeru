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
const img = (id, w = 900) => `https://images.unsplash.com/photo-${id}?auto=format&fit=crop&w=${w}&q=75`;

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
    phone: "+7 776 198 4474",
    whatsapp: "77761984474",          // номер без + и пробелов
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
    /* ---------- ИИ контент ---------- */
    { cat: "ai", status: L.custom, image: img("1519741497674-611481863552"), video: "",
      title: tx("Love Story «Айдос & Мадина»", "Love Story «Айдос & Мадина»", "Love Story “Aidos & Madina”"),
      desc: tx("ИИ-фильм об истории знакомства пары: от первой встречи в университете до предложения в горах. Показали на свадьбе перед 300 гостями.",
               "Жұптың танысу тарихы туралы ИИ-фильм: университеттегі алғашқы кездесуден таудағы ұсынысқа дейін. Тойда 300 қонақтың алдында көрсетілді.",
               "An AI film about how the couple met — from their first meeting at university to the proposal in the mountains. Premiered at the wedding in front of 300 guests."),
      meta: [m(L.duration, "2:40"), m(L.time, L.days(5))] },
    { cat: "ai", status: L.custom, image: img("1511285560929-80b456fea0bc"), video: "",
      title: tx("Сказка для юбилея мамы", "Анамның мерейтойына арналған ертегі", "A fairy tale for mom’s anniversary"),
      desc: tx("Анимированная история жизни по старым фотографиям — семейный архив ожил.",
               "Ескі фотосуреттер бойынша анимацияланған өмір тарихы — отбасылық мұрағат жанданды.",
               "An animated life story made from old photos — the family archive came alive."),
      meta: [m(L.duration, "3:10"), m(L.time, L.days(7))] },
    { cat: "ai", status: tx("реклама", "жарнама", "advertising"), image: img("1495474472287-4d71bcdd2085"), video: "",
      title: tx("ИИ-ролик для кофейни", "Кофеханаға арналған ИИ-ролик", "AI ad for a coffee shop"),
      desc: tx("Рекламный ролик без съёмочной группы: сгенерировали сцены, озвучку и музыку. 120K просмотров в Reels.",
               "Түсірілім тобынсыз жарнамалық ролик: сахналарды, дыбыстауды және музыканы генерацияладық. Reels-те 120K қаралым.",
               "An ad with no film crew: we generated the scenes, voice-over and music. 120K views on Reels."),
      meta: [m(tx("Охват", "Қамту", "Reach"), "120K"), m(L.time, L.days(3))] },
    { cat: "ai", status: tx("бренд", "бренд", "brand"), image: img("1534528741775-53994a69daeb"), video: "",
      title: tx("ИИ-аватар для эксперта", "Сарапшыға арналған ИИ-аватар", "AI avatar for an expert"),
      desc: tx("Цифровой двойник спикера записывает ролики для соцсетей на 3 языках.",
               "Спикердің цифрлық егізі әлеуметтік желілерге 3 тілде ролик жазады.",
               "The speaker’s digital twin records social media videos in 3 languages."),
      meta: [m(L.langs, "KZ · RU · EN")] },
    { cat: "ai", status: tx("клип", "клип", "music video"), image: img("1470225620780-dba8ba36b745"), video: "",
      title: tx("Музыкальный клип", "Музыкалық клип", "Music video"),
      desc: tx("Полностью сгенерированный клип для молодого исполнителя.",
               "Жас әншіге арналған толықтай генерацияланған клип.",
               "A fully AI-generated music video for a young artist."),
      meta: [m(L.duration, "3:30")] },
    { cat: "ai", status: L.custom, image: img("1522673607200-164d1b6ce486"), video: "",
      title: tx("Приглашение на той", "Тойға шақыру", "Toi invitation video"),
      desc: tx("Видео-приглашение с героями-молодожёнами в стиле мультфильма.",
               "Жас жұбайлар кейіпкер болған мультфильм стиліндегі бейне-шақыру.",
               "A cartoon-style video invitation starring the newlyweds."),
      meta: [m(L.duration, "0:45")] },

    /* ---------- Мобилография ---------- */
    { cat: "mobile", status: tx("съёмка", "түсірілім", "shoot"), image: img("1555396273-367ea4eb4db5"), video: "",
      title: tx("Reels для ресторана", "Мейрамханаға арналған Reels", "Reels for a restaurant"),
      desc: tx("Серия из 12 роликов на iPhone: подача блюд, атмосфера, команда. Рост подписчиков +38% за месяц.",
               "iPhone-ға 12 роликтен тұратын серия: тағамдар, атмосфера, команда. Бір айда жазылушылар +38%.",
               "A series of 12 iPhone videos: dishes, atmosphere, team. +38% followers in a month."),
      meta: [m(L.videos, "12"), m(tx("Рост", "Өсім", "Growth"), "+38%")] },
    { cat: "mobile", status: tx("съёмка", "түсірілім", "shoot"), image: img("1441986300917-64674bd600d8"), video: "",
      title: tx("Контент для бренда одежды", "Киім брендіне арналған контент", "Content for a clothing brand"),
      desc: tx("Лукбук и динамичные переходы для новой коллекции.",
               "Жаңа коллекцияға арналған лукбук пен серпінді ауысулар.",
               "A lookbook and dynamic transitions for a new collection."),
      meta: [m(L.shots, "60+")] },
    { cat: "mobile", status: tx("свадьба", "той", "wedding"), image: img("1519225421980-715cb0215aed"), video: "",
      title: tx("Свадебный тизер за 1 день", "Той тизері 1 күнде", "Same-day wedding teaser"),
      desc: tx("Сняли, смонтировали и выдали вертикальный тизер ещё в день свадьбы.",
               "Тойдың өзінде тік тизерді түсіріп, монтаждап, тапсырдық.",
               "Shot, edited and delivered a vertical teaser on the wedding day itself."),
      meta: [m(L.time, tx("в тот же день", "сол күні", "same day"))] },
    { cat: "mobile", status: tx("путешествие", "саяхат", "travel"), image: img("1501785888041-af3ef285b470"), video: "",
      title: tx("Travel-ролик «Бурабай»", "«Бурабай» travel-ролигі", "“Burabay” travel video"),
      desc: tx("Атмосферный ролик для турагентства с кинематографичным цветокором.",
               "Кинематографиялық түс түзетуі бар турагенттікке арналған атмосфералық ролик.",
               "An atmospheric video for a travel agency with cinematic color grading."),
      meta: [m(tx("Формат", "Формат", "Format"), "Reels / Shorts")] },
    { cat: "mobile", status: tx("эксперт", "сарапшы", "expert"), image: img("1506794778202-cad84cf45f1d"), video: "",
      title: tx("Контент-день для эксперта", "Сарапшыға арналған контент-күн", "Content day for an expert"),
      desc: tx("За 4 часа сняли материал на месяц: 20 роликов с продуманными сценариями.",
               "4 сағатта бір айлық материал түсірдік: ойластырылған сценарийлері бар 20 ролик.",
               "In 4 hours we shot a month of content: 20 videos with well-planned scripts."),
      meta: [m(L.videos, "20")] },
    { cat: "mobile", status: tx("предметка", "заттық түсірілім", "product"), image: img("1596462502278-27bfdc403348"), video: "",
      title: tx("Предметная съёмка косметики", "Косметиканың заттық түсірілімі", "Cosmetics product shoot"),
      desc: tx("Фото и видео для карточек маркетплейса и Instagram.",
               "Маркетплейс карточкалары мен Instagram-ға арналған фото және видео.",
               "Photos and videos for marketplace listings and Instagram."),
      meta: [m(L.shots, "40")] },

    /* ---------- Сайты (проекты AZ Group) ---------- */
    { cat: "web", status: L.custom, image: "assets/img/projects/astanatechcup.webp", link: "https://astanatechcup.kz",
      title: "Astana Tech Cup",
      desc: tx("Сайт республиканского чемпионата по робототехнике и дронам: дисциплины, категории участников, таймер до закрытия заявок и регистрация команд.",
               "Робототехника мен дрондар бойынша республикалық чемпионаттың сайты: пәндер, қатысушылар санаттары, өтінім қабылдау аяқталғанға дейінгі таймер және командаларды тіркеу.",
               "Website for the national robotics and drone championship: disciplines, participant categories, an application deadline countdown and team registration."),
      meta: [m(L.client, "AZ Group"), m(L.field, tx("Робототехника", "Робототехника", "Robotics"))] },
    { cat: "web", status: L.custom, image: "assets/img/projects/itecx.webp", link: "https://itecx.kz",
      title: "ITECX",
      desc: tx("Сайт международного научного конгресса (Астана — Рим): форматы участия, этапы, критерии и регистрация. Интерактивный 3D-глобус и три языка.",
               "Халықаралық ғылыми конгресстің сайты (Астана — Рим): қатысу форматтары, кезеңдер, критерийлер және тіркеу. Интерактивті 3D-глобус және үш тіл.",
               "Website for an international science congress (Astana — Rome): participation formats, stages, criteria and registration. Interactive 3D globe and three languages."),
      meta: [m(L.client, "AZ Group"), m(L.field, tx("Наука", "Ғылым", "Science"))] },
    { cat: "web", status: L.custom, image: "assets/img/projects/smarthub.webp", link: "https://smarthub-kz.com",
      title: "SmartHub",
      desc: tx("Сайт академии робототехники и дронов для детей: направления, преподаватели и запись на пробный урок.",
               "Балаларға арналған робототехника және дрондар академиясының сайты: бағыттар, оқытушылар және сынақ сабағына жазылу.",
               "Website for a kids’ robotics and drone academy: programs, teachers and trial lesson sign-up."),
      meta: [m(L.client, "AZ Group"), m(L.field, tx("Робототехника", "Робототехника", "Robotics"))] },
    { cat: "web", status: L.custom, image: "assets/img/projects/ascora.webp", link: "https://www.ascora.education",
      title: "Ascora Education",
      desc: tx("Сайт агентства зарубежного образования: обучение в 40+ странах, летние лагеря, новости и заявка на консультацию.",
               "Шетелде білім беру агенттігінің сайты: 40+ елде оқу, жазғы лагерьлер, жаңалықтар және кеңеске өтінім.",
               "Website for a study-abroad agency: programs in 40+ countries, summer camps, news and consultation requests."),
      meta: [m(L.client, "AZ Group"), m(L.field, tx("Образование", "Білім", "Education"))] },
    { cat: "web", status: L.custom, image: "assets/img/projects/onerlab.webp", link: "https://onerlab.kz",
      title: "OnerLab",
      desc: tx("Сайт детской академии живописи в Астане: видео-интро, галерея работ учеников и запись в группы.",
               "Астанадағы балаларға арналған кескіндеме академиясының сайты: бейне-интро, оқушылар жұмыстарының галереясы және топтарға жазылу.",
               "Website for a children’s painting academy in Astana: video intro, student gallery and group enrollment."),
      meta: [m(L.client, "AZ Group"), m(L.field, tx("Творчество", "Шығармашылық", "Arts"))] },
  ],

  /* Основатели. photo — путь к фото, instagram — ник без @.
     Чтобы добавить пятого участника, скопируйте блок { ... }. */
  team: [
    { name: "Maidyrov Aldiyar Asanuly", instagram: "aldeke7122", photo: "assets/img/team/aldiyar.webp", tag: "web", color: "web",
      role: tx("Tech Lead · Fullstack-разработчик", "Tech Lead · Fullstack-әзірлеуші", "Tech Lead · Fullstack Developer") },
    { name: "Kuandyk Amir Raiymbekuly", instagram: "amqx.r", photo: "assets/img/team/amir.webp", tag: "ai", color: "ai",
      role: tx("ИИ-креатор", "ИИ-креатор", "AI Creator") },
    { name: "Turlygazy Beksultan Zhandosuly", instagram: "bekkss____", photo: "assets/img/team/beksultan.webp", tag: "ai", color: "ai",
      role: tx("ИИ-креатор", "ИИ-креатор", "AI Creator") },
    { name: "Zhumakhan Beibarys Dulatuly", instagram: "b_d_no_", photo: "assets/img/team/beibarys.webp", tag: "mobile", color: "mobile",
      role: tx("Мобилограф · ИИ-креатор", "Мобилограф · ИИ-креатор", "Mobilographer · AI Creator") },
  ],

  packages: {
    ai: [
      { name: tx("Мини", "Мини", "Mini"), price: tx("от 25 000 ₸", "25 000 ₸-ден", "from 25,000 ₸"), note: tx("ролик до 30 сек", "30 сек-қа дейінгі ролик", "video up to 30 sec"),
        items: [tx("Сценарий по вашей истории", "Сіздің тарихыңыз бойынша сценарий", "Script based on your story"), tx("Генерация сцен по фото", "Фото бойынша сахналар генерациясы", "Scenes generated from your photos"), tx("Музыка и титры", "Музыка және титрлер", "Music and titles"), tx("1 правка", "1 түзету", "1 revision")] },
      { name: "Love Story", price: tx("от 60 000 ₸", "60 000 ₸-ден", "from 60,000 ₸"), note: tx("фильм до 3 мин", "3 минутқа дейінгі фильм", "film up to 3 min"), hot: true,
        items: [tx("Интервью и сценарий", "Сұхбат және сценарий", "Interview and script"), tx("Персонажи по вашим фото", "Сіздің фотоңыз бойынша кейіпкерлер", "Characters based on your photos"), tx("Озвучка / голос", "Дыбыстау / дауыс", "Voice-over"), tx("Цветокор и саунд-дизайн", "Түс түзету және саунд-дизайн", "Color grading and sound design"), tx("3 правки", "3 түзету", "3 revisions")] },
      { name: tx("Бизнес", "Бизнес", "Business"), price: tx("от 120 000 ₸", "120 000 ₸-ден", "from 120,000 ₸"), note: tx("реклама / аватар", "жарнама / аватар", "ads / avatar"),
        items: [tx("Креативная концепция", "Креативті концепция", "Creative concept"), tx("ИИ-аватар или сцены", "ИИ-аватар немесе сахналар", "AI avatar or scenes"), tx("Версии под Reels, YouTube, TV", "Reels, YouTube, TV нұсқалары", "Versions for Reels, YouTube, TV"), tx("Субтитры KZ / RU / EN", "KZ / RU / EN субтитрлері", "Subtitles KZ / RU / EN")] },
    ],
    mobile: [
      { name: tx("Старт", "Старт", "Start"), price: tx("от 30 000 ₸", "30 000 ₸-ден", "from 30,000 ₸"), note: tx("3 ролика", "3 ролик", "3 videos"),
        items: [tx("Сценарии роликов", "Ролик сценарийлері", "Video scripts"), tx("Съёмка до 2 часов", "2 сағатқа дейін түсірілім", "Up to 2 hours of shooting"), tx("Монтаж и цветокор", "Монтаж және түс түзету", "Editing and color grading"), tx("Музыка из трендов", "Трендтегі музыка", "Trending music")] },
      { name: tx("Контент-месяц", "Контент-ай", "Content month"), price: tx("от 150 000 ₸", "150 000 ₸-ден", "from 150,000 ₸"), note: tx("12 роликов", "12 ролик", "12 videos"), hot: true,
        items: [tx("Контент-план на месяц", "Бір айлық контент-жоспар", "Monthly content plan"), tx("2 съёмочных дня", "2 түсірілім күні", "2 shooting days"), tx("Монтаж и цветокор", "Монтаж және түс түзету", "Editing and color grading"), tx("Обложки для Reels", "Reels мұқабалары", "Reels covers"), tx("Консультация по SMM", "SMM бойынша кеңес", "SMM consultation")] },
      { name: tx("Событие", "Іс-шара", "Event"), price: tx("от 50 000 ₸", "50 000 ₸-ден", "from 50,000 ₸"), note: tx("свадьба / мероприятие", "той / іс-шара", "wedding / event"),
        items: [tx("Съёмка до 6 часов", "6 сағатқа дейін түсірілім", "Up to 6 hours of shooting"), tx("Тизер в день события", "Іс-шара күні тизер", "Teaser on the event day"), tx("Полный ролик за 5 дней", "Толық ролик 5 күнде", "Full video in 5 days"), tx("Фото-бэкстейдж", "Фото-бэкстейдж", "Behind-the-scenes photos")] },
    ],
    web: [
      { name: tx("Лендинг", "Лендинг", "Landing page"), price: tx("от 150 000 ₸", "150 000 ₸-ден", "from 150,000 ₸"), note: tx("1 страница", "1 бет", "1 page"),
        items: [tx("Прототип и дизайн", "Прототип және дизайн", "Prototype and design"), tx("Адаптив под телефоны", "Телефондарға бейімделу", "Mobile-friendly layout"), tx("Форма заявки / WhatsApp", "Өтінім формасы / WhatsApp", "Lead form / WhatsApp"), tx("Подключение аналитики", "Аналитиканы қосу", "Analytics setup")] },
      { name: tx("Корпоративный сайт", "Корпоративтік сайт", "Corporate website"), price: tx("от 350 000 ₸", "350 000 ₸-ден", "from 350,000 ₸"), note: tx("до 10 страниц", "10 бетке дейін", "up to 10 pages"), hot: true,
        items: [tx("Уникальный дизайн", "Бірегей дизайн", "Unique design"), tx("Анимации и интерактив", "Анимациялар мен интерактив", "Animations and interactivity"), tx("Мультиязычность KZ / RU / EN", "KZ / RU / EN көптілділік", "Multilingual KZ / RU / EN"), tx("Панель управления контентом", "Контентті басқару панелі", "Content management panel"), tx("Хостинг и домен", "Хостинг және домен", "Hosting and domain")] },
      { name: tx("Магазин / сервис", "Дүкен / сервис", "Store / web service"), price: tx("от 700 000 ₸", "700 000 ₸-ден", "from 700,000 ₸"), note: tx("под задачу", "міндетке сай", "custom scope"),
        items: [tx("Каталог, корзина, оплата", "Каталог, себет, төлем", "Catalog, cart, payments"), tx("Интеграции Kaspi / 1С / CRM", "Kaspi / 1С / CRM интеграциялары", "Kaspi / 1C / CRM integrations"), tx("Личный кабинет", "Жеке кабинет", "User account"), tx("Поддержка после запуска", "Іске қосқаннан кейінгі қолдау", "Post-launch support")] },
    ],
  },

  faq: {
    home: [
      { q: tx("С какими клиентами вы работаете?", "Қандай клиенттермен жұмыс істейсіздер?", "What clients do you work with?"),
        a: tx("С частными клиентами (love story, семейные истории, свадьбы) и с бизнесом — от кофеен и салонов до образовательных проектов.",
              "Жеке клиенттермен (love story, отбасылық тарихтар, тойлар) және бизнеспен — кофеханалар мен салондардан бастап білім беру жобаларына дейін.",
              "Private clients (love stories, family stories, weddings) and businesses — from coffee shops and salons to educational projects.") },
      { q: tx("Можно заказать сразу несколько услуг?", "Бірнеше қызметке бірден тапсырыс беруге бола ма?", "Can I order several services at once?"),
        a: tx("Да, и это выгоднее: например, снимем Reels, сделаем ИИ-ролик и лендинг для запуска — единая стилистика и скидка на комплекс.",
              "Иә, бұл тиімдірек: мысалы, Reels түсіреміз, ИИ-ролик пен іске қосуға арналған лендинг жасаймыз — бірыңғай стиль және кешенге жеңілдік.",
              "Yes, and it’s better value: for example, we shoot Reels, make an AI video and a launch landing page — one consistent style and a bundle discount.") },
      { q: tx("Работаете не только в Астане?", "Тек Астанада ғана жұмыс істейсіздер ме?", "Do you work outside Astana?"),
        a: tx("ИИ-контент и сайты делаем удалённо для любого города и страны. Мобилография — Астана и выезды по договорённости.",
              "ИИ-контент пен сайттарды кез келген қала мен елге қашықтан жасаймыз. Мобилография — Астана және келісім бойынша сапарлар.",
              "We create AI content and websites remotely for any city or country. Mobile videography — Astana, plus travel by arrangement.") },
      { q: tx("Как происходит оплата?", "Төлем қалай жүргізіледі?", "How does payment work?"),
        a: tx("Обычно 50% предоплата и 50% после сдачи. Работаем по договору с ТОО и ИП.",
              "Әдетте 50% алдын ала төлем және тапсырғаннан кейін 50%. ЖШС және ЖК-мен келісімшарт бойынша жұмыс істейміз.",
              "Usually 50% upfront and 50% on delivery. We work under contract with LLPs and sole proprietors.") },
    ],
    ai: [
      { q: tx("Что нужно от нас для Love Story?", "Love Story үшін бізден не қажет?", "What do you need from us for a Love Story?"),
        a: tx("10–30 фотографий пары, короткий рассказ о вашей истории (можно голосовым) и пожелания по настроению. Остальное — наша работа.",
              "Жұптың 10–30 фотосуреті, тарихыңыз туралы қысқаша әңгіме (дауыстық хабарламамен болады) және көңіл-күй бойынша тілектер. Қалғаны — біздің жұмысымыз.",
              "10–30 photos of the couple, a short account of your story (a voice message is fine) and your wishes for the mood. The rest is on us.") },
      { q: tx("Будем ли мы похожи на себя?", "Біз өзімізге ұқсаймыз ба?", "Will we look like ourselves?"),
        a: tx("Да. Мы обучаем модель на ваших фото, поэтому персонажи узнаваемы. Перед финальным рендером показываем ключевые кадры.",
              "Иә. Модельді сіздің фотоларыңызбен оқытамыз, сондықтан кейіпкерлер танымал болады. Соңғы рендерге дейін негізгі кадрларды көрсетеміз.",
              "Yes. We train the model on your photos, so the characters are recognizable. We show you key frames before the final render.") },
      { q: tx("Сколько времени занимает?", "Қанша уақыт кетеді?", "How long does it take?"),
        a: tx("Короткий ролик — 2–3 дня, love story до 3 минут — 5–7 дней. Срочно — обсуждаем.",
              "Қысқа ролик — 2–3 күн, 3 минутқа дейінгі love story — 5–7 күн. Шұғыл болса — талқылаймыз.",
              "A short video takes 2–3 days, a love story up to 3 minutes takes 5–7 days. Rush orders — let’s discuss.") },
      { q: tx("Можно ли использовать ролик в рекламе?", "Роликті жарнамада қолдануға бола ма?", "Can the video be used in ads?"),
        a: tx("Да, передаём права на итоговое видео. Используем только лицензированную музыку и коммерческие ИИ-сервисы.",
              "Иә, дайын видеоға құқықтарды береміз. Тек лицензияланған музыка мен коммерциялық ИИ-сервистерді қолданамыз.",
              "Yes, we transfer the rights to the final video. We only use licensed music and commercial AI services.") },
    ],
    mobile: [
      { q: tx("Почему на телефон, а не на камеру?", "Неге камераға емес, телефонға?", "Why a phone and not a camera?"),
        a: tx("Современный iPhone с правильным светом и цветокором даёт картинку уровня кино, а съёмка получается быстрее, мобильнее и дешевле.",
              "Дұрыс жарық пен түс түзетуі бар заманауи iPhone кино деңгейіндегі сурет береді, ал түсірілім жылдамырақ, ұтқырырақ және арзанырақ.",
              "A modern iPhone with proper lighting and color grading delivers cinema-level footage, and the shoot is faster, more mobile and more affordable.") },
      { q: tx("Вы пишете сценарии?", "Сценарийлерді өздеріңіз жазасыздар ма?", "Do you write the scripts?"),
        a: tx("Да. Перед съёмкой готовим сценарии и раскадровку под ваши цели: продажи, охваты или имидж.",
              "Иә. Түсірілімге дейін мақсаттарыңызға сай сценарийлер мен раскадровка дайындаймыз: сату, қамту немесе имидж.",
              "Yes. Before the shoot we prepare scripts and storyboards for your goals: sales, reach or brand image.") },
      { q: tx("Когда будет готово?", "Қашан дайын болады?", "When will it be ready?"),
        a: tx("Первые ролики — через 2–3 дня после съёмки. Тизер со свадьбы — в тот же день.",
              "Алғашқы роликтер — түсірілімнен кейін 2–3 күнде. Тойдан тизер — сол күні.",
              "The first videos — 2–3 days after the shoot. A wedding teaser — the same day.") },
      { q: tx("Сколько правок включено?", "Қанша түзету кіреді?", "How many revisions are included?"),
        a: tx("Две бесплатные правки на каждый ролик.", "Әр роликке екі тегін түзету.", "Two free revisions per video.") },
    ],
    web: [
      { q: tx("Сколько стоит и сколько делается сайт?", "Сайт қанша тұрады және қанша уақытта жасалады?", "How much does a website cost and how long does it take?"),
        a: tx("Лендинг — от 10 дней, корпоративный сайт — от 3 недель, магазин — от 5 недель. Точную оценку даём после брифа.",
              "Лендинг — 10 күннен, корпоративтік сайт — 3 аптадан, дүкен — 5 аптадан. Нақты бағаны брифтен кейін береміз.",
              "A landing page from 10 days, a corporate website from 3 weeks, an online store from 5 weeks. We give an exact estimate after the brief.") },
      { q: tx("Сделаете сайт на трёх языках?", "Сайтты үш тілде жасайсыздар ма?", "Can you build a site in three languages?"),
        a: tx("Да, казахский, русский и английский — как на сайтах ITECX, Ascora и Astana Tech Cup из нашего портфолио.",
              "Иә, қазақ, орыс және ағылшын тілдерінде — портфолиомыздағы ITECX, Ascora және Astana Tech Cup сайттарындағыдай.",
              "Yes — Kazakh, Russian and English, just like the ITECX, Ascora and Astana Tech Cup sites in our portfolio.") },
      { q: tx("Смогу ли я сам менять тексты и фото?", "Мәтіндер мен фотоларды өзім өзгерте аламын ба?", "Can I edit texts and photos myself?"),
        a: tx("Да, подключаем удобную панель управления и проводим обучение.",
              "Иә, ыңғайлы басқару панелін қосып, оқытып береміз.",
              "Yes, we set up a convenient admin panel and train you to use it.") },
      { q: tx("Что после запуска?", "Іске қосқаннан кейін не болады?", "What happens after launch?"),
        a: tx("Месяц бесплатной поддержки, затем — по желанию ежемесячное сопровождение.",
              "Бір ай тегін қолдау, одан кейін — қалауыңыз бойынша ай сайынғы сүйемелдеу.",
              "A month of free support, then optional monthly maintenance.") },
    ],
  },
};
