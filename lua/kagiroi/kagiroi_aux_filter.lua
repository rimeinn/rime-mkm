-- kagiroi_aux_filter.lua
-- implement aux filter logic based on moran
-- license: GPLv3
-- author: ksqsf
--
-- usage:
-- 1. add ` to speller/alphabet
-- 2. add lua_filter to the schema

local moran = require("moran")

---@param aux_table table
---@param candidate user_data<Candidate>
---@return boolean whether this candidate matches the auxcode
local function candidate_match(aux_table, candidate, auxcode)
    local auxcode = " " .. auxcode
    for pos, codepoint in utf8.codes(candidate.text) do
        local auxcodes = " " .. (aux_table[codepoint] or "")
        if auxcodes and auxcodes:match(auxcode) then
            return true
        end
    end
    return false
end

---@param env table
local function init(env)
    if moran == nil then
        env.enabled = false
    end
    env.aux_table = moran.load_zrmdb()
    if env.aux_table then
        env.enabled = true
    end


    local function on_select_post(ctx)
        ctx.input = ctx.input:gsub("`(.*)$", "")
        if ctx.composition:has_finished_composition() then
            ctx:commit()
        end
    end
    env.notifier_post = env.engine.context.select_notifier:connect(on_select_post)
end

---@param env table
local function fini(env)
    env.aux_table = nil
    env.notifier_post:disconnect()
end

---@param t_input Translation
---@param env table
local function func(t_input, env)
    local auxcode = env.engine.context.input:match("`(.*)$")

    if not env.enabled or not auxcode then
        for candidate in t_input:iter() do
            yield(candidate)
        end
        return
    end

    for candidate in t_input:iter() do
        if candidate_match(env.aux_table, candidate, auxcode) then
            yield(candidate)
        end
    end
end

return { init = init, fini = fini, func = func }

-- Local Variables:
-- lua-indent-level: 4
-- End:
