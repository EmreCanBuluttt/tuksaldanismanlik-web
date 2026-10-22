/* =========================================================================
   TUKSAL Danışmanlık — site behaviour (vanilla JS, no dependencies)
   header, mobile nav, dropdowns, hero slider, reveal, lightbox,
   event calendar, contact form.
   ========================================================================= */
(function () {
  "use strict";
  var CFG = window.TUKSAL_CONFIG || {};
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- header shadow on scroll ---------- */
  var header = $(".site-header");
  function onScroll() { if (header) header.classList.toggle("is-scrolled", window.scrollY > 10); }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- mobile nav ---------- */
  var burger = $(".nav-burger");
  var nav = $("#site-nav");
  if (burger && nav) {
    burger.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      burger.setAttribute("aria-expanded", String(open));
      document.body.classList.toggle("nav-open", open);
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 1120 && nav.classList.contains("is-open")) {
        nav.classList.remove("is-open"); burger.setAttribute("aria-expanded", "false"); document.body.classList.remove("nav-open");
      }
    });
  }

  /* ---------- dropdowns (click for touch/mobile, hover via CSS on desktop) ---------- */
  $$(".nav .nav-toggle").forEach(function (btn) {
    var li = btn.closest("li");
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      var open = li.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", String(open));
    });
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".nav li")) {
      $$(".nav li.is-open").forEach(function (li) { li.classList.remove("is-open"); var b = $(".nav-toggle", li); if (b) b.setAttribute("aria-expanded", "false"); });
    }
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      $$(".nav li.is-open").forEach(function (li) { li.classList.remove("is-open"); });
      if (nav && nav.classList.contains("is-open")) { nav.classList.remove("is-open"); burger.setAttribute("aria-expanded", "false"); document.body.classList.remove("nav-open"); }
    }
  });

  /* ---------- hero slider ---------- */
  var hero = $(".hero");
  if (hero) {
    var slides = $$(".hero-slide", hero);
    var quotes = $$(".hero-slide-quote", hero);
    var quoteBox = $(".hero-quote blockquote p", hero);
    var dotsBox = $(".hero-dots", hero);
    var idx = 0, timer = null, INTERVAL = 6500;
    var dots = slides.map(function (_, i) {
      var b = document.createElement("button");
      b.type = "button"; b.setAttribute("aria-label", "Slayt " + (i + 1));
      b.addEventListener("click", function () { go(i); restart(); });
      if (dotsBox) dotsBox.appendChild(b);
      return b;
    });
    // Swap the quote text with a short class-based fade. Never relies on the
    // transition finishing: a timeout always restores the visible state.
    function setQuote(text, animate) {
      if (!quoteBox) return;
      if (!animate || reduceMotion) { quoteBox.textContent = text; return; }
      var done = false;
      function swap() { if (done) return; done = true; quoteBox.textContent = text; quoteBox.classList.remove("is-fading"); }
      quoteBox.classList.add("is-fading");
      quoteBox.addEventListener("transitionend", swap, { once: true });
      setTimeout(swap, 400);
    }
    function go(n, initial) {
      idx = (n + slides.length) % slides.length;
      slides.forEach(function (s, i) { s.classList.toggle("is-active", i === idx); s.setAttribute("aria-hidden", String(i !== idx)); });
      dots.forEach(function (d, i) { if (i === idx) d.setAttribute("aria-current", "true"); else d.removeAttribute("aria-current"); });
      if (quotes[idx]) setQuote(quotes[idx].textContent.trim(), !initial);
    }
    function restart() { stop(); if (!reduceMotion && slides.length > 1) timer = setInterval(function () { go(idx + 1); }, INTERVAL); }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }
    var prev = $(".hero-prev", hero), next = $(".hero-next", hero);
    if (prev) prev.addEventListener("click", function () { go(idx - 1); restart(); });
    if (next) next.addEventListener("click", function () { go(idx + 1); restart(); });
    hero.addEventListener("mouseenter", stop);
    hero.addEventListener("mouseleave", restart);
    hero.addEventListener("focusin", stop);
    hero.addEventListener("focusout", restart);
    document.addEventListener("visibilitychange", function () { document.hidden ? stop() : restart(); });
    // touch swipe
    var x0 = null;
    hero.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    hero.addEventListener("touchend", function (e) {
      if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 40) { go(dx < 0 ? idx + 1 : idx - 1); restart(); }
    });
    go(0, true); restart();
  }

  /* ---------- reveal on scroll ---------- */
  var revealEls = $$(".reveal");
  if (revealEls.length && "IntersectionObserver" in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-visible"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* ---------- lightbox (references) ---------- */
  var lb = $("#lightbox");
  if (lb) {
    var lbImg = $("img", lb), lbCap = $("figcaption", lb);
    $$("[data-lightbox]").forEach(function (el) {
      el.addEventListener("click", function () {
        var src = el.getAttribute("data-lightbox");
        if (!src) return;
        lbImg.src = src; lbImg.alt = el.getAttribute("data-caption") || "";
        if (lbCap) lbCap.textContent = el.getAttribute("data-caption") || "";
        if (typeof lb.showModal === "function") lb.showModal(); else lb.setAttribute("open", "");
      });
    });
    $$(".lightbox-close", lb).forEach(function (b) { b.addEventListener("click", function () { lb.close(); }); });
    lb.addEventListener("click", function (e) { if (e.target === lb) lb.close(); });
  }

  /* ---------- event calendar ---------- */
  var calRoot = $("#calendar");
  var listRoot = $("#event-list");
  if (calRoot || listRoot) {
    var MONTHS = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"];
    var MONTHS_SHORT = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"];
    var DOW = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"];
    var STATUS = { planned: ["Planlanıyor", "pill--navy"], open: ["Kayıt Açık", "pill--green"], full: ["Kontenjan Dolu", "pill"], done: ["Tamamlandı", "pill"] };
    var events = (window.TUKSAL_EVENTS || []).slice().filter(function (e) { return e && e.date; });
    events.forEach(function (e) { e._d = parseDate(e.date); e._e = e.end ? parseDate(e.end) : e._d; });
    events.sort(function (a, b) { return a._d - b._d; });
    var today = new Date(); today.setHours(0, 0, 0, 0);
    var view = new Date(today.getFullYear(), today.getMonth(), 1);
    var firstUpcoming = events.filter(function (e) { return e._e >= today; })[0];
    if (firstUpcoming) view = new Date(firstUpcoming._d.getFullYear(), firstUpcoming._d.getMonth(), 1);

    function parseDate(s) { var p = s.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
    function sameDay(a, b) { return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate(); }
    function eventsOn(d) { return events.filter(function (e) { return d >= e._d && d <= e._e; }); }
    function pad(n) { return (n < 10 ? "0" : "") + n; }
    function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
    function fmtRange(e) {
      var a = e._d, b = e._e;
      if (sameDay(a, b)) return a.getDate() + " " + MONTHS[a.getMonth()] + " " + a.getFullYear();
      if (a.getMonth() === b.getMonth()) return a.getDate() + "–" + b.getDate() + " " + MONTHS[a.getMonth()] + " " + a.getFullYear();
      return a.getDate() + " " + MONTHS[a.getMonth()] + " – " + b.getDate() + " " + MONTHS[b.getMonth()] + " " + b.getFullYear();
    }

    function renderCalendar() {
      if (!calRoot) return;
      var y = view.getFullYear(), m = view.getMonth();
      var first = new Date(y, m, 1); var startDow = (first.getDay() + 6) % 7; // Monday first
      var days = new Date(y, m + 1, 0).getDate();
      var prevDays = new Date(y, m, 0).getDate();
      var html = '<div class="calendar-head"><button type="button" class="cal-prev" aria-label="Önceki ay"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 6l-6 6 6 6"/></svg></button><h3>' + MONTHS[m] + " " + y + '</h3><button type="button" class="cal-next" aria-label="Sonraki ay"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg></button></div><div class="calendar-grid">';
      DOW.forEach(function (d) { html += '<div class="dow">' + d + "</div>"; });
      var cells = [];
      for (var i = startDow - 1; i >= 0; i--) cells.push({ d: new Date(y, m - 1, prevDays - i), muted: true });
      for (var d = 1; d <= days; d++) cells.push({ d: new Date(y, m, d), muted: false });
      while (cells.length % 7) cells.push({ d: new Date(y, m + 1, cells.length - days - startDow + 1), muted: true });
      cells.forEach(function (c) {
        var ev = eventsOn(c.d);
        var cls = "calendar-day" + (c.muted ? " is-muted" : "") + (sameDay(c.d, today) ? " is-today" : "") + (ev.length ? " has-event" : "");
        var key = c.d.getFullYear() + "-" + pad(c.d.getMonth() + 1) + "-" + pad(c.d.getDate());
        var title = ev.map(function (e) { return e.title; }).join(", ");
        html += '<div class="' + cls + '" data-date="' + key + '"' + (ev.length ? ' role="button" tabindex="0" title="' + esc(title) + '"' : "") + ">" + c.d.getDate() + (ev.length ? '<span class="dot"></span>' : "") + "</div>";
      });
      html += '</div>' + (events.length ? '<div class="calendar-legend"><span><i></i>Etkinlik günü</span></div>' : '');
      calRoot.innerHTML = html;
      $(".cal-prev", calRoot).addEventListener("click", function () { view = new Date(view.getFullYear(), view.getMonth() - 1, 1); renderCalendar(); });
      $(".cal-next", calRoot).addEventListener("click", function () { view = new Date(view.getFullYear(), view.getMonth() + 1, 1); renderCalendar(); });
      $$(".calendar-day.has-event", calRoot).forEach(function (el) {
        function act() {
          var d = parseDate(el.getAttribute("data-date"));
          var ev = eventsOn(d)[0]; if (!ev) return;
          var card = $('[data-event-id="' + ev._id + '"]');
          if (card) { $$(".event.is-highlight").forEach(function (x) { x.classList.remove("is-highlight"); }); card.classList.add("is-highlight"); card.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" }); }
        }
        el.addEventListener("click", act);
        el.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); act(); } });
      });
    }

    function renderList() {
      if (!listRoot) return;
      var showPast = listRoot.getAttribute("data-show-past") === "true";
      var limit = parseInt(listRoot.getAttribute("data-limit") || "0", 10);
      var list = events.filter(function (e) { return showPast || e._e >= today; });
      if (limit > 0) list = list.slice(0, limit);
      if (!list.length) {
        if (listRoot.hasAttribute("data-hide-empty")) { var sec = listRoot.closest("section"); if (sec) sec.hidden = true; return; }
        listRoot.innerHTML = '<div class="event-empty">Şu anda planlanmış bir etkinlik bulunmuyor. Yeni etkinlikler bu sayfada duyurulacaktır.</div>';
        return;
      }
      listRoot.innerHTML = list.map(function (e) {
        var st = STATUS[e.status] || null;
        return '<article class="event" data-event-id="' + e._id + '">' +
          '<div class="event-date"><b>' + e._d.getDate() + "</b><span>" + MONTHS_SHORT[e._d.getMonth()] + "</span></div>" +
          '<div class="event-body"><h3>' + esc(e.title) + "</h3>" + (e.desc ? "<p>" + esc(e.desc) + "</p>" : "") +
          '<div class="meta"><span>' + esc(fmtRange(e)) + "</span>" + (e.type ? "<span>" + esc(e.type) + "</span>" : "") + (e.location ? "<span>" + esc(e.location) + "</span>" : "") +
          (st ? '<span class="pill ' + st[1] + '">' + st[0] + "</span>" : "") +
          (e.url ? '<span><a href="' + esc(e.url) + '">Detay / Kayıt →</a></span>' : "") + "</div></div></article>";
      }).join("");
    }
    events.forEach(function (e, i) { e._id = i; });
    renderCalendar(); renderList();
    var upcoming = events.filter(function (e) { return e._e >= today; }).length;
    $$("[data-needs-events]").forEach(function (s) { s.hidden = !upcoming; });
  }

  /* ---------- contact form (shown only when a channel exists) ---------- */
  var form = $("#contact-form");
  if (form && (CFG.formEndpoint || CFG.email)) form.hidden = false;
  if (form && !form.hidden) {
    var status = $(".form-status", form) || $("#form-status");
    function show(msg, ok) { if (!status) return; status.textContent = msg; status.className = "form-status " + (ok ? "is-ok" : "is-err"); }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var hp = $('[name="website"]', form); if (hp && hp.value) return; // honeypot
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var data = {};
      $$("input, select, textarea", form).forEach(function (f) { if (f.name && f.name !== "website" && f.type !== "checkbox") data[f.name] = f.value.trim(); });
      var btn = $('[type="submit"]', form);
      if (CFG.formEndpoint) {
        if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = "Gönderiliyor…"; }
        fetch(CFG.formEndpoint, { method: "POST", headers: { "Accept": "application/json", "Content-Type": "application/json" }, body: JSON.stringify(data) })
          .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); show("Mesajınız iletildi. En kısa sürede size dönüş yapacağız.", true); form.reset(); })
          .catch(function () { show(CFG.email ? "Mesaj gönderilemedi. Lütfen e-posta ile bize ulaşın: " + CFG.email : "Mesaj gönderilemedi. Lütfen daha sonra tekrar deneyin.", false); })
          .then(function () { if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label; } });
      } else {
        var subject = "[Web] " + (data.konu || "İletişim formu") + " — " + (data.ad || "");
        var body = "Ad Soyad: " + (data.ad || "") + "\nKurum: " + (data.kurum || "") + "\nE-posta: " + (data.eposta || "") + "\nTelefon: " + (data.telefon || "") + "\nKonu: " + (data.konu || "") + "\n\n" + (data.mesaj || "");
        window.location.href = "mailto:" + (CFG.email || "") + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
        show("E-posta uygulamanız açılıyor. Açılmazsa mesajınızı doğrudan " + (CFG.email || "") + " adresine gönderebilirsiniz.", true);
      }
    });
  }

  /* ---------- config-driven contact bits (empty = hidden) ---------- */
  function toggle(el, show) { var li = el.closest("li"); (li || el).hidden = !show; if (show) el.hidden = false; }
  $$("[data-email]").forEach(function (a) {
    if (CFG.email) { a.textContent = CFG.email; a.href = "mailto:" + CFG.email; }
    toggle(a, !!CFG.email);
  });
  $$("[data-phone]").forEach(function (el) {
    if (CFG.phone) { el.textContent = CFG.phone; el.href = "tel:" + CFG.phone.replace(/[^+\d]/g, ""); }
    toggle(el, !!CFG.phone);
  });
  $$("[data-whatsapp]").forEach(function (el) {
    if (CFG.whatsapp) el.href = "https://wa.me/" + CFG.whatsapp;
    toggle(el, !!CFG.whatsapp);
  });
  var hasChannel = !!(CFG.email || CFG.phone || CFG.whatsapp);
  $$("[data-contact-empty]").forEach(function (el) { el.hidden = hasChannel; });
  $$(".contact-list").forEach(function (ul) { ul.hidden = !hasChannel; });
  // elements that only make sense when visitors can actually reach the client (CTA buttons, footer column)
  $$("[data-contact-only], [data-contact-col]").forEach(function (el) { el.hidden = !hasChannel; });

  /* ---------- footer year ---------- */
  $$("[data-year]").forEach(function (el) { el.textContent = String(new Date().getFullYear()); });
})();
