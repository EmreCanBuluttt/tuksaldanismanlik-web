/* TUKSAL Danışmanlık — event calendar data (edit freely, no build step).
   While the list is empty the site shows "Yaklaşan etkinlik bulunmuyor…".
   Add one object per event, e.g.:
   {
     date: "2026-11-05",            // YYYY-MM-DD (required)
     end: "2026-11-06",             // optional, multi-day events
     title: "Yönetici Geliştirme Programı — Tanıtım Semineri",
     type: "Seminer",               // Seminer | Atölye | Eğitim | Kongre ...
     location: "İzmir",             // or "Online"
     desc: "Kısa açıklama.",
     url: "",                       // optional registration / detail link
     status: "open"                 // planned | open | full | done
   }
*/
window.TUKSAL_EVENTS = [];
