/* Serves published reels videos from the ben-reels R2 bucket.

   GET /reels-v2-2026-10-05.mp4  ->  object published/reels-v2-2026-10-05.mp4

   Only objects under published/ are reachable; drafts/ never are. Range
   requests are answered with 206 so a <video> can seek without downloading
   the whole file. Published names carry a date and are never overwritten,
   so browsers may cache them for a year.

   Cost: each request reads R2 once (a Class B operation). The account is on
   the Workers Free plan, which stops at 100,000 requests a day instead of
   billing, so reads stay under R2's 10 million a month free tier. */

const PREFIX = "published/";

export default {
  async fetch(request, env) {
    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Method not allowed", { status: 405, headers: { Allow: "GET, HEAD" } });
    }
    const name = decodeURIComponent(new URL(request.url).pathname.slice(1));
    if (!name || name.includes("..") || name.startsWith("/")) {
      return new Response("Not found", { status: 404 });
    }
    const key = PREFIX + name;

    const object = request.method === "HEAD"
      ? await env.BUCKET.head(key)
      : await env.BUCKET.get(key, { range: request.headers, onlyIf: request.headers });
    if (object === null) return new Response("Not found", { status: 404 });

    const headers = new Headers();
    object.writeHttpMetadata(headers);
    headers.set("ETag", object.httpEtag);
    headers.set("Accept-Ranges", "bytes");
    headers.set("Cache-Control", "public, max-age=31536000, immutable");
    headers.set("Access-Control-Allow-Origin", "*");

    if (request.method === "HEAD") {
      headers.set("Content-Length", String(object.size));
      return new Response(null, { headers });
    }
    // A conditional request that matched (If-None-Match etc.) comes back without a body.
    if (!("body" in object)) return new Response(null, { status: 304, headers });

    const r = object.range;
    if (r && request.headers.has("Range")) {
      // R2 gives either { suffix } (the last n bytes) or { offset, length? }.
      const tail = r.suffix !== undefined;
      const start = tail ? Math.max(0, object.size - r.suffix) : (r.offset ?? 0);
      const end = !tail && r.length !== undefined ? start + r.length - 1 : object.size - 1;
      headers.set("Content-Range", `bytes ${start}-${end}/${object.size}`);
      headers.set("Content-Length", String(end - start + 1));
      return new Response(object.body, { status: 206, headers });
    }
    headers.set("Content-Length", String(object.size));
    return new Response(object.body, { headers });
  },
};
