using Test
using JuliaCif
using PyCall

# And get our Python stuff

@pyimport lark

# We need to see the local directory
pushfirst!(PyVector(pyimport("sys")["path"]), "")

@pyimport jl_transformer

## Configuration for what is to come...

grammar_file = "lark_grammar.ebnf"
dic_file = "/home/jrh/COMCIFS/cif_core/cif_core.dic"
ddlm_dic = "/home/jrh/COMCIFS/cif_core/ddl.dic"

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
    target_cat = String(dict[dname]["_name.category_id"])
    target_obj = String(dict[dname]["_name.object_id"])
    is_func = false
    if String(get(dict[dname],"_definition.class","Datum")) == "Function"
        is_func = true
    end
    catlist = [a for a in keys(dict) if String(get(dict[a],"_definition.scope","Item")) == "Category"]
    tt = jl_transformer.TreeToPy(dname,"myfunc",target_cat,target_obj,catlist,is_func=is_func)
end

get_cifdic() = begin
    cifdic(dic_file)
end

get_drel_methods(cd) = begin
    has_meth = [n for n in cd if "_method.expression" in keys(n) && String(get(n,"_definition.scope","Item")) != "Category"]
    meths = [(String(n["_definition.id"]),get_loop(n,"_method.expression")) for n in has_meth]
    println("Found $(length(meths)) methods")
    return meths
end

process_a_phrase(phrase::AbstractString,parser,transformer=nothing) = begin
    println("=========")
    println(phrase)
    tokens = parser[:lex](phrase)
    tree = parser[:parse](phrase,debug=false)
    x = ""
    if !(transformer == nothing)
        x = transformer[:transform](tree)
        end
    println(x)
    return x,transformer
end

evaluate_a_phrase(phrase,transformer) = begin
    parser = lark_grammar()
    println("==================\nProcessing:")
    println(phrase)
    x,t = process_a_phrase(phrase,parser,transformer)
    println("-------------------\n")
    println(x*"\n==================")
    Meta.parse(x)
    println("Parsing successful")
end
        
@testset "Syntax checking" begin
    @test begin
        phrase = "_a = 0"
        evaluate_a_phrase(phrase,simple_transformer())
        true
    end
    @test begin
        phrase = "With c as return
    return.value = Acosd(
    (Cosd(c.angle_beta)*Cosd(c.angle_gamma)-Cosd(c.angle_alpha))/(Sind(c.angle_beta)*Sind(c.angle_gamma)))"
        evaluate_a_phrase(phrase,simple_transformer())
        true
    end
    @test begin
        phrase = "b = 'uani'"
        evaluate_a_phrase(phrase,simple_transformer())
        true
    end
end

@testset "Dictionary syntax runthrough" begin
    d = get_cifdic()
    meths = get_drel_methods(d)
    for one_meth in meths
        dname,meth_loop = one_meth
        println("$dname")
        for one_pack in meth_loop
            if String(one_pack["_method.purpose"])=="Evaluation"
                meth_text = String(one_pack["_method.expression"])
                @test begin
                    evaluate_a_phrase(meth_text,full_on_transformer(dname,d))
                    true
                end
            end
        end
    end
end
