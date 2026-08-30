from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any, Protocol

from .models import ExperienceSpec, ValidationError


class RendererAdapter(Protocol):
    name: str

    def render(
        self,
        *,
        collection_release: dict[str, Any],
        experience_spec: ExperienceSpec,
        out_dir: Path,
    ) -> list[Path]:
        ...


def _safe_embedded_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).replace("<", "\\u003c")


class StaticNavigatorRenderer:
    name = "static-navigator"

    def render(
        self,
        *,
        collection_release: dict[str, Any],
        experience_spec: ExperienceSpec,
        out_dir: Path,
    ) -> list[Path]:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        title = experience_spec.title or collection_release["title"]
        payload = {
            "title": title,
            "description": collection_release.get("description"),
            "collection_id": collection_release["collection_id"],
            "collection_release_id": collection_release["release_id"],
            "items": collection_release["items"],
            "config": {
                "search": experience_spec.search,
                "facets": list(experience_spec.facets),
                "default_sort": experience_spec.default_sort,
                "visibility": experience_spec.visibility,
            },
        }
        embedded = _safe_embedded_json(payload)
        curated = experience_spec.default_sort == "curated"
        curated_option = '<option value="curated">Curated order</option>\n' if curated else ""
        curated_branch = '  if(state.sort==="curated") return [...items];\n' if curated else ""
        page = (
            _HTML_TEMPLATE.replace("__TITLE__", html.escape(title))
            .replace("__DATA__", embedded)
            .replace("__CURATED_SORT_OPTION__", curated_option)
            .replace("__CURATED_SORT_BRANCH__", curated_branch)
        )
        path = out_dir / "index.html"
        path.write_text(page, encoding="utf-8")
        return [path]


_RENDERERS: dict[str, RendererAdapter] = {"static-navigator": StaticNavigatorRenderer()}


def get_renderer(name: str) -> RendererAdapter:
    try:
        return _RENDERERS[name]
    except KeyError as exc:
        raise ValidationError(f"unsupported renderer: {name!r}") from exc


_HTML_TEMPLATE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
:root{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color-scheme:light dark}
body{margin:0;background:Canvas;color:CanvasText}
main{max-width:1040px;margin:auto;padding:2rem 1rem 4rem}
header{margin-bottom:1.5rem}
h1{font-size:clamp(1.8rem,5vw,3rem);margin:.2rem 0}
.meta{opacity:.7}.controls{display:grid;grid-template-columns:minmax(12rem,1fr) auto;gap:.75rem;margin:1.2rem 0}
input,select{font:inherit;padding:.7rem;border:1px solid color-mix(in srgb,CanvasText 25%,transparent);border-radius:.5rem;background:Canvas}
.facets{display:flex;flex-wrap:wrap;gap:.6rem;margin-bottom:1rem}.facets label{display:flex;gap:.35rem;align-items:center}
#items{display:grid;gap:.8rem}.card{border:1px solid color-mix(in srgb,CanvasText 18%,transparent);border-radius:.7rem;padding:1rem}
.card h2{font-size:1.08rem;margin:.1rem 0 .35rem}.card p{margin:.35rem 0;line-height:1.45}.chips{display:flex;flex-wrap:wrap;gap:.35rem}.chip{font-size:.78rem;padding:.15rem .45rem;border-radius:999px;background:color-mix(in srgb,CanvasText 9%,transparent)}
a{color:inherit}.empty{opacity:.7;padding:2rem 0}
@media(max-width:640px){.controls{grid-template-columns:1fr}}
</style>
</head>
<body>
<main>
<header>
<p class="meta" id="release"></p>
<h1 id="title"></h1>
<p id="description"></p>
</header>
<section class="controls">
<input id="search" type="search" placeholder="Search title, summary, contributors…" aria-label="Search">
<select id="sort" aria-label="Sort">
<option value="title">Title</option>
<option value="date">Date</option>
<option value="source">Source</option>
__CURATED_SORT_OPTION__</select>
</section>
<section class="facets" id="facets"></section>
<section id="items"></section>
</main>
<script id="kx-data" type="application/json">__DATA__</script>
<script>
const data=JSON.parse(document.getElementById("kx-data").textContent);
const state={query:"",sort:data.config.default_sort,facets:{}};
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]));
document.getElementById("title").textContent=data.title;
document.getElementById("description").textContent=data.description||"";
document.getElementById("release").textContent=`${data.collection_id} · ${data.collection_release_id} · ${data.config.visibility}`;
const search=document.getElementById("search");
if(!data.config.search) search.hidden=true;
search.addEventListener("input",e=>{state.query=e.target.value.toLowerCase();render()});
const sort=document.getElementById("sort"); sort.value=state.sort; sort.addEventListener("change",e=>{state.sort=e.target.value;render()});
const facetRoot=document.getElementById("facets");
for(const key of data.config.facets){
  const values=[...new Set(data.items.flatMap(x=>{const v=x.facets?.[key];return Array.isArray(v)?v:(v===undefined||v===null?[]:[v])}).map(String))].sort();
  if(!values.length) continue;
  const label=document.createElement("label");
  label.innerHTML=`<span>${esc(key)}</span>`;
  const sel=document.createElement("select"); sel.innerHTML=`<option value="">All</option>`+values.map(v=>`<option>${esc(v)}</option>`).join("");
  sel.addEventListener("change",e=>{state.facets[key]=e.target.value;render()}); label.appendChild(sel); facetRoot.appendChild(label);
}
function matches(item){
  const hay=[item.title,item.subtitle,item.summary,...(item.contributors||[]),...(item.tags||[])].filter(Boolean).join(" ").toLowerCase();
  if(state.query && !hay.includes(state.query)) return false;
  for(const [key,want] of Object.entries(state.facets)){
    if(!want) continue;
    const raw=item.facets?.[key]; const vals=(Array.isArray(raw)?raw:[raw]).filter(v=>v!==undefined&&v!==null).map(String);
    if(!vals.includes(want)) return false;
  }
  return true;
}
function sourceLabel(item){return item.source_ref?.authority||""}
function sorted(items){
__CURATED_SORT_BRANCH__  return [...items].sort((a,b)=>{
    if(state.sort==="date") return String(b.date||"").localeCompare(String(a.date||""))||a.title.localeCompare(b.title);
    if(state.sort==="source") return sourceLabel(a).localeCompare(sourceLabel(b))||a.title.localeCompare(b.title);
    return a.title.localeCompare(b.title);
  });
}
function card(item){
  const href=item.canonical_url||item.source_ref?.url;
  const title=href?`<a href="${esc(href)}">${esc(item.title)}</a>`:esc(item.title);
  const chips=[...(item.contributors||[]),...(item.tags||[])].map(x=>`<span class="chip">${esc(x)}</span>`).join("");
  return `<article class="card" id="${encodeURIComponent(item.item_id)}"><h2>${title}</h2>${item.subtitle?`<p>${esc(item.subtitle)}</p>`:""}${item.summary?`<p>${esc(item.summary)}</p>`:""}${chips?`<div class="chips">${chips}</div>`:""}<p class="meta">${esc(item.date||"")} ${esc(sourceLabel(item))}</p></article>`;
}
function render(){
  const items=sorted(data.items.filter(matches)); const root=document.getElementById("items");
  root.innerHTML=items.length?items.map(card).join(""):`<p class="empty">No matching items.</p>`;
}
render();
</script>
</body>
</html>
'''