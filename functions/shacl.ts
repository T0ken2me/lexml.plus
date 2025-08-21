export const onRequest: PagesFunction = async ({ request }) => {
  return Response.redirect(new URL("/shacl/0.1/lexml_shapes.ttl", request.url), 303);
};