using Test
using JuliaCif
using PyCall
using DataFrames

# And get our Python stuff

@pyimport lark

# We need to see the local directory
pushfirst!(PyVector(pyimport("sys")["path"]), "")

@pyimport jl_transformer

## Configuration for what is to come...

const grammar_file = "lark_grammar.ebnf"
const dic_file = "/home/jrh/COMCIFS/cif_core/cif_core.dic"
const ddlm_dic = "/home/jrh/COMCIFS/cif_core/ddl.dic"

lark_grammar() = begin
    grammar_text = read(joinpath(@__DIR__,grammar_file),String)
    parser = lark.Lark(grammar_text,start="input",parser="lalr",lexer="contextual")
end

simple_transformer() = begin
    tt = jl_transformer.TreeToPy("return.val","myfunc","return","val",
                                 ["return"])
end

full_on_transformer(dname,dict) = begin
    # get out the information to pass to python
    println("Now transforming $dname using definition $(dict[dname])")
    target_cat = String(dict[dname]["_name.category_id"][1])
    target_obj = String(dict[dname]["_name.object_id"][1])
    is_func = false
    if String(get(dict[target_cat],"_definition.class",["Datum"])[1]) == "Functions"
        is_func = true
    end
    catlist = [a for a in keys(dict) if String(get(dict[a],"_definition.scope",["Item"])[1]) == "Category"]
    tt = jl_transformer.TreeToPy(dname,"myfunc",target_cat,target_obj,catlist,is_func=is_func)
end

get_cifdic() = begin
    cifdic(dic_file)
end

get_drel_methods(cd) = begin
    has_meth = [n for n in cd if "_method.expression" in keys(n) && String(get(n,"_definition.scope",["Item"])[1]) != "Category"]
    meths = [(String(n["_definition.id"][1]),get_loop(n,"_method.expression")) for n in has_meth]
    println("Found $(length(meths)) methods")
    return meths
end

process_a_phrase(phrase::String,parser,transformer=nothing) = begin
    println("=========")
    println(phrase)
    tokens = parser[:lex](phrase)
    tree = parser[:parse](phrase,debug=false)
    x = ""
    aliases = ""
    if !(transformer == nothing)
        tc_aliases,x = transformer[:transform](tree)
        end
    println(x)
    return x,tc_aliases,transformer
end

parse_a_phrase(phrase,transformer) = begin
    parser = lark_grammar()
    println("==================\nProcessing:")
    println(phrase)
    x,aliases,t = process_a_phrase(phrase,parser,transformer)
    println("-------------------\n")
    println(x*"\n==================")
    parsed = ast_fix_indexing(Meta.parse(x),Symbol.(["__packet"]))
    if aliases != ""  #the target category was aliased Aaaargh!
        parsed = find_target(parsed,aliases,transformer[:target_object])
    end
    println("-----------------")
    println(parsed)
    return parsed
end

#include("syntax_checks.jl")
include("semantic_checks.jl")

