-- course-links.lua: two reader-facing link conventions, applied at render time.
--
-- 1. Claim markers. The source files cite evidence as plain-text markers such
--    as [S-05], which scripts/check_sources.py reconciles against
--    sources/claims.csv. On the rendered site each marker becomes a link to
--    the matching entry on the public Sources page (sources.qmd, generated
--    from the same CSV), so a reader can follow every citation.
-- 2. Page references. Lessons refer to other pages by path in inline code,
--    for example `learn/tokens-context.qmd`. These become real links whose
--    text is the page title.
--
-- Both run only for HTML-family outputs and leave the source files untouched.

local titles = {
  ["learn/how-created"] = "From Text to Numbers",
  ["learn/neural-networks"] = "Neurons, Layers, and Learning",
  ["learn/why-transformers"] = "Why Transformers",
  ["learn/transformers-attention"] = "How Self-Attention Moves Information",
  ["learn/softmax-sampling"] = "Softmax, Sampling, and Temperature",
  ["learn/training"] = "How Pretraining Works",
  ["learn/posttraining"] = "Post-training",
  ["learn/agents"] = "From Assistant to Agent",
  ["learn/using-models-well"] = "Using Models Well",
  ["learn/tokens-context"] = "Tokens, Embeddings, and the Context Window",
  ["short-story"] = "The Short Story",
  ["resources"] = "Resources",
  ["glossary"] = "Glossary",
  ["milestones"] = "Milestones",
  ["sources"] = "Sources",
}

local function root()
  local o = quarto.project.offset
  if o == nil or o == "" then o = "." end
  return o
end

local function html_output()
  return quarto.doc.is_format("html") or quarto.doc.is_format("revealjs")
end

local function claim_link(id)
  return pandoc.Link({pandoc.Str("[S-" .. id .. "]")},
    root() .. "/sources.html#s-" .. id, "Source S-" .. id,
    pandoc.Attr("", {"claim-id"}))
end

function Str(el)
  if not html_output() then return nil end
  local t = el.text
  if not t:find("%[S%-%d+%]") then return nil end
  local out, pos = {}, 1
  while true do
    local s, e, id = t:find("%[S%-(%d+)%]", pos)
    if not s then break end
    if s > pos then table.insert(out, pandoc.Str(t:sub(pos, s - 1))) end
    table.insert(out, claim_link(id))
    pos = e + 1
  end
  if pos <= #t then table.insert(out, pandoc.Str(t:sub(pos))) end
  return out
end

function Code(el)
  if not html_output() then return nil end
  local key = el.text:match("^(learn/[a-z%-]+)%.qmd$") or el.text:match("^([a-z%-]+)%.qmd$")
  if key and titles[key] then
    return pandoc.Link({pandoc.Str(titles[key])}, root() .. "/" .. key .. ".html")
  end
  return nil
end
