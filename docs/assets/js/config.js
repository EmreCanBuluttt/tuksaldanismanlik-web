/* TUKSAL Danışmanlık — site configuration (edit freely, no build needed).
   Anything left empty is hidden on the site.
   email / phones / whatsapp / address : contact channels (contact page, footer, KVKK page).
                              While email, phones and whatsapp are all empty the contact page shows a "coming soon" notice.
   formEndpoint             : JSON POST endpoint for the contact form (e.g. https://formsubmit.co/ajax/<email> or Formspree).
                              The form is shown when formEndpoint OR email is set; without an endpoint it opens the
                              visitor's e-mail app (mailto) addressed to `email`. */
window.TUKSAL_CONFIG = {
  siteName: "TUKSAL Danışmanlık",
  email: "info@tuksaldanismanlik.com",
  phones: ["+90 532 305 16 93", "+90 533 790 06 70"],
  whatsapp: "905323051693",   // digits only; +90 532 305 16 93 (confirmed 22 Oct 2026)
  address: "4244 Sk. No:1/84 Bornova / İZMİR",
  mapsQuery: "4244 Sokak No:1 Bornova İzmir",
  formEndpoint: ""    // set after the info@ mailbox can receive mail (see README)
};
