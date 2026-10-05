# Reels №3 · «СЪЁМКА ИЗ ПУСТОТЫ» — сценарий про ИИ-видео

Тема: **ИИ-видео** (реклама, love story, клипы, визуал для брендов).
Формат: 9:16 · 1080×1920 · ~30 секунд · лайм #E7FF00 + чёрный + белый (без синего).
Герой — броневой герой в красно-золотом костюме и **закрытом шлеме** (лица нет). Основателей в кадре нет, голос за кадром.
Права и оговорки — в конце файла (раздел 7), прочитайте перед съёмкой.

---

## 1. Идея

Герой стоит в **пустой чёрной студии**: ни декораций, ни камер, ни команды. Он просто **диктует сцену**, и мир вокруг него «печатается» из нейросети: строка промпта набирается лаймом, город вырастает из сетки. Так за 30 секунд мы показываем, что именно делает ИИ-видео: съёмочной группы нет, а кино есть.

Главная фраза: **«Этого ролика никто не снимал.»**

Отличие от рилса-образца: у нас нет ведущей в кадре, нет цифр 1-2-3, нет гэгов про смену локаций и аватары. Сюжетный двигатель — «пустота → промпт → готовое кино».

## 2. Текст для озвучки (целиком, читать ~27 секунд)

> Этого ролика никто не снимал.
> Обычная реклама — это команда, камеры, разрешения и три недели ожидания.
> А у нас есть пустая комната и слова.
> Закат над Астаной. Двое идут по набережной. Камера — следом.
> Готово: love story, которую не нужно снимать.
> Новый продукт. Свет сверху. Брызги. Реклама без студии.
> Клип: ночной город, бит, дрон над крышами.
> ИИ-видео от Mazzeru: реклама, love story, клипы, визуал для брендов.
> Вы даёте идею — мы делаем кино.
> Напишите «КИНО» в Direct.

Вариант короче (для сторис 15 с): строки 1, 3, 4, 8, 10.

## 3. Раскадровка

| № | Время | Что в кадре | Текст на экране | Голос |
|---|---|---|---|---|
| 1 | 0–3 с | Чёрная пустая студия. Герой в шлеме стоит в центре, мерцает свет реактора. Камера медленно наезжает. | **ЭТОГО РОЛИКА / НИКТО НЕ СНИМАЛ** | «Этого ролика никто не снимал.» |
| 2 | 3–7 с | Красные «ценники» вылетают вокруг него и зачёркиваются: команда, камеры, разрешения, локация. | `КОМАНДА` `КАМЕРЫ` `РАЗРЕШЕНИЯ` `3 НЕДЕЛИ` (красные плашки, зачёркнуты) | «Обычная реклама: команда, камеры, разрешения и три недели ожидания.» |
| 3 | 7–10 с | Герой поднимает ладонь. В воздухе печатается лаймовая строка промпта, под ней вырастает сетка города. | `ЗАКАТ НАД АСТАНОЙ. ДВОЕ ИДУТ ПО НАБЕРЕЖНОЙ.` (печатается с курсором) | «А у нас есть пустая комната и слова. Закат над Астаной. Двое идут по набережной.» |
| 4 | 10–14 с | Сетка «заливается» цветом — готовая сцена love story: пара силуэтами на набережной, тёплый закат, камера плывёт следом. | `LOVE STORY` | «Готово: love story, которую не нужно снимать.» |
| 5 | 14–18 с | Новая строка промпта; сцена меняется: вращается продукт (флакон/кроссовок), брызги и блики, свет сверху. | `РЕКЛАМА ПРОДУКТА` | «Новый продукт. Свет сверху. Брызги. Реклама без студии.» |
| 6 | 18–22 с | Быстрая нарезка на бит: ночной город с дрона, неон, герой в профиль; резкие склейки. | `КЛИПЫ И ВИЗУАЛ` | «Клип: ночной город, бит, дрон над крышами.» |
| 7 | 22–26 с | Герой стоит в пустой студии, сцены «собираются» в карточки на HUD; рядом `ИДЕЯ → РОЛИК` со стрелкой. | **MAZZERU · ИИ-ВИДЕО** · `РЕКЛАМА / LOVE STORY / КЛИПЫ` | «ИИ-видео от Mazzeru: реклама, love story, клипы, визуал для брендов. Вы даёте идею — мы делаем кино.» |
| 8 | 26–30 с | Ладонь к камере, лаймовая вспышка, знак ZZ, подпись. | `@mazzeru.studio` · **НАПИШИТЕ «КИНО» В DIRECT** · мелко: `ИИ-контент` | «Напишите «КИНО» в Direct.» |

Заметка по звуку: шаги в пустой студии, лёгкое эхо; «печать» промпта — тихие щелчки клавиш; на смене сцены — свайп; бит 140 BPM с провалом перед финалом. Музыку берите свою (как `brand/video/src/music.py`) или лицензионную — не чужую песню в файле.

## 4. Промпты для Syntx.ai

Я не вижу ваш интерфейс и не знаю, какие модели у вас включены, поэтому промпты универсальные, на английском. Если поля «Negative prompt» нет — добавьте его в конец основного.

**Порядок работы:**
1. Мастер-кадр героя (промпт A) — 4 варианта, выбираем один.
2. Каждый кадр — **image-to-video**: мастер-кадр (или последний кадр прошлой сцены) как первый кадр + промпт сцены.
3. 9:16, 5 с, seed фиксируем, если он есть.
4. **Текст, цифры, HUD и логотип не просим у нейросети** — она ломает буквы. Их добавляем в CapCut поверх (могу собрать лаймовые оверлеи скриптом).

