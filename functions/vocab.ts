export const onRequest: PagesFunction = async ({ request }) => {
  const accept = request.headers.get("Accept") || "";
  if (/application\/ld\+json/i.test(accept)) {
    return Response.redirect(new URL("/vocab/0.1/vocab.jsonld", request.url), 303);
  }
  if (/text\/turtle/i.test(accept)) {
    return Response.redirect(new URL("/vocab/0.1/vocab.ttl", request.url), 303);
  }
  return Response.redirect(new URL("/vocab/index.html", request.url), 303);
};