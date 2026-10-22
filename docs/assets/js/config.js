/* TUKSAL Danışmanlık — site configuration (edit freely, no build needed).
   Anything left empty is hidden on the site.
   email / phone / whatsapp : contact channels (contact page + footer). While all three are empty the contact page
                              shows a "coming soon" notice.
   formEndpoint             : JSON POST endpoint for the contact form (e.g. https://formspree.io/f/xxxx).
                              The form is shown when formEndpoint OR email is set; without an endpoint it opens the
                              visitor's e-mail app (mailto) addressed to `email`.
   The street address was removed at the client's request (18 Oct 2026). */
window.TUKSAL_CONFIG = {
  siteName: "TUKSAL Danışmanlık",
  email: "",          // e.g. "info@tuksaldanismanlik.com" (needs a working mailbox / MX record first)
  phone: "",          // e.g. "+90 232 000 00 00"
  whatsapp: "",       // e.g. "905320000000" (digits only)
  formEndpoint: ""    // e.g. "https://formspree.io/f/xxxxxxxx"
};