### A. Мастер-кадр героя (image)
```
A sleek armored hero in a red and gold powered exoskeleton suit, closed faceplate helmet with glowing white-blue eye slits, no visible face, circular glowing reactor in the chest, polished metal with subtle battle scratches, standing alone in the center of a vast empty black studio, single soft rim light from above, anamorphic lens flare, shallow depth of field, photorealistic, 9:16 vertical, high contrast with acid lime accent glow on the floor, ultra detailed
```
Negative:
```
human face, open helmet, actor likeness, text, letters, logo, watermark, cartoon, extra fingers, deformed hands, blurry, low quality
```

### B. Кадры (image-to-video, референс — мастер-кадр)

**1 · пустая студия (5 с)**
```
Slow cinematic push-in on the armored hero standing motionless in the center of a huge empty black studio, faint reactor glow pulsing on the glossy floor, a few dust particles in the light beam, deep silence mood, subtle camera drift, 9:16, photorealistic
```

**2 · «ценники» (5 с)**
```
The armored hero in an empty black studio, red glowing rectangular holographic tags fly in around him from all sides and then crack and dissolve into sparks one by one, dark moody red lighting shifting to neutral, cinematic, no readable text, 9:16
```

**3 · промпт и сетка (5 с)**
```
The armored hero raises his open palm, a glowing acid-lime wireframe grid of a city skyline spreads out from his hand across the dark studio, lines of light drawing buildings and a river embankment in the distance, particles gathering into shapes, slow camera pull-back, 9:16, photorealistic, no readable text
```

**4 · love story (5 с)**
```
Golden hour at a modern city embankment with a glass-and-steel skyline, a couple walks away from the camera along the water holding hands, silhouettes against a warm orange sunset, soft lens flare, slow cinematic tracking shot following them, teal and orange colour grade, shallow depth of field, 9:16, photorealistic
```

**5 · реклама продукта (5 с)**
```
Premium commercial product shot of a sleek perfume bottle rotating slowly on a black glossy surface, top softbox light, water splash arcing around it in slow motion, tiny droplets catching acid-lime rim light, dramatic reflections, macro lens, 9:16, photorealistic, no readable text
```

**6 · клип (5 с)**
```
Fast cinematic drone flight over a neon-lit modern city at night, wet streets reflecting lights, sudden fast push between skyscrapers, strong anamorphic flares, high contrast, teal shadows with acid lime highlights, music video energy, 9:16, photorealistic
```

**7 · герой и карточки (5 с)**
```
The armored hero stands in the empty black studio, small glowing holographic screens orbit around him, each showing a different cinematic shot with no readable text, acid-lime edge light, slow camera orbit, confident calm mood, 9:16, photorealistic
```

**8 · финал (5 с)**
```
The armored hero steps forward and raises his open palm towards the camera, a bright acid-lime burst of light fills the dark studio and floods the screen to white, dramatic slow motion, 9:16
```

### C. Если модель «уплывает»
Добавляйте в конец каждого промпта:
```
consistent character design, same suit, same helmet, same studio, cinematic lighting, teal shadows with acid lime highlights, high contrast, film grain, 9:16 vertical
```
Негатив общий:
```
human face, open helmet, actor likeness, text, letters, numbers, logo, watermark, subtitle, cartoon, anime, extra limbs, deformed hands, morphing, flicker, low resolution
```
Держите формулировку брони «red and gold» в каждом промпте без изменений.

## 5. Монтаж (CapCut)
1. Кадры встык; склейки на долях музыки, между 3 и 4 — «заливка» лаймом.
2. Оверлеи: красные «ценники» (зачёркиваются), печать промпта (Unbounded, лайм, курсор), названия сцен, финальный блок.
3. Цветокор единый: тени teal, акценты лайм; кадры 4–6 чуть теплее.
4. Финал: знак ZZ из нашей анимации аутро (лайм/чёрный), 1,5 с.
5. Обложка: кадр 1 + надпись «ЭТОГО РОЛИКА НИКТО НЕ СНИМАЛ».

## 6. Подпись к рилсу
```
Этого ролика никто не снимал: ни команды, ни камер, ни локаций.
ИИ-видео от Mazzeru: реклама, love story, клипы и визуал для брендов.
Вы даёте идею — мы делаем кино. Напишите «КИНО» в Direct.
#mazzeru #астана #ииво #lovestory #реклама #reels
```
Включите в Instagram метку «AI-контент» — платформа просит помечать реалистичный ИИ-контент.

## 7. Права и оговорки
- **Персонаж Marvel (Disney).** Броневой герой — Железный человек, правообладатель — Marvel. Платная реклама услуг с ним может получить жалобу и быть снята. Что мы делаем: закрытый шлем (без лица актёра), в промптах нет «Iron Man», «Marvel», «Stark», в тексте и подписи герой не назван по имени. Риск это снижает, но не убирает. Безопасный вариант — свой герой (лаймово-чёрная броня) при том же сценарии.
- **«Без команды» и «три недели»** — образ, не гарантия сроков. Точные цифры (сроки, цену) говорите только если готовы выполнить.
- **Пара в love story** — сгенерированные люди; реальных людей без согласия не используем.
