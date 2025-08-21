export const onRequest: PagesFunction = async ({ params, request }) => {
  const id = String(params.id);
  const origin = new URL(request.url).origin;
  const head = async (path: string) => fetch(origin + path, { method: "HEAD" });
  if ((await head(`/rule/${id}.jsonld`)).ok) return Response.redirect(new URL(`/rule/${id}.jsonld`, request.url), 303);
  if ((await head(`/rule/${id}.lrml.xml`)).ok) return Response.redirect(new URL(`/rule/${id}.lrml.xml`, request.url), 303);
  return new Response("Not found", { status: 404 });
};