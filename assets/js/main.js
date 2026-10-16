/* ==========================================================
   MAZZERU — логика сайта
   Тексты: i18n.js (интерфейс) и data.js (проекты, цены, FAQ, команда).
   Здесь — интро, язык, отрисовка и анимации.
   ========================================================== */
(() => {
  const S = window.SITE;
  const DICT = window.I18N || {};
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const root = document.documentElement;
  const page = document.body.dataset.page;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fine = matchMedia("(hover: hover) and (pointer: fine)").matches;
  const hasGsap = () => !!window.gsap && !reduce;
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const esc = (t = "") => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const store = {
    get: (k, s = localStorage) => { try { return s.getItem(k); } catch { return null; } },
    set: (k, v, s = localStorage) => { try { s.setItem(k, v); } catch {} },
  };

  /* ---------- Язык ---------- */
  const LANGS = ["kz", "ru", "en"];
  const fromUrl = new URLSearchParams(location.search).get("lang");
  let lang = LANGS.includes(fromUrl) ? fromUrl : LANGS.includes(store.get("lang")) ? store.get("lang") : "ru";
  const L = (v) => (v && typeof v === "object" ? v[lang] ?? v.ru : v ?? "");
  const tr = (key) => (DICT[key] ? DICT[key][lang] ?? DICT[key].ru : key);

  /* ---------- Иконки ---------- */
  const i = (p, w = 1.8) => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round">${p}</svg>`;
  const ICON = {
    arrow: i('<path d="M5 12h14M13 6l6 6-6 6"/>', 2.2),
    external: i('<path d="M7 17 17 7M8 7h9v9"/>', 2.2),
    play: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4.5v15a1 1 0 0 0 1.5.86l12-7.5a1 1 0 0 0 0-1.72l-12-7.5A1 1 0 0 0 7 4.5z"/></svg>`,
    plus: i('<path d="M12 5v14M5 12h14"/>', 2.2),
    close: i('<path d="M6 6l12 12M18 6 6 18"/>', 2.2),
    ai: i('<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>'),
    mobile: i('<rect x="6" y="2.5" width="12" height="19" rx="3"/><circle cx="12" cy="9" r="2.6"/><path d="M10.5 18h3"/>'),
    web: i('<rect x="2.5" y="4" width="19" height="16" rx="2.5"/><path d="M2.5 9h19M9 14l-2 1.5L9 17M15 14l2 1.5-2 1.5"/>'),
    whatsapp: i('<path d="M3.5 20.5 5 16a8.5 8.5 0 1 1 3 3z"/><path d="M9 9.5c0 3 2.5 5.5 5.5 5.5l1-1.5-2-1-1 1c-1-.5-2-1.5-2.5-2.5l1-1-1-2z"/>'),
    telegram: i('<path d="m21 4-18 7 6 2 2 6 3-4 5 4z"/><path d="m9 13 8-6"/>'),
    instagram: i('<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>'),
    mail: i('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'),
    pin: i('<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>'),
    spark: i('<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>'),
    clock: i('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
    shield: i('<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>'),
    layers: i('<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>'),
    chat: i('<path d="M4 5h16v11H8l-4 4z"/><path d="M8 10h8M8 13h5"/>'),
    photo: i('<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="m21 16-5-5-9 9"/>'),
    wand: i('<path d="m4 20 11-11M14 4l1 2 2 1-2 1-1 2-1-2-2-1 2-1zM19 11l.7 1.3L21 13l-1.3.7L19 15l-.7-1.3L17 13l1.3-.7z"/>'),
    film: i('<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 4v16M17 4v16M3 9h4M3 15h4M17 9h4M17 15h4"/>'),
  };
  $$("[data-icon]").forEach((el) => (el.innerHTML = ICON[el.dataset.icon] || ""));

  /* ---------- Тема ---------- */
  const savedTheme = store.get("theme");
  if (savedTheme) root.dataset.theme = savedTheme;
  $$("[data-theme-toggle]").forEach((b) => b.addEventListener("click", () => {
    const next = root.dataset.theme === "dark" ? "light" : "dark";
    root.dataset.theme = next; store.set("theme", next);
  }));

  /* ---------- Шапка и мобильное меню ---------- */
  const header = $(".header");
  const onScroll = () => header && header.classList.toggle("scrolled", scrollY > 10);
  addEventListener("scroll", onScroll, { passive: true }); onScroll();
  const burger = $("[data-burger]");
  const setMenu = (open) => {
    document.body.classList.toggle("menu-open", open);
    burger?.setAttribute("aria-expanded", open);
  };
  burger?.addEventListener("click", () => setMenu(!document.body.classList.contains("menu-open")));
  $$(".mmenu a").forEach((a) => a.addEventListener("click", () => setMenu(false)));
  addEventListener("keydown", (e) => e.key === "Escape" && setMenu(false));

  /* ---------- Контакты ---------- */
  const C = S.contacts;
  const wa = (text) => `https://wa.me/${C.whatsapp}?text=${encodeURIComponent(text)}`;

  /* ---------- Проекты ---------- */
  const catName = (c) => L(S.categories[c]?.name);
  const placeholder = (p) => `<div class="ph">${ICON[p.cat]}<b>${esc(L(p.title))}</b></div>`;
  const mediaInner = (p) => p.image ? `<img src="${esc(p.image)}" alt="${esc(L(p.title))}" loading="lazy" data-fallback>` : placeholder(p);
  const metaHtml = (p) => p.meta ? `<div class="proj-meta">${p.meta.map((x) => `<span>${esc(L(x.k))}: <b>${esc(L(x.v))}</b></span>`).join("")}</div>` : "";

  function handleImgErrors(scope) {
    $$("img[data-fallback]", scope).forEach((im) => im.addEventListener("error", () => {
      const p = S.projects[+im.closest("[data-idx]")?.dataset.idx];
      im.outerHTML = p ? placeholder(p) : "";
    }, { once: true }));
  }

  const projCard = (p, idx) => {
    const title = esc(L(p.title));
    const media = p.link
      ? `<a class="media" href="${esc(p.link)}" target="_blank" rel="noopener" data-cursor="open" aria-label="${title}">${mediaInner(p)}<span class="media-go">${ICON.external}</span></a>`
      : `<button class="media" type="button" data-open="${idx}" data-cursor="view" aria-label="${title}">${mediaInner(p)}${p.video ? `<span class="play"><span>${ICON.play}</span></span>` : `<span class="media-go">${ICON.arrow}</span>`}</button>`;
    const link = p.link ? `<a class="link-arrow" href="${esc(p.link)}" target="_blank" rel="noopener">${tr("ui.openSite")} ${ICON.external}</a>` : "";
    return `<article class="proj proj--${p.cat}" data-idx="${idx}">
      ${media}
      <div class="proj-info">
        <div class="chips"><span class="chip chip--${p.cat}">${esc(catName(p.cat))}</span><span class="chip">${esc(L(p.status))}</span></div>
        <h3>${title}</h3>
        <p>${esc(L(p.desc))}</p>
        ${metaHtml(p)}${link}
      </div>
    </article>`;
  };

  const reelCard = (p, idx) => `<article class="reel reel--${p.cat}" data-idx="${idx}">
      <button class="media" type="button" data-open="${idx}" data-cursor="view" aria-label="${esc(L(p.title))}">
        ${mediaInner(p)}
        <span class="chip media-badge">${esc(L(p.status))}</span>
        <span class="play"><span>${ICON.play}</span></span>
      </button>
      <h3>${esc(L(p.title))}</h3>
      <p>${esc(L(p.desc))}</p>
    </article>`;

  function renderProjects(el, animate) {
    const cat = el.dataset.current || el.dataset.projects;
    const reels = el.dataset.layout === "reels";
    const list = S.projects.map((p, idx) => ({ p, idx })).filter(({ p }) => cat === "all" || p.cat === cat);
    el.className = reels ? "reels" : "projects";
    el.innerHTML = list.length
      ? list.map(({ p, idx }) => (reels ? reelCard(p, idx) : projCard(p, idx))).join("")
      : `<p class="sec-note">${tr("ui.empty")}</p>`;
    handleImgErrors(el);
    if (animate && hasGsap()) gsap.fromTo(el.children, { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: .8, stagger: .06, ease: "expo.out" });
  }

  /* Фильтры работают и для сетки, и для орбиты */
  function renderFilters(el, onChange) {
    const box = el.closest("section")?.querySelector("[data-filters]");
    if (!box) return;
    const current = el.dataset.current || "all";
    const count = (c) => S.projects.filter((p) => c === "all" || p.cat === c).length;
    const dot = { ai: "var(--blue)", web: "var(--ink)", mobile: "var(--yellow)" };
    const opts = [["all", tr("ui.all")], ...Object.keys(S.categories).filter((k) => count(k)).map((k) => [k, catName(k)])];
    box.innerHTML = opts.map(([k, n]) => `<button type="button" class="${k === current ? "active" : ""}" data-f="${k}">${dot[k] ? `<i style="background:${dot[k]}"></i>` : ""}${esc(n)}<sup>${count(k)}</sup></button>`).join("");
    if (box.dataset.bound) return;
    box.dataset.bound = 1;
    box.addEventListener("click", (e) => {
      const b = e.target.closest("button"); if (!b) return;
      $$("button", box).forEach((x) => x.classList.toggle("active", x === b));
      el.dataset.current = b.dataset.f;
      onChange();
      if (window.ScrollTrigger) ScrollTrigger.refresh();
    });
  }

  /* ---------- Орбита проектов ---------- */
  class Orbit {
    constructor(el) {
      this.el = el;
      this.info = $(".orbit-info", el);
      this.countEl = $("[data-orbit-count]", el);
      this.items = [];
      this.t = 0; this.speed = 1; this.target = 1;
      this.active = null; this.visible = true; this.last = performance.now();
      this.touch = matchMedia("(hover: none)").matches;
      this.resize();
      addEventListener("resize", () => this.resize());
      el.addEventListener("pointermove", (e) => this.move(e));
      el.addEventListener("pointerleave", () => this.later(() => this.deactivate(), 220));
      el.addEventListener("click", (e) => this.click(e), true);
      el.addEventListener("focusin", (e) => { const it = this.find(e.target); if (it) this.activate(it); });
      new IntersectionObserver(([en]) => { this.visible = en.isIntersecting; if (this.visible) this.loop(); }, { rootMargin: "100px" }).observe(el);
      this.build();
    }
    resize() {
      const r = this.el.getBoundingClientRect();
      this.W = r.width; this.H = r.height;
      this.size = this.W < 640 ? 64 : this.W < 1000 ? 86 : 108;
      this.big = this.W < 640 ? 1.8 : 2.1;
      this.R = Math.min(this.W / 2 - this.size * .75, this.W < 640 ? this.H * .62 : this.W * .34);
      this.el.style.setProperty("--bs", this.size + "px");
    }
    build() {
      this.deactivate();
      this.items.forEach((it) => it.el.remove());
      const cat = this.el.dataset.current || this.el.dataset.orbit;
      const list = S.projects.map((p, idx) => ({ p, idx })).filter(({ p }) => cat === "all" || p.cat === cat);
      if (this.countEl) this.countEl.textContent = list.length;
      const n = list.length <= 6 ? 1 : list.length <= 12 ? 2 : 3;
      const RINGS = [
        { r: n === 1 ? .8 : .72, tilt: 1.12, rot: -.2, dir: 1, sp: .00017 },
        { r: 1, tilt: 1.2, rot: .22, dir: -1, sp: .00012 },
        { r: .52, tilt: .98, rot: .06, dir: 1, sp: .00024 },
      ].slice(0, n);
      const buckets = RINGS.map(() => []);
      list.forEach((x, k) => buckets[k % n].push(x));
      this.items = [];
      buckets.forEach((b, ri) => b.forEach(({ p, idx }, j) => {
        const title = esc(L(p.title));
        const el = document.createElement(p.link ? "a" : "button");
        el.className = `orbit-bubble b-${p.cat}`;
        el.dataset.idx = idx;
        el.setAttribute("aria-label", L(p.title));
        if (p.link) { el.href = p.link; el.target = "_blank"; el.rel = "noopener"; el.dataset.cursor = "open"; }
        else { el.type = "button"; el.dataset.open = idx; el.dataset.cursor = "view"; }
        el.innerHTML = p.image ? `<img src="${esc(p.image)}" alt="${title}" loading="lazy">` : placeholder(p);
        const img = $("img", el);
        img?.addEventListener("error", () => (img.outerHTML = placeholder(p)), { once: true });
        this.el.appendChild(el);
        this.items.push({ el, p, idx, ring: RINGS[ri], phase: (j / b.length) * Math.PI * 2 + ri * .8, sc: 0, x: 0, y: 0 });
      }));
      this.frame();
      this.loop();
    }
    loop() {
      if (this.raf || !this.visible) return;
      const tick = (now) => {
        this.raf = null;
        if (!this.visible) return;
        const dt = Math.min(48, now - this.last); this.last = now;
        this.speed += (this.target - this.speed) * .08;
        if (!reduce) this.t += dt * this.speed;
        this.frame();
        this.raf = requestAnimationFrame(tick);
      };
      this.last = performance.now();
      this.raf = requestAnimationFrame(tick);
    }
    frame() {
      const cx = this.W / 2, cy = this.H / 2 - 10, half = this.size / 2;
      this.items.forEach((it) => {
        const g = it.ring, R = g.r * this.R;
        const th = it.phase + this.t * g.sp * g.dir;
        const x = R * Math.cos(th), y0 = R * Math.sin(th);
        const y = y0 * Math.cos(g.tilt), z = y0 * Math.sin(g.tilt);
        const xr = x * Math.cos(g.rot) - y * Math.sin(g.rot);
        const yr = x * Math.sin(g.rot) + y * Math.cos(g.rot);
        const depth = R ? z / R : 0;                        // -1 (сзади) … 1 (спереди)
        const on = it === this.active;
        const base = .6 + .4 * (depth + 1) / 2;
        it.sc += ((on ? this.big : base) - it.sc) * .14;
        it.x = cx + xr; it.y = cy + yr;
        it.el.style.transform = `translate3d(${(it.x - half).toFixed(1)}px, ${(it.y - half).toFixed(1)}px, 0) scale(${it.sc.toFixed(3)})`;
        it.el.style.zIndex = on ? 50 : depth > 0 ? 20 + Math.round(depth * 20) : 1 + Math.round((depth + 1) * 4);
        it.el.style.opacity = on ? 1 : (.5 + .5 * (depth + 1) / 2).toFixed(2);
      });
      if (this.active) this.place();
    }
    find(target) { const b = target.closest?.(".orbit-bubble"); return b && this.items.find((it) => it.el === b); }
    later(fn, ms) { clearTimeout(this.tm); this.tm = setTimeout(fn, ms); }
    move(e) {
      if (this.touch || e.pointerType === "touch") return;
      if (this.info.contains(e.target)) { clearTimeout(this.tm); return; }
      const r = this.el.getBoundingClientRect();
      const px = e.clientX - r.left, py = e.clientY - r.top;
      let best = null, bd = Infinity;
      this.items.forEach((it) => {
        const d = Math.hypot(px - it.x, py - it.y);
        const reach = (this.size * it.sc) / 2 + (it === this.active ? 30 : 22);
        if (d < reach && d < bd) { best = it; bd = d; }
      });
      if (best) { clearTimeout(this.tm); if (best !== this.active) this.activate(best); }
      else if (this.active) this.later(() => this.deactivate(), 260);
    }
    click(e) {
      const it = this.find(e.target);
      if (!it) { if (!this.info.contains(e.target)) this.deactivate(); return; }
      // на телефоне первый тап — показать проект, второй — открыть
      if (this.touch && this.active !== it) { e.preventDefault(); e.stopPropagation(); this.activate(it); }
    }
    activate(it) {
      this.active?.el.classList.remove("on");
      this.active = it;
      it.el.classList.add("on");
      this.el.classList.add("dim");
      this.target = 0;
      const p = it.p;
      const action = p.link
        ? `<a class="btn btn--dark" href="${esc(p.link)}" target="_blank" rel="noopener">${tr("ui.openSite")}<span class="arr">${ICON.external}</span></a>`
        : `<button class="btn btn--blue" type="button" data-open="${it.idx}">${tr("ui.watch")}<span class="arr">${ICON.play}</span></button>`;
      this.info.innerHTML = `
        <div class="chips"><span class="chip chip--${p.cat}">${esc(catName(p.cat))}</span><span class="chip">${esc(L(p.status))}</span></div>
        <h3>${esc(L(p.title))}</h3>
        <p>${esc(L(p.desc))}</p>
        ${metaHtml(p)}${action}`;
      this.info.classList.add("show");
      this.place();
    }
    deactivate() {
      if (!this.active) return;
      this.active.el.classList.remove("on");
      this.active = null;
      this.el.classList.remove("dim");
      this.target = 1;
      this.info.classList.remove("show");
    }
    place() {
      if (this.W < 640) return;                           // на телефоне карточка снизу
      const it = this.active, s = (this.size * it.sc) / 2;
      const w = this.info.offsetWidth, h = this.info.offsetHeight;
      const left = it.x < this.W / 2 ? it.x + s + 24 : it.x - s - 24 - w;
      this.info.style.left = clamp(left, 12, this.W - w - 12) + "px";
      this.info.style.top = clamp(it.y - h / 2, 12, this.H - h - 12) + "px";
    }
  }

  /* ---------- Команда ---------- */
  const tagName = (tg) => (S.categories[tg] ? catName(tg) : tr("tag." + tg));
  function renderTeam() {
    $$("[data-team]").forEach((el) => {
      el.innerHTML = S.team.map((m, k) => {
        const name = L(m.name);
        const words = name.split(" ");
        const first = (words[1] || words[0]).toUpperCase();
        const initials = words.map((w) => w[0]).join("").slice(0, 2);
        const photo = m.photo ? `<img src="${esc(m.photo)}" alt="${esc(name)}" loading="lazy">` : `<div class="avatar-ph">${esc(initials)}</div>`;
        const ig = !!m.instagram;
        const ring = `${first} • MAZZERU • FOUNDER • `.repeat(2);
        const chip = m.tag === "mobile" ? "mobile" : m.tag === "web" ? "web" : "ai";
        return `<article class="founder" role="button" tabindex="0" data-member="${k}" data-cursor="profile" aria-haspopup="dialog" aria-label="${esc(name)} — ${esc(L(m.role))}">
          <div class="f-ava">
            <svg class="f-ring" viewBox="0 0 200 200" aria-hidden="true"><defs><path id="fr${k}" d="M100,100 m-88,0 a88,88 0 1,1 176,0 a88,88 0 1,1 -176,0"/></defs><text><textPath href="#fr${k}" textLength="548" lengthAdjust="spacing">${esc(ring)}</textPath></text></svg>
            <div class="f-photo">${photo}</div>
            ${ig ? `<span class="f-badge">${ICON.instagram}</span>` : ""}
          </div>
          <span class="chip chip--${chip}">${esc(tagName(m.tag))}</span>
          <b>${esc(words.slice(0, 2).join(" "))}${words[2] ? `<small>${esc(words.slice(2).join(" "))}</small>` : ""}</b>
          <span class="f-role">${esc(L(m.role))}</span>
          ${ig ? `<span class="f-ig">${ICON.instagram}@${esc(m.instagram)}</span>` : ""}
        </article>`;
      }).join("");
    });
    if (fine && !reduce) $$(".founder").forEach((el) => {
      el.addEventListener("mousemove", (e) => {
        const r = el.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width - .5, py = (e.clientY - r.top) / r.height - .5;
        el.style.transform = `perspective(900px) rotateX(${-py * 8}deg) rotateY(${px * 10}deg) translateY(-6px)`;
      });
      el.addEventListener("mouseleave", () => (el.style.transform = ""));
    });
  }

  /* ---------- Пакеты ---------- */
  function renderPackages() {
    $$("[data-packages]").forEach((el) => {
      el.innerHTML = (S.packages[el.dataset.packages] || []).map((k) => `
        <div class="pkg ${k.hot ? "hot" : ""}">
          <span class="label">${k.hot ? tr("ui.popular") : tr("ui.package")}</span>
          <h3>${esc(L(k.name))}</h3>
          <div class="price">${esc(L(k.price))}<small>${esc(L(k.note))}</small></div>
          <ul>${k.items.map((x) => `<li>${esc(L(x))}</li>`).join("")}</ul>
          <a class="btn ${k.hot ? "" : "btn--dark"}" href="${wa(tr("ui.waPackage").replace("{name}", L(k.name)))}" target="_blank" rel="noopener">${tr("ui.choose")}<span class="arr">${ICON.arrow}</span></a>
        </div>`).join("");
    });
  }

  /* ---------- FAQ ---------- */
  function renderFaq() {
    $$("[data-faq]").forEach((el) => {
      el.innerHTML = (S.faq[el.dataset.faq] || []).map((f) => `<details><summary>${esc(L(f.q))}<i>${ICON.plus}</i></summary><p>${esc(L(f.a))}</p></details>`).join("");
      if (el.dataset.bound) return;
      el.dataset.bound = 1;
      el.addEventListener("toggle", (e) => {
        if (e.target.open) $$("details", el).forEach((d) => d !== e.target && (d.open = false));
      }, true);
    });
  }

  /* ---------- Контакты / подвал ---------- */
  function renderContacts() {
    const item = (href, icon, label, val) => `<a class="contact-item" href="${href}" ${href.startsWith("http") ? 'target="_blank" rel="noopener"' : ""}>${ICON[icon]}<div><b>${label}</b><span>${esc(val)}</span></div></a>`;
    const pages = [["index.html", "nav.home"], ["ai-content.html", "nav.ai"], ["websites.html", "nav.web"], ["mobilography.html", "nav.mobile"]];
    $$("[data-contacts]").forEach((el) => {
      el.innerHTML = `
        <span class="label">${tr("ui.contactsTag")}</span>
        <h2>${tr("ui.contactsH2")}</h2>
        <p>${tr("ui.contactsP")}</p>
        <div class="contact-grid">
          ${item(wa(tr("ui.waHello")), "whatsapp", "WhatsApp", C.phone)}
          ${item(`https://t.me/${C.telegram}`, "telegram", "Telegram", "@" + C.telegram)}
          ${item(`https://instagram.com/${C.instagram}`, "instagram", "Instagram", "@" + C.instagram)}
          ${item(`mailto:${C.email}`, "mail", "Email", C.email)}
        </div>
        <div class="footer-nav">
          <nav>${pages.map(([h, k]) => `<a href="${h}">${tr(k)}</a>`).join("")}</nav>
          <span class="loc">${ICON.pin}${esc(L(C.city))}</span>
          <span>© ${new Date().getFullYear()} mazzeru</span>
        </div>
        <div class="big-word" aria-hidden="true">mazzeru</div>`;
    });
  }

  /* ---------- Бегущие ленты ---------- */
  function renderMarquee() {
    $$("[data-marquee]").forEach((el) => {
      const row = tr(el.dataset.marquee).split("|").map((w) => `<span>${esc(w)}</span>`).join("");
      el.innerHTML = `<div class="band-track">${row}${row}${row}${row}</div>`;
    });
  }

  /* ---------- Заголовок по строкам ---------- */
  function splitLines(h) {
    h.innerHTML = h.innerHTML.split(/<br\s*\/?>/i).map((part) => `<span class="line"><span>${part.trim()}</span></span>`).join("");
  }

  /* Заголовок hero: максимальный размер, при котором самое длинное слово помещается */
  function fitHeadline() {
    $$(".hero h1").forEach((h) => {
      const box = h.parentElement.getBoundingClientRect().width;
      if (!box) return;
      h.style.fontSize = "100px";
      const probe = document.createElement("span");
      probe.style.cssText = "position:absolute;white-space:nowrap;visibility:hidden;left:0;top:0";
      h.appendChild(probe);
      let max = 0;
      $$(".line > span", h).forEach((s) => {
        const txt = s.textContent;
        const parts = txt.includes(" ") ? [txt] : txt.split(/\s+/);
        parts.forEach((w) => { probe.textContent = w; max = Math.max(max, probe.getBoundingClientRect().width / 100); });
      });
      probe.remove();
      h.style.fontSize = max ? clamp((box / max) * 0.96, 38, 150).toFixed(1) + "px" : "";
    });
  }
  addEventListener("resize", () => { clearTimeout(fitHeadline.t); fitHeadline.t = setTimeout(fitHeadline, 120); });
  document.fonts?.ready.then(fitHeadline);

  /* ---------- Статичные тексты ---------- */
  function applyStatic() {
    root.lang = lang === "kz" ? "kk" : lang;
    $$("[data-i18n]").forEach((el) => { if (DICT[el.dataset.i18n]) el.innerHTML = tr(el.dataset.i18n); });
    $$("[data-lines]").forEach(splitLines);
    fitHeadline();
    $$("[data-i18n-aria]").forEach((el) => el.setAttribute("aria-label", tr(el.dataset.i18nAria)));
    document.title = tr(`meta.${page}.title`);
    $('meta[name="description"]')?.setAttribute("content", tr(`meta.${page}.desc`));
    $$("[data-wa]").forEach((a) => { a.href = wa(tr("ui.waHello")); a.target = "_blank"; a.rel = "noopener"; });
    $$("[data-lang]").forEach((b) => {
      b.classList.toggle("active", b.dataset.lang === lang);
      b.setAttribute("aria-pressed", b.dataset.lang === lang);
    });
    $$('a[href*=".html"]').forEach((a) => {
      const [base, hash] = a.getAttribute("href").split("#");
      const clean = base.split("?")[0];
      a.setAttribute("href", (lang === "ru" ? clean : `${clean}?lang=${lang}`) + (hash ? "#" + hash : ""));
    });
  }

  const orbits = [];
  function renderAll(animate) {
    applyStatic();
    $$("[data-projects]").forEach((el) => { renderProjects(el, animate); renderFilters(el, () => renderProjects(el, true)); });
    $$("[data-orbit]").forEach((el) => {
      if (!el._orbit) { el._orbit = new Orbit(el); orbits.push(el._orbit); } else el._orbit.build();
      renderFilters(el, () => el._orbit.build());
    });
    renderTeam(); renderPackages(); renderFaq(); renderContacts(); renderMarquee();
    heroConsole();
  }

  /* ---------- «Студийная консоль» в hero ---------- */
  let consoleRun = 0;
  function heroConsole() {
    const typeEl = $("[data-type]");
    if (!typeEl) return;
    const run = ++consoleRun;
    const bar = $("[data-bar]"), pct = $("[data-pct]"), frames = $$(".vp-frames i");
    const text = tr(typeEl.dataset.type);
    if (reduce) { typeEl.textContent = text; if (bar) bar.style.width = "100%"; if (pct) pct.textContent = "100%"; frames.forEach((f) => f.classList.add("on")); return; }
    const wait = (ms) => new Promise((r) => setTimeout(r, ms));
    (async () => {
      while (run === consoleRun) {
        typeEl.textContent = ""; frames.forEach((f) => f.classList.remove("on"));
        if (bar) bar.style.width = "0%"; if (pct) pct.textContent = "0%";
        for (const ch of text) { if (run !== consoleRun) return; typeEl.textContent += ch; await wait(28 + Math.random() * 40); }
        await wait(300);
        for (let v = 0; v <= 100; v += 2) {
          if (run !== consoleRun) return;
          if (bar) bar.style.width = v + "%"; if (pct) pct.textContent = v + "%";
          frames.forEach((f, k) => f.classList.toggle("on", v >= (k + 1) * 25));
          await wait(36);
        }
        await wait(1800);
      }
    })();
  }
  // таймкод, лайки и часы Астаны
  (() => {
    const tc = $("[data-timecode]"), likes = $("[data-likes]"), clock = $("[data-clock]");
    let sec = 0, lk = 1200;
    const fmt = new Intl.DateTimeFormat("ru-RU", { timeZone: "Asia/Almaty", hour: "2-digit", minute: "2-digit" });
    const tick = () => {
      if (tc) { sec = (sec + 1) % 60; tc.textContent = `00:${String(sec).padStart(2, "0")}`; }
      if (likes && Math.random() > .5) { lk += Math.round(Math.random() * 9); likes.textContent = (lk / 1000).toFixed(1) + "K"; }
      if (clock) { try { clock.textContent = fmt.format(new Date()); } catch { clock.textContent = ""; } }
    };
    tick();
    if (!reduce) setInterval(tick, 1000);
  })();

  renderAll(false);

  $$("[data-lang]").forEach((b) => b.addEventListener("click", () => {
    if (b.dataset.lang === lang) return;
    lang = b.dataset.lang;
    store.set("lang", lang);
    const url = new URL(location.href);
    if (lang === "ru") url.searchParams.delete("lang"); else url.searchParams.set("lang", lang);
    history.replaceState(null, "", url);
    renderAll(true);
    if (hasGsap()) gsap.from(".hero h1 .line > span", { yPercent: 110, duration: .8, stagger: .06, ease: "expo.out" });
    if (window.ScrollTrigger) ScrollTrigger.refresh();
  }));

  /* ---------- Лайтбокс ---------- */
  const lb = document.createElement("div");
  lb.className = "lightbox";
  lb.innerHTML = `<button class="icon-btn" type="button">${ICON.close}</button><div class="lb-body"></div><div class="lightbox-cap label"></div>`;
  document.body.appendChild(lb);
  const closeLb = () => { lb.classList.remove("open", "lightbox--member"); $(".lb-body", lb).innerHTML = ""; document.body.style.overflow = ""; };
  lb.addEventListener("click", (e) => { if (e.target === lb || e.target.closest(".icon-btn")) closeLb(); });
  addEventListener("keydown", (e) => e.key === "Escape" && closeLb());
  /* Профиль участника команды: сначала карточка, Instagram — отдельной кнопкой */
  const openMember = (k) => {
    const m = S.team[k]; if (!m) return;
    const name = L(m.name), words = name.split(" ");
    const chip = m.tag === "mobile" ? "mobile" : m.tag === "web" ? "web" : "ai";
    const skills = (m.skills || []).map((x) => `<li>${esc(L(x))}</li>`).join("");
    $(".icon-btn", lb).setAttribute("aria-label", tr("ui.close"));
    $(".lightbox-cap", lb).textContent = "";
    $(".lb-body", lb).innerHTML = `<div class="member" role="dialog" aria-modal="true" aria-label="${esc(name)}">
      <div class="member-photo">${m.photo ? `<img src="${esc(m.photo)}" alt="${esc(name)}">` : ""}</div>
      <div class="member-info">
        <span class="chip chip--${chip}">${esc(tagName(m.tag))}</span>
        <h3>${esc(words.slice(0, 2).join(" "))}${words[2] ? `<small>${esc(words.slice(2).join(" "))}</small>` : ""}</h3>
        <p class="member-role">${esc(L(m.role))}</p>
        ${m.bio ? `<p class="member-bio">${esc(L(m.bio))}</p>` : ""}
        ${skills ? `<ul class="member-skills">${skills}</ul>` : ""}
        <div class="member-actions">
          ${m.instagram ? `<a class="btn btn--sm" href="https://instagram.com/${encodeURIComponent(m.instagram)}" target="_blank" rel="noopener"><span>${ICON.instagram}@${esc(m.instagram)}</span><span class="arr">${ICON.external}</span></a>` : ""}
          <a class="link-arrow" href="${wa(tr("ui.waHello"))}" target="_blank" rel="noopener"><span>${esc(tr("team.write"))}</span>${ICON.arrow}</a>
        </div>
      </div>
    </div>`;
    lb.classList.add("open", "lightbox--member"); document.body.style.overflow = "hidden";
    $(".icon-btn", lb).focus();
  };
  document.addEventListener("click", (e) => {
    const f = e.target.closest("[data-member]"); if (f) openMember(+f.dataset.member);
  });
  document.addEventListener("keydown", (e) => {
    const f = e.target.closest?.("[data-member]");
    if (f && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); openMember(+f.dataset.member); }
  });
  document.addEventListener("click", (e) => {
    const b = e.target.closest("[data-open]"); if (!b) return;
    const v = b.dataset.open, p = S.projects[+v] || S.projects.find((x) => x.id === v); if (!p) return;
    const title = L(p.title);
    $(".icon-btn", lb).setAttribute("aria-label", tr("ui.close"));
    $(".lb-body", lb).innerHTML = p.video
      ? `<video src="${esc(p.video)}" controls autoplay playsinline poster="${esc(p.image || "")}"></video>`
      : p.image ? `<img src="${esc(p.image.replace("w=900", "w=1600"))}" alt="${esc(title)}">` : "";
    $(".lightbox-cap", lb).textContent = p.video ? title : `${title} — ${tr("ui.videoSoon")}`;
    lb.classList.add("open"); document.body.style.overflow = "hidden";
  });

  /* ---------- Счётчики ---------- */
  const ioC = new IntersectionObserver((ents) => ents.forEach((en) => {
    if (!en.isIntersecting) return; ioC.unobserve(en.target);
    const el = en.target, cat = el.dataset.countCat;
    const end = cat ? S.projects.filter((p) => cat === "all" || p.cat === cat).length : +el.dataset.count, suf = el.dataset.suffix || "";
    if (reduce) { el.textContent = end + suf; return; }
    const t0 = performance.now(), dur = 1600;
    const step = (tm) => { const k = Math.min(1, (tm - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - k, 4))) + suf; if (k < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  }), { threshold: .5 });
  $$("[data-count]").forEach((c) => ioC.observe(c));

  /* ---------- Прогресс прокрутки ---------- */
  const bar = $(".progress");
  if (bar) addEventListener("scroll", () => {
    const h = document.documentElement.scrollHeight - innerHeight;
    bar.style.transform = `scaleX(${h > 0 ? scrollY / h : 0})`;
  }, { passive: true });

  /* ---------- Курсор ---------- */
  const cur = $(".cursor");
  if (cur && fine && !reduce) {
    let x = -100, y = -100, cx = x, cy = y;
    addEventListener("mousemove", (e) => { x = e.clientX; y = e.clientY; });
    const loop = () => { cx += (x - cx) * .22; cy += (y - cy) * .22; cur.style.transform = `translate(${cx}px,${cy}px) translate(-50%,-50%)`; requestAnimationFrame(loop); };
    loop();
    document.addEventListener("mouseover", (e) => {
      const tg = e.target.closest("a, button, summary, [data-member]");
      const mode = tg?.dataset.cursor;
      cur.classList.toggle("hover", !!tg && !mode);
      cur.classList.toggle("view", !!mode);
      if (mode) cur.dataset.label = tr(mode === "open" ? "ui.open" : mode === "profile" ? "ui.profile" : "ui.watch");
    });
  } else cur?.remove();

  /* ---------- Магнитные кнопки ---------- */
  if (fine && !reduce) document.addEventListener("mousemove", (e) => {
    $$("[data-magnetic]").forEach((b) => {
      const r = b.getBoundingClientRect();
      const dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2);
      b.style.transform = Math.hypot(dx, dy) < 100 ? `translate(${dx * .2}px, ${dy * .3}px)` : "";
    });
  });

  /* ---------- Параллакс hero ---------- */
  const hv = $("[data-parallax]");
  if (hv && fine && !reduce) {
    const layers = [[".hero-circle", -8], [".hero-sun", 16], [".vis-prompt", 26], [".vis-phone", -22], [".vis-browser", 18]];
    let raf = 0, px = 0, py = 0;
    addEventListener("mousemove", (e) => {
      px = e.clientX / innerWidth - .5; py = e.clientY / innerHeight - .5;
      if (raf) return;
      raf = requestAnimationFrame(() => {
        raf = 0;
        layers.forEach(([s, k]) => { const el = $(s, hv); if (el) el.style.translate = `${(px * k).toFixed(1)}px ${(py * k).toFixed(1)}px`; });
      });
    });
  }

  /* ---------- Переход между страницами (CSS, без зависаний) ---------- */
  const wipe = $(".wipe");
  // шторка новой страницы уезжает на CSS сама; тут только убираем флаг
  if (root.classList.contains("wiping")) {
    store.set("wipe", "0", sessionStorage);
    setTimeout(() => root.classList.remove("wiping"), 800);
  }
  const prefetched = new Set();
  const isPage = (a) => a && a.target !== "_blank" && /\.html(\?|#|$)/.test(a.getAttribute("href") || "") && !a.getAttribute("href").startsWith("#");
  const prefetch = (href) => {
    const url = href.split("#")[0];
    if (prefetched.has(url) || url === location.href.split("#")[0]) return;
    prefetched.add(url);
    const l = document.createElement("link"); l.rel = "prefetch"; l.href = url; document.head.appendChild(l);
  };
  const onIntent = (e) => { const a = e.target.closest?.("a[href]"); if (isPage(a)) prefetch(a.href); };
  ["pointerover", "touchstart", "focusin"].forEach((ev) => document.addEventListener(ev, onIntent, { passive: true }));
  // в простое заранее подгружаем все страницы меню (они лёгкие)
  const idle = window.requestIdleCallback || ((f) => setTimeout(f, 1500));
  addEventListener("load", () => idle(() => $$(".nav a, .mmenu a").forEach((a) => isPage(a) && prefetch(a.href))));
  document.addEventListener("click", (e) => {
    const a = e.target.closest("a[href]");
    if (!isPage(a) || !wipe || reduce || e.metaKey || e.ctrlKey || e.shiftKey || e.defaultPrevented) return;
    const url = new URL(a.href);
    if (url.pathname === location.pathname && url.hash) return;   // якорь на этой же странице
    e.preventDefault();
    store.set("wipe", "1", sessionStorage);
    wipe.classList.remove("out");
    wipe.classList.add("in");
    setTimeout(() => (location.href = a.href), 320);
  });
  addEventListener("pageshow", (e) => { if (e.persisted && wipe) { wipe.classList.remove("in"); root.classList.remove("wiping"); } });

  /* ---------- Анимации страницы ---------- */
  function pageIn() {
    if (!hasGsap()) return;
    gsap.registerPlugin(ScrollTrigger);
    const tl = gsap.timeline({ defaults: { ease: "expo.out" } });
    tl.from(".header .wrap > *", { y: -24, opacity: 0, duration: .7, stagger: .06 }, 0)
      .from(".hero h1 .line > span", { yPercent: 115, duration: 1, stagger: .08 }, .05)
      .from(".hero-eyebrow, .hero-tag, .hero-lead, .hero-actions", { y: 24, opacity: 0, duration: .8, stagger: .06 }, .25)
      .from(".hero-circle", { scale: .5, rotate: -40, opacity: 0, duration: 1.1 }, .1)
      .from(".hero-sun", { scale: 0, duration: 1 }, .3)
      .fromTo(".vis", { "--vs": .5, opacity: 0 }, { "--vs": 1, opacity: 1, duration: .9, stagger: .12, ease: "back.out(1.6)" }, .45)
      .from(".bands .band", { xPercent: (k) => (k ? 30 : -30), opacity: 0, duration: 1, stagger: .1 }, .4);

    const sel = "[data-reveal], .proj, .reel, .pkg, .faq details, .orbit";
    $$(sel).forEach((el) => { if (el.getBoundingClientRect().top > innerHeight * .95) gsap.set(el, { opacity: 0 }); });
    ScrollTrigger.batch(sel, {
      start: "top 90%", once: true,
      onEnter: (els) => gsap.fromTo(els, { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: .9, stagger: .07, ease: "expo.out", overwrite: true }),
    });
    // основатели переворачиваются как карты
    $$(".founder").forEach((el) => { if (el.getBoundingClientRect().top > innerHeight * .92) gsap.set(el, { opacity: 0 }); });
    ScrollTrigger.batch(".founder", {
      start: "top 92%", once: true,
      onEnter: (els) => gsap.fromTo(els, { rotateY: -80, opacity: 0, transformOrigin: "left center" }, { rotateY: 0, opacity: 1, duration: 1.1, stagger: .12, ease: "expo.out", clearProps: "transform" }),
    });
    $$(".dir-orb").forEach((o) => gsap.fromTo(o, { yPercent: 20 }, { yPercent: -20, ease: "none", scrollTrigger: { trigger: o.parentElement, scrub: true } }));
    gsap.to(".big-word", { xPercent: -6, ease: "none", scrollTrigger: { trigger: ".contact", scrub: true } });
  }

  /* ---------- Интро: быстрое, только transform/opacity ---------- */
  const intro = $(".intro");
  function runIntro() {
    const mark = $(".intro-mark", intro), letters = $$(".intro-word span", intro), slash = $(".intro-slash", intro);
    document.body.style.overflow = "hidden";
    let started = false;
    const go = () => { if (started) return; started = true; pageIn(); };
    const tl = gsap.timeline({
      defaults: { ease: "expo.out" },
      onComplete: () => { store.set("intro", "1", sessionStorage); document.body.style.overflow = ""; intro.remove(); },
    });
    // знак: круг вырастает из точки, две Z влетают навстречу друг другу и «защёлкиваются»
    const bg = $(".mk-bg", mark), z1 = $(".mk-z1", mark), z2 = $(".mk-z2", mark);
    tl.fromTo(bg, { scale: 0 }, { scale: 1, duration: .5, ease: "back.out(1.8)", transformOrigin: "50% 50%" }, 0)
      .fromTo(z1, { x: -760, skewX: -35, opacity: 0 }, { x: 0, skewX: 0, opacity: 1, duration: .48 }, .1)
      .fromTo(z2, { x: 760, skewX: -35, opacity: 0 }, { x: 0, skewX: 0, opacity: 1, duration: .48 }, .14)
      .fromTo(mark, { scale: 1.14 }, { scale: 1, duration: .45, ease: "elastic.out(1, .45)" }, .5)
      .fromTo(letters, { yPercent: 110 }, { yPercent: 0, duration: .55, stagger: .035 }, .22)
      .fromTo(slash, { scaleX: 0 }, { scaleX: 1, duration: .38, ease: "expo.inOut" }, .08)
      .to(slash, { scaleX: 0, transformOrigin: "right center", duration: .32, ease: "expo.inOut" }, .5)
      .fromTo(".intro-tag", { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: .5 }, .3)
      .to(".intro-stage", { y: -40, opacity: 0, duration: .35, ease: "power2.in" }, 1.0)
      .to(".intro-tag", { opacity: 0, duration: .2 }, 1.0)
      .to(intro, { yPercent: -100, duration: .65, ease: "expo.inOut", onStart: go }, 1.1);
    intro.addEventListener("click", () => tl.progress(.95), { once: true });
  }

  function boot() {
    // время анимаций = реальное время: на слабых устройствах интро не растягивается
    if (window.gsap) gsap.ticker.lagSmoothing(0);
    if (!intro || root.classList.contains("intro-seen") || !hasGsap()) {
      intro?.remove();
      pageIn();
      return;
    }
    runIntro();
  }
  // старт сразу после загрузки шрифтов (но не дольше 600 мс), не дожидаясь картинок
  const fontsReady = document.fonts?.ready || Promise.resolve();
  Promise.race([fontsReady, new Promise((r) => setTimeout(r, 600))]).then(boot);
})();
